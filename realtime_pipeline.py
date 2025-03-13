"""Module reading kafka stream and cleaning data"""
import logging.config
import logging
from os import getenv
import time
import argparse
import json
from datetime import datetime, time as date_time
from dotenv import load_dotenv
from confluent_kafka import Consumer
from database import get_connection, get_cursor, upload_rating_interaction, upload_request_interaction

load_dotenv()
TOPIC = "lmnh"  # Kafka Topic
VALID_TYPES = [0, 1]  # Valid values for 'type'
VALID_VALS = [-1, 0, 1, 2, 3, 4]  # Valid values for 'val'
VALID_SITES = [0, 1, 2, 3, 4, 5]  # Valid sites
TIME_SOD = date_time(0, 0)  # Start Of Day Time (Midnight)
TIME_EOD = date_time(23, 59, 59)  # End Of Day Time (23:59:59)
TIME_MUSEUM_OPENING = date_time(8, 45)  # Time Museum opens
TIME_MUSEUM_CLOSING = date_time(18, 15)  # Time Museum closes
CONSUMER_POLL_TIMEOUT = 1.0  # Kafka Consumer Timeout length

kafka_config = {
    'bootstrap.servers': getenv('BOOTSTRAP_SERVERS'),
    'security.protocol': 'SASL_SSL',
    'sasl.mechanisms': 'PLAIN',
    'sasl.username': getenv('USERNAME_KAFKA'),
    'sasl.password': getenv('PASSWORD'),
    'group.id': getenv('GROUP_ID'),
    'auto.offset.reset': 'earliest',
    'client.id': 'kafka-client-python',
    'enable.auto.commit': False,
}


def parse_message(message_obj: dict) -> dict:
    """Parse messages to ensure they are valid and meet checks"""
    at = message_obj.get('at')
    site = message_obj.get('site')
    val = message_obj.get('val')
    msg_type = message_obj.get('type')

    if at is None or site is None or val is None:
        raise ValueError("Data is missing")

    try:
        site = int(site)
        val = int(val)
        at = datetime.fromisoformat(at).replace(tzinfo=None)
    except ValueError as value_err:
        raise ValueError("Incorrect Data Passed!") from value_err

    # Validation Checks

    validate_val(val, msg_type)

    msg_type = validate_type(msg_type)

    site = validate_site(site)

    validate_time(at)

    return {'at': at, 'site': site, 'val': val, 'type': msg_type}


def validate_type(msg_type):
    """If type is passed, ensure it is 0 or 1"""
    if msg_type is not None:
        msg_type = int(msg_type)
        if msg_type not in VALID_TYPES:
            raise ValueError("Type out of range")
    return msg_type


def validate_site(site):
    """Ensure site in range"""
    if site not in VALID_SITES:
        raise ValueError("Site out of range")
    return site + 1


def validate_val(val: int, msg_type: int) -> None:
    """Ensure val is in range and if is -1, type is passed"""
    if val not in VALID_VALS:
        raise ValueError("Value provided out of range")

    if val == -1 and msg_type is None:
        raise ValueError("Type required when Val is -1!")


def validate_time(at: datetime) -> None:
    """Make sure time is in range"""
    if at.date() > datetime.now().date():
        raise ValueError("'At' time is out of range")

    if TIME_SOD < at.time() < TIME_MUSEUM_OPENING:
        raise ValueError("Value out of range - Museum Not Open!")

    if TIME_MUSEUM_CLOSING < at.time() < TIME_EOD:
        raise ValueError("Value out of range - Museum Closed!")


def upload_data(message_data: dict) -> None:
    """Take a message and upload it to the database"""
    msg_type = message_data.get('type')
    at = message_data.get('at')
    val = message_data.get('val')
    site = message_data.get('site')

    db_conn = get_connection()
    db_cursor = get_cursor(db_conn)

    if msg_type is not None:
        data = (site, msg_type, at)
        upload_request_interaction(data, db_cursor)
    else:
        data = (site, val, at)
        upload_rating_interaction(data, db_cursor)

    db_conn.commit()
    db_cursor.close()
    db_conn.close()


def main_loop(consumer: Consumer, logger: logging.Logger) -> None:
    """Main method"""
    while True:
        message = consumer.poll(CONSUMER_POLL_TIMEOUT)
        if not message:
            time.sleep(0.5)
            continue
        if message.error():
            logger.error(message.error())
            continue

        try:
            msg = json.loads(message.value())
            msg = parse_message(msg)
            logger.info(msg)
            upload_data(msg)
        except (ValueError) as error:
            logger.error("INVALID: %s, %s", error, message.value())


def setup_arguments() -> argparse.ArgumentParser:
    """Set up ArgParse to parse arguments"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-l", "--log", help="Log errors to file instead of console", action='store_true')
    return parser.parse_args()


def setup_logger(args) -> None:
    """Runs basic config setup for the logger"""
    if args.log:
        logging.basicConfig(
            level=logging.ERROR,
            filename="pipeline-errors.log",
            encoding="utf-8",
            filemode="a",
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )
    else:
        logging.basicConfig(
            level=logging.INFO,
            format="{asctime} - {levelname} - {message}",
            style="{",
            datefmt="%Y-%m-%d %H:%M",
        )


if __name__ == '__main__':
    args = setup_arguments()
    setup_logger(args)

    consumer = Consumer(kafka_config)
    consumer.subscribe([TOPIC])

    logger = logging.getLogger('Kafka Consumer')
    main_loop(consumer, logger)

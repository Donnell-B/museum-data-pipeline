# pylint: skip-file
from unittest.mock import MagicMock, patch
import pytest
from datetime import datetime, timedelta
from realtime_pipeline import validate_time, validate_site, validate_type, validate_val, parse_message, upload_data


def test_validate_time_future():
    tomorrow = datetime.now() + timedelta(days=1)
    with pytest.raises(ValueError):
        validate_time(tomorrow)


def test_validate_time_early():
    early = datetime.now().replace(hour=8, minute=44)
    with pytest.raises(ValueError):
        validate_time(early)


def test_validate_time_late():
    late = datetime.now().replace(hour=18, minute=16)
    with pytest.raises(ValueError):
        validate_time(late)


def test_validate_time_open():
    open = datetime.now().replace(hour=9, minute=30)
    validate_time(open)


def test_validate_site_low():
    with pytest.raises(ValueError):
        validate_site(-1)


def test_validate_site_high():
    with pytest.raises(ValueError):
        validate_site(10)


def test_validate_site_correct():
    validate_site(1)


def test_validate_type():
    with pytest.raises(ValueError):
        validate_type(2)


def test_validate_none():
    validate_type(None)


def test_validate_val_low():
    with pytest.raises(ValueError):
        validate_val(-2, None)


def test_validate_val_high():
    with pytest.raises(ValueError):
        validate_val(7, None)


def test_validate_val_no_type():
    with pytest.raises(ValueError):
        validate_val(-1, None)


def test_validate_val_no_type():
    validate_val(-1, 1)


def test_parse_message():
    valid_msg = {'at': '2025-01-01T09:30:00', 'site': '0', 'val': '4'}

    with pytest.raises(ValueError):
        parse_message({'at': '2025-01-01T09:30:00', 'site': '0', 'val': '-1'})

    with pytest.raises(ValueError):
        parse_message({'at': '2025-01-01T09:30:00', 'site': '-1', 'val': '4'})

    with pytest.raises(ValueError):
        parse_message({'at': '2025-01-01T09:30:00',
                      'site': '0', 'val': '-1', 'type': 'INF'})

    with pytest.raises(ValueError):
        parse_message({'site': '0', 'val': '1'})

    with pytest.raises(ValueError):
        parse_message({'at': '2026-01-01T09:30:00', 'site': '0', 'val': '1'})

    with pytest.raises(ValueError):
        parse_message({'at': '2025-01-01T09:30:00'})

    with pytest.raises(ValueError):
        parse_message({'at': '2025-01-01T09:30:00',
                      'site': '0', 'val': '-1', 'type': '6'})

    parse_message(valid_msg)


@patch('realtime_pipeline.get_connection')
@patch('realtime_pipeline.get_cursor')
@patch('realtime_pipeline.upload_rating_interaction')
def test_upload_rating_interaction_called(mock_upload_rating, mock_get_cursor, mock_get_connection):
    message_data = {
        'at': '2025-03-13T10:00:00',
        'val': '4',
        'site': '2'
    }

    mock_db_conn = MagicMock()
    mock_db_cursor = MagicMock()
    mock_get_connection.return_value = mock_db_conn
    mock_get_cursor.return_value = mock_db_cursor

    upload_data(message_data)

    mock_upload_rating.assert_called_once_with(
        ('2', '4', '2025-03-13T10:00:00'), mock_db_cursor)
    mock_db_conn.commit.assert_called_once()
    mock_db_cursor.close.assert_called_once()
    mock_db_conn.close.assert_called_once()


@patch('realtime_pipeline.get_connection')
@patch('realtime_pipeline.get_cursor')
@patch('realtime_pipeline.upload_request_interaction')
def test_upload_request_interaction_called(mock_upload_request, mock_get_cursor, mock_get_connection):
    message_data = {
        'at': '2025-03-13T10:00:00',
        'site': '1',
        'val': '4',
        'type': '0'
    }

    mock_db_conn = MagicMock()
    mock_db_cursor = MagicMock()
    mock_get_connection.return_value = mock_db_conn
    mock_get_cursor.return_value = mock_db_cursor

    upload_data(message_data)

    mock_upload_request.assert_called_once_with(
        ('1', '0', '2025-03-13T10:00:00'), mock_db_cursor)
    mock_db_conn.commit.assert_called_once()
    mock_db_cursor.close.assert_called_once()
    mock_db_conn.close.assert_called_once()

-- This file should contain all code required to create & seed database tables.
DROP TABLE IF EXISTS department, floor, request, rating, exhibition, request_interaction, rating_interaction;


CREATE TABLE department(
    department_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    department_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (department_id)
);

CREATE TABLE floor(
    floor_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    floor_name VARCHAR(100) NOT NULL,
    PRIMARY KEY (floor_id)
);

CREATE TABLE request(
    request_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    request_value SMALLINT NOT NULL,
    request_description VARCHAR(100),
    PRIMARY KEY (request_id)
);

CREATE TABLE rating(
    rating_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    rating_value SMALLINT NOT NULL,
    rating_description VARCHAR(100),
    PRIMARY KEY (rating_id)
);

CREATE TABLE exhibition(
    exhibition_id SMALLINT GENERATED ALWAYS AS IDENTITY,
    exhibition_name VARCHAR(100) NOT NULL,
    exhibition_description TEXT,
    department_id SMALLINT NOT NULL,
    floor_id SMALLINT NOT NULL,
    exhibition_start_date DATE DEFAULT CURRENT_DATE CHECK(exhibition_start_date <= CURRENT_DATE),
    public_id TEXT,
    PRIMARY KEY (exhibition_id),
    CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES department(department_id),
    CONSTRAINT fk_floor FOREIGN KEY (floor_id) REFERENCES floor(floor_id)
);

CREATE TABLE request_interaction(
    request_interaction_id BIGINT GENERATED ALWAYS AS IDENTITY,
    exhibition_id SMALLINT NOT NULL,
    request_id SMALLINT NOT NULL,
    event_at TIMESTAMP CHECK(DATE(event_at) <= DATE(NOW())) NOT NULL DEFAULT NOW(),
    PRIMARY KEY (request_interaction_id),
    CONSTRAINT fk_exhibition FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    CONSTRAINT fk_request FOREIGN KEY (request_id) REFERENCES request(request_id)
);

CREATE TABLE rating_interaction(
    rating_interaction_id BIGINT GENERATED ALWAYS AS IDENTITY,
    exhibition_id SMALLINT NOT NULL,
    rating_id SMALLINT NOT NULL,
    event_at TIMESTAMP CHECK(DATE(event_at) <= DATE(NOW())) NOT NULL DEFAULT NOW(),
    PRIMARY KEY (rating_interaction_id),
    CONSTRAINT fk_exhibition FOREIGN KEY (exhibition_id) REFERENCES exhibition(exhibition_id),
    CONSTRAINT fk_rating FOREIGN KEY (rating_id) REFERENCES rating(rating_id)
);

INSERT INTO department (department_name) VALUES ('Zoology'), ('Entomology'), ('Geology'), ('Palaeontology'), ('Ecology');

INSERT INTO floor (floor_name) VALUES ('Vault'), ('Ground'), ('1'), ('2'), ('3');

INSERT INTO request (request_value, request_description) VALUES (0, 'Assistance'), (1, 'Emergency');

INSERT INTO rating (rating_value, rating_description) VALUES (4,'5/5'),(3,'4/5'),(2,'3/5'),(1,'2/5'),(0,'1/5');

INSERT INTO exhibition (exhibition_name, exhibition_description, department_id, floor_id, exhibition_start_date) VALUES 
    ('Measureless to Man', 'An immersive 3D experience: delve deep into a previously-inaccessible cave system.', 3, 3, '2021/08/23'),
    ('Adaptation','How insect evolution has kept pace with an industrialised world', 2, 1, '2019/07/01'),
    ('The Crenshaw Collection', 'An exhibition of 18th Century watercolours, mostly focused on South American wildlife.', 1, 4, '2021/03/03'),
    ('Cetacean Sensations', 'Whales: from ancient myth to critically endangered.', 1, 3, '2019/07/01'),
    ('Our Polluted World', 'A hard-hitting exploration of humanity''s impact on the environment', 5, 5, '2021/05/12'),
    ('Thunder Lizards', 'How new research is making scientists rethink what dinosaurs really looked like.', 4, 3, '2023/02/01');
-- Create Language table
CREATE TABLE IF NOT EXISTS language (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Create Question table
CREATE TABLE IF NOT EXISTS question (
    id SERIAL PRIMARY KEY,
    code VARCHAR(255) NOT NULL
);

-- Create Test table
CREATE TABLE IF NOT EXISTS test (
    id SERIAL PRIMARY KEY,
    code VARCHAR(255) NOT NULL,
    question_id INTEGER REFERENCES question(id) ON DELETE CASCADE,
    language_id INTEGER REFERENCES language(id)
);

-- Insert some static languages
INSERT INTO language (name) VALUES
  ('Python'),
  ('Java');

-- Insert some static questions
INSERT INTO question (code) VALUES
  ('Q001'),
  ('Q002');

-- Insert some static tests
INSERT INTO test (code, question_id, language_id) VALUES
  ('ZGVmIHRlc3RfYWRkXzIoc2VsZik6DQoJc29sID0gU29sdXRpb24oKQ0KCXNlbGYuYXNzZXJ0RXF1YWwoc29sLmFkZCg2LCAzKSwgOSk=', 1, 1),  -- Python test for question 1
  ('QFRlc3QNCnB1YmxpYyBpbnQgYWRkKGludCBhLCBpbnQgYil7DQoJcmV0dXJuIGEgKyBiOw0KfQ==', 1, 2)  -- Java test for question 1
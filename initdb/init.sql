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
  ('QFRlc3QNCnB1YmxpYyB2b2lkIHRlc3RTdW1Qb3NpdGl2ZU51bWJlcnMoKSB7DQoJU29sdXRpb24gcyA9IG5ldyBTb2x1dGlvbigpOw0KCWFzc2VydEVxdWFscyg1LCBzLmFkZCgyLCAzKSk7DQp9', 1, 2)  -- Java test for question 1
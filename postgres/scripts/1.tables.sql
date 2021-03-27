DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS conversations;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS keywords;
DROP TABLE IF EXISTS user_conversation_map;
DROP TABLE IF EXISTS user_subscribed_keywords_map;
DROP TABLE IF EXISTS conversation_keywords_map;
DROP TABLE IF EXISTS messages_read_by_map;


CREATE TABLE IF NOT EXISTS users (
    user_id serial PRIMARY KEY,
	email VARCHAR (50) UNIQUE NOT NULL,
	username VARCHAR(50) UNIQUE NOT NULL,
	password VARCHAR(300) NOT NULL);

CREATE TABLE IF NOT EXISTS conversations (
    conversation_id serial PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    is_public BOOLEAN NOT NULL);

CREATE TABLE IF NOT EXISTS messages (
    message_id serial PRIMARY KEY,
    content VARCHAR(500) NOT NULL,
    conversation_id INTEGER NOT NULL,
    sent_by INTEGER NOT NULL,
    time_sent TIMESTAMP NOT NULL,
    FOREIGN KEY (sent_by) REFERENCES users,
    FOREIGN KEY (conversation_id) REFERENCES conversations);

CREATE TABLE IF NOT EXISTS keywords (
    keyword_id serial PRIMARY KEY,
	content VARCHAR(30));

CREATE TABLE IF NOT EXISTS user_conversation_map (
    user_id INTEGER,
    conversation_id INTEGER,
    PRIMARY KEY (user_id, conversation_id),
    FOREIGN KEY (user_id) REFERENCES users,
    FOREIGN KEY (conversation_id) REFERENCES conversations);

CREATE TABLE IF NOT EXISTS user_subscribed_keywords_map (
    user_id INTEGER,
    keyword_id INTEGER,
    PRIMARY KEY (user_id, keyword_id),
    FOREIGN KEY (user_id) REFERENCES users,
    FOREIGN KEY (keyword_id) REFERENCES keywords);

CREATE TABLE IF NOT EXISTS conversation_keywords_map (
    conversation_id INTEGER,
    keyword_id INTEGER,
    PRIMARY KEY (conversation_id, keyword_id),
    FOREIGN KEY (conversation_id) REFERENCES conversations,
    FOREIGN KEY (keyword_id) REFERENCES keywords);

CREATE TABLE IF NOT EXISTS messages_read_by_map (
    message_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY (message_id, user_id),
    FOREIGN KEY (message_id) REFERENCES messages,
    FOREIGN KEY (user_id) REFERENCES users);
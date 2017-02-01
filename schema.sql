CREATE DATABASE IF 'MockSalutes';

CREATE TABLE MockSalutes.PendingComments
(
    id INT PRIMARY KEY AUTO_INCREMENT,
    comment_id TINYTEXT NOT NULL,
    salute TINYTEXT NOT NULL
);
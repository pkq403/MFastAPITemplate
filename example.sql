CREATE TABLE toy
(
  id   integer     ,
  name varchar(100) NOT NULL,
  type varchar(50)  NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE user
(
  id       integer     ,
  username varchar(100) NOT NULL,
  email    varchar(100) NOT NULL,
  PRIMARY KEY (id)
);

CREATE TABLE user_toy
(
  user_id integer NOT NULL,
  toy_id  integer NOT NULL,
  PRIMARY KEY (user_id, toy_id)
);

ALTER TABLE user_toy
  ADD CONSTRAINT FK_user_TO_user_toy
    FOREIGN KEY (user_id)
    REFERENCES user (id);

ALTER TABLE user_toy
  ADD CONSTRAINT FK_toy_TO_user_toy
    FOREIGN KEY (toy_id)
    REFERENCES toy (id);
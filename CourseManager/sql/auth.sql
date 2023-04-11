CREATE TABLE course_users (
    id INTEGER GENERATED BY DEFAULT ON NULL
    AS IDENTITY PRIMARY KEY,
    email       VARCHAR2(100) NOT NULL,
    password    VARCHAR2(102) NOT NULL,
    name        VARCHAR2(1000) NOT NULL,
    avatar_path VARCHAR2(1000)
)
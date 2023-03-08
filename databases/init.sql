CREATE USER 'gpe_user'@'%' IDENTIFIED BY 'XZe&pR5%2397';
GRANT ALL PRIVILEGES ON * . * TO 'gpe_user'@'%';
FLUSH PRIVILEGES;


CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT,
    name VARCHAR(100) , 
    username VARCHAR(100) , 
    password VARCHAR(100) , 
    mail VARCHAR(100) , 
    role INT , 
    created_at timestamp default current_timestamp , 
    primary key (id)
);
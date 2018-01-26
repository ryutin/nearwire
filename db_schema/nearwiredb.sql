CREATE DATABASE IF NOT EXISTS nearwire_db;
USE nearwire_db;

SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

/*!50503 set default_storage_engine = InnoDB */;
/*!50503 select CONCAT('storage engine: ', @@default_storage_engine) as INFO */;

CREATE TABLE news_result_blob (
        id    INT NOT NULL AUTO_INCREMENT,
        pull_datetime  datetime,
        json mediumblob    NOT NULL,
       part_id    int not null default 0,
       PRIMARY KEY (id)
);

CREATE TABLE news_result_item (
       id      INT  NOT NULL AUTO_INCREMENT,
       news_result_blob_id  INT,
       location varchar(255) NOT NULL,
       state   varchar(255) NOT NULL,
       url   varchar(511),
       host_name  varchar(255),  -- "site full"
       domain_name  varchar(255), -- "site"
       publish_date datetime,
       title varchar(511),
       text  blob,
       json  blob NOT NULL,
       INDEX location_state (location,state),
       PRIMARY KEY (id),
       FOREIGN KEY(news_result_blob_id)
          REFERENCES news_result_blob(id) ON DELETE RESTRICT
);

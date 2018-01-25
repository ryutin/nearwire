CREATE DATABASE IF NOT EXISTS nearwiredb;
USE nearwiredb;

SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

/*!50503 set default_storage_engine = InnoDB */;
/*!50503 select CONCAT('storage engine: ', @@default_storage_engine) as INFO */;

CREATE TABLE news_result_result (
       id      INT  NOT NULL AUTO_INCREMENT,
       news_results long_blob   NOT NULL,
       pull_date    datetime,
       location varchar(255) NOT NULL,
       state       varchar(255) NOT NULL,
       part_id    int not null default 0,
       url   varchar(512)
       PRIMARY KEY (ns_json_id)
);

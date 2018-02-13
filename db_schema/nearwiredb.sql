CREATE DATABASE IF NOT EXISTS nearwire_db;
USE nearwire_db;

SELECT 'CREATING DATABASE STRUCTURE' as 'INFO';

/*!50503 set default_storage_engine = InnoDB */;
/*!50503 select CONCAT('storage engine: ', @@default_storage_engine) as INFO */;

CREATE TABLE news_result_blob (
        id    int unsigned not null auto_increment,
        part_id   int unsigned not null default 0,
        pull_datetime  datetime,
        webhose_json mediumblob  not null,
        location varchar(100) not null,
        state  varchar(50) not null,
       INDEX location_state (location,state),
       INDEX (pull_datetime),
       PRIMARY KEY (id)
);

CREATE TABLE news_result_item (
       id      int  unsigned not null auto_increment,
       news_result_blob_id int unsigned,  -- fk news_result_blob.id
       request_counter              smallint unsigned,
       webhose_uuid varchar(63) not null,
       domain_name  varchar(250) not null, -- "site"
       host_name  varchar(150) not null,   -- "site full"
       article_url  varchar(500) not null,
       article_title varchar(500) not null,
       article_text  blob not null,
       publish_datetime datetime,
       webhose_json  blob not null,
       INDEX (publish_datetime),
       PRIMARY KEY (id),
       FOREIGN KEY (news_result_blob_id)
          REFERENCES news_result_blob(id) ON DELETE RESTRICT
);

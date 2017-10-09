-- Table: plant_app_etl.huodian_news

-- DROP TABLE plant_app_etl.huodian_news;

CREATE TABLE plant_app_etl.huodian_news
(
  ID INT PRIMARY KEY      NOT NULL,
  title character varying(255),
  href character varying(255),
  content text

)
WITH (
  OIDS=FALSE
);
ALTER TABLE plant_app_etl.huodian_news
  OWNER TO postgres;

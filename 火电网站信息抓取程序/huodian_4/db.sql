-- Table: plant_app_etl.huodian_news

-- DROP TABLE plant_app_etl.huodian_news;

CREATE TABLE plant_app_etl.tb_etl_huodian_news
(
  datetime timestamp(6) without time zone NOT NULL,
  title character varying NOT NULL,
  href character varying,
  source character varying, --新闻来源
  content text,
  content_sha1 character varying(255) NOT NULL DEFAULT 1,
  CONSTRAINT tb_etl_huodian_news_pkey PRIMARY KEY (datetime, title)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE plant_app_etl.tb_etl_huodian_news
  OWNER TO postgres;

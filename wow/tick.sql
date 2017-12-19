CREATE TABLE sun_tick_datas.threed_datas
(
  date date NOT NULL,
  no int NOT NULL,
  num char(3) NOT NULL,
  CONSTRAINT threed_datas_pkey PRIMARY KEY (date, no)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE sun_tick_datas.threed_datas
  OWNER TO postgres;
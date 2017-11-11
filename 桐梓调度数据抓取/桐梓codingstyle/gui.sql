CREATE TABLE plant_app_tcx.tb_gui_data
(

  date_str timestamp(6) without time zone NOT NULL,
  json_data character varying NOT NULL,
  CONSTRAINT tb_gui_data_pkey PRIMARY KEY (date_str)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE plant_app_tcx.tb_gui_data
  OWNER TO postgres;
-- Table: plant_app_tcx.tb_acquisition_new_data

-- DROP TABLE plant_app_tcx.tb_acquisition_new_data;

CREATE TABLE plant_app_tcx.tb_acquisition_new_data
(
  province_id integer NOT NULL,
  monitor_point character varying NOT NULL,
  monitor_time timestamp(6) without time zone NOT NULL,
  project_id character varying NOT NULL,
  monitor_value double precision,
  standard_limit_value double precision,
  evaluation_criterion character varying,
  enterprise_id character varying NOT NULL,
  CONSTRAINT tb_acquisition_new_data_pkey PRIMARY KEY (province_id, enterprise_id, monitor_point, project_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE plant_app_tcx.tb_acquisition_new_data
  OWNER TO postgres;
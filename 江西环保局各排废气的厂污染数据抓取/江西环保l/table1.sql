-- Table: plant_app_tcx.tb_acquisition

-- DROP TABLE plant_app_tcx.tb_acquisition;

CREATE TABLE plant_app_tcx.tb_acquisition
(
  province_id integer NOT NULL,
  monitor_point character varying NOT NULL,
  monitor_time timestamp(6) without time zone NOT NULL,
  project_id character varying NOT NULL,
  monitor_value double precision,
  standard_limit_value double precision,
  evaluation_criterion character varying,
  enterprise_id character varying NOT NULL,
  CONSTRAINT tb_acquisition_pkey PRIMARY KEY (province_id, enterprise_id, monitor_time, monitor_point, project_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE plant_app_tcx.tb_acquisition
  OWNER TO postgres;

-- Index: plant_app_tcx.acquisition_index_enterprise

-- DROP INDEX plant_app_tcx.acquisition_index_enterprise;

CREATE INDEX acquisition_index_enterprise
  ON plant_app_tcx.tb_acquisition
  USING btree
  (enterprise_id COLLATE pg_catalog."default");

-- Index: plant_app_tcx.acquisition_index_point

-- DROP INDEX plant_app_tcx.acquisition_index_point;

CREATE INDEX acquisition_index_point
  ON plant_app_tcx.tb_acquisition
  USING btree
  (monitor_point COLLATE pg_catalog."default");

-- Index: plant_app_tcx.acquisition_index_project

-- DROP INDEX plant_app_tcx.acquisition_index_project;

CREATE INDEX acquisition_index_project
  ON plant_app_tcx.tb_acquisition
  USING btree
  (project_id COLLATE pg_catalog."default");

-- Index: plant_app_tcx.acquisition_index_province

-- DROP INDEX plant_app_tcx.acquisition_index_province;

CREATE INDEX acquisition_index_province
  ON plant_app_tcx.tb_acquisition
  USING btree
  (province_id DESC NULLS LAST);

-- Index: plant_app_tcx.acquisition_index_time

-- DROP INDEX plant_app_tcx.acquisition_index_time;

CREATE INDEX acquisition_index_time
  ON plant_app_tcx.tb_acquisition
  USING btree
  (monitor_time DESC NULLS LAST);
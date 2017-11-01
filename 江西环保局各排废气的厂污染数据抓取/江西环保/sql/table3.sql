-- Table: plant_app_tcx.tb_enterprise

-- DROP TABLE plant_app_tcx.tb_enterprise;

CREATE TABLE plant_app_tcx.tb_enterprise
(
  qy_name character varying,
  qy_wrylx character varying,
  qy_jd character varying,
  qy_wd character varying,
  qy_address character varying,
  qy_corporation character varying,
  qy_industry character varying,
  qy_link_user character varying,
  qy_link_phone character varying,
  qy_tysj character varying,
  qy_auto_monitor_style character varying,
  qy_manual_monitor_style character varying,
  qy_auto_monitor_operation_style character varying,
  qy_pfwrwmc character varying,
  qy_zyscgy character varying,
  qy_zycp character varying,
  qy_zlss character varying,
  qy_lead_time character varying,
  qy_url character varying,
  qy_introduce text,
  qy_organization_code character varying,
  province_id integer NOT NULL,
  qy_link_email character varying,
  qy_id character varying NOT NULL,
  qy_style integer,
  qy_unit_category character varying,
  qy_register_type character varying,
  qy_manager_dept character varying,
  qy_scale character varying,
  qy_fax character varying,
  qy_city character varying,
  qy_city_id character varying,
  CONSTRAINT tb_enterprise_pkey PRIMARY KEY (qy_id, province_id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE plant_app_tcx.tb_enterprise
  OWNER TO postgres;
--label files only; NOT LABEL AND CODES
--the user should change all schema.table names for use in local programs

-- Table: hmda.all_label_2012

DROP TABLE if exists hmda.all_label_2012;

CREATE TABLE hmda.all_label_2012
(
  tract_to_msamd_income numeric,
  rate_spread numeric,
  population integer,
  minority_population numeric,
  number_of_owner_occupied_units numeric,
  number_of_1_to_4_family_units numeric,
  loan_amount_000s numeric,
  hud_median_family_income numeric,
  applicant_income_000s numeric,
  state_name character varying(25),
  state_abbr character varying(2),
  sequence_number numeric,
  respondent_id character varying(20),
  purchaser_type_name character varying(80),
  property_type_name character varying(70),
  preapproval_name character varying(35),
  owner_occupancy_name character varying(45),
  msamd_name character varying(60),
  loan_type_name character varying(20),
  loan_purpose_name character varying(20),
  lien_status_name character varying(30),
  hoepa_status_name character varying(16),
  edit_status_name character varying(30),
  denial_reason_name_3 character varying(50),
  denial_reason_name_2 character varying(50),
  denial_reason_name_1 character varying(50),
  county_name character varying(40),
  co_applicant_sex_name character varying(100),
  co_applicant_race_name_5 character varying(100),
  co_applicant_race_name_4 character varying(100),
  co_applicant_race_name_3 character varying(100),
  co_applicant_race_name_2 character varying(100),
  co_applicant_race_name_1 character varying(100),
  co_applicant_ethnicity_name character varying(100),
  census_tract_number character varying(7),
  as_of_year character varying(4),
  application_date_indicator character varying(1),
  applicant_sex_name character varying(100),
  applicant_race_name_5 character varying(100),
  applicant_race_name_4 character varying(100),
  applicant_race_name_3 character varying(100),
  applicant_race_name_2 character varying(100),
  applicant_race_name_1 character varying(100),
  applicant_ethnicity_name character varying(100),
  agency_name character varying(50),
  agency_abbr character varying(4),
  action_taken_name character varying(60)
)
WITH (
  OIDS=TRUE
);
ALTER TABLE hmda.all_label_2012
  OWNER TO postgres;
  
--creating index's for further use in post processing
create index hmda_all_label_2012_state_abbr_btree on hmda.all_label_2012 using btree (state_abbr);
create index hmda_all_label_2012_county_name_btree on hmda.all_label_2012 using btree (county_name);

--testing to make sure there are 0 records
select count(*) from hmda.all_label_2012

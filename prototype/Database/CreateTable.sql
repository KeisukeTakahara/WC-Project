CREATE TABLE compartment (
  comp_id integer(1),
  status varchar(1),
  upd_dt DATETIME,
  PRIMARY KEY (comp_id,
               upd_dt));

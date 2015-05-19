drop table if exists pdu_data;
create table entries (
  id integer primary key autoincrement,
  ip text unique not null,
  acc_str text not null
);

drop table if exists tweets;
create table tweets (
  id integer primary key autoincrement,
  tweet text not null,
  Ttime text not null,
  Tdate text not null
);
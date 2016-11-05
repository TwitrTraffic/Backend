drop table if exists tweets;
create table tweets (
  id text primary key,
  tweet text not null,
  Ttime text not null,
  Tdate text not null,
);

drop table if exists coordinates;
create table coordinates (
	location text primary key,
	lat text not null,
	long text not null
);

drop table if exists routes;
create table routes (
	src text not null,
	dest text not null,
	day text not null,
	route_time text not null,
	primary key (src, dest) 
);

drop table if exists places;
create table places (
	src text not null,
	dest text not null,
	checkpoints text not null,
	FOREIGN KEY(dest) REFERENCES routes(dest),
    FOREIGN KEY(src) REFERENCES routes(src)
);
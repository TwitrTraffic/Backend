create table if not exists tweets (
  id text primary key,
  tweet text not null,
  Ttime text not null,
  Tdate date not null
);

create table if not exists coordinates (
	location text primary key,
	lat text not null,
	long text not null
);

create table if not exists routes (
	src text not null,
	dest text not null,
	day text not null,
	route_time text not null,
	primary key (src, dest) 
);

create table if not exists places (
	src text not null,
	dest text not null,
	checkpoints text not null,
	FOREIGN KEY(dest) REFERENCES routes(dest),
    FOREIGN KEY(src) REFERENCES routes(src)
);
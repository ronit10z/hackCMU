drop table if exists entries;
create table cards (
  id integer primary key autoincrement,
  title text not null,
  description text not null,
  score int,
  status text not null,
  author text not null
  'text' text not null,
);

create table user_data (
  id integer primary key autoincrement,
  username text not null,
  password text not null,
  rating integer not null,
  upvoted text not null
);

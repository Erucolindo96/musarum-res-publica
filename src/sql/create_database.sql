CREATE TABLE IF NOT EXISTS deputy(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   name TEXT NOT NULL UNIQUE,
   party TEXT
);

CREATE TABLE IF NOT EXISTS interpellation(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   date TEXT,
   content TEXT,
   parsed_content TEXT
);

CREATE TABLE IF NOT EXISTS deputy_interpellation(
   deputy_id INTEGER NOT NULL,
   interpellation_id INTEGER NOT NULL,
   FOREIGN KEY(deputy_id) REFERENCES deputy(id),
   FOREIGN KEY(interpellation_id) REFERENCES interpellation(id),
   PRIMARY KEY(deputy_id, interpellation_id)
);

CREATE TABLE IF NOT EXISTS voivodeship(
   id INTEGER PRIMARY KEY ,
   name TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS county(
   id INTEGER,
   voivodeship_id INTEGER,
   name TEXT NOT NULL,
   FOREIGN KEY(voivodeship_id) REFERENCES voivodeship(id)
   PRIMARY KEY(id, voivodeship_id)
);

CREATE TABLE IF NOT EXISTS settle(
   id INTEGER PRIMARY KEY AUTOINCREMENT,
   county_id INTEGER,
   voivodeship_id INTEGER,
   name TEXT NOT NULL,
   FOREIGN KEY(county_id, voivodeship_id) REFERENCES county(id, voivodeship_id)
   UNIQUE(county_id, voivodeship_id, name)
);

CREATE TABLE IF NOT EXISTS interpellation_settles(
   settle_id INTEGER NOT NULL,
   interpellation_id INTEGER NOT NULL,
   FOREIGN KEY(settle_id) REFERENCES settle(id),
   FOREIGN KEY(interpellation_id) REFERENCES interpellation(id),
   PRIMARY KEY(settle_id, interpellation_id)
);
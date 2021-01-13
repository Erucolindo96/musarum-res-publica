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


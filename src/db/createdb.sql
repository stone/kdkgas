BEGIN TRANSACTION;
CREATE TABLE buyer (buyer_id INTEGER PRIMARY KEY, buyer_name TEXT);
INSERT INTO buyer VALUES(1,'Klas Köpare');
INSERT INTO buyer VALUES(2,'Benny Bryt');

CREATE TABLE bottle (bottle_id INTEGER PRIMARY KEY, size NUMERIC, maxpres NUMERIC, buyer_id INTEGER REFERENCES buyer);
INSERT INTO bottle VALUES(1, 12, 232, 1);
INSERT INTO bottle VALUES(2, 15, 232, 1);
INSERT INTO bottle VALUES(3, 10, 300, 2);
INSERT INTO bottle VALUES(4, 7, 300, 2);

CREATE TABLE filler (filler_id INTEGER PRIMARY KEY, filler_name TEXT);
INSERT INTO filler VALUES(1,'John Doe');
INSERT INTO filler VALUES(2,'Kalle Kula');

CREATE TABLE pricelist (pricelist_id INTEGER PRIMARY KEY, name TEXT, price NUMERIC);
INSERT INTO pricelist VALUES(1,'O2',0.05);
INSERT INTO pricelist VALUES(2,'HE',0.5);

COMMIT;

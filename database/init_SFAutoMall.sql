-- Create Tables
CREATE TABLE "Manufacturer" (
	"M_Name" TEXT NOT NULL UNIQUE,
	"Phone"	integer,
	"State"	TEXT,
	PRIMARY KEY("M_Name")
);
CREATE TABLE "Offices" (
	"State"	TEXT NOT NULL,
	"Phone"	integer,
	"District_id"	INTEGER NOT NULL DEFAULT 1 UNIQUE,
	PRIMARY KEY("District_id" AUTOINCREMENT)
);
CREATE TABLE "Person" (
	"P_Name"	TEXT NOT NULL,
	"Age"	integer,
	"License"	integer NOT NULL,
	PRIMARY KEY("P_Name")
);
CREATE TABLE "Vehicle" (
	"Make"	TEXT NOT NULL,
	"Model"	TEXT NOT NULL,
	"Year"	integer,
	"Value"	integer,
	"Buyer"	TEXT DEFAULT 'NA',
	"Repair"	INTEGER,
	"District_Id"	INTEGER NOT NULL DEFAULT 0,
	PRIMARY KEY("Model"),
	FOREIGN KEY("District_id") REFERENCES "Offices",
	FOREIGN KEY("Make") REFERENCES "Manufacturer"("M_Name"),
	FOREIGN KEY("Buyer") REFERENCES "Person"("P_Name")
);
-- Indexes
CREATE INDEX "Drivers" ON "Person" (
	"P_Name",
	"License"
);
CREATE INDEX "Pricing" ON "Vehicle" (
	"Make",
	"Value"	DESC
);
CREATE INDEX "Quick_Search" ON "Vehicle" (
	"Make",
	"Model"
);
-- Views
CREATE VIEW Buyers AS
SELECT Car.Buyer,Car.Make,Car.Model,Car.Year,Car.Value
FROM Vehicle Car;
WHERE NOT Buyer='NA';

CREATE VIEW Inventory 
AS SELECT Make,Model,Year,Buyer,District_id
FROM Vehicle
WHERE Buyer='NA';

CREATE VIEW Makes AS
SELECT Car.Make,Car.Model,Car.Year
FROM Manufacturer Maker, Vehicle Car
WHERE Maker.M_Name = Car.Make;

CREATE VIEW Repairs AS
SELECT Car.Buyer,Car.Make,Car.Model,Car.Year,Car.Repair
FROM Vehicle Car
WHERE Car.Repair = 1;
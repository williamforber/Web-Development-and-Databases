CREATE SCHEMA HorizonTravels;
USE HorizonTravels;
CREATE TABLE UserAccounts
(
	UserId INT AUTO_INCREMENT,
	UserName VARCHAR(45) UNIQUE,
	EmailAddress VARCHAR(45) UNIQUE,
	Password VARCHAR(72),
	Salt VARCHAR(32),
	isAdmin INT DEFAULT 0,
	PRIMARY KEY (UserId)
);

CREATE TABLE Prices
(
	PriceId INT,
    Price DOUBLE,
    PRIMARY KEY (PriceId)
);

CREATE TABLE TimeTable
(
	TimeId INT,
    Origin VARCHAR (45),
    Destination VARCHAR (45),
    TimeToLeave TIME,
    TimeToArrive TIME,
    PRIMARY KEY (TimeId)
);

CREATE TABLE TimeTableToPrices
(
	PriceId INT,
    TimeId INT,
    FOREIGN KEY (PriceId) REFERENCES Prices(PriceId)
		ON DELETE CASCADE,
    FOREIGN KEY (TimeId) REFERENCES TimeTable(TimeId)
		ON DELETE CASCADE,	
    PRIMARY KEY (PriceId,TimeId)
);

CREATE TABLE Bookings
(
	BookingId INT AUTO_INCREMENT,
    UserId INT,
    PriceId INT,
    DateOfBooking DATE,
	DaysInAdvance INT,
	DateBookingMade DATE,
	isBusinessClass INT,
    TimeId INT,
	
	
    FOREIGN KEY (UserId) REFERENCES UserAccounts(UserId)
		ON DELETE CASCADE,
	FOREIGN KEY (PriceId) REFERENCES Prices(PriceId),
	FOREIGN KEY (TimeId) REFERENCES TimeTable(TimeId),
    PRIMARY KEY (BookingId)
);

INSERT INTO TimeTable (TimeId,Origin,Destination,TimeToLeave,TimeToArrive) VALUES
	 (1,"Newcastle","Bristol","16:45:00","18:00:00"),
	 (2,"Bristol","Newcastle","08:00:00","09:15:00"),
	 (3,"Cardiff","Edinburgh","06:00:00","07:30:00"),
	 (4,"Bristol","Manchester","11:30:00","12:30:00"),
	 (5,"Manchester","Bristol","12:20:00","13:20:00"),
	 (6,"Bristol","London","07:40:00","08:20:00"),
	 (7,"London","Manchester","11:00:00","12:20:00"),
	 (8,"Manchester","Glasgow","12:20:00","13:30:00"),
	 (9,"Bristol","Glasgow","07:40:00","08:45:00"),
	 (10,"Glasgow","Newcastle","14:30:00","15:45:00"),
	 (11,"Newcastle","Manchester","16:15:00","17:05:00"),
	 (12,"Manchester","Bristol","18:25:00","19:30:00"),
	 (13,"Bristol","Manchester","06:20:00","07:20:00"),
	 (14,"Portsmouth","Dundee","12:00:00","14:00:00"),
	 (15,"Dundee","Portsmouth","10:00:00","12:00:00"),
	 (16,"Edinburgh","Cardiff","18:30:00","20:00:00"),
	 (17,"Southampton","Manchester","12:00:00","13:30:00"),
	 (18,"Manchester","Southampton","19:00:00","20:30:00"),
	 (19,"Birmingham","Newcastle","16:00:00","17:30:00"),
	 (20,"Newcastle","Birmingham","06:00:00","07:30:00"),
	 (21,"Aberdeen","Portsmouth","07:00:00","09:00:00");
	
INSERT INTO Prices VALUES
	(1,100.00),
	(2,60.00),
	(3,80.00),
	(4,90.00),
	(5,70.00),
	(6,75.00);
	
	
INSERT INTO TimeTableToPrices(PriceId,TimeId) VALUES
	(1,14),
	(1,15),
	(2,4),
	(2,5),
	(2,6),
	(3,1),
	(3,2),
	(3,3),
	(3,16),
	(4,9),
	(5,17),
	(5,18),
	(6,7),
	(6,8),
	(6,10),
	(6,11),
	(6,12),
	(6,13),
	(6,19),
	(6,20),
	(6,21);

INSERT INTO UserAccounts(UserName,EmailAddress,Password,Salt,isAdmin)VALUES
	("Test Admin","testadmin@test.com","b'$2b$12$c.G7hqE4QF6NsRl7URdng.NBfE5jZX41kAPTEaMlE7taRzJHKeTTy'","b'$2b$12$c.G7hqE4QF6NsRl7URdng.'",1),
	("Test User","testuser@test.com","b'$2b$12$0rKOVB0FHgGDXiDwyf0O/OZcsh.TwOyFHTd0WLBPL6y0DPAxHspU.'","b'$2b$12$0rKOVB0FHgGDXiDwyf0O/O'",0);

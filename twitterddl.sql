drop database twitter;
create database twitter;

\c twitter;

create table Users (
	UserId VARCHAR(50) NOT NULL,
	ScreenName VARCHAR(50) NOT NULL,
	Age INT,
	Gender VARCHAR(50),
	UserCreatedAt DATE,
	Verified VARCHAR(50),
	PRIMARY KEY (UserId)
);


create table Tweet (
	TweetId VARCHAR(50) NOT NULL,
	Text VARCHAR(50) NOT NULL,
	TweetCreatedAt DATE,
	Location VARCHAR(50),
	RetweetCount INT,
	FavouriteCount INT,
	UserId VARCHAR(50) NOT NULL,
	SourceType VARCHAR(50),
	PRIMARY KEY (TweetId),
	FOREIGN KEY (UserId) REFERENCES Users(UserId)
);


create table Source (
	Type VARCHAR(50) NOT NULL,
	PRIMARY KEY (Type)
);


create table Hashtag (
	Name VARCHAR(50) NOT NULL,
	UNIQUE (Name),
	PRIMARY KEY (Name)
);


create table Link (
	Address VARCHAR(1000) NOT NULL,
	Secured VARCHAR(50),
	PRIMARY KEY (Address)
);

Alter Table Tweet Add Constraint FK_SourceType FOREIGN KEY (SourceType) REFERENCES Source(Type);
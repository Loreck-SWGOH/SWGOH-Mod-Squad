-- Feel free to modify this file to match your development goal.

CREATE TABLE Users (
    ID int NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    email varchar UNIQUE NOT NULL,
    password varchar(255) NOT NULL,
    firstName varchar(255) NOT NULL,
    lastName varchar(255) NOT NULL,
    isAdmin int NOT NULL,
    CONSTRAINT usersPK PRIMARY KEY (ID),
    CONSTRAINT isAdminBool CHECK (isAdmin IN (1,0)) 
);

CREATE TABLE Clans (
    ID int NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    name varchar(255) NOT NULL,
    CONSTRAINT clansPK PRIMARY KEY (ID)
);

CREATE TABLE Profiles (
    userID int NOT NULL,
    joinDate date NOT NULL,
    allyCode int,
    swgohInfo varchar(255),
    swgohName varchar (255),
    clanID int,
    CONSTRAINT ProfilesPK PRIMARY KEY (userID),
    CONSTRAINT UsersFK FOREIGN KEY (userID) references Users(ID),
    CONSTRAINT ClansFK FOREIGN KEY (clanID) references Clans(ID)
);

CREATE TABLE GamePlay (
    ID int NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    name varchar (255),
    CONSTRAINT GamePlayPK PRIMARY KEY (ID)
);

CREATE TABLE Campaigns (
    ID int NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    gamePlayID int NOT NULL,
    name varchar(255),
    CONSTRAINT CampaignssPK PRIMARY KEY (ID),
    CONSTRAINT GamePlayFK FOREIGN KEY (gamePlayID) references GamePlay(ID)
);

CREATE TABLE Events (
    ID int NOT NULL GENERATED BY DEFAULT AS IDENTITY,
    campaignID int NOT NULL,
  	name varchar(255),
  	CONSTRAINT EventsPK PRIMARY KEY (ID),
  	CONSTRAINT CampaignsFK FOREIGN KEY (campaignID) references Campaigns(ID)
);

CREATE TABLE Products (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    name varchar(255) UNIQUE NOT NULL,
    price DECIMAL(12,2) NOT NULL,
    available BOOLEAN DEFAULT TRUE
);

CREATE TABLE Purchases (
    id INT NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
    uid INT NOT NULL REFERENCES Users(id),
    pid INT NOT NULL REFERENCES Products(id),
    time_purchased timestamp without time zone NOT NULL DEFAULT (current_timestamp AT TIME ZONE 'UTC')
);

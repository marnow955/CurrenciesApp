START TRANSACTION;

DROP DATABASE currenciesdb;

CREATE DATABASE currenciesdb CHARACTER SET utf8 COLLATE utf8_polish_ci;

USE currenciesdb;

CREATE TABLE `CURRENCY` 
(	`CODE`				        VARCHAR(4)			NOT NULL,
	`NAME`				        VARCHAR(60) 		NOT NULL,
	`TYPE`						VARCHAR(30)			NOT NULL, 
	`AREA`						VARCHAR(30)			,
	PRIMARY KEY (CODE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `CURRENCY_RATES` 
(	`ID`						INT(11)				NOT NULL AUTO_INCREMENT,  
	`CURRENCY_CODE`				VARCHAR(4) 			NOT NULL ,
	`BASE_CURRENCY_CODE`		VARCHAR(4)			NOT NULL ,
	`DATE`						DATETIME			NOT NULL ,
	`PRICE`						DECIMAL(65,4)		NOT NULL ,
	`CHANGE`					DECIMAL(65,2)		NOT NULL ,
	PRIMARY KEY (ID),
	FOREIGN KEY (CURRENCY_CODE) REFERENCES CURRENCY(CODE),
	FOREIGN KEY (BASE_CURRENCY_CODE) REFERENCES CURRENCY(CODE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `REPORT` 
(	`ID`						INT(11)				NOT NULL AUTO_INCREMENT,  
	`REPORT_DATE`				DATETIME		 	NOT NULL,
	`DATE_FROM`					DATETIME			NOT NULL, 
	`DATE_TO`					DATETIME			NOT NULL,
	`TYPE`						VARCHAR(30)			NOT NULL,
	PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `REPORT_CURRENCY` 
(	`CURRENCY_CODE`				VARCHAR(4)			NOT NULL,  
	`REPORT_ID`					INT(11)			 	NOT NULL,
	FOREIGN KEY (CURRENCY_CODE) REFERENCES CURRENCY(CODE),
	FOREIGN KEY (REPORT_ID) REFERENCES REPORT(ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `HPARAMS` 
(	`ID`						INT(11)				NOT NULL AUTO_INCREMENT,  
	`TRAINING_DATE`				DATETIME 			NOT NULL ,
	`NEURONS_NUM`				INT(11)				NOT NULL , 
	`ACTIV_FUNC`				VARCHAR(25)			NOT NULL ,
	`HID_LAYER_SIZE`			INT(11)				NOT NULL ,
	`DROPOUT`					DECIMAL(65,4)		NOT NULL ,
	`LOSS_FUNC`					VARCHAR(25)			NOT NULL ,
	`OPTIMIZER`					VARCHAR(25)			NOT NULL ,
	PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `PREDICTIONS` 
(	`ID`						INT(11)				NOT NULL AUTO_INCREMENT,  
	`CURRENCY_CODE`				VARCHAR(4) 			NOT NULL ,
	`MODEL_PARAMS_ID`			INT(11)				NOT NULL , 
	`TYPE`						VARCHAR(30)			NOT NULL ,
	`DATE`						DATETIME			NOT NULL ,
	`PRICE`						DECIMAL(65,4)		NOT NULL ,
	PRIMARY KEY (ID),
	FOREIGN KEY (CURRENCY_CODE) REFERENCES CURRENCY(CODE),
	FOREIGN KEY (MODEL_PARAMS_ID) REFERENCES HPARAMS(ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `USERS` 
(	`ID`						INT(11)				NOT NULL AUTO_INCREMENT,
	`USERNAME`					VARCHAR(20)			NOT NULL,
	`EMAIL`						VARCHAR(50)			NOT NULL,
	`PASSWORD`					VARCHAR(250)		NOT NULL,
	`FIRST_NAME`				VARCHAR(50)			NOT NULL,
	`LAST_NAME`					VARCHAR(100)		NOT NULL,
	`TOKEN`                     VARCHAR(600)        ,
	PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `FAVOURITES` 
(	`ID`                        INT(11)				NOT NULL AUTO_INCREMENT,
    `USER_ID`					INT(11)				NOT NULL,
	`CURRENCY_CODE`				VARCHAR(4)			NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (USER_ID) REFERENCES USERS(ID),
	FOREIGN KEY (CURRENCY_CODE) REFERENCES CURRENCY(CODE)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `EXCHANGE_OFFICES` 
(	`ID`						INT(11)				NOT NULL AUTO_INCREMENT,
	`NAME`						VARCHAR(150)		NOT NULL,
	`RANK`						INT(11)				,
	PRIMARY KEY (ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `ADDRESS` 
(	`ID`						INT(11)				NOT NULL UNIQUE,
	`COUNTRY`					VARCHAR(150)		NOT NULL,
	`PROVINCE`                  VARCHAR(150)        NOT NULL,
	`CITY`						VARCHAR(150)		NOT NULL,
	`STREET`					VARCHAR(150)		NOT NULL,
	`STREET_NUM`				INT(11)				,
	`FLAT_NUM`					INT(11)				,
	`POSTAL_CODE`				VARCHAR(10)			,
	FOREIGN KEY (ID) REFERENCES EXCHANGE_OFFICES(ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

CREATE TABLE `USER_COMMENTS` 
(	`ID`						INT(11)				NOT NULL AUTO_INCREMENT,
	`USER_ID`					INT(11)				NOT NULL,
	`EXCHANGE_OFFICE_ID`		INT(11)				NOT NULL,
	`COMMENT`					TEXT				NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (USER_ID) REFERENCES USERS(ID),
	FOREIGN KEY (EXCHANGE_OFFICE_ID) REFERENCES EXCHANGE_OFFICES(ID)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_polish_ci;

COMMIT;
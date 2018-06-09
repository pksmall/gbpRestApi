-- --------------------------------------------------------
-- Хост:                         127.0.0.1
-- Версия сервера:               10.3.7-MariaDB - mariadb.org binary distribution
-- Операционная система:         Win64
-- HeidiSQL Версия:              9.4.0.5125
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Дамп структуры базы данных searchandratewords
DROP DATABASE IF EXISTS `searchandratewords`;
CREATE DATABASE IF NOT EXISTS `searchandratewords` /*!40100 DEFAULT CHARACTER SET utf8 */;
USE `searchandratewords`;

-- Дамп структуры для таблица searchandratewords.keywords
CREATE TABLE IF NOT EXISTS `keywords` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `personID` int(11) NOT NULL,
  `name` varchar(2048) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_keywords_persons` (`personID`),
  CONSTRAINT `FK_keywords_persons` FOREIGN KEY (`personID`) REFERENCES `persons` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- Экспортируемые данные не выделены.
-- Дамп структуры для таблица searchandratewords.log
CREATE TABLE IF NOT EXISTS `log` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `adminID` int(11) NOT NULL,
  `action` varchar(2048) NOT NULL,
  `logDate` datetime NOT NULL DEFAULT current_timestamp(),
  PRIMARY KEY (`ID`),
  KEY `FK_log_users` (`adminID`),
  CONSTRAINT `FK_log_users` FOREIGN KEY (`adminID`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4;

-- Экспортируемые данные не выделены.
-- Дамп структуры для таблица searchandratewords.pages
CREATE TABLE IF NOT EXISTS `pages` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `siteID` int(11) NOT NULL,
  `URL` varchar(700) NOT NULL,
  `foundDateTime` datetime NOT NULL DEFAULT current_timestamp(),
  `lastScanDate` datetime DEFAULT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `URL` (`URL`),
  KEY `FK_pages_sites` (`siteID`),
  CONSTRAINT `FK_pages_sites` FOREIGN KEY (`siteID`) REFERENCES `sites` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Экспортируемые данные не выделены.
-- Дамп структуры для таблица searchandratewords.persons
CREATE TABLE IF NOT EXISTS `persons` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(2048) NOT NULL,
  `addedBy` int(11) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_persons_users` (`addedBy`),
  CONSTRAINT `FK_persons_users` FOREIGN KEY (`addedBy`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Экспортируемые данные не выделены.
-- Дамп структуры для таблица searchandratewords.personspagerank
CREATE TABLE IF NOT EXISTS `personspagerank` (
  `PersonID` int(11) NOT NULL,
  `PageID` int(11) NOT NULL,
  `Rank` int(11) DEFAULT NULL,
  KEY `FK_personspagerank_pages` (`PageID`),
  KEY `FK_personspagerank_persons` (`PersonID`),
  CONSTRAINT `FK_personspagerank_pages` FOREIGN KEY (`PageID`) REFERENCES `pages` (`ID`),
  CONSTRAINT `FK_personspagerank_persons` FOREIGN KEY (`PersonID`) REFERENCES `persons` (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Экспортируемые данные не выделены.
-- Дамп структуры для таблица searchandratewords.sites
CREATE TABLE IF NOT EXISTS `sites` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(2048) NOT NULL,
  `addedBy` int(11) NOT NULL,
  `siteDescription` varchar(2048) DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `FK_sites_users` (`addedBy`),
  CONSTRAINT `FK_sites_users` FOREIGN KEY (`addedBy`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

-- Экспортируемые данные не выделены.
-- Дамп структуры для таблица searchandratewords.users
CREATE TABLE IF NOT EXISTS `users` (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `parentID` int(11) DEFAULT NULL,
  `isAdmin` int(11) NOT NULL,
  `login` varchar(2048) NOT NULL,
  `password` varchar(2048) NOT NULL,
  `email` varchar(2048) NOT NULL,
  `token` varchar(700) DEFAULT NULL,
  `tokenCreatedDate` DATETIME DEFAULT current_timestamp(),
  `tokenLastAccess` DATETIME DEFAULT current_timestamp(),
  PRIMARY KEY (`ID`),
  KEY `FK_users_users` (`parentID`),
  UNIQUE KEY `token` (`token`),
  CONSTRAINT `FK_users_users` FOREIGN KEY (`parentID`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- Экспортируемые данные не выделены.
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

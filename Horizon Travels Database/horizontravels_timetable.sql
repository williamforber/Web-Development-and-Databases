CREATE DATABASE  IF NOT EXISTS `horizontravels` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `horizontravels`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: horizontravels
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `timetable`
--

DROP TABLE IF EXISTS `timetable`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `timetable` (
  `TimeId` int NOT NULL,
  `Origin` varchar(45) DEFAULT NULL,
  `Destination` varchar(45) DEFAULT NULL,
  `TimeToLeave` time DEFAULT NULL,
  `TimeToArrive` time DEFAULT NULL,
  PRIMARY KEY (`TimeId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `timetable`
--

LOCK TABLES `timetable` WRITE;
/*!40000 ALTER TABLE `timetable` DISABLE KEYS */;
INSERT INTO `timetable` VALUES (1,'Newcastle','Bristol','16:45:00','18:00:00'),(2,'Bristol','Newcastle','08:00:00','09:15:00'),(3,'Cardiff','Edinburgh','06:00:00','07:30:00'),(4,'Bristol','Manchester','11:30:00','12:30:00'),(5,'Manchester','Bristol','12:20:00','13:20:00'),(6,'Bristol','London','07:40:00','08:20:00'),(7,'London','Manchester','11:00:00','12:20:00'),(8,'Manchester','Glasgow','12:20:00','13:30:00'),(9,'Bristol','Glasgow','07:40:00','08:45:00'),(10,'Glasgow','Newcastle','14:30:00','15:45:00'),(11,'Newcastle','Manchester','16:15:00','17:05:00'),(12,'Manchester','Bristol','18:25:00','19:30:00'),(13,'Bristol','Manchester','06:20:00','07:20:00'),(14,'Portsmouth','Dundee','12:00:00','14:00:00'),(15,'Dundee','Portsmouth','10:00:00','12:00:00'),(16,'Edinburgh','Cardiff','18:30:00','20:00:00'),(17,'Southampton','Manchester','12:00:00','13:30:00'),(18,'Manchester','Southampton','19:00:00','20:30:00'),(19,'Birmingham','Newcastle','16:00:00','17:30:00'),(20,'Newcastle','Birmingham','06:00:00','07:30:00'),(21,'Aberdeen','Portsmouth','07:00:00','09:00:00');
/*!40000 ALTER TABLE `timetable` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-04-19 14:29:39

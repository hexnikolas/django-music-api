-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: localhost    Database: django_music
-- ------------------------------------------------------
-- Server version	8.0.33-0ubuntu0.22.04.2

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `album`
--
use django_music;
DROP TABLE IF EXISTS `album`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `album` (
  `name` varchar(100) NOT NULL,
  `type` varchar(20) NOT NULL,
  `artist_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`name`),
  KEY `album_artist_id_6f838eaa_fk_artist_name` (`artist_id`),
  CONSTRAINT `album_artist_id_6f838eaa_fk_artist_name` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `album`
--

LOCK TABLES `album` WRITE;
/*!40000 ALTER TABLE `album` DISABLE KEYS */;
INSERT INTO `album` VALUES ('1989','Album','Taylor Swift'),('AM','Album','Arctic Monkeys'),('Led Zeppelin IV','Single','Led Zeppelin'),('Listen','Album','David Guetta'),('Master of Puppets','EP','Metallica');
/*!40000 ALTER TABLE `album` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `artist`
--

DROP TABLE IF EXISTS `artist`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `artist` (
  `name` varchar(100) NOT NULL,
  `short_description` longtext NOT NULL,
  `genre` varchar(20) NOT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `artist`
--

LOCK TABLES `artist` WRITE;
/*!40000 ALTER TABLE `artist` DISABLE KEYS */;
INSERT INTO `artist` VALUES ('Arctic Monkeys','English indie rock band','Indie'),('David Guetta','French DJ and record producer','House'),('Led Zeppelin','English rock band','Rock'),('Metallica','American heavy metal band','Metal'),('Taylor Swift','American singer-songwriter','Pop');
/*!40000 ALTER TABLE `artist` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'music','0001_initial','2023-06-23 19:54:15.728959');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `track`
--

DROP TABLE IF EXISTS `track`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `track` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(100) NOT NULL,
  `lyrics` longtext,
  `duration` varchar(5) NOT NULL,
  `album_id` varchar(100) NOT NULL,
  `artist_id` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `track_album_id_66d5353c_fk_album_name` (`album_id`),
  KEY `track_artist_id_83139ff9_fk_artist_name` (`artist_id`),
  CONSTRAINT `track_album_id_66d5353c_fk_album_name` FOREIGN KEY (`album_id`) REFERENCES `album` (`name`),
  CONSTRAINT `track_artist_id_83139ff9_fk_artist_name` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `track`
--

LOCK TABLES `track` WRITE;
/*!40000 ALTER TABLE `track` DISABLE KEYS */;
INSERT INTO `track` VALUES (1,'Blank Space','Nice to meet you, where you been?','03:51','1989','Taylor Swift'),(2,'Shake It Off','I stay out too late, got nothing in my brain','03:39','1989','Taylor Swift'),(3,'Stairway to Heaven','There\'s a lady who\'s sure all that glitters is gold','08:02','Led Zeppelin IV','Led Zeppelin'),(4,'Enter Sandman','Say your prayers, little one, don\'t forget my son','05:31','Master of Puppets','Metallica'),(5,'Fade to Black','Life, it seems, will fade away','06:56','Master of Puppets','Metallica'),(6,'Do I Wanna Know?','Have you got color in your cheeks?','04:33','AM','Arctic Monkeys'),(7,'R U Mine?','I\'m a puppet on a string','03:21','AM','Arctic Monkeys'),(8,'Bad','Show me the way, show me the way','04:30','Listen','David Guetta'),(9,'Lovers on the Sun','We\'ll find a way to make it right','03:23','Listen','David Guetta');
/*!40000 ALTER TABLE `track` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `subscription_start` date DEFAULT NULL,
  `subscription_end` date DEFAULT NULL,
  `id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES ('2022-01-01','2023-01-01',1),('2023-01-01','2023-07-01',2),(NULL,NULL,3);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-06-24 17:36:29

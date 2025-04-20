-- MySQL dump 10.13  Distrib 5.1.56, for redhat-linux-gnu (x86_64)
--
-- Host: localhost    Database: biodb
-- ------------------------------------------------------
-- Server version	5.1.56

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `class`
--

DROP TABLE IF EXISTS `recipe`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recipe` (
  `id` varchar(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `area` varchar(255) DEFAULT NULL,
  `category_id` int(10) DEFAULT NULL,
  `instruction` TEXT NOT NULL,
  `img_link` TEXT DEFAULT NULL,
  `tags` varchar(255) DEFAULT NULL,
  `youtube_link` TEXT DEFAULT NULL,
  `rating` double DEFAULT NULL,
  `total_user_rated` int(10) DEFAULT NULL,
  `source_link` text DEFAULT NULL,
  `time_cooking` varchar(255) DEFAULT NULL,
  `etl_date` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
ALTER TABLE `recipe` CONVERT TO CHARACTER SET utf8;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `area`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `area` (
  `id` int(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `etl_date` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `category` (
  `id` int(10) NOT NULL,
  `name` varchar(255) NOT NULL,
  `img_link` TEXT DEFAULT NULL,
  `description` TEXT DEFAULT NULL,
  `etl_date` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `recipe_category`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `recipe_category` (
  `recipe_id` varchar(255) NOT NULL,
  `category_id` int(10) NOT NULL,
  `category_pred` varchar(255) DEFAULT NULL,
  `etl_date` varchar(10) NOT NULL,
  KEY `fk_category` (`category_id`),
  KEY `fk_recipe` (`recipe_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

DROP TABLE IF EXISTS `ingredient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `ingredient` (
  `id` int(10) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `serving_unit` varchar(20) DEFAULT NULL,
  `serving_size` double DEFAULT NULL,
  `amount_g` double DEFAULT NULL,
  `calories` double DEFAULT NULL,
  `total_fat_g` double DEFAULT NULL,
  `cholesterol_mg` double DEFAULT NULL,
  `sodium_mg` double DEFAULT NULL,
  `carbonhydrate_g` double DEFAULT NULL,
  `protein_g` double DEFAULT NULL,
  `calcium_mg` double DEFAULT NULL,
  `iron_mg` double DEFAULT NULL,
  `potassium_mg` double DEFAULT NULL,
  `vitamin_d_mcg` double DEFAULT NULL,
  `caffeine_mg` double DEFAULT NULL,
  `img_link` TEXT DEFAULT NULL,
  `etl_date` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;


DROP TABLE IF EXISTS `measure`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `measure` (
  `recipe_id` varchar(10) NOT NULL,
  `ingredient_name_in_meal` varchar(255) NOT NULL,
  `map_perc` double default null,
  `map_ingredient_id` int(10) NOT NULL,
  `map_ingredient_name` varchar(255) NOT NULL,
  `measure_quantity` double DEFAULT NULL,
  `measure_unit` varchar(20) DEFAULT NULL,
  `etl_date` varchar(10) NOT NULL,
  KEY `fk_igredient` (`map_ingredient_id`),
  KEY `fk_recipe` (`recipe_id`)
) ENGINE=MyISAM DEFAULT CHARSET=latin1;
ALTER TABLE `measure` CONVERT TO CHARACTER SET utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
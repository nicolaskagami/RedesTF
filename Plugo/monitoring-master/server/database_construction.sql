CREATE DATABASE  IF NOT EXISTS `monitor` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `monitor`;
-- MySQL dump 10.13  Distrib 5.6.19, for osx10.7 (i386)
--
-- Host: localhost    Database: monitor
-- ------------------------------------------------------
-- Server version	5.6.14

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
-- Table structure for table `audio_bytes_decoded_per_second`
--

DROP TABLE IF EXISTS `audio_bytes_decoded_per_second`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `audio_bytes_decoded_per_second` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_audio_bytes_decoded` bigint(64) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  `audio_bytes` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `audio_bytes_decoded_per_second`
--

LOCK TABLES `audio_bytes_decoded_per_second` WRITE;
/*!40000 ALTER TABLE `audio_bytes_decoded_per_second` DISABLE KEYS */;
INSERT INTO `audio_bytes_decoded_per_second` VALUES (1,176.043,1438263884025,0,144999),(2,177.041,1438263885030,0,31650),(3,178.04,1438263886032,0,27969),(4,177.343,1438263901723,1,186953);
/*!40000 ALTER TABLE `audio_bytes_decoded_per_second` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `buffer_interval`
--

DROP TABLE IF EXISTS `buffer_interval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `buffer_interval` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_buffer_time` float NOT NULL,
  `end_buffer_time` float NOT NULL,
  `video_information_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `buffer_interval`
--

LOCK TABLES `buffer_interval` WRITE;
/*!40000 ALTER TABLE `buffer_interval` DISABLE KEYS */;
INSERT INTO `buffer_interval` VALUES (1,0,14.656,0),(2,172.8,178.214,0),(3,0,14.656,1),(4,172.8,178.214,1);
/*!40000 ALTER TABLE `buffer_interval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `frame_per_second`
--

DROP TABLE IF EXISTS `frame_per_second`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `frame_per_second` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_frame` bigint(64) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  `number_of_frames` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `frame_per_second`
--

LOCK TABLES `frame_per_second` WRITE;
/*!40000 ALTER TABLE `frame_per_second` DISABLE KEYS */;
INSERT INTO `frame_per_second` VALUES (1,176.043,1438263884025,0,107),(2,177.041,1438263885030,0,25),(3,178.04,1438263886032,0,23),(4,177.343,1438263901723,1,141);
/*!40000 ALTER TABLE `frame_per_second` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `length_of_stall`
--

DROP TABLE IF EXISTS `length_of_stall`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `length_of_stall` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_stall` bigint(64) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  `duration_of_stall` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `length_of_stall`
--

LOCK TABLES `length_of_stall` WRITE;
/*!40000 ALTER TABLE `length_of_stall` DISABLE KEYS */;
INSERT INTO `length_of_stall` VALUES (1,175.788,1438263883684,0,0.104),(2,0,1438263899768,1,0.102),(3,176.484,1438263900642,1,0.26);
/*!40000 ALTER TABLE `length_of_stall` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `mute_state`
--

DROP TABLE IF EXISTS `mute_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `mute_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_mute_state` bigint(64) NOT NULL,
  `state` int(11) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `mute_state`
--

LOCK TABLES `mute_state` WRITE;
/*!40000 ALTER TABLE `mute_state` DISABLE KEYS */;
INSERT INTO `mute_state` VALUES (1,176.043,1438263884026,0,0),(2,176.484,1438263900723,0,1);
/*!40000 ALTER TABLE `mute_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `network_state`
--

DROP TABLE IF EXISTS `network_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `network_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_network_state` bigint(64) NOT NULL,
  `state` int(11) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `network_state`
--

LOCK TABLES `network_state` WRITE;
/*!40000 ALTER TABLE `network_state` DISABLE KEYS */;
INSERT INTO `network_state` VALUES (1,176.043,1438263884026,1,0),(2,176.484,1438263900723,1,1);
/*!40000 ALTER TABLE `network_state` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `playback_quality`
--

DROP TABLE IF EXISTS `playback_quality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `playback_quality` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `timestamp_of_quality` bigint(64) NOT NULL,
  `current_video_position` float NOT NULL,
  `video_width` int(11) NOT NULL,
  `video_height` int(11) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `playback_quality`
--

LOCK TABLES `playback_quality` WRITE;
/*!40000 ALTER TABLE `playback_quality` DISABLE KEYS */;
INSERT INTO `playback_quality` VALUES (1,1438263884024,0,1280,720,0),(2,1438263900721,0,1280,720,1);
/*!40000 ALTER TABLE `playback_quality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `played_interval`
--

DROP TABLE IF EXISTS `played_interval`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `played_interval` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_play` float NOT NULL,
  `end_play` float NOT NULL,
  `video_information_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `played_interval`
--

LOCK TABLES `played_interval` WRITE;
/*!40000 ALTER TABLE `played_interval` DISABLE KEYS */;
INSERT INTO `played_interval` VALUES (1,0,0.719245,0),(2,175.788,178.214,0),(3,0,0.742464,1),(4,176.484,178.214,1);
/*!40000 ALTER TABLE `played_interval` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `questionario`
--

DROP TABLE IF EXISTS `questionario`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `questionario` (
  `idquestionario` int(11) NOT NULL AUTO_INCREMENT,
  `ip` varchar(40) NOT NULL,
  `hash` varchar(64) NOT NULL,
  `rating` int(11) DEFAULT NULL,
  `timestamp` bigint(64) DEFAULT NULL,
  `conteudo` varchar(64) DEFAULT NULL,
  `diario` int(11) DEFAULT NULL,
  `idade` int(11) DEFAULT NULL,
  `sexo` varchar(12) DEFAULT NULL,
  `pais` varchar(45) DEFAULT NULL,
  `tempo` int(11) DEFAULT NULL,
  `comentario` varchar(300) DEFAULT NULL,
  `opinion` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`idquestionario`),
  UNIQUE KEY `idquestionario_UNIQUE` (`idquestionario`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `questionario`
--

LOCK TABLES `questionario` WRITE;
/*!40000 ALTER TABLE `questionario` DISABLE KEYS */;
/*!40000 ALTER TABLE `questionario` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `skip_play`
--

DROP TABLE IF EXISTS `skip_play`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `skip_play` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_skip` bigint(64) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  `skip_duration` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `skip_play`
--

LOCK TABLES `skip_play` WRITE;
/*!40000 ALTER TABLE `skip_play` DISABLE KEYS */;
INSERT INTO `skip_play` VALUES (1,0,1438263883016,0,0.510274),(2,0.719245,1438263883529,0,175.138),(3,0,1438263899714,1,0.115551),(4,0.719245,1438263900532,1,175.857);
/*!40000 ALTER TABLE `skip_play` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_in_buffer`
--

DROP TABLE IF EXISTS `time_in_buffer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `time_in_buffer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_time` bigint(64) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  `remaining_time_in_buffer` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_in_buffer`
--

LOCK TABLES `time_in_buffer` WRITE;
/*!40000 ALTER TABLE `time_in_buffer` DISABLE KEYS */;
INSERT INTO `time_in_buffer` VALUES (1,176.043,1438263884025,0,2.17092),(2,177.041,1438263885030,0,1.17251),(3,178.04,1438263886032,0,0.174091),(4,176.484,1438263900722,1,1.7296),(5,177.343,1438263901723,1,0.87104);
/*!40000 ALTER TABLE `time_in_buffer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_bytes_decoded_per_second`
--

DROP TABLE IF EXISTS `video_bytes_decoded_per_second`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_bytes_decoded_per_second` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_video_bytes_decoded` bigint(64) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  `video_bytes` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_bytes_decoded_per_second`
--

LOCK TABLES `video_bytes_decoded_per_second` WRITE;
/*!40000 ALTER TABLE `video_bytes_decoded_per_second` DISABLE KEYS */;
INSERT INTO `video_bytes_decoded_per_second` VALUES (1,176.043,1438263884025,0,758882),(2,177.041,1438263885030,0,68495),(3,178.04,1438263886032,0,239),(4,177.343,1438263901723,1,828291);
/*!40000 ALTER TABLE `video_bytes_decoded_per_second` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_information`
--

DROP TABLE IF EXISTS `video_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_information` (
  `ip` varchar(40) NOT NULL,
  `start_timestamp` bigint(64) NOT NULL,
  `hash` varchar(64) NOT NULL,
  `netmetric` varchar(45) DEFAULT NULL,
  `total_played_time` float NOT NULL,
  `total_played_time_with_stall` float NOT NULL,
  `total_stall_length` float NOT NULL,
  `total_number_of_stall` float NOT NULL,
  `video_duration` float NOT NULL,
  `dropped_frames` int(11) NOT NULL,
  `left_time` float NOT NULL,
  `video_information_id` int(11) NOT NULL DEFAULT '0',
  `video_preload` varchar(16) NOT NULL,
  `video_start_time` float NOT NULL,
  PRIMARY KEY (`ip`,`start_timestamp`,`hash`),
  UNIQUE KEY `video_information_id_UNIQUE` (`video_information_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_information`
--

LOCK TABLES `video_information` WRITE;
/*!40000 ALTER TABLE `video_information` DISABLE KEYS */;
INSERT INTO `video_information` VALUES ('::ffff:127.0.0.1',1438263883015,'XEcW6glE3lxRdmrMqeMhucVJE5AVWpiG8AgG4Qjexbu9Mag7UtobSpTCceccyRHM','',3.14504,3.24903,0.104,1,178.214,0,178.214,0,'auto',0),('::ffff:127.0.0.1',1438263899713,'AdOlym5FUEODi5bTMQzVJThws5vg7746TB60FK7KItzO72rbR0UNIOMwLJ2dN8mv','',2.47206,2.83406,0.362,2,178.214,0,178.214,1,'auto',0.102);
/*!40000 ALTER TABLE `video_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `video_source`
--

DROP TABLE IF EXISTS `video_source`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `video_source` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `source` varchar(512) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `video_source`
--

LOCK TABLES `video_source` WRITE;
/*!40000 ALTER TABLE `video_source` DISABLE KEYS */;
INSERT INTO `video_source` VALUES (1,'http://200.220.254.22/b.html',0),(2,'http://200.220.254.22/hobbit-720p.mp4',0),(3,'http://200.220.254.22/b.html',1),(4,'http://200.220.254.22/hobbit-720p.mp4',1);
/*!40000 ALTER TABLE `video_source` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `volume_state`
--

DROP TABLE IF EXISTS `volume_state`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `volume_state` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `current_video_position` float NOT NULL,
  `timestamp_of_volume` bigint(64) NOT NULL,
  `video_information_id` int(11) NOT NULL,
  `volume` float NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `volume_state`
--

LOCK TABLES `volume_state` WRITE;
/*!40000 ALTER TABLE `volume_state` DISABLE KEYS */;
INSERT INTO `volume_state` VALUES (1,176.043,1438263884026,0,1),(2,176.484,1438263900723,1,1);
/*!40000 ALTER TABLE `volume_state` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2015-07-30 10:52:34

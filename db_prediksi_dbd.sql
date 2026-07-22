mysqldump: Deprecated program name. It will be removed in a future release, use '/usr/bin/mariadb-dump' instead
/*M!999999\- enable the sandbox mode */ 
-- MariaDB dump 10.19-12.3.2-MariaDB, for Linux (x86_64)
--
-- Host: localhost    Database: db_prediksi_dbd
-- ------------------------------------------------------
-- Server version	12.3.2-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*M!100616 SET @OLD_NOTE_VERBOSITY=@@NOTE_VERBOSITY, NOTE_VERBOSITY=0 */;

--
-- Table structure for table `data_training`
--

DROP TABLE IF EXISTS `data_training`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `data_training` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bulan` int(11) NOT NULL,
  `tahun` int(11) NOT NULL,
  `jumlah_kasus` int(11) NOT NULL,
  `rata_rata_usia` decimal(5,2) DEFAULT NULL,
  `jumlah_laki` int(11) DEFAULT 0,
  `jumlah_perempuan` int(11) DEFAULT 0,
  `rata_rata_lama_rawat` decimal(5,2) DEFAULT NULL,
  `tingkat_risiko` enum('Rendah','Sedang','Tinggi') NOT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `data_training`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `data_training` WRITE;
/*!40000 ALTER TABLE `data_training` DISABLE KEYS */;
/*!40000 ALTER TABLE `data_training` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `hasil_prediksi`
--

DROP TABLE IF EXISTS `hasil_prediksi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `hasil_prediksi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tanggal_prediksi` datetime NOT NULL,
  `bulan_prediksi` varchar(20) NOT NULL,
  `tahun_prediksi` int(11) NOT NULL,
  `jumlah_kasus_prediksi` int(11) DEFAULT NULL,
  `tingkat_risiko_prediksi` enum('Rendah','Sedang','Tinggi') DEFAULT NULL,
  `confidence_score` decimal(5,2) DEFAULT NULL,
  `model_version` varchar(50) DEFAULT NULL,
  `created_by` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `created_by` (`created_by`),
  CONSTRAINT `hasil_prediksi_ibfk_1` FOREIGN KEY (`created_by`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hasil_prediksi`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `hasil_prediksi` WRITE;
/*!40000 ALTER TABLE `hasil_prediksi` DISABLE KEYS */;
INSERT INTO `hasil_prediksi` VALUES
(1,'2026-02-07 22:46:33','Maret',2026,NULL,'Sedang',52.00,'1.0.0',1,'2026-02-07 15:46:33'),
(2,'2026-02-07 23:28:29','Januari',2026,12,'Sedang',76.00,'1.0.0',1,'2026-02-07 16:28:29'),
(3,'2026-02-07 23:28:29','September',2026,18,'Sedang',80.00,'1.0.0',1,'2026-02-07 16:28:29'),
(4,'2026-02-07 23:28:29','April',2026,4,'Sedang',88.00,'1.0.0',1,'2026-02-07 16:28:29'),
(5,'2026-02-07 23:28:29','Oktober',2026,33,'Tinggi',76.00,'1.0.0',1,'2026-02-07 16:28:29'),
(6,'2026-02-07 23:28:29','Desember',2026,3,'Sedang',92.00,'1.0.0',1,'2026-02-07 16:28:29'),
(7,'2026-02-07 23:55:20','Mei',2026,NULL,'Sedang',56.00,'1.0.0',1,'2026-02-07 16:55:20'),
(8,'2026-02-08 00:10:45','Juni',2026,20,'Sedang',48.00,'1.0.0',2,'2026-02-07 17:10:45'),
(9,'2026-02-08 00:10:45','Januari',2026,5,'Tinggi',50.67,'1.0.0',2,'2026-02-07 17:10:45'),
(10,'2026-02-08 00:10:45','Januari',2026,30,'Tinggi',40.00,'1.0.0',2,'2026-02-07 17:10:45'),
(11,'2026-02-08 00:10:45','Juli',2026,3,'Tinggi',76.00,'1.0.0',2,'2026-02-07 17:10:45'),
(12,'2026-02-08 00:15:10','Juni',2026,20,'Sedang',48.00,'1.0.0',2,'2026-02-07 17:15:10'),
(13,'2026-02-08 00:15:10','Januari',2026,5,'Tinggi',50.67,'1.0.0',2,'2026-02-07 17:15:10'),
(14,'2026-02-08 00:15:10','Januari',2026,30,'Tinggi',40.00,'1.0.0',2,'2026-02-07 17:15:10'),
(15,'2026-02-08 00:15:10','Juli',2026,3,'Tinggi',76.00,'1.0.0',2,'2026-02-07 17:15:10'),
(16,'2026-02-08 00:19:21','Juni',2026,20,'Sedang',48.00,'1.0.0',2,'2026-02-07 17:19:21'),
(17,'2026-02-08 00:19:21','Januari',2026,5,'Tinggi',50.67,'1.0.0',2,'2026-02-07 17:19:21'),
(18,'2026-02-08 00:19:21','Januari',2026,30,'Tinggi',40.00,'1.0.0',2,'2026-02-07 17:19:21'),
(19,'2026-02-08 00:19:21','Juli',2026,3,'Tinggi',76.00,'1.0.0',2,'2026-02-07 17:19:21'),
(20,'2026-02-08 00:23:02','Juni',2026,20,'Sedang',48.00,'1.0.0',2,'2026-02-07 17:23:02'),
(21,'2026-02-08 00:23:02','Januari',2026,5,'Tinggi',50.67,'1.0.0',2,'2026-02-07 17:23:02'),
(22,'2026-02-08 00:23:02','Januari',2026,30,'Tinggi',40.00,'1.0.0',2,'2026-02-07 17:23:02'),
(23,'2026-02-08 00:23:02','Juli',2026,3,'Tinggi',76.00,'1.0.0',2,'2026-02-07 17:23:02'),
(24,'2026-02-08 14:13:30','Januari',2026,5,'Rendah',100.00,'1.0.0',2,'2026-02-08 07:13:30'),
(25,'2026-02-08 14:13:30','Maret',2026,12,'Sedang',76.00,'1.0.0',2,'2026-02-08 07:13:30'),
(26,'2026-02-08 14:13:30','September',2026,20,'Tinggi',72.00,'1.0.0',2,'2026-02-08 07:13:30'),
(27,'2026-02-08 14:13:30','Oktober',2026,33,'Tinggi',72.00,'1.0.0',2,'2026-02-08 07:13:30'),
(28,'2026-02-08 14:13:30','Desember',2026,3,'Rendah',64.00,'1.0.0',2,'2026-02-08 07:13:30'),
(29,'2026-07-21 21:26:06','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 14:26:06'),
(30,'2026-07-21 21:31:55','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 14:31:55'),
(31,'2026-07-21 21:34:25','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 14:34:25'),
(32,'2026-07-21 21:40:04','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 14:40:04'),
(33,'2026-07-21 21:40:04','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 14:40:04'),
(34,'2026-07-21 21:41:34','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 14:41:34'),
(35,'2026-07-21 21:41:36','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 14:41:36'),
(36,'2026-07-21 22:45:10','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 15:45:10'),
(37,'2026-07-21 22:45:12','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 15:45:12'),
(38,'2026-07-21 22:45:47','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 15:45:47'),
(39,'2026-07-21 22:45:49','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 15:45:49'),
(40,'2026-07-21 22:46:46','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 15:46:46'),
(41,'2026-07-21 22:46:47','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 15:46:47'),
(42,'2026-07-22 00:03:15','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 17:03:15'),
(43,'2026-07-22 00:03:17','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 17:03:17'),
(44,'2026-07-22 06:36:25','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 23:36:25'),
(45,'2026-07-22 06:36:30','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 23:36:30'),
(46,'2026-07-22 06:40:53','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 23:40:53'),
(47,'2026-07-22 06:40:55','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 23:40:55'),
(48,'2026-07-22 06:47:55','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 23:47:55'),
(49,'2026-07-22 06:47:57','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-21 23:47:57'),
(50,'2026-07-22 07:37:15','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 00:37:15'),
(51,'2026-07-22 07:37:17','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 00:37:17'),
(52,'2026-07-22 07:37:32','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 00:37:32'),
(53,'2026-07-22 07:38:17','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 00:38:17'),
(54,'2026-07-22 07:38:19','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 00:38:19'),
(55,'2026-07-22 08:48:36','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 01:48:36'),
(56,'2026-07-22 08:51:24','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 01:51:24'),
(57,'2026-07-22 09:11:50','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 02:11:50'),
(58,'2026-07-22 09:11:53','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 02:11:53'),
(59,'2026-07-22 09:19:39','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 02:19:39'),
(60,'2026-07-22 09:19:42','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 02:19:42'),
(61,'2026-07-22 09:48:23','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 02:48:23'),
(62,'2026-07-22 09:48:25','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 02:48:25'),
(63,'2026-07-22 10:23:42','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 03:23:42'),
(64,'2026-07-22 10:23:43','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 03:23:43'),
(65,'2026-07-22 10:24:00','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 03:24:00'),
(66,'2026-07-22 10:24:01','Januari',2026,NULL,'Sedang',100.00,'1.0.0',1,'2026-07-22 03:24:01');
/*!40000 ALTER TABLE `hasil_prediksi` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `kasus_bulanan`
--

DROP TABLE IF EXISTS `kasus_bulanan`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `kasus_bulanan` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `bulan` varchar(20) NOT NULL,
  `tahun` int(11) NOT NULL,
  `jumlah_kasus` int(11) DEFAULT 0,
  `jumlah_sembuh` int(11) DEFAULT 0,
  `jumlah_meninggal` int(11) DEFAULT 0,
  `tingkat_risiko` enum('Rendah','Sedang','Tinggi') DEFAULT 'Sedang',
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kasus_bulanan`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `kasus_bulanan` WRITE;
/*!40000 ALTER TABLE `kasus_bulanan` DISABLE KEYS */;
INSERT INTO `kasus_bulanan` VALUES
(85,'Januari',2024,14,0,0,'Sedang','2026-07-22 04:13:00'),
(86,'Februari',2024,14,0,0,'Sedang','2026-07-22 04:13:00'),
(87,'Maret',2024,14,0,0,'Sedang','2026-07-22 04:13:00'),
(88,'April',2024,14,0,0,'Sedang','2026-07-22 04:13:00'),
(89,'Mei',2024,14,0,0,'Sedang','2026-07-22 04:13:00'),
(90,'Juni',2024,14,0,0,'Sedang','2026-07-22 04:13:00'),
(91,'Juli',2024,14,0,0,'Sedang','2026-07-22 04:13:00'),
(92,'Agustus',2024,13,0,0,'Sedang','2026-07-22 04:13:00'),
(93,'September',2024,13,0,0,'Sedang','2026-07-22 04:13:00'),
(94,'Oktober',2024,13,0,0,'Sedang','2026-07-22 04:13:00'),
(95,'November',2024,13,0,0,'Sedang','2026-07-22 04:13:00'),
(96,'Desember',2024,13,0,0,'Sedang','2026-07-22 04:13:00');
/*!40000 ALTER TABLE `kasus_bulanan` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `log_aktivitas`
--

DROP TABLE IF EXISTS `log_aktivitas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `log_aktivitas` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `aksi` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `ip_address` varchar(45) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `log_aktivitas_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_aktivitas`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `log_aktivitas` WRITE;
/*!40000 ALTER TABLE `log_aktivitas` DISABLE KEYS */;
INSERT INTO `log_aktivitas` VALUES
(1,1,'Login','Login berhasil','127.0.0.1','2026-01-28 18:24:47'),
(2,1,'Login','Login berhasil','127.0.0.1','2026-02-01 15:58:29'),
(3,1,'Login','Login berhasil','127.0.0.1','2026-02-05 09:20:57'),
(4,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-05 10:00:47'),
(5,1,'Login','Login berhasil','127.0.0.1','2026-02-05 10:00:54'),
(6,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-05 10:02:50'),
(7,1,'Login','Login berhasil','127.0.0.1','2026-02-05 10:06:57'),
(8,1,'UPDATE_USER','Mengubah data pengguna: pimpinan','127.0.0.1','2026-02-05 11:01:40'),
(9,1,'UPDATE_USER','Mengubah data pengguna: petugas','127.0.0.1','2026-02-05 11:01:48'),
(10,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-05 11:01:51'),
(11,NULL,'Login','Login berhasil','127.0.0.1','2026-02-05 11:01:58'),
(12,NULL,'Logout','Logout dari sistem','127.0.0.1','2026-02-05 11:02:01'),
(13,2,'Login','Login berhasil','127.0.0.1','2026-02-05 11:02:06'),
(14,2,'Logout','Logout dari sistem','127.0.0.1','2026-02-05 11:02:12'),
(15,1,'Login','Login berhasil','127.0.0.1','2026-02-05 18:34:55'),
(16,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-05 18:35:03'),
(17,1,'Login','Login berhasil','127.0.0.1','2026-02-05 18:44:32'),
(18,1,'Login','Login berhasil','127.0.0.1','2026-02-07 15:20:53'),
(19,1,'Login','Login berhasil','127.0.0.1','2026-02-07 16:01:21'),
(20,1,'Login','Login berhasil','127.0.0.1','2026-02-07 16:28:29'),
(21,1,'Login','Login berhasil','127.0.0.1','2026-02-07 17:10:44'),
(22,2,'Login','Login berhasil','127.0.0.1','2026-02-07 17:10:44'),
(23,NULL,'Login','Login berhasil','127.0.0.1','2026-02-07 17:10:44'),
(24,1,'CREATE_USER','Menambah pengguna baru: testuser99','127.0.0.1','2026-02-07 17:10:44'),
(25,1,'UPDATE_USER','Mengubah data pengguna: testuser99','127.0.0.1','2026-02-07 17:10:45'),
(26,1,'DELETE_USER','Menghapus pengguna: testuser99','127.0.0.1','2026-02-07 17:10:45'),
(27,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-07 17:10:45'),
(28,1,'Login','Login berhasil','127.0.0.1','2026-02-07 17:15:09'),
(29,2,'Login','Login berhasil','127.0.0.1','2026-02-07 17:15:09'),
(30,NULL,'Login','Login berhasil','127.0.0.1','2026-02-07 17:15:09'),
(31,1,'CREATE_USER','Menambah pengguna baru: testv2user','127.0.0.1','2026-02-07 17:15:10'),
(32,1,'UPDATE_USER','Mengubah data pengguna: admin','127.0.0.1','2026-02-07 17:15:10'),
(33,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-07 17:15:10'),
(34,1,'Login','Login berhasil','127.0.0.1','2026-02-07 17:17:13'),
(35,1,'Login','Login berhasil','127.0.0.1','2026-02-07 17:19:20'),
(36,2,'Login','Login berhasil','127.0.0.1','2026-02-07 17:19:20'),
(37,NULL,'Login','Login berhasil','127.0.0.1','2026-02-07 17:19:20'),
(38,1,'CREATE_USER','Menambah pengguna baru: testv2user','127.0.0.1','2026-02-07 17:19:20'),
(39,1,'UPDATE_USER','Mengubah data pengguna: admin','127.0.0.1','2026-02-07 17:19:20'),
(40,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-07 17:19:21'),
(41,1,'Login','Login berhasil','127.0.0.1','2026-02-07 17:20:20'),
(42,1,'Login','Login berhasil','127.0.0.1','2026-02-07 17:23:01'),
(43,2,'Login','Login berhasil','127.0.0.1','2026-02-07 17:23:01'),
(44,NULL,'Login','Login berhasil','127.0.0.1','2026-02-07 17:23:01'),
(45,1,'CREATE_USER','Menambah pengguna baru: testv2user','127.0.0.1','2026-02-07 17:23:02'),
(46,1,'UPDATE_USER','Mengubah data pengguna: testv2user','127.0.0.1','2026-02-07 17:23:02'),
(47,1,'DELETE_USER','Menghapus pengguna: testv2user','127.0.0.1','2026-02-07 17:23:02'),
(48,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-07 17:23:02'),
(49,1,'Login','Login berhasil','127.0.0.1','2026-02-08 07:00:33'),
(50,2,'Login','Login berhasil','127.0.0.1','2026-02-08 07:13:29'),
(51,1,'Logout','Logout dari sistem','127.0.0.1','2026-02-08 07:19:43'),
(52,1,'Login','Login berhasil','127.0.0.1','2026-02-08 07:19:52'),
(53,1,'Login','Login berhasil','127.0.0.1','2026-02-08 10:05:55'),
(54,1,'DELETE_USER','Menghapus pengguna: pimpinan','127.0.0.1','2026-02-08 10:13:17'),
(55,1,'Login','Login berhasil','127.0.0.1','2026-02-11 12:04:55'),
(56,1,'Login','Login berhasil','127.0.0.1','2026-07-21 08:03:04'),
(57,1,'Logout','Logout dari sistem','127.0.0.1','2026-07-21 08:04:09'),
(58,2,'Login','Login berhasil','127.0.0.1','2026-07-21 08:04:26'),
(59,2,'Logout','Logout dari sistem','127.0.0.1','2026-07-21 08:10:56'),
(60,1,'Login','Login berhasil','127.0.0.1','2026-07-21 08:10:59'),
(61,1,'Login','Login berhasil','127.0.0.1','2026-07-21 10:58:10'),
(62,1,'Login','Login berhasil','127.0.0.1','2026-07-21 13:15:02'),
(63,1,'Login','Login berhasil','127.0.0.1','2026-07-21 13:41:06'),
(64,1,'Import Data Excel','Berhasil mengimport 163 data pasien dari file Data DBD 15 Sampel.xlsx','127.0.0.1','2026-07-21 13:48:01'),
(65,1,'Logout','Logout dari sistem','127.0.0.1','2026-07-21 14:36:21'),
(66,2,'Login','Login berhasil','127.0.0.1','2026-07-21 14:36:24'),
(67,1,'Login','Login berhasil','127.0.0.1','2026-07-21 14:39:10'),
(68,1,'Login','Login berhasil','127.0.0.1','2026-07-21 14:40:18'),
(69,1,'Login','Login berhasil','127.0.0.1','2026-07-21 14:40:31'),
(70,2,'Logout','Logout dari sistem','127.0.0.1','2026-07-21 14:45:33'),
(71,2,'Login','Login berhasil','127.0.0.1','2026-07-21 14:46:20'),
(72,2,'Logout','Logout dari sistem','127.0.0.1','2026-07-21 14:46:24'),
(73,1,'Login','Login berhasil','127.0.0.1','2026-07-21 14:46:29'),
(74,1,'Login','Login berhasil','127.0.0.1','2026-07-21 15:36:01'),
(75,1,'Login','Login berhasil','127.0.0.1','2026-07-21 15:46:32'),
(76,1,'Login','Login berhasil','127.0.0.1','2026-07-21 15:48:33'),
(77,1,'Logout','Logout dari sistem','127.0.0.1','2026-07-21 16:12:03'),
(78,2,'Login','Login berhasil','127.0.0.1','2026-07-21 16:12:09'),
(79,2,'Login','Login berhasil','127.0.0.1','2026-07-21 16:12:32'),
(80,1,'Login','Login berhasil','127.0.0.1','2026-07-21 16:13:12'),
(81,1,'Login','Login berhasil','127.0.0.1','2026-07-21 16:13:34'),
(82,1,'Login','Login berhasil','127.0.0.1','2026-07-21 16:20:20'),
(83,1,'Login','Login berhasil','127.0.0.1','2026-07-21 16:34:51'),
(84,1,'Login','Login berhasil','127.0.0.1','2026-07-21 16:53:37'),
(85,1,'Login','Login berhasil','127.0.0.1','2026-07-22 01:04:12'),
(86,1,'Login','Login berhasil','127.0.0.1','2026-07-22 01:06:43'),
(87,1,'Login','Login berhasil','127.0.0.1','2026-07-22 02:23:00'),
(88,1,'Login','Login berhasil','127.0.0.1','2026-07-22 02:47:14'),
(89,1,'Login','Login berhasil','127.0.0.1','2026-07-22 03:07:48'),
(90,1,'Import Data Excel','Berhasil mengimport 2 data pasien dari file test_import.xlsx','127.0.0.1','2026-07-22 03:15:44'),
(91,1,'Hapus Semua Data','Berhasil menghapus 205 data pasien','127.0.0.1','2026-07-22 03:16:05');
/*!40000 ALTER TABLE `log_aktivitas` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `model_evaluasi`
--

DROP TABLE IF EXISTS `model_evaluasi`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `model_evaluasi` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tanggal_training` datetime NOT NULL,
  `accuracy` decimal(5,4) DEFAULT NULL,
  `precision_score` decimal(5,4) DEFAULT NULL,
  `recall_score` decimal(5,4) DEFAULT NULL,
  `f1_score` decimal(5,4) DEFAULT NULL,
  `mae` decimal(10,4) DEFAULT NULL,
  `rmse` decimal(10,4) DEFAULT NULL,
  `r2_score` decimal(5,4) DEFAULT NULL,
  `n_estimators` int(11) DEFAULT NULL,
  `max_depth` int(11) DEFAULT NULL,
  `confusion_matrix` text DEFAULT NULL,
  `feature_importance` text DEFAULT NULL,
  `model_path` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=120 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_evaluasi`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `model_evaluasi` WRITE;
/*!40000 ALTER TABLE `model_evaluasi` DISABLE KEYS */;
INSERT INTO `model_evaluasi` VALUES
(1,'2026-01-29 01:24:53',1.0000,1.0000,1.0000,1.0000,NULL,NULL,NULL,100,NULL,'[[1, 0, 0], [0, 1, 0], [0, 0, 1]]','{\"bulan\": 0.33917424815522634, \"jumlah_kasus\": 0.6608257518447738, \"usia\": 0.0, \"jenis_kelamin\": 0.0, \"lama_rawat\": 0.0}','models/random_forest_model.pkl','2026-01-28 18:24:53'),
(2,'2026-02-07 22:38:10',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 15:38:10'),
(3,'2026-02-07 22:46:10',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,10,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 15:46:10'),
(4,'2026-02-07 22:46:59',0.2500,0.1667,0.2500,0.2000,0.7500,0.8660,-0.5000,25,NULL,'[[0, 1, 0], [1, 1, 0], [0, 1, 0]]','{\"Usia\": 0.6243708432720754, \"Lama Rawat Inap\": 0.2795450749158002, \"Jenis Kelamin\": 0.0960840818121245}','models/random_forest_model.pkl','2026-02-07 15:46:59'),
(5,'2026-02-07 22:47:11',0.4167,0.4722,0.4167,0.3917,0.5833,0.7638,-0.1667,25,NULL,'[[0, 3, 0], [2, 4, 0], [0, 2, 1]]','{\"Usia\": 0.6093756453701614, \"Lama Rawat Inap\": 0.31151181120524174, \"Jenis Kelamin\": 0.07911254342459681}','models/random_forest_model.pkl','2026-02-07 15:47:11'),
(6,'2026-02-07 22:58:42',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 15:58:42'),
(7,'2026-02-07 23:01:21',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 16:01:21'),
(8,'2026-02-07 23:28:29',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 16:28:29'),
(9,'2026-02-07 23:33:58',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 16:33:58'),
(10,'2026-02-07 23:55:04',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 16:55:04'),
(11,'2026-02-08 00:10:45',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 17:10:45'),
(12,'2026-02-08 00:15:10',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 17:15:10'),
(13,'2026-02-08 00:19:20',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 17:19:20'),
(14,'2026-02-08 00:23:02',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-07 17:23:02'),
(15,'2026-02-08 14:00:57',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,50,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.6071827962384108, \"Lama Rawat Inap\": 0.29688955056252414, \"Jenis Kelamin\": 0.0959276531990651}','models/random_forest_model.pkl','2026-02-08 07:00:57'),
(16,'2026-02-08 14:01:39',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,100,NULL,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.6338819914640001, \"Lama Rawat Inap\": 0.27955976418594786, \"Jenis Kelamin\": 0.08655824435005208}','models/random_forest_model.pkl','2026-02-08 07:01:39'),
(17,'2026-02-08 14:01:45',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,100,15,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.6338819914640001, \"Lama Rawat Inap\": 0.27955976418594786, \"Jenis Kelamin\": 0.08655824435005208}','models/random_forest_model.pkl','2026-02-08 07:01:45'),
(18,'2026-02-08 14:01:57',0.5000,0.2500,0.5000,0.3333,0.5000,0.7071,0.0000,25,15,'[[0, 2, 0], [0, 4, 0], [0, 2, 0]]','{\"Usia\": 0.5911802896963372, \"Lama Rawat Inap\": 0.3026345076076135, \"Jenis Kelamin\": 0.10618520269604934}','models/random_forest_model.pkl','2026-02-08 07:01:57'),
(19,'2026-02-08 14:13:29',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.1295132026539335, \"Lama Rawat Inap\": 0.09598519775977282, \"Jenis Kelamin\": 0.025712773280500513, \"Jumlah Kasus\": 0.7487888263057931}','models/random_forest_model.pkl','2026-02-08 07:13:29'),
(20,'2026-02-08 14:13:29',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.12126503560182741, \"Lama Rawat Inap\": 0.038306446981233165, \"Jenis Kelamin\": 0.033113720891893274, \"Jumlah Kasus\": 0.8073147965250462}','models/random_forest_model.pkl','2026-02-08 07:13:29'),
(21,'2026-02-08 14:13:29',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.14253747396127064, \"Lama Rawat Inap\": 0.035924525873964656, \"Jenis Kelamin\": 0.04861363248966553, \"Jumlah Kasus\": 0.7729243676750991}','models/random_forest_model.pkl','2026-02-08 07:13:29'),
(22,'2026-02-08 14:13:29',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.16522581624200466, \"Lama Rawat Inap\": 0.048808096764571554, \"Jenis Kelamin\": 0.04956990232796257, \"Jumlah Kasus\": 0.7363961846654612}','models/random_forest_model.pkl','2026-02-08 07:13:29'),
(23,'2026-02-08 14:13:30',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.11812335104329362, \"Lama Rawat Inap\": 0.08081591773854283, \"Jenis Kelamin\": 0.055710624666253344, \"Jumlah Kasus\": 0.7453501065519103}','models/random_forest_model.pkl','2026-02-08 07:13:30'),
(24,'2026-02-08 14:20:03',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.14586981427150833, \"Lama Rawat Inap\": 0.0670118913049584, \"Jenis Kelamin\": 0.03874662102119297, \"Jumlah Kasus\": 0.7483716734023403}','models/random_forest_model.pkl','2026-02-08 07:20:03'),
(25,'2026-02-08 14:20:12',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,10,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.07432274341838462, \"Lama Rawat Inap\": 0.055151791428951734, \"Jenis Kelamin\": 0.03258474201924165, \"Jumlah Kasus\": 0.8379407231334219}','models/random_forest_model.pkl','2026-02-08 07:20:12'),
(26,'2026-02-08 14:20:21',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,50,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12540213013339113, \"Lama Rawat Inap\": 0.042051123933359816, \"Jenis Kelamin\": 0.04118363275094633, \"Jumlah Kasus\": 0.7913631131823027}','models/random_forest_model.pkl','2026-02-08 07:20:21'),
(27,'2026-02-08 14:20:23',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.10626565120808407, \"Lama Rawat Inap\": 0.05421182585813375, \"Jenis Kelamin\": 0.011888854202891088, \"Jumlah Kasus\": 0.8276336687308912}','models/random_forest_model.pkl','2026-02-08 07:20:23'),
(28,'2026-02-08 14:20:25',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.1441831137656698, \"Lama Rawat Inap\": 0.0722304931954522, \"Jenis Kelamin\": 0.0312757828995315, \"Jumlah Kasus\": 0.7523106101393465}','models/random_forest_model.pkl','2026-02-08 07:20:25'),
(29,'2026-02-08 14:20:26',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.15139152985196822, \"Lama Rawat Inap\": 0.06539789563387927, \"Jenis Kelamin\": 0.020057934735995205, \"Jumlah Kasus\": 0.7631526397781573}','models/random_forest_model.pkl','2026-02-08 07:20:26'),
(30,'2026-02-08 14:20:29',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.13026676738343201, \"Lama Rawat Inap\": 0.03968952726094192, \"Jenis Kelamin\": 0.04124762712454053, \"Jumlah Kasus\": 0.7887960782310856}','models/random_forest_model.pkl','2026-02-08 07:20:29'),
(31,'2026-02-08 14:20:31',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.1293748033951231, \"Lama Rawat Inap\": 0.06535926924983611, \"Jenis Kelamin\": 0.04303104636831884, \"Jumlah Kasus\": 0.7622348809867219}','models/random_forest_model.pkl','2026-02-08 07:20:31'),
(32,'2026-02-08 14:20:42',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[3, 0, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.14423807142311473, \"Lama Rawat Inap\": 0.11619301774465166, \"Jenis Kelamin\": 0.015769805371768825, \"Jumlah Kasus\": 0.7237991054604648}','models/random_forest_model.pkl','2026-02-08 07:20:42'),
(33,'2026-02-08 14:20:44',0.9231,0.9327,0.9231,0.9179,0.0769,0.2774,0.8333,50,5,'[[3, 0, 0], [0, 7, 0], [0, 1, 2]]','{\"Usia\": 0.16340319981430035, \"Lama Rawat Inap\": 0.07106295246436091, \"Jenis Kelamin\": 0.04350747380987267, \"Jumlah Kasus\": 0.7220263739114661}','models/random_forest_model.pkl','2026-02-08 07:20:44'),
(34,'2026-02-08 14:20:45',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[3, 0, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.2107488238287032, \"Lama Rawat Inap\": 0.08660182161160312, \"Jenis Kelamin\": 0.06380223746507764, \"Jumlah Kasus\": 0.6388471170946161}','models/random_forest_model.pkl','2026-02-08 07:20:45'),
(35,'2026-02-08 14:20:46',0.8462,0.8803,0.8462,0.8173,0.1538,0.3922,0.6667,50,5,'[[1, 2, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.18647274028733887, \"Lama Rawat Inap\": 0.055031607026378056, \"Jenis Kelamin\": 0.05257120229129376, \"Jumlah Kasus\": 0.7059244503949893}','models/random_forest_model.pkl','2026-02-08 07:20:46'),
(36,'2026-02-08 14:20:47',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[3, 0, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.1662670195782408, \"Lama Rawat Inap\": 0.06268546403377531, \"Jenis Kelamin\": 0.0330719389975996, \"Jumlah Kasus\": 0.7379755773903843}','models/random_forest_model.pkl','2026-02-08 07:20:47'),
(37,'2026-02-08 14:20:48',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[3, 0, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.11412929778556943, \"Lama Rawat Inap\": 0.11969429412003446, \"Jenis Kelamin\": 0.037776344886509744, \"Jumlah Kasus\": 0.7284000632078863}','models/random_forest_model.pkl','2026-02-08 07:20:48'),
(38,'2026-02-08 14:20:49',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[3, 0, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.16405966467392719, \"Lama Rawat Inap\": 0.07436100647343702, \"Jenis Kelamin\": 0.05330885552235493, \"Jumlah Kasus\": 0.7082704733302809}','models/random_forest_model.pkl','2026-02-08 07:20:49'),
(39,'2026-02-08 14:20:50',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[3, 0, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.1505006688141005, \"Lama Rawat Inap\": 0.06252614221814834, \"Jenis Kelamin\": 0.03490619797761296, \"Jumlah Kasus\": 0.7520669909901382}','models/random_forest_model.pkl','2026-02-08 07:20:50'),
(40,'2026-02-08 14:20:51',0.9231,0.9327,0.9231,0.9179,0.0769,0.2774,0.8333,50,5,'[[3, 0, 0], [0, 7, 0], [0, 1, 2]]','{\"Usia\": 0.13868410605226048, \"Lama Rawat Inap\": 0.052831475531718325, \"Jenis Kelamin\": 0.04534138476140976, \"Jumlah Kasus\": 0.7631430336546113}','models/random_forest_model.pkl','2026-02-08 07:20:51'),
(41,'2026-02-08 14:20:57',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[3, 0, 0], [0, 7, 0], [0, 0, 3]]','{\"Usia\": 0.1524310563586562, \"Lama Rawat Inap\": 0.08243815022743137, \"Jenis Kelamin\": 0.0580195556736385, \"Jumlah Kasus\": 0.7071112377402738}','models/random_forest_model.pkl','2026-02-08 07:20:57'),
(42,'2026-02-08 14:20:59',0.9231,0.9327,0.9231,0.9179,0.0769,0.2774,0.8333,50,5,'[[3, 0, 0], [0, 7, 0], [0, 1, 2]]','{\"Usia\": 0.11528616164106559, \"Lama Rawat Inap\": 0.09328578360456896, \"Jenis Kelamin\": 0.019316851275574882, \"Jumlah Kasus\": 0.7721112034787906}','models/random_forest_model.pkl','2026-02-08 07:20:59'),
(43,'2026-02-08 14:21:04',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,50,5,'[[1, 0, 0], [0, 2, 0], [0, 0, 1]]','{\"Usia\": 0.14162551163510553, \"Lama Rawat Inap\": 0.07937133723105777, \"Jenis Kelamin\": 0.037764889294954, \"Jumlah Kasus\": 0.7412382618388828}','models/random_forest_model.pkl','2026-02-08 07:21:04'),
(44,'2026-02-08 14:21:05',0.7500,0.5833,0.7500,0.6500,0.2500,0.5000,0.5000,50,5,'[[1, 0, 0], [0, 2, 0], [0, 1, 0]]','{\"Usia\": 0.12070581337329336, \"Lama Rawat Inap\": 0.05121656165368543, \"Jenis Kelamin\": 0.028074726403313634, \"Jumlah Kasus\": 0.8000028985697075}','models/random_forest_model.pkl','2026-02-08 07:21:05'),
(45,'2026-02-08 14:21:15',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,5,'[[1, 0, 0], [0, 2, 0], [0, 0, 1]]','{\"Usia\": 0.1732901495827238, \"Lama Rawat Inap\": 0.08453968969844533, \"Jenis Kelamin\": 0.054801781311705565, \"Jumlah Kasus\": 0.6873683794071254}','models/random_forest_model.pkl','2026-02-08 07:21:15'),
(46,'2026-02-08 14:21:18',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,5,'[[1, 0, 0], [0, 2, 0], [0, 0, 1]]','{\"Usia\": 0.13448889587255802, \"Lama Rawat Inap\": 0.057747150057640514, \"Jenis Kelamin\": 0.026585679607245536, \"Jumlah Kasus\": 0.7811782744625558}','models/random_forest_model.pkl','2026-02-08 07:21:18'),
(47,'2026-02-08 14:21:19',0.7500,0.5833,0.7500,0.6500,0.2500,0.5000,0.5000,25,5,'[[1, 0, 0], [0, 2, 0], [0, 1, 0]]','{\"Usia\": 0.10472874988662614, \"Lama Rawat Inap\": 0.08652319539485671, \"Jenis Kelamin\": 0.019375032916155284, \"Jumlah Kasus\": 0.7893730218023619}','models/random_forest_model.pkl','2026-02-08 07:21:19'),
(48,'2026-02-08 14:21:20',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,5,'[[1, 0, 0], [0, 2, 0], [0, 0, 1]]','{\"Usia\": 0.13079481378507538, \"Lama Rawat Inap\": 0.032618723039429115, \"Jenis Kelamin\": 0.05337680495585331, \"Jumlah Kasus\": 0.7832096582196423}','models/random_forest_model.pkl','2026-02-08 07:21:20'),
(49,'2026-02-08 14:21:21',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,5,'[[1, 0, 0], [0, 2, 0], [0, 0, 1]]','{\"Usia\": 0.07008138619944891, \"Lama Rawat Inap\": 0.05679697015428159, \"Jenis Kelamin\": 0.014927936220415853, \"Jumlah Kasus\": 0.8581937074258537}','models/random_forest_model.pkl','2026-02-08 07:21:21'),
(50,'2026-02-08 14:21:22',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,5,'[[1, 0, 0], [0, 2, 0], [0, 0, 1]]','{\"Usia\": 0.10568801578619519, \"Lama Rawat Inap\": 0.05608017443664727, \"Jenis Kelamin\": 0.045890557915511256, \"Jumlah Kasus\": 0.7923412518616463}','models/random_forest_model.pkl','2026-02-08 07:21:22'),
(51,'2026-02-08 14:24:23',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:24:23'),
(52,'2026-02-08 14:24:27',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:24:27'),
(53,'2026-02-08 14:24:29',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:24:29'),
(54,'2026-02-08 14:24:30',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:24:30'),
(55,'2026-02-08 14:24:31',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:24:31'),
(56,'2026-02-08 14:24:37',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,30,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.1253583209970295, \"Lama Rawat Inap\": 0.08769940210139444, \"Jenis Kelamin\": 0.022294152606173998, \"Jumlah Kasus\": 0.764648124295402}','models/random_forest_model.pkl','2026-02-08 07:24:37'),
(57,'2026-02-08 14:24:39',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,30,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.1253583209970295, \"Lama Rawat Inap\": 0.08769940210139444, \"Jenis Kelamin\": 0.022294152606173998, \"Jumlah Kasus\": 0.764648124295402}','models/random_forest_model.pkl','2026-02-08 07:24:39'),
(58,'2026-02-08 14:24:40',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,30,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.1253583209970295, \"Lama Rawat Inap\": 0.08769940210139444, \"Jenis Kelamin\": 0.022294152606173998, \"Jumlah Kasus\": 0.764648124295402}','models/random_forest_model.pkl','2026-02-08 07:24:40'),
(59,'2026-02-08 14:24:41',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,30,NULL,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.1253583209970295, \"Lama Rawat Inap\": 0.08769940210139444, \"Jenis Kelamin\": 0.022294152606173998, \"Jumlah Kasus\": 0.764648124295402}','models/random_forest_model.pkl','2026-02-08 07:24:41'),
(60,'2026-02-08 14:24:43',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,30,5,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.12346966258946356, \"Lama Rawat Inap\": 0.0888817349718717, \"Jenis Kelamin\": 0.02555259463767547, \"Jumlah Kasus\": 0.7620960078009893}','models/random_forest_model.pkl','2026-02-08 07:24:43'),
(61,'2026-02-08 14:24:43',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,30,5,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.12346966258946356, \"Lama Rawat Inap\": 0.0888817349718717, \"Jenis Kelamin\": 0.02555259463767547, \"Jumlah Kasus\": 0.7620960078009893}','models/random_forest_model.pkl','2026-02-08 07:24:43'),
(62,'2026-02-08 14:24:50',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,40,5,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.123598833740023, \"Lama Rawat Inap\": 0.07898049722251493, \"Jenis Kelamin\": 0.02491644231978325, \"Jumlah Kasus\": 0.7725042267176788}','models/random_forest_model.pkl','2026-02-08 07:24:50'),
(63,'2026-02-08 14:33:45',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,NULL,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:33:45'),
(64,'2026-02-08 14:33:49',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,3,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.15213831874679298, \"Lama Rawat Inap\": 0.11482663259963725, \"Jenis Kelamin\": 0.02748642789987284, \"Jumlah Kasus\": 0.705548620753697}','models/random_forest_model.pkl','2026-02-08 07:33:49'),
(65,'2026-02-08 14:33:51',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,10,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:33:51'),
(66,'2026-02-08 14:33:54',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,10,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:33:54'),
(67,'2026-02-08 14:33:55',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,10,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:33:55'),
(68,'2026-02-08 14:33:56',0.8750,0.9000,0.8750,0.8611,0.1250,0.3536,0.7500,25,10,'[[2, 0, 0], [0, 4, 0], [0, 1, 1]]','{\"Usia\": 0.12539638259055805, \"Lama Rawat Inap\": 0.09015033050753364, \"Jenis Kelamin\": 0.026752983127408803, \"Jumlah Kasus\": 0.7577003037744996}','models/random_forest_model.pkl','2026-02-08 07:33:56'),
(69,'2026-02-08 14:33:58',1.0000,1.0000,1.0000,1.0000,0.0000,0.0000,1.0000,25,3,'[[2, 0, 0], [0, 4, 0], [0, 0, 2]]','{\"Usia\": 0.15213831874679298, \"Lama Rawat Inap\": 0.11482663259963725, \"Jenis Kelamin\": 0.02748642789987284, \"Jumlah Kasus\": 0.705548620753697}','models/random_forest_model.pkl','2026-02-08 07:33:58'),
(70,'2026-02-08 17:06:04',0.9750,0.9800,0.9750,0.9722,0.0250,0.0707,0.9500,25,NULL,'[[10, 0, 0], [0, 21, 0], [0, 1, 8]]','{\"Usia\": 0.11480266443957779, \"Lama Rawat Inap\": 0.056885722718082656, \"Jenis Kelamin\": 0.014749961420027317, \"Jumlah Kasus\": 0.8135616514223122}','models/random_forest_model.pkl','2026-02-08 10:06:04'),
(71,'2026-02-08 17:06:12',0.9750,0.9800,0.9750,0.9722,0.0250,0.0707,0.9500,25,3,'[[10, 0, 0], [0, 21, 0], [0, 1, 8]]','{\"Usia\": 0.11974714615919195, \"Lama Rawat Inap\": 0.0640242682848864, \"Jenis Kelamin\": 0.018800820086683368, \"Jumlah Kasus\": 0.7974277654692383}','models/random_forest_model.pkl','2026-02-08 10:06:12'),
(72,'2026-02-08 17:06:18',0.9750,0.9800,0.9750,0.9722,0.0250,0.0707,0.9500,25,10,'[[10, 0, 0], [0, 21, 0], [0, 1, 8]]','{\"Usia\": 0.11480266443957779, \"Lama Rawat Inap\": 0.056885722718082656, \"Jenis Kelamin\": 0.014749961420027317, \"Jumlah Kasus\": 0.8135616514223122}','models/random_forest_model.pkl','2026-02-08 10:06:18'),
(73,'2026-02-08 17:06:23',0.9750,0.9800,0.9750,0.9722,0.0250,0.0707,0.9500,25,15,'[[10, 0, 0], [0, 21, 0], [0, 1, 8]]','{\"Usia\": 0.11480266443957779, \"Lama Rawat Inap\": 0.056885722718082656, \"Jenis Kelamin\": 0.014749961420027317, \"Jumlah Kasus\": 0.8135616514223122}','models/random_forest_model.pkl','2026-02-08 10:06:23'),
(74,'2026-02-08 17:06:31',0.9750,0.9800,0.9750,0.9722,0.0250,0.0707,0.9500,30,15,'[[10, 0, 0], [0, 21, 0], [0, 1, 8]]','{\"Usia\": 0.1218998560861414, \"Lama Rawat Inap\": 0.060288781176746575, \"Jenis Kelamin\": 0.013417834307411438, \"Jumlah Kasus\": 0.8043935284297005}','models/random_forest_model.pkl','2026-02-08 10:06:31'),
(75,'2026-07-21 15:04:39',0.2500,0.2042,0.2500,0.2158,0.8500,1.0129,-1.2761,5,NULL,'[[2, 6, 2], [5, 8, 8], [2, 7, 0]]','{\"Usia\": 0.6476156177739673, \"Lama Rawat Inap\": 0.2976023608591754, \"Jenis Kelamin\": 0.054782021366857336}','models/random_forest_model.pkl','2026-07-21 08:04:39'),
(76,'2026-07-21 21:18:18',0.7928,0.7542,0.7928,0.7715,0.2715,0.6227,-0.5364,5,NULL,'[[1, 1, 8], [1, 3, 17], [5, 10, 157]]','{\"Usia\": 0.5948834303931801, \"Lama Rawat Inap\": 0.17365830527065218, \"Jenis Kelamin\": 0.23145826433616773}','models/random_forest_model.pkl','2026-07-21 14:18:18'),
(77,'2026-07-21 21:26:06',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:26:06'),
(78,'2026-07-21 21:27:08',0.8077,0.8102,0.8077,0.8034,0.1923,0.4349,-0.2146,15,NULL,'[[19, 21, 0], [18, 145, 0], [0, 0, 0]]','{\"Usia\": 0.41996419449982353, \"Lama Rawat Inap\": 0.12688503672776363, \"Jenis Kelamin\": 0.4531507687724128}','models/random_forest_model.pkl','2026-07-21 14:27:08'),
(79,'2026-07-21 21:27:20',0.8077,0.8102,0.8077,0.8034,0.1923,0.4349,-0.2146,15,NULL,'[[19, 21, 0], [18, 145, 0], [0, 0, 0]]','{\"Usia\": 0.41996419449982353, \"Lama Rawat Inap\": 0.12688503672776363, \"Jenis Kelamin\": 0.4531507687724128}','models/random_forest_model.pkl','2026-07-21 14:27:20'),
(80,'2026-07-21 21:31:55',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:31:55'),
(81,'2026-07-21 21:32:41',0.8077,0.8102,0.8077,0.8034,0.1923,0.4349,-0.2146,15,NULL,'[[19, 21, 0], [18, 145, 0], [0, 0, 0]]','{\"Usia\": 0.41996419449982353, \"Lama Rawat Inap\": 0.12688503672776363, \"Jenis Kelamin\": 0.4531507687724128}','models/random_forest_model.pkl','2026-07-21 14:32:41'),
(82,'2026-07-21 21:34:25',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:34:25'),
(83,'2026-07-21 21:40:03',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:40:03'),
(84,'2026-07-21 21:40:04',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:40:04'),
(85,'2026-07-21 21:41:34',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:41:34'),
(86,'2026-07-21 21:41:36',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:41:36'),
(87,'2026-07-21 21:47:03',0.8077,0.8102,0.8077,0.8034,0.1923,0.4349,-0.2146,15,NULL,'[[19, 21, 0], [18, 145, 0], [0, 0, 0]]','{\"Usia\": 0.41996419449982353, \"Lama Rawat Inap\": 0.12688503672776363, \"Jenis Kelamin\": 0.4531507687724128}','models/random_forest_model.pkl','2026-07-21 14:47:03'),
(88,'2026-07-21 21:50:20',0.7928,0.7950,0.7928,0.7890,0.2072,0.4494,-0.3081,15,NULL,'[[19, 21, 0], [21, 142, 0], [0, 0, 0]]','{\"Usia\": 0.46307541709827976, \"Lama Rawat Inap\": 0.1391373787804843, \"Jenis Kelamin\": 0.39778720412123586}','models/random_forest_model.pkl','2026-07-21 14:50:20'),
(89,'2026-07-21 21:53:19',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 14:53:20'),
(90,'2026-07-21 22:45:09',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 15:45:09'),
(91,'2026-07-21 22:45:11',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 15:45:11'),
(92,'2026-07-21 22:45:46',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 15:45:46'),
(93,'2026-07-21 22:45:48',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 15:45:48'),
(94,'2026-07-21 22:46:45',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 15:46:45'),
(95,'2026-07-21 22:46:46',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 15:46:46'),
(96,'2026-07-21 23:18:04',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 16:18:04'),
(97,'2026-07-21 23:18:34',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 16:18:34'),
(98,'2026-07-22 00:03:14',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 17:03:14'),
(99,'2026-07-22 00:03:16',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 17:03:16'),
(100,'2026-07-22 06:36:23',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 23:36:23'),
(101,'2026-07-22 06:36:28',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 23:36:28'),
(102,'2026-07-22 06:40:52',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 23:40:52'),
(103,'2026-07-22 06:40:54',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 23:40:54'),
(104,'2026-07-22 06:47:54',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 23:47:54'),
(105,'2026-07-22 06:47:56',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-21 23:47:56'),
(106,'2026-07-22 07:37:14',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 00:37:14'),
(107,'2026-07-22 07:37:16',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 00:37:16'),
(108,'2026-07-22 07:37:30',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 00:37:30'),
(109,'2026-07-22 07:38:16',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 00:38:16'),
(110,'2026-07-22 07:38:18',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 00:38:18'),
(111,'2026-07-22 08:04:24',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 01:04:24'),
(112,'2026-07-22 08:48:35',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 01:48:35'),
(113,'2026-07-22 08:51:23',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 01:51:23'),
(114,'2026-07-22 09:11:49',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 02:11:49'),
(115,'2026-07-22 09:11:52',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 02:11:52'),
(116,'2026-07-22 09:19:38',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 02:19:38'),
(117,'2026-07-22 09:19:41',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 02:19:41'),
(118,'2026-07-22 09:48:22',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 02:48:22'),
(119,'2026-07-22 09:48:24',0.8272,0.8221,0.8272,0.8214,0.1728,0.4121,-0.0903,5,NULL,'[[20, 20, 0], [15, 148, 0], [0, 0, 0]]','{\"Usia\": 0.4274588462566583, \"Lama Rawat Inap\": 0.1254081821297206, \"Jenis Kelamin\": 0.4471329716136211}','models/random_forest_model.pkl','2026-07-22 02:48:24');
/*!40000 ALTER TABLE `model_evaluasi` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `pasien_dbd`
--

DROP TABLE IF EXISTS `pasien_dbd`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `pasien_dbd` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `no_rm` varchar(20) DEFAULT NULL,
  `nama_pasien` varchar(100) NOT NULL,
  `usia` int(11) NOT NULL,
  `jenis_kelamin` enum('L','P') NOT NULL,
  `alamat` text DEFAULT NULL,
  `tanggal_masuk` date NOT NULL,
  `tanggal_keluar` date DEFAULT NULL,
  `lama_rawat` int(11) DEFAULT NULL,
  `bulan` varchar(20) DEFAULT NULL,
  `tahun` int(11) DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `no_rm` (`no_rm`)
) ENGINE=InnoDB AUTO_INCREMENT=414 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasien_dbd`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `pasien_dbd` WRITE;
/*!40000 ALTER TABLE `pasien_dbd` DISABLE KEYS */;
INSERT INTO `pasien_dbd` VALUES
(251,'RM-2024-0001','Neni Sumetria',34,'P','Kab. Agam','2024-01-01',NULL,3,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(252,'RM-2024-0002','Malki Amron',43,'L','Kab. Agam','2024-02-02',NULL,3,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(253,'RM-2024-0003','Arifa Qyaratul',23,'P','Kab. Agam','2024-03-03',NULL,5,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(254,'RM-2024-0004','Rezki Mhd',18,'L','Kab. Agam','2024-04-04',NULL,2,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(255,'RM-2024-0005','Selfiolla',14,'P','Kab. Agam','2024-05-05',NULL,4,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(256,'RM-2024-0006','M.Albiruni',12,'L','Kab. Agam','2024-06-06',NULL,1,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(257,'RM-2024-0007','Yurika Azarine',4,'P','Kab. Agam','2024-07-07',NULL,2,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(258,'RM-2024-0008','Rahmad Ihtiar',16,'L','Kab. Agam','2024-08-08',NULL,6,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(259,'RM-2024-0009','Tiara Endiwa',18,'P','Kab. Agam','2024-09-09',NULL,5,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(260,'RM-2024-0010','Boby',24,'L','Kab. Agam','2024-10-10',NULL,5,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(261,'RM-2024-0011','Defi Putri',23,'P','Kab. Agam','2024-11-11',NULL,3,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(262,'RM-2024-0012','Nini Efriza',47,'P','Kab. Agam','2024-12-12',NULL,2,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(263,'RM-2024-0013','Novi Agus',49,'L','Kab. Agam','2024-01-13',NULL,4,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(264,'RM-2024-0014','Siska Rahmadani',21,'P','Kab. Agam','2024-02-14',NULL,2,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(265,'RM-2024-0015','Kalmani',66,'L','Kab. Agam','2024-03-15',NULL,5,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(266,'RM-2024-0016','Nayra Dhika',2,'P','Kab. Agam','2024-04-16',NULL,3,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(267,'RM-2024-0017','Andri Naldi',49,'L','Kab. Agam','2024-05-17',NULL,4,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(268,'RM-2024-0018','Qhanita Nur',8,'P','Kab. Agam','2024-06-18',NULL,4,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(269,'RM-2024-0019','Shecillia Hanifah',15,'P','Kab. Agam','2024-07-19',NULL,5,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(270,'RM-2024-0020','Haziq Arsyad',10,'L','Kab. Agam','2024-08-20',NULL,5,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(271,'RM-2024-0021','Naira Giska',6,'P','Kab. Agam','2024-09-21',NULL,3,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(272,'RM-2024-0022','Eko Ady',28,'L','Kab. Agam','2024-10-22',NULL,4,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(273,'RM-2024-0023','Suwarni',60,'P','Kab. Agam','2024-11-23',NULL,4,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(274,'RM-2024-0024','Mayang',81,'P','Kab. Agam','2024-12-24',NULL,5,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(275,'RM-2024-0025','Janibar',75,'L','Kab. Agam','2024-01-25',NULL,4,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(276,'RM-2024-0026','Hendra Wadi',37,'L','Kab. Agam','2024-02-26',NULL,4,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(277,'RM-2024-0027','Heru Pratama',22,'L','Kab. Agam','2024-03-27',NULL,2,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(278,'RM-2024-0028','Ade Sepriyanto',19,'L','Kab. Agam','2024-04-28',NULL,2,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(279,'RM-2024-0029','Diendri Barakta',3,'L','Kab. Agam','2024-05-01',NULL,2,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(280,'RM-2024-0030','Suwardi',64,'L','Kab. Agam','2024-06-02',NULL,4,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(281,'RM-2024-0031','Emelya Nora',54,'P','Kab. Agam','2024-07-03',NULL,4,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(282,'RM-2024-0032','Eosel Rizkia',19,'L','Kab. Agam','2024-08-04',NULL,4,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(283,'RM-2024-0033','Warmaneti',55,'P','Kab. Agam','2024-09-05',NULL,3,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(284,'RM-2024-0034','Yandril',40,'L','Kab. Agam','2024-10-06',NULL,3,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(285,'RM-2024-0035','Romy Herina',27,'L','Kab. Agam','2024-11-07',NULL,1,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(286,'RM-2024-0036','Ilham Saputra',28,'L','Kab. Agam','2024-12-08',NULL,4,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(287,'RM-2024-0037','Berli Simanjuntak',52,'L','Kab. Agam','2024-01-09',NULL,3,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(288,'RM-2024-0038','M. Hafiz',12,'L','Kab. Agam','2024-02-10',NULL,5,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(289,'RM-2024-0039','Yusril',65,'L','Kab. Agam','2024-03-11',NULL,3,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(290,'RM-2024-0040','Anggifa Fitria',8,'P','Kab. Agam','2024-04-12',NULL,4,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(291,'RM-2024-0041','Abdul Fikri',21,'L','Kab. Agam','2024-05-13',NULL,5,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(292,'RM-2024-0042','Refa Anggraini',15,'P','Kab. Agam','2024-06-14',NULL,4,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(293,'RM-2024-0043','Dosil Abdul',28,'L','Kab. Agam','2024-07-15',NULL,5,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(294,'RM-2024-0044','Zulkifli',75,'L','Kab. Agam','2024-08-16',NULL,3,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(295,'RM-2024-0045','Nurhayati',62,'P','Kab. Agam','2024-09-17',NULL,2,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(296,'RM-2024-0046','Muhara Mulya',19,'P','Kab. Agam','2024-10-18',NULL,2,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(297,'RM-2024-0047','Basri',50,'L','Kab. Agam','2024-11-19',NULL,5,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(298,'RM-2024-0048','Yuharni',64,'P','Kab. Agam','2024-12-20',NULL,5,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(299,'RM-2024-0049','Tiara Putri',19,'P','Kab. Agam','2024-01-21',NULL,5,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(300,'RM-2024-0050','Afria Puspa',48,'P','Kab. Agam','2024-02-22',NULL,4,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(301,'RM-2024-0051','Zeinal Efendi',59,'L','Kab. Agam','2024-03-23',NULL,4,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(302,'RM-2024-0052','David Eka Putra',35,'L','Kab. Agam','2024-04-24',NULL,4,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(303,'RM-2024-0053','Khaira Umamah',7,'P','Kab. Agam','2024-05-25',NULL,3,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(304,'RM-2024-0054','Yusuf Andrian',7,'L','Kab. Agam','2024-06-26',NULL,4,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(305,'RM-2024-0055','Riva Afrilliana',4,'P','Kab. Agam','2024-07-27',NULL,3,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(306,'RM-2024-0056','Rizal Putra',2,'L','Kab. Agam','2024-08-28',NULL,2,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(307,'RM-2024-0057','Olivia Kirana',17,'P','Kab. Agam','2024-09-01',NULL,3,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(308,'RM-2024-0058','Fitri Novita',28,'P','Kab. Agam','2024-10-02',NULL,4,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(309,'RM-2024-0059','Elianti',68,'P','Kab. Agam','2024-11-03',NULL,4,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(310,'RM-2024-0060','Reza Refninda',29,'L','Kab. Agam','2024-12-04',NULL,3,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(311,'RM-2024-0061','Fauzan',43,'L','Kab. Agam','2024-01-05',NULL,4,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(312,'RM-2024-0062','El Alisa Putri',25,'P','Kab. Agam','2024-02-06',NULL,3,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(313,'RM-2024-0063','Sirat',35,'P','Kab. Agam','2024-03-07',NULL,1,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(314,'RM-2024-0064','Emi',49,'P','Kab. Agam','2024-04-08',NULL,3,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(315,'RM-2024-0065','Rezky',21,'L','Kab. Agam','2024-05-09',NULL,5,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(316,'RM-2024-0066','Mhd Rivaldo',21,'L','Kab. Agam','2024-06-10',NULL,3,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(317,'RM-2024-0067','Sri Suhermi',44,'P','Kab. Agam','2024-07-11',NULL,5,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(318,'RM-2024-0068','Syaifullah',24,'L','Kab. Agam','2024-08-12',NULL,4,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(319,'RM-2024-0069','Riwanto',26,'L','Kab. Agam','2024-09-13',NULL,3,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(320,'RM-2024-0070','Yunizar',84,'P','Kab. Agam','2024-10-14',NULL,3,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(321,'RM-2024-0071','Aqlan Havizh',3,'L','Kab. Agam','2024-11-15',NULL,5,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(322,'RM-2024-0072','Dzacky Claresta',15,'L','Kab. Agam','2024-12-16',NULL,3,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(323,'RM-2024-0073','Arumi Putri',9,'P','Kab. Agam','2024-01-17',NULL,4,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(324,'RM-2024-0074','Ibnu Sadri',2,'L','Kab. Agam','2024-02-18',NULL,2,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(325,'RM-2024-0075','Deliana',70,'P','Kab. Agam','2024-03-19',NULL,2,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(326,'RM-2024-0076','Zakra',16,'L','Kab. Agam','2024-04-20',NULL,4,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(327,'RM-2024-0077','Ulfa Oktavia',6,'P','Kab. Agam','2024-05-21',NULL,3,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(328,'RM-2024-0078','Nafilsa Abdul',29,'P','Kab. Agam','2024-06-22',NULL,3,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(329,'RM-2024-0079','Mulyadi',27,'L','Kab. Agam','2024-07-23',NULL,3,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(330,'RM-2024-0080','Fadli Kurniawan',23,'L','Kab. Agam','2024-08-24',NULL,5,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(331,'RM-2024-0081','Oktavianus',28,'L','Kab. Agam','2024-09-25',NULL,3,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(332,'RM-2024-0082','Nipralaini',50,'P','Kab. Agam','2024-10-26',NULL,3,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(333,'RM-2024-0083','Marzoni',42,'L','Kab. Agam','2024-11-27',NULL,4,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(334,'RM-2024-0084','Putri Maylia',27,'P','Kab. Agam','2024-12-28',NULL,9,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(335,'RM-2024-0085','Muthi Navisa',23,'P','Kab. Agam','2024-01-01',NULL,3,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(336,'RM-2024-0086','Mutia Diva',21,'P','Kab. Agam','2024-02-02',NULL,3,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(337,'RM-2024-0087','Anugrah Illahi',20,'L','Kab. Agam','2024-03-03',NULL,4,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(338,'RM-2024-0088','Mon Sri',32,'P','Kab. Agam','2024-04-04',NULL,4,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(339,'RM-2024-0089','Surya Masalfi',47,'P','Kab. Agam','2024-05-05',NULL,3,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(340,'RM-2024-0090','Aat Kusmayadi',35,'L','Kab. Agam','2024-06-06',NULL,1,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(341,'RM-2024-0091','Fitria Anita',55,'P','Kab. Agam','2024-07-07',NULL,7,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(342,'RM-2024-0092','Rosavita',65,'P','Kab. Agam','2024-08-08',NULL,4,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(343,'RM-2024-0093','Jauza Jahira',12,'P','Kab. Agam','2024-09-09',NULL,4,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(344,'RM-2024-0094','Menzo Khaira',11,'L','Kab. Agam','2024-10-10',NULL,3,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(345,'RM-2024-0095','Zulfa Yenti',56,'P','Kab. Agam','2024-11-11',NULL,4,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(346,'RM-2024-0096','Syahlan Yuanda',16,'L','Kab. Agam','2024-12-12',NULL,2,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(347,'RM-2024-0097','Kenzi Romanja',16,'L','Kab. Agam','2024-01-13',NULL,2,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(348,'RM-2024-0098','Abdurrahman As Saoli',4,'L','Kab. Agam','2024-02-14',NULL,2,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(349,'RM-2024-0099','Aisyah Difani',19,'P','Kab. Agam','2024-03-15',NULL,6,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(350,'RM-2024-0100','Rosli Asamara',42,'P','Kab. Agam','2024-04-16',NULL,5,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(351,'RM-2024-0101','Lisma Erni',41,'P','Kab. Agam','2024-05-17',NULL,4,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(352,'RM-2024-0102','Rahmi',22,'P','Kab. Agam','2024-06-18',NULL,5,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(353,'RM-2024-0103','Eki Hendra',37,'L','Kab. Agam','2024-07-19',NULL,4,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(354,'RM-2024-0104','Yusbardar',61,'L','Kab. Agam','2024-08-20',NULL,3,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(355,'RM-2024-0105','Aris Lucky',23,'L','Kab. Agam','2024-09-21',NULL,3,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(356,'RM-2024-0106','Murniaty',48,'P','Kab. Agam','2024-10-22',NULL,5,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(357,'RM-2024-0107','Agus',69,'L','Kab. Agam','2024-11-23',NULL,7,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(358,'RM-2024-0108','Indra Melvi',40,'L','Kab. Agam','2024-12-24',NULL,3,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(359,'RM-2024-0109','Musliadi',42,'L','Kab. Agam','2024-01-25',NULL,2,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(360,'RM-2024-0110','Ulfa Alifia',25,'P','Kab. Agam','2024-02-26',NULL,4,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(361,'RM-2024-0111','Martias',61,'L','Kab. Agam','2024-03-27',NULL,3,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(362,'RM-2024-0112','Masri',69,'L','Kab. Agam','2024-04-28',NULL,1,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(363,'RM-2024-0113','Dzikra Maulana',14,'L','Kab. Agam','2024-05-01',NULL,2,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(364,'RM-2024-0114','Indra Mastari',52,'L','Kab. Agam','2024-06-02',NULL,3,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(365,'RM-2024-0115','Budi Kargo',32,'L','Kab. Agam','2024-07-03',NULL,4,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(366,'RM-2024-0116','Adril Yusuf',49,'L','Kab. Agam','2024-08-04',NULL,4,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(367,'RM-2024-0117','M. Fatih',67,'L','Kab. Agam','2024-09-05',NULL,4,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(368,'RM-2024-0118','Nila Purnama Sari',30,'P','Kab. Agam','2024-10-06',NULL,7,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(369,'RM-2024-0119','Edo Madani',26,'L','Kab. Agam','2024-11-07',NULL,4,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(370,'RM-2024-0120','Idris',82,'L','Kab. Agam','2024-12-08',NULL,5,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(371,'RM-2024-0121','Randi',28,'L','Kab. Agam','2024-01-09',NULL,3,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(372,'RM-2024-0122','Destia Izani',22,'P','Kab. Agam','2024-02-10',NULL,4,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(373,'RM-2024-0123','M. Raihan',24,'L','Kab. Agam','2024-03-11',NULL,3,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(374,'RM-2024-0124','Widya Anggraini',39,'P','Kab. Agam','2024-04-12',NULL,4,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(375,'RM-2024-0125','Misrita Indra',51,'L','Kab. Agam','2024-05-13',NULL,3,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(376,'RM-2024-0126','Sintia',21,'P','Kab. Agam','2024-06-14',NULL,2,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(377,'RM-2024-0127','Irmalinda',38,'P','Kab. Agam','2024-07-15',NULL,2,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(378,'RM-2024-0128','Andini Putri',4,'P','Kab. Agam','2024-08-16',NULL,3,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(379,'RM-2024-0129','Siti Aisyah',12,'P','Kab. Agam','2024-09-17',NULL,4,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(380,'RM-2024-0130','Naura Salsabila',10,'P','Kab. Agam','2024-10-18',NULL,2,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(381,'RM-2024-0131','Reza Chaniago',10,'L','Kab. Agam','2024-11-19',NULL,3,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(382,'RM-2024-0132','Humaira Denifa',6,'P','Kab. Agam','2024-12-20',NULL,4,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(383,'RM-2024-0133','Azzam',4,'L','Kab. Agam','2024-01-21',NULL,2,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(384,'RM-2024-0134','Adha Lestari',10,'P','Kab. Agam','2024-02-22',NULL,2,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(385,'RM-2024-0135','Nadira Puti',6,'P','Kab. Agam','2024-03-23',NULL,2,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(386,'RM-2024-0136','Reza Andriansyah',3,'L','Kab. Agam','2024-04-24',NULL,1,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(387,'RM-2024-0137','Rafael Sebastian',13,'L','Kab. Agam','2024-05-25',NULL,3,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(388,'RM-2024-0138','Yulia Neri',52,'P','Kab. Agam','2024-06-26',NULL,7,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(389,'RM-2024-0139','Rajab',74,'L','Kab. Agam','2024-07-27',NULL,5,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(390,'RM-2024-0140','Widya Mayang',36,'P','Kab. Agam','2024-08-28',NULL,2,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(391,'RM-2024-0141','Rahmat Fitra',39,'L','Kab. Agam','2024-09-01',NULL,2,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(392,'RM-2024-0142','Alvin Noradilla',20,'L','Kab. Agam','2024-10-02',NULL,4,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(393,'RM-2024-0143','Martias',61,'L','Kab. Agam','2024-11-03',NULL,4,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(394,'RM-2024-0144','Zhaya',28,'L','Kab. Agam','2024-12-04',NULL,4,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(395,'RM-2024-0145','Ahmad Faizin',34,'L','Kab. Agam','2024-01-05',NULL,2,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(396,'RM-2024-0146','Asrizal',66,'L','Kab. Agam','2024-02-06',NULL,10,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(397,'RM-2024-0147','Yunaldi',55,'L','Kab. Agam','2024-03-07',NULL,3,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(398,'RM-2024-0148','Yanti Devina',19,'P','Kab. Agam','2024-04-08',NULL,5,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(399,'RM-2024-0149','Syafrizal',61,'L','Kab. Agam','2024-05-09',NULL,5,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(400,'RM-2024-0150','Weri Oktavia',24,'P','Kab. Agam','2024-06-10',NULL,3,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(401,'RM-2024-0151','Zulkarnain',47,'L','Kab. Agam','2024-07-11',NULL,3,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(402,'RM-2024-0152','Zainal Abidin',73,'L','Kab. Agam','2024-08-12',NULL,7,'Agustus',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(403,'RM-2024-0153','Kendi Cahya',18,'L','Kab. Agam','2024-09-13',NULL,5,'September',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(404,'RM-2024-0154','Budiyono',19,'L','Kab. Agam','2024-10-14',NULL,5,'Oktober',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(405,'RM-2024-0155','Najwa',5,'P','Kab. Agam','2024-11-15',NULL,2,'November',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(406,'RM-2024-0156','Abdul Aziz',15,'L','Kab. Agam','2024-12-16',NULL,4,'Desember',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(407,'RM-2024-0157','Hanifa Puti',5,'P','Kab. Agam','2024-01-17',NULL,2,'Januari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(408,'RM-2024-0158','Celsi Sapira',17,'P','Kab. Agam','2024-02-18',NULL,2,'Februari',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(409,'RM-2024-0159','Anita Puspita',16,'P','Kab. Agam','2024-03-19',NULL,3,'Maret',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(410,'RM-2024-0160','Diffa Cayriful',12,'L','Kab. Agam','2024-04-20',NULL,3,'April',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(411,'RM-2024-0161','Febrianto Angger',22,'L','Kab. Agam','2024-05-21',NULL,3,'Mei',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(412,'RM-2024-0162','Desrizal',34,'L','Kab. Agam','2024-06-22',NULL,4,'Juni',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00'),
(413,'RM-2024-0163','Aprillia Khairunnisa',10,'P','Kab. Agam','2024-07-23',NULL,6,'Juli',2024,'2026-07-22 04:13:00','2026-07-22 04:13:00');
/*!40000 ALTER TABLE `pasien_dbd` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nama_lengkap` varchar(100) NOT NULL,
  `email` varchar(100) DEFAULT NULL,
  `role` enum('admin','petugas') DEFAULT 'petugas',
  `foto` varchar(255) DEFAULT 'default.png',
  `status` enum('aktif','nonaktif') DEFAULT 'aktif',
  `last_login` datetime DEFAULT NULL,
  `created_at` datetime DEFAULT current_timestamp(),
  `updated_at` datetime DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES
(1,'admin','scrypt:32768:8:1$dW2jNJLFDi0i6UfL$6aff2348914b68f4a8d36743bfd852f7e98a34695a41e0651051c440db69d93fbb37db31cd4bea8cd10d00a64fea9ca9f941ecbcf47f5fbf959c1f222f449f99','V2 Modified','mod@test.com','admin','default.png','aktif','2026-07-22 10:07:48','2026-01-29 01:23:33','2026-07-22 04:14:14'),
(2,'petugas','scrypt:32768:8:1$MoAKZkKxMSYIu5qx$dcdeabaec18385a91044114ea168f07368742ef20ac72b718395b8be66b7edc1f642b74022b7617eef8be5dbf81fdc4c145a8a8d50484c9b0e6a7937f36a3e1c','Petugas Kesehatan','petugas@rsud.go.id','petugas','default.png','aktif','2026-07-21 23:12:32','2026-02-05 10:56:16','2026-07-22 04:14:14');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
COMMIT;
SET AUTOCOMMIT=@OLD_AUTOCOMMIT;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*M!100616 SET NOTE_VERBOSITY=@OLD_NOTE_VERBOSITY */;

-- Dump completed on 2026-07-22 11:14:21

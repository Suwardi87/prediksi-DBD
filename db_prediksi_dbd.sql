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
) ENGINE=InnoDB AUTO_INCREMENT=92 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `hasil_prediksi`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `hasil_prediksi` WRITE;
/*!40000 ALTER TABLE `hasil_prediksi` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=133 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `kasus_bulanan`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `kasus_bulanan` WRITE;
/*!40000 ALTER TABLE `kasus_bulanan` DISABLE KEYS */;
INSERT INTO `kasus_bulanan` VALUES
(121,'Januari',2024,12,0,0,'Sedang','2026-07-22 15:03:23'),
(122,'Februari',2024,7,0,0,'Rendah','2026-07-22 15:03:23'),
(123,'Maret',2024,14,0,0,'Sedang','2026-07-22 15:03:23'),
(124,'April',2024,4,0,0,'Rendah','2026-07-22 15:03:23'),
(125,'Mei',2024,13,0,0,'Sedang','2026-07-22 15:03:23'),
(126,'Juni',2024,15,0,0,'Sedang','2026-07-22 15:03:23'),
(127,'Juli',2024,10,0,0,'Sedang','2026-07-22 15:03:23'),
(128,'Agustus',2024,13,0,0,'Sedang','2026-07-22 15:03:23'),
(129,'September',2024,18,0,0,'Tinggi','2026-07-22 15:03:23'),
(130,'Oktober',2024,33,0,0,'Tinggi','2026-07-22 15:03:23'),
(131,'November',2024,21,0,0,'Tinggi','2026-07-22 15:03:23'),
(132,'Desember',2024,3,0,0,'Rendah','2026-07-22 15:03:23');
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
) ENGINE=InnoDB AUTO_INCREMENT=128 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log_aktivitas`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `log_aktivitas` WRITE;
/*!40000 ALTER TABLE `log_aktivitas` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=152 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `model_evaluasi`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `model_evaluasi` WRITE;
/*!40000 ALTER TABLE `model_evaluasi` DISABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=903 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pasien_dbd`
--

SET @OLD_AUTOCOMMIT=@@AUTOCOMMIT, @@AUTOCOMMIT=0;
LOCK TABLES `pasien_dbd` WRITE;
/*!40000 ALTER TABLE `pasien_dbd` DISABLE KEYS */;
INSERT INTO `pasien_dbd` VALUES
(740,'RM-2024-0001','Febrianto Angger',22,'L','Kab. Agam','2024-12-02',NULL,3,'Desember',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(741,'RM-2024-0002','Desrizal',34,'L','Kab. Agam','2024-12-04',NULL,4,'Desember',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(742,'RM-2024-0003','Aprillia Khairunnisa',10,'P','Kab. Agam','2024-12-06',NULL,6,'Desember',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(743,'RM-2024-0004','Yandril',40,'L','Kab. Agam','2024-04-02',NULL,3,'April',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(744,'RM-2024-0005','Romy Herina',27,'L','Kab. Agam','2024-04-04',NULL,1,'April',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(745,'RM-2024-0006','Ilham Saputra',28,'L','Kab. Agam','2024-04-06',NULL,4,'April',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(746,'RM-2024-0007','Berli Simanjuntak',52,'L','Kab. Agam','2024-04-08',NULL,3,'April',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(747,'RM-2024-0008','Novi Agus',49,'L','Kab. Agam','2024-02-02',NULL,4,'Februari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(748,'RM-2024-0009','Siska Rahmadani',21,'P','Kab. Agam','2024-02-04',NULL,2,'Februari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(749,'RM-2024-0010','Kalmani',66,'L','Kab. Agam','2024-02-06',NULL,5,'Februari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(750,'RM-2024-0011','Nayra Dhika',2,'P','Kab. Agam','2024-02-08',NULL,3,'Februari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(751,'RM-2024-0012','Andri Naldi',49,'L','Kab. Agam','2024-02-10',NULL,4,'Februari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(752,'RM-2024-0013','Qhanita Nur',8,'P','Kab. Agam','2024-02-12',NULL,4,'Februari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(753,'RM-2024-0014','Shecillia Hanifah',15,'P','Kab. Agam','2024-02-14',NULL,5,'Februari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(754,'RM-2024-0015','Mhd Rivaldo',21,'L','Kab. Agam','2024-07-02',NULL,3,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(755,'RM-2024-0016','Sri Suhermi',44,'P','Kab. Agam','2024-07-04',NULL,5,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(756,'RM-2024-0017','Syaifullah',24,'L','Kab. Agam','2024-07-06',NULL,4,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(757,'RM-2024-0018','Riwanto',26,'L','Kab. Agam','2024-07-08',NULL,3,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(758,'RM-2024-0019','Yunizar',84,'P','Kab. Agam','2024-07-10',NULL,3,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(759,'RM-2024-0020','Aqlan Havizh',3,'L','Kab. Agam','2024-07-12',NULL,5,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(760,'RM-2024-0021','Dzacky Claresta',15,'L','Kab. Agam','2024-07-14',NULL,3,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(761,'RM-2024-0022','Arumi Putri',9,'P','Kab. Agam','2024-07-16',NULL,4,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(762,'RM-2024-0023','Ibnu Sadri',2,'L','Kab. Agam','2024-07-18',NULL,2,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(763,'RM-2024-0024','Deliana',70,'P','Kab. Agam','2024-07-20',NULL,2,'Juli',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(764,'RM-2024-0025','Neni Sumetria',34,'P','Kab. Agam','2024-01-02',NULL,3,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(765,'RM-2024-0026','Malki Amron',43,'L','Kab. Agam','2024-01-04',NULL,3,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(766,'RM-2024-0027','Arifa Qyaratul',23,'P','Kab. Agam','2024-01-06',NULL,5,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(767,'RM-2024-0028','Rezki Mhd',18,'L','Kab. Agam','2024-01-08',NULL,2,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(768,'RM-2024-0029','Selfiolla',14,'P','Kab. Agam','2024-01-10',NULL,4,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(769,'RM-2024-0030','M.Albiruni',12,'L','Kab. Agam','2024-01-12',NULL,1,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(770,'RM-2024-0031','Yurika Azarine',4,'P','Kab. Agam','2024-01-14',NULL,2,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(771,'RM-2024-0032','Rahmad Ihtiar',16,'L','Kab. Agam','2024-01-16',NULL,6,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(772,'RM-2024-0033','Tiara Endiwa',18,'P','Kab. Agam','2024-01-18',NULL,5,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(773,'RM-2024-0034','Boby',24,'L','Kab. Agam','2024-01-20',NULL,5,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(774,'RM-2024-0035','Defi Putri',23,'P','Kab. Agam','2024-01-22',NULL,3,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(775,'RM-2024-0036','Nini Efriza',47,'P','Kab. Agam','2024-01-24',NULL,2,'Januari',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(776,'RM-2024-0037','M. Hafiz',12,'L','Kab. Agam','2024-05-02',NULL,5,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(777,'RM-2024-0038','Yusril',65,'L','Kab. Agam','2024-05-04',NULL,3,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(778,'RM-2024-0039','Anggifa Fitria',8,'P','Kab. Agam','2024-05-06',NULL,4,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(779,'RM-2024-0040','Abdul Fikri',21,'L','Kab. Agam','2024-05-08',NULL,5,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(780,'RM-2024-0041','Refa Anggraini',15,'P','Kab. Agam','2024-05-10',NULL,4,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(781,'RM-2024-0042','Dosil Abdul',28,'L','Kab. Agam','2024-05-12',NULL,5,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(782,'RM-2024-0043','Zulkifli',75,'L','Kab. Agam','2024-05-14',NULL,3,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(783,'RM-2024-0044','Nurhayati',62,'P','Kab. Agam','2024-05-16',NULL,2,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(784,'RM-2024-0045','Muhara Mulya',19,'P','Kab. Agam','2024-05-18',NULL,2,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(785,'RM-2024-0046','Basri',50,'L','Kab. Agam','2024-05-20',NULL,5,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(786,'RM-2024-0047','Yuharni',64,'P','Kab. Agam','2024-05-22',NULL,5,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(787,'RM-2024-0048','Tiara Putri',19,'P','Kab. Agam','2024-05-24',NULL,5,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(788,'RM-2024-0049','Afria Puspa',48,'P','Kab. Agam','2024-05-26',NULL,4,'Mei',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(789,'RM-2024-0050','Zakra',16,'L','Kab. Agam','2024-08-02',NULL,4,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(790,'RM-2024-0051','Ulfa Oktavia',6,'P','Kab. Agam','2024-08-04',NULL,3,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(791,'RM-2024-0052','Nafilsa Abdul',29,'P','Kab. Agam','2024-08-06',NULL,3,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(792,'RM-2024-0053','Mulyadi',27,'L','Kab. Agam','2024-08-08',NULL,3,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(793,'RM-2024-0054','Fadli Kurniawan',23,'L','Kab. Agam','2024-08-10',NULL,5,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(794,'RM-2024-0055','Oktavianus',28,'L','Kab. Agam','2024-08-12',NULL,3,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(795,'RM-2024-0056','Nipralaini',50,'P','Kab. Agam','2024-08-14',NULL,3,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(796,'RM-2024-0057','Marzoni',42,'L','Kab. Agam','2024-08-16',NULL,4,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(797,'RM-2024-0058','Putri Maylia',27,'P','Kab. Agam','2024-08-18',NULL,9,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(798,'RM-2024-0059','Muthi Navisa',23,'P','Kab. Agam','2024-08-20',NULL,3,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(799,'RM-2024-0060','Mutia Diva',21,'P','Kab. Agam','2024-08-22',NULL,3,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(800,'RM-2024-0061','Anugrah Illahi',20,'L','Kab. Agam','2024-08-24',NULL,4,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(801,'RM-2024-0062','Mon Sri',32,'P','Kab. Agam','2024-08-26',NULL,4,'Agustus',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(802,'RM-2024-0063','Haziq Arsyad',10,'L','Kab. Agam','2024-03-02',NULL,5,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(803,'RM-2024-0064','Naira Giska',6,'P','Kab. Agam','2024-03-04',NULL,3,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(804,'RM-2024-0065','Eko Ady',28,'L','Kab. Agam','2024-03-06',NULL,4,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(805,'RM-2024-0066','Suwarni',60,'P','Kab. Agam','2024-03-08',NULL,4,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(806,'RM-2024-0067','Mayang',81,'P','Kab. Agam','2024-03-10',NULL,5,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(807,'RM-2024-0068','Janibar',75,'L','Kab. Agam','2024-03-12',NULL,4,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(808,'RM-2024-0069','Hendra Wadi',37,'L','Kab. Agam','2024-03-14',NULL,4,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(809,'RM-2024-0070','Heru Pratama',22,'L','Kab. Agam','2024-03-16',NULL,2,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(810,'RM-2024-0071','Ade Sepriyanto',19,'L','Kab. Agam','2024-03-18',NULL,2,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(811,'RM-2024-0072','Diendri Barakta',3,'L','Kab. Agam','2024-03-20',NULL,2,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(812,'RM-2024-0073','Suwardi',64,'L','Kab. Agam','2024-03-22',NULL,4,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(813,'RM-2024-0074','Emelya Nora',54,'P','Kab. Agam','2024-03-24',NULL,4,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(814,'RM-2024-0075','Eosel Rizkia',19,'L','Kab. Agam','2024-03-26',NULL,4,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(815,'RM-2024-0076','Warmaneti',55,'P','Kab. Agam','2024-03-28',NULL,3,'Maret',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(816,'RM-2024-0077','Zeinal Efendi',59,'L','Kab. Agam','2024-06-02',NULL,4,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(817,'RM-2024-0078','David Eka Putra',35,'L','Kab. Agam','2024-06-04',NULL,4,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(818,'RM-2024-0079','Khaira Umamah',7,'P','Kab. Agam','2024-06-06',NULL,3,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(819,'RM-2024-0080','Yusuf Andrian',7,'L','Kab. Agam','2024-06-08',NULL,4,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(820,'RM-2024-0081','Riva Afrilliana',4,'P','Kab. Agam','2024-06-10',NULL,3,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(821,'RM-2024-0082','Rizal Putra',2,'L','Kab. Agam','2024-06-12',NULL,2,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(822,'RM-2024-0083','Olivia Kirana',17,'P','Kab. Agam','2024-06-14',NULL,3,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(823,'RM-2024-0084','Fitri Novita',28,'P','Kab. Agam','2024-06-16',NULL,4,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(824,'RM-2024-0085','Elianti',68,'P','Kab. Agam','2024-06-18',NULL,4,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(825,'RM-2024-0086','Reza Refninda',29,'L','Kab. Agam','2024-06-20',NULL,3,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(826,'RM-2024-0087','Fauzan',43,'L','Kab. Agam','2024-06-22',NULL,4,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(827,'RM-2024-0088','El Alisa Putri',25,'P','Kab. Agam','2024-06-24',NULL,3,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(828,'RM-2024-0089','Sirat',35,'P','Kab. Agam','2024-06-26',NULL,1,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(829,'RM-2024-0090','Emi',49,'P','Kab. Agam','2024-06-28',NULL,3,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(830,'RM-2024-0091','Rezky',21,'L','Kab. Agam','2024-06-28',NULL,5,'Juni',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(831,'RM-2024-0092','Surya Masalfi',47,'P','Kab. Agam','2024-09-02',NULL,3,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(832,'RM-2024-0093','Aat Kusmayadi',35,'L','Kab. Agam','2024-09-04',NULL,1,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(833,'RM-2024-0094','Fitria Anita',55,'P','Kab. Agam','2024-09-06',NULL,7,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(834,'RM-2024-0095','Rosavita',65,'P','Kab. Agam','2024-09-08',NULL,4,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(835,'RM-2024-0096','Jauza Jahira',12,'P','Kab. Agam','2024-09-10',NULL,4,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(836,'RM-2024-0097','Menzo Khaira',11,'L','Kab. Agam','2024-09-12',NULL,3,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(837,'RM-2024-0098','Zulfa Yenti',56,'P','Kab. Agam','2024-09-14',NULL,4,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(838,'RM-2024-0099','Syahlan Yuanda',16,'L','Kab. Agam','2024-09-16',NULL,2,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(839,'RM-2024-0100','Kenzi Romanja',16,'L','Kab. Agam','2024-09-18',NULL,2,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(840,'RM-2024-0101','Abdurrahman As Saoli',4,'L','Kab. Agam','2024-09-20',NULL,2,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(841,'RM-2024-0102','Aisyah Difani',19,'P','Kab. Agam','2024-09-22',NULL,6,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(842,'RM-2024-0103','Rosli Asamara',42,'P','Kab. Agam','2024-09-24',NULL,5,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(843,'RM-2024-0104','Lisma Erni',41,'P','Kab. Agam','2024-09-26',NULL,4,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(844,'RM-2024-0105','Rahmi',22,'P','Kab. Agam','2024-09-28',NULL,5,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(845,'RM-2024-0106','Eki Hendra',37,'L','Kab. Agam','2024-09-28',NULL,4,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(846,'RM-2024-0107','Yusbardar',61,'L','Kab. Agam','2024-09-28',NULL,3,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(847,'RM-2024-0108','Aris Lucky',23,'L','Kab. Agam','2024-09-28',NULL,3,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(848,'RM-2024-0109','Murniaty',48,'P','Kab. Agam','2024-09-28',NULL,5,'September',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(849,'RM-2024-0110','Yulia Neri',52,'P','Kab. Agam','2024-11-02',NULL,7,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(850,'RM-2024-0111','Rajab',74,'L','Kab. Agam','2024-11-04',NULL,5,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(851,'RM-2024-0112','Widya Mayang',36,'P','Kab. Agam','2024-11-06',NULL,2,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(852,'RM-2024-0113','Rahmat Fitra',39,'L','Kab. Agam','2024-11-08',NULL,2,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(853,'RM-2024-0114','Alvin Noradilla',20,'L','Kab. Agam','2024-11-10',NULL,4,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(854,'RM-2024-0115','Martias',61,'L','Kab. Agam','2024-11-12',NULL,4,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(855,'RM-2024-0116','Zhaya',28,'L','Kab. Agam','2024-11-14',NULL,4,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(856,'RM-2024-0117','Ahmad Faizin',34,'L','Kab. Agam','2024-11-16',NULL,2,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(857,'RM-2024-0118','Asrizal',66,'L','Kab. Agam','2024-11-18',NULL,10,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(858,'RM-2024-0119','Yunaldi',55,'L','Kab. Agam','2024-11-20',NULL,3,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(859,'RM-2024-0120','Yanti Devina',19,'P','Kab. Agam','2024-11-22',NULL,5,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(860,'RM-2024-0121','Syafrizal',61,'L','Kab. Agam','2024-11-24',NULL,5,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(861,'RM-2024-0122','Weri Oktavia',24,'P','Kab. Agam','2024-11-26',NULL,3,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(862,'RM-2024-0123','Zulkarnain',47,'L','Kab. Agam','2024-11-28',NULL,3,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(863,'RM-2024-0124','Zainal Abidin',73,'L','Kab. Agam','2024-11-28',NULL,7,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(864,'RM-2024-0125','Kendi Cahya',18,'L','Kab. Agam','2024-11-28',NULL,5,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(865,'RM-2024-0126','Budiyono',19,'L','Kab. Agam','2024-11-28',NULL,5,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(866,'RM-2024-0127','Najwa',5,'P','Kab. Agam','2024-11-28',NULL,2,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(867,'RM-2024-0128','Abdul Aziz',15,'L','Kab. Agam','2024-11-28',NULL,4,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(868,'RM-2024-0129','Hanifa Puti',5,'P','Kab. Agam','2024-11-28',NULL,2,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(869,'RM-2024-0130','Celsi Sapira',17,'P','Kab. Agam','2024-11-28',NULL,2,'November',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(870,'RM-2024-0131','Agus',69,'L','Kab. Agam','2024-10-02',NULL,7,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(871,'RM-2024-0132','Indra Melvi',40,'L','Kab. Agam','2024-10-04',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(872,'RM-2024-0133','Musliadi',42,'L','Kab. Agam','2024-10-06',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(873,'RM-2024-0134','Ulfa Alifia',25,'P','Kab. Agam','2024-10-08',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(874,'RM-2024-0135','Martias',61,'L','Kab. Agam','2024-10-10',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(875,'RM-2024-0136','Masri',69,'L','Kab. Agam','2024-10-12',NULL,1,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(876,'RM-2024-0137','Dzikra Maulana',14,'L','Kab. Agam','2024-10-14',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(877,'RM-2024-0138','Indra Mastari',52,'L','Kab. Agam','2024-10-16',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(878,'RM-2024-0139','Budi Kargo',32,'L','Kab. Agam','2024-10-18',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(879,'RM-2024-0140','Adril Yusuf',49,'L','Kab. Agam','2024-10-20',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(880,'RM-2024-0141','M. Fatih',67,'L','Kab. Agam','2024-10-22',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(881,'RM-2024-0142','Nila Purnama Sari',30,'P','Kab. Agam','2024-10-24',NULL,7,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(882,'RM-2024-0143','Edo Madani',26,'L','Kab. Agam','2024-10-26',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(883,'RM-2024-0144','Idris',82,'L','Kab. Agam','2024-10-28',NULL,5,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(884,'RM-2024-0145','Randi',28,'L','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(885,'RM-2024-0146','Destia Izani',22,'P','Kab. Agam','2024-10-28',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(886,'RM-2024-0147','M. Raihan',24,'L','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(887,'RM-2024-0148','Widya Anggraini',39,'P','Kab. Agam','2024-10-28',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(888,'RM-2024-0149','Misrita Indra',51,'L','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(889,'RM-2024-0150','Sintia',21,'P','Kab. Agam','2024-10-28',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(890,'RM-2024-0151','Irmalinda',38,'P','Kab. Agam','2024-10-28',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(891,'RM-2024-0152','Andini Putri',4,'P','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(892,'RM-2024-0153','Siti Aisyah',12,'P','Kab. Agam','2024-10-28',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(893,'RM-2024-0154','Naura Salsabila',10,'P','Kab. Agam','2024-10-28',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(894,'RM-2024-0155','Reza Chaniago',10,'L','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(895,'RM-2024-0156','Humaira Denifa',6,'P','Kab. Agam','2024-10-28',NULL,4,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(896,'RM-2024-0157','Azzam',4,'L','Kab. Agam','2024-10-28',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(897,'RM-2024-0158','Adha Lestari',10,'P','Kab. Agam','2024-10-28',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(898,'RM-2024-0159','Nadira Puti',6,'P','Kab. Agam','2024-10-28',NULL,2,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(899,'RM-2024-0160','Reza Andriansyah',3,'L','Kab. Agam','2024-10-28',NULL,1,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(900,'RM-2024-0161','Rafael Sebastian',13,'L','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(901,'RM-2024-0162','Anita Puspita',16,'P','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23'),
(902,'RM-2024-0163','Diffa Cayriful',12,'L','Kab. Agam','2024-10-28',NULL,3,'Oktober',2024,'2026-07-22 15:03:23','2026-07-22 15:03:23');
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
(1,'admin','scrypt:32768:8:1$dW2jNJLFDi0i6UfL$6aff2348914b68f4a8d36743bfd852f7e98a34695a41e0651051c440db69d93fbb37db31cd4bea8cd10d00a64fea9ca9f941ecbcf47f5fbf959c1f222f449f99','V2 Modified','mod@test.com','admin','default.png','aktif','2026-07-22 22:04:25','2026-01-29 01:23:33','2026-07-22 15:04:25'),
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

-- Dump completed on 2026-07-22 22:17:33

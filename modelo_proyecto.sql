-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: localhost    Database: modelo_proyecto
-- ------------------------------------------------------
-- Server version	8.0.41

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
-- Table structure for table `compra`
--

DROP TABLE IF EXISTS `compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Proveedor_id` int NOT NULL,
  `fecha` datetime DEFAULT NULL,
  `Empleado_id` int NOT NULL,
  `total_compra` float DEFAULT NULL,
  `estado` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_Compra_Proveedor_idx` (`Proveedor_id`),
  KEY `fk_Compra_Empleado1_idx` (`Empleado_id`),
  CONSTRAINT `fk_Compra_Empleado1` FOREIGN KEY (`Empleado_id`) REFERENCES `empleado` (`id`),
  CONSTRAINT `fk_Compra_Proveedor` FOREIGN KEY (`Proveedor_id`) REFERENCES `proveedor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `compra`
--

LOCK TABLES `compra` WRITE;
/*!40000 ALTER TABLE `compra` DISABLE KEYS */;
INSERT INTO `compra` VALUES (1,1,'2025-05-17 14:51:52',2,1402,1),(2,1,'2025-05-17 15:10:30',2,978,1),(3,1,'2025-05-17 15:13:48',2,85,1),(4,2,'2025-05-17 15:32:36',2,1487,1),(5,1,'2025-05-17 15:56:36',2,17,1),(6,2,'2025-05-17 15:58:08',2,2316,1),(10,2,'2025-05-17 23:48:29',2,234,1),(11,1,'2025-05-18 00:09:46',2,1086,1),(12,2,'2025-05-18 12:31:15',2,906,1),(13,1,'2025-05-19 21:57:47',2,1419,0),(14,2,'2025-05-19 22:01:01',2,1130,0),(15,2,'2025-05-19 22:42:59',2,1480,1),(16,1,'2025-05-20 08:29:59',2,646,1);
/*!40000 ALTER TABLE `compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_compra`
--

DROP TABLE IF EXISTS `detalle_compra`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_compra` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Producto_id` int NOT NULL,
  `Compra_id` int NOT NULL,
  `cantidad` int NOT NULL,
  `precio_unitario` float NOT NULL,
  `cantidad_recibida` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Producto_has_Compra_Compra1_idx` (`Compra_id`),
  KEY `fk_Producto_has_Compra_Producto1_idx` (`Producto_id`),
  CONSTRAINT `fk_Producto_has_Compra_Compra1` FOREIGN KEY (`Compra_id`) REFERENCES `compra` (`id`),
  CONSTRAINT `fk_Producto_has_Compra_Producto1` FOREIGN KEY (`Producto_id`) REFERENCES `producto` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_compra`
--

LOCK TABLES `detalle_compra` WRITE;
/*!40000 ALTER TABLE `detalle_compra` DISABLE KEYS */;
INSERT INTO `detalle_compra` VALUES (1,7,1,3,1.06,3),(2,8,1,4,12.75,2),(3,12,1,2,127.5,2),(4,13,1,5,212.5,5),(5,11,1,3,10.2,3),(6,6,2,2,63.75,2),(7,14,2,5,170,5),(8,10,3,10,8.5,10),(9,14,4,5,170,4),(10,11,4,6,10.2,6),(11,8,4,3,12.75,3),(12,10,4,8,8.5,2),(13,7,4,2,1.06,2),(14,6,4,10,63.75,10),(15,15,5,4,4.25,4),(16,12,6,10,127.5,10),(17,14,6,6,170,6),(18,15,6,5,4.25,3),(19,16,10,100,2.34,75),(20,6,11,3,63.75,3),(21,7,11,2,1.06,2),(22,12,11,7,127.5,7),(23,14,12,5,170,5),(24,16,12,13,2.34,13),(25,8,12,2,12.75,1),(26,8,13,5,3,5),(27,11,13,2,10.2,2),(28,14,13,10,8,10),(29,10,14,5,3,5),(30,13,14,2,212.5,2),(31,14,14,3,4,3),(32,14,15,2,170,1),(33,12,15,10,127.5,10),(34,16,15,15,2.34,15),(35,13,16,5,212.5,3),(36,15,16,3,4.25,2);
/*!40000 ALTER TABLE `detalle_compra` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `detalle_venta`
--

DROP TABLE IF EXISTS `detalle_venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `detalle_venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Producto_id` int NOT NULL,
  `Venta_id` int NOT NULL,
  `cantidad` int DEFAULT NULL,
  `precio` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Producto_has_Venta_Venta1_idx` (`Venta_id`),
  KEY `fk_Producto_has_Venta_Producto1_idx` (`Producto_id`),
  CONSTRAINT `fk_Producto_has_Venta_Producto1` FOREIGN KEY (`Producto_id`) REFERENCES `producto` (`id`),
  CONSTRAINT `fk_Producto_has_Venta_Venta1` FOREIGN KEY (`Venta_id`) REFERENCES `venta` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=22 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `detalle_venta`
--

LOCK TABLES `detalle_venta` WRITE;
/*!40000 ALTER TABLE `detalle_venta` DISABLE KEYS */;
INSERT INTO `detalle_venta` VALUES (1,13,2,4,250),(2,6,2,7,75),(3,11,3,3,12),(4,12,3,4,150),(5,11,8,5,12),(6,13,8,2,250),(7,10,8,4,10),(8,11,9,5,12),(9,13,9,4,250),(10,6,9,2,75),(11,11,10,3,12),(12,14,10,2,200),(13,6,10,5,75),(14,8,11,2,15),(15,14,11,4,200),(16,16,11,3,3),(17,6,11,6,75),(18,12,12,8,150),(19,15,12,2,5),(20,12,12,5,150),(21,7,12,15,1);
/*!40000 ALTER TABLE `detalle_venta` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `empleado`
--

DROP TABLE IF EXISTS `empleado`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `empleado` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `tipo` varchar(45) DEFAULT NULL,
  `contrasennia` varchar(128) DEFAULT NULL,
  `telefono` varchar(11) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `empleado`
--

LOCK TABLES `empleado` WRITE;
/*!40000 ALTER TABLE `empleado` DISABLE KEYS */;
INSERT INTO `empleado` VALUES (1,'Pedro','pedro@gmail.com','Vendedor','$2b$12$z6cFdZYqW17ApRwEqN7sp.xDVFBrkDJvw4ic5b5C495gip702qD0e','45256325',1),(2,'Juan','juan@gmail.com','Administrador','$2b$12$M8aXQmiywfEMFjsbNOqvmucfA9MLtwjmmOR2emxZ46jfRP3ZK5vUG','54799632',1),(3,'Paco','paco@gmail.com','Administrador','$2b$12$CHhKgG7T4UgaGJdSAHJgEe3Uuj6jtP5X32kHa2m.HTHtR82lu9qwa','45885632',1),(4,'memo','memoG@gmail.com','Vendedor','$2b$12$zxJfz5fsYDsu6mmgpmWbGO8afXKOCcXRdBZ/jMcWsfC8ucanhTihO','4845165451',1);
/*!40000 ALTER TABLE `empleado` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto`
--

DROP TABLE IF EXISTS `producto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) NOT NULL,
  `precio` float DEFAULT NULL,
  `stock` int DEFAULT '0',
  `descripcion` varchar(45) DEFAULT NULL,
  `costo` float DEFAULT NULL,
  `stock_minimo` int DEFAULT '0',
  `estado` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto`
--

LOCK TABLES `producto` WRITE;
/*!40000 ALTER TABLE `producto` DISABLE KEYS */;
INSERT INTO `producto` VALUES (6,'Resma de hojas',80,20,'Resma de 500 hojas',63.75,10,1),(7,'Lápiz 3B',1.25,17,'Lápiz mongol',5,5,1),(8,'Pegamento prueba',15,29,'Pegamento 2',12.75,6,1),(10,'Vaso de agua',10,20,'Descripción',81.6,13,1),(11,'Tijera',12,17,'Tijeras marca ###',10.2,5,1),(12,'Calculadora',150,35,'Calculadora casio fx-###',127.5,5,1),(13,'Calculadora FX-991',250,23,'Calculadora con 200 funciones',212.5,5,1),(14,'Audifonos',200,16,'Audífonos skullcandy',170,5,1),(15,'Borrador',5,4,'Borrador marca maped ',4.25,2,1),(16,'Cartulina',2.75,100,'Pliego de papel bond blanco',2.3375,5,1);
/*!40000 ALTER TABLE `producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `proveedor`
--

DROP TABLE IF EXISTS `proveedor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `proveedor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(45) DEFAULT NULL,
  `direccion` varchar(45) DEFAULT NULL,
  `email` varchar(45) DEFAULT NULL,
  `telefono` varchar(12) DEFAULT NULL,
  `estado` tinyint(1) DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `proveedor`
--

LOCK TABLES `proveedor` WRITE;
/*!40000 ALTER TABLE `proveedor` DISABLE KEYS */;
INSERT INTO `proveedor` VALUES (1,'Jorge','Quetzaltenango','jorge@gmail.com','43432212',1),(2,'Miguel','Xela','migue@gmail.com','56622141',1);
/*!40000 ALTER TABLE `proveedor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `telefono`
--

DROP TABLE IF EXISTS `telefono`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `telefono` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `telefono` varchar(8) DEFAULT NULL,
  `Proveedor_id` int DEFAULT NULL,
  `Empleado_id` int DEFAULT NULL,
  PRIMARY KEY (`ID`),
  KEY `fk_Telefono_Proveedor1_idx` (`Proveedor_id`),
  KEY `fk_Telefono_Empleado1_idx` (`Empleado_id`),
  CONSTRAINT `fk_Telefono_Empleado1` FOREIGN KEY (`Empleado_id`) REFERENCES `empleado` (`id`),
  CONSTRAINT `fk_Telefono_Proveedor1` FOREIGN KEY (`Proveedor_id`) REFERENCES `proveedor` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `telefono`
--

LOCK TABLES `telefono` WRITE;
/*!40000 ALTER TABLE `telefono` DISABLE KEYS */;
/*!40000 ALTER TABLE `telefono` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `venta`
--

DROP TABLE IF EXISTS `venta`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `venta` (
  `id` int NOT NULL AUTO_INCREMENT,
  `Empleado_id` int NOT NULL,
  `fecha` datetime NOT NULL,
  `total_venta` float NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_Venta_Empleado1_idx` (`Empleado_id`),
  CONSTRAINT `fk_Venta_Empleado1` FOREIGN KEY (`Empleado_id`) REFERENCES `empleado` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `venta`
--

LOCK TABLES `venta` WRITE;
/*!40000 ALTER TABLE `venta` DISABLE KEYS */;
INSERT INTO `venta` VALUES (2,1,'2025-04-17 21:22:13',1525),(3,1,'2025-04-17 21:45:44',636),(4,1,'2024-03-21 15:10:30',432),(8,2,'2025-05-17 21:38:17',600),(9,2,'2025-05-17 22:18:12',1210),(10,2,'2025-05-17 23:46:29',811),(11,2,'2025-05-18 10:24:23',1288),(12,2,'2025-05-19 09:15:19',1979);
/*!40000 ALTER TABLE `venta` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-21  8:55:35

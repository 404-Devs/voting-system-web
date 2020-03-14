-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 14, 2020 at 08:47 AM
-- Server version: 10.4.8-MariaDB
-- PHP Version: 7.3.11

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `web`
--

-- --------------------------------------------------------

--
-- Table structure for table `kin`
--

CREATE TABLE `kin` (
  `kinID` int(11) NOT NULL,
  `patientID` int(11) NOT NULL,
  `fName` varchar(35) NOT NULL,
  `surname` varchar(35) NOT NULL,
  `relationship` enum('Spouse','Parent','Uncle','Aunt','Guardian') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `kin`
--

INSERT INTO `kin` (`kinID`, `patientID`, `fName`, `surname`, `relationship`) VALUES
(1, 5000, 'Stephen', 'Mwanfi', 'Spouse'),
(2, 7878, 'Via', 'Via', 'Spouse'),
(3, 8000, 'Via', 'Via', 'Spouse'),
(4, 5000, 'sadf', 'asdfasdf', 'Spouse');

-- --------------------------------------------------------

--
-- Table structure for table `patient`
--

CREATE TABLE `patient` (
  `patientID` int(11) NOT NULL,
  `fName` varchar(35) NOT NULL,
  `mName` varchar(35) NOT NULL,
  `surname` varchar(35) NOT NULL,
  `dob` date NOT NULL,
  `gender` enum('Male','Female') NOT NULL,
  `county` varchar(35) NOT NULL,
  `nationalID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `patient`
--

INSERT INTO `patient` (`patientID`, `fName`, `mName`, `surname`, `dob`, `gender`, `county`, `nationalID`) VALUES
(1, 'fName', 'mName', 'surname', '2019-11-13', 'Male', 'county', 5000),
(2, 'fsdgsdg', 'asdfads', 'asdfasdf', '2019-11-12', 'Male', '1', 7878),
(4, 'Stephen', 'Kioni', 'Mwangi', '2019-11-28', 'Male', '', 8000),
(5, 'qwer', 'werwer', 'wqrqwer', '2019-11-06', 'Male', '', 234),
(6, 'rwqer', 'qwer', 'wrqwer', '2019-11-20', 'Male', 'Mombasa', 2345);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `kin`
--
ALTER TABLE `kin`
  ADD PRIMARY KEY (`kinID`),
  ADD KEY `patientID` (`patientID`);

--
-- Indexes for table `patient`
--
ALTER TABLE `patient`
  ADD PRIMARY KEY (`patientID`),
  ADD UNIQUE KEY `nationalID` (`nationalID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `kin`
--
ALTER TABLE `kin`
  MODIFY `kinID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `patient`
--
ALTER TABLE `patient`
  MODIFY `patientID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `kin`
--
ALTER TABLE `kin`
  ADD CONSTRAINT `patientID` FOREIGN KEY (`patientID`) REFERENCES `patient` (`nationalID`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

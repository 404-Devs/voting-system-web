-- noinspection SqlNoDataSourceInspectionForFile

-- phpMyAdmin SQL Dump
-- version 4.9.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 14, 2020 at 11:27 AM
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
-- Database: `campus_voting`
--

-- --------------------------------------------------------

--
-- Table structure for table `aspirant`
--

CREATE TABLE `aspirant` (
  `aspirant_id` int(20) NOT NULL,
  `voter_id` int(20) NOT NULL,
  `aspirant_photo` longtext NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `election`
--

CREATE TABLE `election` (
  `election_id` int(20) NOT NULL,
  `election_name` varchar(255) NOT NULL,
  `start_timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `end_timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `school`
--

CREATE TABLE `school` (
  `school_id` int(20) NOT NULL,
  `school_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `team`
--

CREATE TABLE `team` (
  `team_id` int(20) NOT NULL,
  `team_name` varchar(255) NOT NULL,
  `team_logo` longtext NOT NULL,
  `election_id` int(20) NOT NULL,
  `chairman_id` int(20) NOT NULL,
  `sec_gen_id` int(20) NOT NULL,
  `treasurer_id` int(20) NOT NULL,
  `blockchain_address` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `vote`
--

CREATE TABLE `vote` (
  `vote_id` int(20) NOT NULL,
  `election_id` int(20) NOT NULL,
  `voter_id` int(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `voter`
--

CREATE TABLE `voter` (
  `voter_id` int(20) NOT NULL,
  `voter_regno` varchar(50) NOT NULL,
  `school_id` int(11) NOT NULL,
  `email` varchar(255) NOT NULL,
  `voter_password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `aspirant`
--
ALTER TABLE `aspirant`
  ADD PRIMARY KEY (`aspirant_id`),
  ADD KEY `voter_id` (`voter_id`);

--
-- Indexes for table `election`
--
ALTER TABLE `election`
  ADD PRIMARY KEY (`election_id`);

--
-- Indexes for table `school`
--
ALTER TABLE `school`
  ADD PRIMARY KEY (`school_id`);

--
-- Indexes for table `team`
--
ALTER TABLE `team`
  ADD PRIMARY KEY (`team_id`),
  ADD KEY `election_id` (`election_id`),
  ADD KEY `chairman_id` (`chairman_id`),
  ADD KEY `sec_gen_id` (`sec_gen_id`),
  ADD KEY `treasurer_id` (`treasurer_id`);

--
-- Indexes for table `vote`
--
ALTER TABLE `vote`
  ADD PRIMARY KEY (`vote_id`),
  ADD KEY `election_id` (`election_id`),
  ADD KEY `voter_id` (`voter_id`);

--
-- Indexes for table `voter`
--
ALTER TABLE `voter`
  ADD PRIMARY KEY (`voter_id`),
  ADD KEY `school_id` (`school_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `aspirant`
--
ALTER TABLE `aspirant`
  MODIFY `aspirant_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `election`
--
ALTER TABLE `election`
  MODIFY `election_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `school`
--
ALTER TABLE `school`
  MODIFY `school_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `team`
--
ALTER TABLE `team`
  MODIFY `team_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `vote`
--
ALTER TABLE `vote`
  MODIFY `vote_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `voter`
--
ALTER TABLE `voter`
  MODIFY `voter_id` int(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `aspirant`
--
ALTER TABLE `aspirant`
  ADD CONSTRAINT `voter_id2` FOREIGN KEY (`voter_id`) REFERENCES `voter` (`voter_id`);

--
-- Constraints for table `team`
--
ALTER TABLE `team`
  ADD CONSTRAINT `chairman_id` FOREIGN KEY (`chairman_id`) REFERENCES `aspirant` (`aspirant_id`),
  ADD CONSTRAINT `election_id2` FOREIGN KEY (`election_id`) REFERENCES `election` (`election_id`),
  ADD CONSTRAINT `sec_gen_id` FOREIGN KEY (`sec_gen_id`) REFERENCES `aspirant` (`aspirant_id`),
  ADD CONSTRAINT `treasurer_id` FOREIGN KEY (`treasurer_id`) REFERENCES `aspirant` (`aspirant_id`);

--
-- Constraints for table `vote`
--
ALTER TABLE `vote`
  ADD CONSTRAINT `election_id` FOREIGN KEY (`election_id`) REFERENCES `election` (`election_id`),
  ADD CONSTRAINT `voter_id` FOREIGN KEY (`voter_id`) REFERENCES `voter` (`voter_id`),
  ADD CONSTRAINT `voter_id1` FOREIGN KEY (`voter_id`) REFERENCES `voter` (`voter_id`);

--
-- Constraints for table `voter`
--
ALTER TABLE `voter`
  ADD CONSTRAINT `school_id` FOREIGN KEY (`school_id`) REFERENCES `school` (`school_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

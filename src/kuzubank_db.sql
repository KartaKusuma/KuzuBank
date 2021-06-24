#File   : kuzubank_db.sql
#Author : Karta Kusuma

CREATE SCHEMA `kuzubank` ;


CREATE TABLE `kuzubank`.`users` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `password` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`user_id`, `username`));

CREATE TABLE `kuzubank`.`activeuser` (
  `id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`));

CREATE TABLE `kuzubank`.`balances` (
  `user_id` INT NOT NULL AUTO_INCREMENT,
  `username` VARCHAR(45) NOT NULL,
  `amount` INT NOT NULL DEFAULT 0,
  PRIMARY KEY (`user_id`, `username`));

CREATE TABLE `kuzubank`.`payment` (
  `counter` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `action` VARCHAR(100) NULL,
  PRIMARY KEY (`counter`, `user_id`));

CREATE TABLE `kuzubank`.`transfer` (
  `counter` INT NOT NULL AUTO_INCREMENT,
  `user_id` INT NOT NULL,
  `action` VARCHAR(100) NULL,
  PRIMARY KEY (`counter`, `user_id`));

INSERT INTO `kuzubank`.`users` (`user_id`, `username`, `password`) VALUES ('1', 'user', '12345');
INSERT INTO `kuzubank`.`users` (`user_id`, `username`, `password`) VALUES ('2', 'budi123', '123budi');
INSERT INTO `kuzubank`.`users` (`user_id`, `username`, `password`) VALUES ('3', 'maya', 'm4y4');

INSERT INTO `kuzubank`.`balances` (`user_id`, `username`, `amount`) VALUES ('1', 'user', '100000000');
INSERT INTO `kuzubank`.`balances` (`user_id`, `username`, `amount`) VALUES ('2', 'budi123', '75000000');
INSERT INTO `kuzubank`.`balances` (`user_id`, `username`, `amount`) VALUES ('3', 'maya', '50000000');


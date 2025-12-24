-- MySQL schema for Civil Engineering LIMS

CREATE DATABASE IF NOT EXISTS lims_db DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE lims_db;

CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(80) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(30) NOT NULL DEFAULT 'Lab Technician'
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS samples (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sample_id VARCHAR(50) NOT NULL UNIQUE,
  sample_type VARCHAR(50) NOT NULL,
  project_name VARCHAR(120),
  client_name VARCHAR(120),
  date_collected VARCHAR(30)
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS test_results (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sample_id INT NOT NULL,
  test_name VARCHAR(120) NOT NULL,
  raw_values TEXT,
  calculated_result TEXT,
  date_tested DATETIME,
  FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE CASCADE
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reports (
  id INT AUTO_INCREMENT PRIMARY KEY,
  sample_id INT,
  test_result_id INT,
  file_path VARCHAR(255),
  created_at DATETIME,
  FOREIGN KEY (sample_id) REFERENCES samples(id) ON DELETE SET NULL,
  FOREIGN KEY (test_result_id) REFERENCES test_results(id) ON DELETE SET NULL
) ENGINE=InnoDB;

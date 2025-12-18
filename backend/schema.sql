-- schema.sql (v1, normalized PK/FK naming, 1NF/2NF-friendly)

CREATE DATABASE IF NOT EXISTS edusmart
  DEFAULT CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE edusmart;

-- ===============
-- Basic Table: users
-- ===============
CREATE TABLE IF NOT EXISTS users (
  user_id        BIGINT AUTO_INCREMENT,
  username       VARCHAR(50) NOT NULL,
  password_hash  VARCHAR(255) NOT NULL,
  full_name      VARCHAR(100) NOT NULL,
  role           ENUM('admin','teacher','student') NOT NULL,
  email          VARCHAR(100),
  avatar         VARCHAR(255),
  is_active      TINYINT(1) NOT NULL DEFAULT 1,
  created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT pk_users PRIMARY KEY (user_id),
  CONSTRAINT uq_users__username UNIQUE (username)
) ENGINE=InnoDB;

-- ===============
-- classes (A class is managed by one teacher)
-- ===============
CREATE TABLE IF NOT EXISTS classes (
  class_id       BIGINT AUTO_INCREMENT,
  name           VARCHAR(50) NOT NULL,
  grade          VARCHAR(50) NOT NULL,
  teacher_id     BIGINT NULL,
  students_count INT DEFAULT 0,
  avg_attendance DECIMAL(5,2) DEFAULT 0,
  created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT pk_classes PRIMARY KEY (class_id),
  CONSTRAINT fk_classes__teacher FOREIGN KEY (teacher_id)
      REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
  INDEX idx_classes__teacher_id (teacher_id)
) ENGINE=InnoDB;

-- ===============
-- notices
-- ===============
CREATE TABLE IF NOT EXISTS notices (
  notice_id     BIGINT AUTO_INCREMENT,
  title         VARCHAR(200) NOT NULL,
  content       TEXT NOT NULL,
  author_id     BIGINT NULL,
  date          DATE NOT NULL,
  priority      ENUM('important','normal') DEFAULT 'normal',
  category      VARCHAR(50),
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_notices PRIMARY KEY (notice_id),
  CONSTRAINT fk_notices__author FOREIGN KEY (author_id)
      REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE SET NULL,
  INDEX idx_notices__author_id (author_id)
) ENGINE=InnoDB;

-- ===============
-- grades (Unique for each student x term x subject)
-- ===============
CREATE TABLE IF NOT EXISTS grades (
  grade_id      BIGINT AUTO_INCREMENT,
  student_id    BIGINT NOT NULL,
  subject       ENUM('chinese','math','english') NOT NULL,
  term          VARCHAR(50),
  score         DECIMAL(5,2) NOT NULL,
  created_at    DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT pk_grades PRIMARY KEY (grade_id),
  CONSTRAINT fk_grades__student FOREIGN KEY (student_id)
      REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
  CONSTRAINT uq_grades__student_term_subject UNIQUE (student_id, term, subject),
  INDEX idx_grades__student_id (student_id)
) ENGINE=InnoDB;


-- ==================
-- user_preferences
-- ==================
CREATE TABLE IF NOT EXISTS user_preferences (
  user_id        BIGINT,
  dark_mode      TINYINT(1) NOT NULL DEFAULT 0,
  language       VARCHAR(10) NOT NULL DEFAULT 'en',
  notifications  TINYINT(1) NOT NULL DEFAULT 1,
  email_alerts   TINYINT(1) NOT NULL DEFAULT 0,
  created_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at     DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT pk_user_preferences PRIMARY KEY (user_id),
  CONSTRAINT fk_user_preferences__user FOREIGN KEY (user_id)
      REFERENCES users(user_id) ON UPDATE CASCADE ON DELETE CASCADE
) ENGINE=InnoDB;

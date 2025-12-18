-- seed_data.sql (aligned with normalized schema)
USE edusmart;

-- example 'hashed:123456'
INSERT INTO users (username, password_hash, full_name, role, email, avatar)
VALUES
('admin',   'hashed:123456', 'Administrator', 'admin',   'admin@example.com',   '👨‍💼'),
('teacher', 'hashed:123456', 'Teacher Lawliet', 'teacher', 'teacher@example.com', '👨‍🏫'),
('student', 'hashed:123456', 'Student Mike', 'student', 'student@example.com', '👨‍🎓'),
-- Class 1A students (28)
('s001', 'hashed:123456', 'Alice Wang', 'student', 'alice@example.com', '👧'),
('s002', 'hashed:123456', 'Bob Chen', 'student', 'bob@example.com', '👦'),
('s003', 'hashed:123456', 'Carol Liu', 'student', 'carol@example.com', '👧'),
('s004', 'hashed:123456', 'David Zhang', 'student', 'david@example.com', '👦'),
('s005', 'hashed:123456', 'Emma Li', 'student', 'emma@example.com', '👧'),
('s006', 'hashed:123456', 'Frank Wu', 'student', 'frank@example.com', '👦'),
('s007', 'hashed:123456', 'Grace Zhou', 'student', 'grace@example.com', '👧'),
('s008', 'hashed:123456', 'Henry Sun', 'student', 'henry@example.com', '👦'),
('s009', 'hashed:123456', 'Ivy Ma', 'student', 'ivy@example.com', '👧'),
('s010', 'hashed:123456', 'Jack Zhao', 'student', 'jack@example.com', '👦'),
('s011', 'hashed:123456', 'Kelly Qian', 'student', 'kelly@example.com', '👧'),
('s012', 'hashed:123456', 'Leo Sun', 'student', 'leo@example.com', '👦'),
('s013', 'hashed:123456', 'Mia Li', 'student', 'mia@example.com', '👧'),
('s014', 'hashed:123456', 'Noah Wang', 'student', 'noah@example.com', '👦'),
('s015', 'hashed:123456', 'Olivia Chen', 'student', 'olivia@example.com', '👧'),
('s016', 'hashed:123456', 'Paul Zhang', 'student', 'paul@example.com', '👦'),
('s017', 'hashed:123456', 'Quinn Liu', 'student', 'quinn@example.com', '👧'),
('s018', 'hashed:123456', 'Ryan Wu', 'student', 'ryan@example.com', '👦'),
('s019', 'hashed:123456', 'Sophia Zhou', 'student', 'sophia@example.com', '👧'),
('s020', 'hashed:123456', 'Tom Sun', 'student', 'tom@example.com', '👦'),
('s021', 'hashed:123456', 'Uma Ma', 'student', 'uma@example.com', '👧'),
('s022', 'hashed:123456', 'Victor Zhao', 'student', 'victor@example.com', '👦'),
('s023', 'hashed:123456', 'Wendy Qian', 'student', 'wendy@example.com', '👧'),
('s024', 'hashed:123456', 'Xavier Sun', 'student', 'xavier@example.com', '👦'),
('s025', 'hashed:123456', 'Yuki Li', 'student', 'yuki@example.com', '👧'),
('s026', 'hashed:123456', 'Zoe Wang', 'student', 'zoe@example.com', '👧'),
('s027', 'hashed:123456', 'Alex Chen', 'student', 'alex@example.com', '👦'),
('s028', 'hashed:123456', 'Bella Zhang', 'student', 'bella@example.com', '👧'),
-- Class 1B students (30)
('s029', 'hashed:123456', 'Charlie Liu', 'student', 'charlie@example.com', '👦'),
('s030', 'hashed:123456', 'Diana Wu', 'student', 'diana@example.com', '👧'),
('s031', 'hashed:123456', 'Ethan Zhou', 'student', 'ethan@example.com', '👦'),
('s032', 'hashed:123456', 'Fiona Sun', 'student', 'fiona@example.com', '👧'),
('s033', 'hashed:123456', 'George Ma', 'student', 'george@example.com', '👦'),
('s034', 'hashed:123456', 'Hannah Zhao', 'student', 'hannah@example.com', '👧'),
('s035', 'hashed:123456', 'Ian Qian', 'student', 'ian@example.com', '👦'),
('s036', 'hashed:123456', 'Julia Sun', 'student', 'julia@example.com', '👧'),
('s037', 'hashed:123456', 'Kevin Li', 'student', 'kevin@example.com', '👦'),
('s038', 'hashed:123456', 'Luna Wang', 'student', 'luna@example.com', '👧'),
('s039', 'hashed:123456', 'Max Chen', 'student', 'max@example.com', '👦'),
('s040', 'hashed:123456', 'Nina Zhang', 'student', 'nina@example.com', '👧'),
('s041', 'hashed:123456', 'Owen Liu', 'student', 'owen@example.com', '👦'),
('s042', 'hashed:123456', 'Penny Wu', 'student', 'penny@example.com', '👧'),
('s043', 'hashed:123456', 'Quinn Zhou', 'student', 'quinn2@example.com', '👦'),
('s044', 'hashed:123456', 'Ruby Sun', 'student', 'ruby@example.com', '👧'),
('s045', 'hashed:123456', 'Sam Ma', 'student', 'sam@example.com', '👦'),
('s046', 'hashed:123456', 'Tina Zhao', 'student', 'tina@example.com', '👧'),
('s047', 'hashed:123456', 'Ugo Qian', 'student', 'ugo@example.com', '👦'),
('s048', 'hashed:123456', 'Vera Sun', 'student', 'vera@example.com', '👧'),
('s049', 'hashed:123456', 'Will Li', 'student', 'will@example.com', '👦'),
('s050', 'hashed:123456', 'Xara Wang', 'student', 'xara@example.com', '👧'),
('s051', 'hashed:123456', 'Yuan Chen', 'student', 'yuan@example.com', '👦'),
('s052', 'hashed:123456', 'Zara Zhang', 'student', 'zara@example.com', '👧'),
('s053', 'hashed:123456', 'Aiden Liu', 'student', 'aiden@example.com', '👦'),
('s054', 'hashed:123456', 'Bria Wu', 'student', 'bria@example.com', '👧'),
('s055', 'hashed:123456', 'Cade Zhou', 'student', 'cade@example.com', '👦'),
('s056', 'hashed:123456', 'Dara Sun', 'student', 'dara@example.com', '👧'),
('s057', 'hashed:123456', 'Evan Ma', 'student', 'evan@example.com', '👦'),
('s058', 'hashed:123456', 'Faye Zhao', 'student', 'faye@example.com', '👧');

-- Example classes (teacher_id references users.user_id)
INSERT INTO classes (name, grade, teacher_id, students_count, avg_attendance)
VALUES
('Class 1A', 'Grade 1', 2, 28, 95.0),
('Class 1B', 'Grade 1', 2, 30, 92.0);

-- Student profiles - Class 1A (28 students)
-- avg_grade changed to DECIMAL, initialized to NULL, later refreshed by grades table
INSERT INTO student_profiles (user_id, class_id, student_no, status, attendance_rate, avg_grade)
VALUES
(4, 1, 'S001', 'active', 98.0, NULL),
(5, 1, 'S002', 'active', 95.0, NULL),
(6, 1, 'S003', 'active', 92.0, NULL),
(7, 1, 'S004', 'active', 88.0, NULL),
(8, 1, 'S005', 'active', 100.0, NULL),
(9, 1, 'S006', 'active', 87.0, NULL),
(10, 1, 'S007', 'active', 94.0, NULL),
(11, 1, 'S008', 'active', 91.0, NULL),
(12, 1, 'S009', 'active', 96.0, NULL),
(13, 1, 'S010', 'active', 89.0, NULL),
(14, 1, 'S011', 'active', 93.0, NULL),
(15, 1, 'S012', 'active', 97.0, NULL),
(16, 1, 'S013', 'active', 90.0, NULL),
(17, 1, 'S014', 'active', 85.0, NULL),
(18, 1, 'S015', 'active', 99.0, NULL),
(19, 1, 'S016', 'active', 86.0, NULL),
(20, 1, 'S017', 'active', 92.0, NULL),
(21, 1, 'S018', 'active', 94.0, NULL),
(22, 1, 'S019', 'active', 91.0, NULL),
(23, 1, 'S020', 'active', 88.0, NULL),
(24, 1, 'S021', 'active', 95.0, NULL),
(25, 1, 'S022', 'active', 93.0, NULL),
(26, 1, 'S023', 'active', 90.0, NULL),
(27, 1, 'S024', 'active', 97.0, NULL),
(28, 1, 'S025', 'active', 89.0, NULL),
(29, 1, 'S026', 'active', 96.0, NULL),
(30, 1, 'S027', 'active', 92.0, NULL),
(31, 1, 'S028', 'active', 94.0, NULL);

-- Student profiles - Class 1B (30 students)
INSERT INTO student_profiles (user_id, class_id, student_no, status, attendance_rate, avg_grade)
VALUES
(32, 2, 'S029', 'active', 91.0, NULL),
(33, 2, 'S030', 'active', 88.0, NULL),
(34, 2, 'S031', 'active', 95.0, NULL),
(35, 2, 'S032', 'active', 93.0, NULL),
(36, 2, 'S033', 'active', 90.0, NULL),
(37, 2, 'S034', 'active', 87.0, NULL),
(38, 2, 'S035', 'active', 96.0, NULL),
(39, 2, 'S036', 'active', 94.0, NULL),
(40, 2, 'S037', 'active', 89.0, NULL),
(41, 2, 'S038', 'active', 92.0, NULL),
(42, 2, 'S039', 'active', 98.0, NULL),
(43, 2, 'S040', 'active', 91.0, NULL),
(44, 2, 'S041', 'active', 85.0, NULL),
(45, 2, 'S042', 'active', 97.0, NULL),
(46, 2, 'S043', 'active', 93.0, NULL),
(47, 2, 'S044', 'active', 90.0, NULL),
(48, 2, 'S045', 'active', 88.0, NULL),
(49, 2, 'S046', 'active', 95.0, NULL),
(50, 2, 'S047', 'active', 92.0, NULL),
(51, 2, 'S048', 'active', 94.0, NULL),
(52, 2, 'S049', 'active', 89.0, NULL),
(53, 2, 'S050', 'active', 96.0, NULL),
(54, 2, 'S051', 'active', 91.0, NULL),
(55, 2, 'S052', 'active', 87.0, NULL),
(56, 2, 'S053', 'active', 93.0, NULL),
(57, 2, 'S054', 'active', 90.0, NULL),
(58, 2, 'S055', 'active', 95.0, NULL),
(59, 2, 'S056', 'active', 88.0, NULL),
(60, 2, 'S057', 'active', 92.0, NULL),
(61, 2, 'S058', 'active', 94.0, NULL);


-- Example notices
INSERT INTO notices (title, content, author_id, date, priority, category)
VALUES
('Final Exam Schedule Released',
 'The final exam schedule for this semester has been released. Please check the student portal for detailed information about exam dates, times, and locations. All students are required to review the schedule and prepare accordingly.',
 1, '2024-02-15', 'important', 'Academic'),
('Parent-Teacher Meeting',
 'Parent-teacher meeting will be held on February 20th. All parents are encouraged to attend to discuss their children\'s academic progress and any concerns. Please confirm your attendance by February 18th.',
 1, '2025-09-12', 'important', 'Event'),
('Winter Holiday Homework',
 'Please remind students to complete their winter holiday homework before the new semester starts. All assignments must be submitted by the first day of school. Late submissions will not be accepted.',
 1, '2025-09-10', 'normal', 'Academic'),
('School Festival Announcement',
 'The annual school festival will take place on March 15th. We encourage all students to prepare performances and activities. This is a great opportunity to showcase talents and celebrate our school community.',
 1, '2025-10-08', 'normal', 'Event'),
('Library Hours Extended',
 'The library will now be open until 8 PM on weekdays to support student studying. This extended schedule will help students who need extra time for research and homework. Please make use of this opportunity.',
 1, '2025-10-15', 'normal', 'Facility');

-- Student grades data (three subjects: Chinese, Math, English, score range 1-100)
-- Class 1A student grades (28 students, user_id 4-31)
INSERT INTO grades (student_id, subject, term, score)
VALUES
-- S001-S005
(4, 'chinese', 'current', 92), (4, 'math', 'current', 95), (4, 'english', 'current', 88),
(5, 'chinese', 'current', 88), (5, 'math', 'current', 90), (5, 'english', 'current', 87),
(6, 'chinese', 'current', 85), (6, 'math', 'current', 87), (6, 'english', 'current', 84),
(7, 'chinese', 'current', 82), (7, 'math', 'current', 85), (7, 'english', 'current', 80),
(8, 'chinese', 'current', 96), (8, 'math', 'current', 98), (8, 'english', 'current', 95),
-- S006-S010
(9, 'chinese', 'current', 80), (9, 'math', 'current', 83), (9, 'english', 'current', 78),
(10, 'chinese', 'current', 90), (10, 'math', 'current', 92), (10, 'english', 'current', 88),
(11, 'chinese', 'current', 87), (11, 'math', 'current', 89), (11, 'english', 'current', 85),
(12, 'chinese', 'current', 93), (12, 'math', 'current', 95), (12, 'english', 'current', 90),
(13, 'chinese', 'current', 84), (13, 'math', 'current', 86), (13, 'english', 'current', 82),
-- S011-S015
(14, 'chinese', 'current', 89), (14, 'math', 'current', 91), (14, 'english', 'current', 87),
(15, 'chinese', 'current', 94), (15, 'math', 'current', 96), (15, 'english', 'current', 92),
(16, 'chinese', 'current', 86), (16, 'math', 'current', 88), (16, 'english', 'current', 84),
(17, 'chinese', 'current', 79), (17, 'math', 'current', 82), (17, 'english', 'current', 76),
(18, 'chinese', 'current', 97), (18, 'math', 'current', 99), (18, 'english', 'current', 96),
-- S016-S020
(19, 'chinese', 'current', 81), (19, 'math', 'current', 84), (19, 'english', 'current', 79),
(20, 'chinese', 'current', 88), (20, 'math', 'current', 90), (20, 'english', 'current', 86),
(21, 'chinese', 'current', 91), (21, 'math', 'current', 93), (21, 'english', 'current', 89),
(22, 'chinese', 'current', 87), (22, 'math', 'current', 89), (22, 'english', 'current', 85),
(23, 'chinese', 'current', 83), (23, 'math', 'current', 85), (23, 'english', 'current', 81),
-- S021-S025
(24, 'chinese', 'current', 91), (24, 'math', 'current', 93), (24, 'english', 'current', 89),
(25, 'chinese', 'current', 89), (25, 'math', 'current', 91), (25, 'english', 'current', 87),
(26, 'chinese', 'current', 86), (26, 'math', 'current', 88), (26, 'english', 'current', 84),
(27, 'chinese', 'current', 94), (27, 'math', 'current', 96), (27, 'english', 'current', 92),
(28, 'chinese', 'current', 84), (28, 'math', 'current', 86), (28, 'english', 'current', 82),
-- S026-S028
(29, 'chinese', 'current', 93), (29, 'math', 'current', 95), (29, 'english', 'current', 91),
(30, 'chinese', 'current', 88), (30, 'math', 'current', 90), (30, 'english', 'current', 86),
(31, 'chinese', 'current', 90), (31, 'math', 'current', 92), (31, 'english', 'current', 88);

-- Class 1B student grades (30 students, user_id 32-61)
INSERT INTO grades (student_id, subject, term, score)
VALUES
-- S029-S033
(32, 'chinese', 'current', 87), (32, 'math', 'current', 89), (32, 'english', 'current', 85),
(33, 'chinese', 'current', 83), (33, 'math', 'current', 85), (33, 'english', 'current', 81),
(34, 'chinese', 'current', 91), (34, 'math', 'current', 93), (34, 'english', 'current', 89),
(35, 'chinese', 'current', 89), (35, 'math', 'current', 91), (35, 'english', 'current', 87),
(36, 'chinese', 'current', 86), (36, 'math', 'current', 88), (36, 'english', 'current', 84),
-- S034-S038
(37, 'chinese', 'current', 82), (37, 'math', 'current', 84), (37, 'english', 'current', 80),
(38, 'chinese', 'current', 93), (38, 'math', 'current', 95), (38, 'english', 'current', 91),
(39, 'chinese', 'current', 90), (39, 'math', 'current', 92), (39, 'english', 'current', 88),
(40, 'chinese', 'current', 85), (40, 'math', 'current', 87), (40, 'english', 'current', 83),
(41, 'chinese', 'current', 88), (41, 'math', 'current', 90), (41, 'english', 'current', 86),
-- S039-S043
(42, 'chinese', 'current', 95), (42, 'math', 'current', 97), (42, 'english', 'current', 93),
(43, 'chinese', 'current', 87), (43, 'math', 'current', 89), (43, 'english', 'current', 85),
(44, 'chinese', 'current', 79), (44, 'math', 'current', 82), (44, 'english', 'current', 76),
(45, 'chinese', 'current', 94), (45, 'math', 'current', 96), (45, 'english', 'current', 92),
(46, 'chinese', 'current', 89), (46, 'math', 'current', 91), (46, 'english', 'current', 87),
-- S044-S048
(47, 'chinese', 'current', 86), (47, 'math', 'current', 88), (47, 'english', 'current', 84),
(48, 'chinese', 'current', 83), (48, 'math', 'current', 85), (48, 'english', 'current', 81),
(49, 'chinese', 'current', 91), (49, 'math', 'current', 93), (49, 'english', 'current', 89),
(50, 'chinese', 'current', 93), (50, 'math', 'current', 95), (50, 'english', 'current', 91),
(51, 'chinese', 'current', 90), (51, 'math', 'current', 92), (51, 'english', 'current', 88),
-- S049-S053
(52, 'chinese', 'current', 87), (52, 'math', 'current', 89), (52, 'english', 'current', 85),
(53, 'chinese', 'current', 82), (53, 'math', 'current', 84), (53, 'english', 'current', 80),
(54, 'chinese', 'current', 89), (54, 'math', 'current', 91), (54, 'english', 'current', 87),
(55, 'chinese', 'current', 86), (55, 'math', 'current', 88), (55, 'english', 'current', 84),
(56, 'chinese', 'current', 91), (56, 'math', 'current', 93), (56, 'english', 'current', 89),
-- S054-S058
(57, 'chinese', 'current', 86), (57, 'math', 'current', 88), (57, 'english', 'current', 84),
(58, 'chinese', 'current', 88), (58, 'math', 'current', 90), (58, 'english', 'current', 86),
(59, 'chinese', 'current', 83), (59, 'math', 'current', 85), (59, 'english', 'current', 81),
(60, 'chinese', 'current', 88), (60, 'math', 'current', 90), (60, 'english', 'current', 86),
(61, 'chinese', 'current', 90), (61, 'math', 'current', 92), (61, 'english', 'current', 88);

-- Update student_profiles.avg_grade by aggregating grades 
UPDATE student_profiles sp
JOIN (
    SELECT student_id, ROUND(AVG(score), 2) AS avg_score
    FROM grades
    GROUP BY student_id
) g ON g.student_id = sp.user_id
SET sp.avg_grade = g.avg_score;

-- Example assignments (only including Chinese/Math/English)
INSERT INTO assignments (title, subject, description, due_date, status, class_id, teacher_id)
VALUES
('Math Homework - Chapter 5 Practice', 'math', 'Geometry fundamentals exercises', '2024-02-15', 'pending', 1, 2),
('English Essay - My Dream', 'english', 'Write an essay about your dream', '2024-02-12', 'grading', 1, 2),
('Chinese Reading Comprehension', 'chinese', 'Read the passage and answer the questions', '2024-02-18', 'pending', 1, 2);

-- Initialize user preferences
INSERT INTO user_preferences (user_id, dark_mode, language, notifications, email_alerts)
SELECT user_id, 0, 'en', 1, 0 FROM users;
PRAGMA foreign_keys = ON;

CREATE TABLE Students (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 email TEXT UNIQUE
);

CREATE TABLE Instructors (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 name TEXT NOT NULL,
 email TEXT UNIQUE
);

CREATE TABLE Courses (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 title TEXT NOT NULL,
 description TEXT,
 instructor_id INTEGER,
 FOREIGN KEY (instructor_id) REFERENCES Instructors(id)
);

CREATE TABLE Enrollments (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 student_id INTEGER,
 course_id INTEGER,
 status TEXT DEFAULT 'in-progress',
 FOREIGN KEY (student_id) REFERENCES Students(id),
 FOREIGN KEY (course_id) REFERENCES Courses(id)
);

CREATE TABLE Assignments (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 course_id INTEGER,
 title TEXT,
 max_score INTEGER,
 FOREIGN KEY (course_id) REFERENCES Courses(id)
);

CREATE TABLE Grades (
 id INTEGER PRIMARY KEY AUTOINCREMENT,
 enrollment_id INTEGER,
 assignment_id INTEGER,
 score INTEGER,
 FOREIGN KEY (enrollment_id) REFERENCES Enrollments(id),
 FOREIGN KEY (assignment_id) REFERENCES Assignments(id)
);

-- Trigger: auto-update enrollment status
CREATE TRIGGER update_enrollment_status
AFTER INSERT ON Grades
BEGIN
    UPDATE Enrollments
    SET status = (
        CASE 
            WHEN (
                SELECT AVG(score) 
                FROM Grades g
                WHERE g.enrollment_id = NEW.enrollment_id
            ) >= 50 THEN 'completed'
            ELSE 'in-progress'
        END
    )
    WHERE id = NEW.enrollment_id;
END;

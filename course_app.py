import sqlite3
import os

DB_FILE = "course_management.db"
SCHEMA_FILE = "schema.sql"

# ---------------------------
# 1) Initialize Database
# ---------------------------
def init_db():
    if not os.path.exists(DB_FILE):
        print("Initializing database from schema.sql...")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        with open(SCHEMA_FILE, 'r') as f:
            cursor.executescript(f.read())
        conn.commit()
        conn.close()
        print(f"Database initialized: {DB_FILE}")
    else:
        print(f"Database found: {DB_FILE}")

# ---------------------------
# 2) Connect to DB
# ---------------------------
def get_conn():
    conn = sqlite3.connect(DB_FILE)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

# ---------------------------
# 3) CLI Commands
# ---------------------------
def add_student(name, email):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Students (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    print(f"Added student: {name}")

def add_instructor(name, email):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Instructors (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    conn.close()
    print(f"Added instructor: {name}")

def add_course(title, description, instructor_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Courses (title, description, instructor_id) VALUES (?, ?, ?)",
                   (title, description, instructor_id))
    conn.commit()
    conn.close()
    print(f"Added course: {title}")

def enroll(student_id, course_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
    conn.commit()
    conn.close()
    print(f"Student {student_id} enrolled in course {course_id}")

def add_assignment(course_id, title, max_score):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Assignments (course_id, title, max_score) VALUES (?, ?, ?)",
                   (course_id, title, max_score))
    conn.commit()
    conn.close()
    print(f"Added assignment: {title}")

def add_grade(enrollment_id, assignment_id, score):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Grades (enrollment_id, assignment_id, score) VALUES (?, ?, ?)",
                   (enrollment_id, assignment_id, score))
    conn.commit()
    conn.close()
    print(f"Added grade: {score} for enrollment {enrollment_id}")

def transcript(student_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.name, c.title AS course, a.title AS assignment, g.score
        FROM Grades g
        JOIN Enrollments e ON g.enrollment_id = e.id
        JOIN Students s ON e.student_id = s.id
        JOIN Assignments a ON g.assignment_id = a.id
        JOIN Courses c ON a.course_id = c.id
        WHERE s.id = ?
    """, (student_id,))
    rows = cursor.fetchall()
    if rows:
        print(f"\nTranscript for Student ID {student_id}:")
        for row in rows:
            print(f"Course: {row[1]}, Assignment: {row[2]}, Score: {row[3]}")
    else:
        print(f"No grades found for Student ID {student_id}")
    conn.close()

def list_students(course_id):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT s.id, s.name, e.status
        FROM Enrollments e
        JOIN Students s ON e.student_id = s.id
        WHERE e.course_id = ?
    """, (course_id,))
    rows = cursor.fetchall()
    if rows:
        print(f"\nStudents in Course ID {course_id}:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Status: {row[2]}")
    else:
        print(f"No students enrolled in Course ID {course_id}")
    conn.close()

# ---------------------------
# 4) CLI Loop
# ---------------------------
def main():
    init_db()
    print("\n🎓 Online Course Management CLI")
    print("Commands: add_student, add_instructor, add_course, enroll, add_assignment, add_grade, transcript, list_students, exit\n")
    
    while True:
        cmd = input("cmd> ").strip().split()
        if not cmd:
            continue
        command = cmd[0].lower()
        args = cmd[1:]
        
        try:
            if command == "add_student":
                add_student(args[0], args[1])
            elif command == "add_instructor":
                add_instructor(args[0], args[1])
            elif command == "add_course":
                add_course(args[0], args[1], int(args[2]))
            elif command == "enroll":
                enroll(int(args[0]), int(args[1]))
            elif command == "add_assignment":
                add_assignment(int(args[0]), args[1], int(args[2]))
            elif command == "add_grade":
                add_grade(int(args[0]), int(args[1]), int(args[2]))
            elif command == "transcript":
                transcript(int(args[0]))
            elif command == "list_students":
                list_students(int(args[0]))
            elif command in {"exit", "quit", "q"}:
                print("Bye! 👋")
                break
            else:
                print("Unknown command")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

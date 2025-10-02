import sqlite3

# 1️⃣ Connect to the database
conn = sqlite3.connect("course_management.db")
cursor = conn.cursor()

# 2️⃣ List of tables in your project
tables = ["Students", "Instructors", "Courses", "Enrollments", "Assignments", "Grades"]

# 3️⃣ Loop through tables and print all rows
for table in tables:
    print(f"\n=== Contents of {table} ===")
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(row)
    else:
        print("No data found.")

# 4️⃣ Close the connection
conn.close()
print("\n✅ Done viewing database.")

# import sqlite3

# conn = sqlite3.connect('jobportal.db')
# cursor = conn.cursor()



# # Insert Admin
# cursor.execute("INSERT OR IGNORE INTO users (name, email, role) VALUES (?, ?, ?)",
#                ('Admin', 'admin@jobhub.com', 'admin'))

# # Sample Users
# users = [
#     ('Alice', 'alice@example.com', 'job_seeker'),
#     ('Bob', 'bob@company.com', 'employer'),
# ]
# cursor.executemany("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", users)

# # Sample Jobs
# jobs = [
#     ('Software Engineer', 'Develop software apps', 'TechCorp', 'Delhi', '10LPA', 1),
#     ('HR Manager', 'Manage HR tasks', 'PeopleCo', 'Mumbai', '7LPA', 0),
# ]
# cursor.executemany("INSERT INTO jobs (title, description, company, location, salary, is_approved) VALUES (?, ?, ?, ?, ?, ?)", jobs)

# conn.commit()
# conn.close()
# print("Sample data inserted.")

################################################################################################################

import sqlite3
import os

# Use the same path as in app.py
# DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'job_portal.db')
# conn = sqlite3.connect(DATABASE)
conn = sqlite3.connect('job_portal.db')  # no path needed, creates in current folder
cursor = conn.cursor()

# Create users table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL
)
""")

# Create jobs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    company TEXT,
    location TEXT,
    salary TEXT,
    is_approved INTEGER DEFAULT 0
)
""")

# Insert Admin
cursor.execute("INSERT OR IGNORE INTO users (name, email, role) VALUES (?, ?, ?)",
               ('Admin', 'admin@jobhub.com', 'admin'))

# Sample Users
users = [
    ('Alice', 'alice@example.com', 'job_seeker'),
    ('Bob', 'bob@company.com', 'employer'),
]
cursor.executemany("INSERT INTO users (name, email, role) VALUES (?, ?, ?)", users)

# Sample Jobs
jobs = [
    ('Software Engineer', 'Develop software apps', 'TechCorp', 'Delhi', '10LPA', 1),
    ('HR Manager', 'Manage HR tasks', 'PeopleCo', 'Mumbai', '7LPA', 0),
]
cursor.executemany("INSERT INTO jobs (title, description, company, location, salary, is_approved) VALUES (?, ?, ?, ?, ?, ?)", jobs)

conn.commit()
conn.close()
print("✅ Tables created and sample data inserted.")

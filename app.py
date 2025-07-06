
from flask import Flask, render_template , g, session, request, redirect, url_for, flash
import sqlite3
import os
app = Flask(__name__) 
 
@app.route('/') 
def home(): 
    return render_template('index.html') 

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Required to use sessions

# ------------------ Database ------------------
DATABASE = os.path.join(os.path.dirname(__file__), 'database', 'job_portal.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# ------------------ In-memory Users ------------------
users = {
    'john': {'password': '1234'},
    'admin': {'password': 'admin123'}
}

# ------------------ Routes ------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        flash('Please log in first', 'warning')
        return redirect(url_for('login'))
    return f"Welcome {session['username']} to the dashboard!"

@app.route('/apply-job', methods=['GET', 'POST'])
def apply_job():
    db = get_db()
    jobs = db.execute("SELECT * FROM jobs").fetchall()
    if request.method == 'POST':
        user_id = session.get('user_id')
        job_id = request.form['job_id']
        db.execute("INSERT INTO applications (user_id, job_id) VALUES (?, ?)", (user_id, job_id))
        db.commit()
        return redirect('/apply-job')
    return render_template('apply-job.html', jobs=jobs)

@app.route('/manage-users')
def manage_users():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template('manage-users.html', users=users)

@app.route('/employer/manage-jobs')
def manage_jobs():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM jobs")
    jobs = cursor.fetchall()
    return render_template('manage-jobs.html', jobs=jobs)

@app.route('/delete-user/<int:user_id>')
def delete_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect('/login')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id=?", (user_id,))
    conn.commit()
    return redirect('/manage-users')

@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    if not session.get('admin_logged_in'):
        return redirect('/login')
    conn = get_db()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        role = request.form['role']
        cursor.execute("UPDATE users SET name=?, email=?, role=? WHERE id=?", (name, email, role, user_id))
        conn.commit()
        return redirect('/manage-users')
    cursor.execute("SELECT * FROM users WHERE id=?", (user_id,))
    user = cursor.fetchone()
    return render_template('edit-user.html', user=user)

# ------------------ Run App ------------------
if __name__ == '__main__':
    app.run(debug=True)

 


from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the SQLite database
conn = sqlite3.connect('employees.db')
cur = conn.cursor()

# Create tables if not exists
cur.executescript('''
    CREATE TABLE IF NOT EXISTS employees (
        emp_no INTEGER PRIMARY KEY,
        birth_date DATE NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        gender TEXT NOT NULL,
        hire_date DATE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS departments (
        dept_no CHAR(4) PRIMARY KEY,
        dept_name TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS dept_emp (
        emp_no INTEGER,
        dept_no CHAR(4),
        from_date DATE NOT NULL,
        to_date DATE NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
        FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
        PRIMARY KEY (emp_no, dept_no)
    );

    CREATE TABLE IF NOT EXISTS dept_manager (
        emp_no INTEGER,
        dept_no CHAR(4),
        from_date DATE NOT NULL,
        to_date DATE NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
        FOREIGN KEY (dept_no) REFERENCES departments(dept_no),
        PRIMARY KEY (emp_no, dept_no)
    );

    CREATE TABLE IF NOT EXISTS titles (
        emp_no INTEGER,
        title TEXT NOT NULL,
        from_date DATE NOT NULL,
        to_date DATE NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
        PRIMARY KEY (emp_no, title, from_date)
    );

    CREATE TABLE IF NOT EXISTS salaries (
        emp_no INTEGER,
        salary INTEGER NOT NULL,
        from_date DATE NOT NULL,
        to_date DATE NOT NULL,
        FOREIGN KEY (emp_no) REFERENCES employees(emp_no),
        PRIMARY KEY (emp_no, from_date)
    );
''')
conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def get_data():
    cur.execute("SELECT * FROM employees")
    rows = cur.fetchall()
    data = [{'emp_no': row[0], 'birth_date': row[1], 'first_name': row[2], 'last_name': row[3], 'gender': row[4], 'hire_date': row[5]} for row in rows]
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add_record():
    emp_no = request.form['empNo']
    birth_date = request.form['birthDate']
    first_name = request.form['firstName']
    last_name = request.form['lastName']
    gender = request.form['gender']
    hire_date = request.form['hireDate']
    cur.execute("INSERT INTO employees (emp_no, birth_date, first_name, last_name, gender, hire_date) VALUES (?, ?, ?, ?, ?, ?)", (emp_no, birth_date, first_name, last_name, gender, hire_date))
    conn.commit()
    return jsonify({'message': 'Record added successfully'})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to the database
conn = sqlite3.connect('example.db')
cur = conn.cursor()

# Create table if not exists
cur.execute('''CREATE TABLE IF NOT EXISTS users 
               (id INTEGER PRIMARY KEY, name TEXT, email TEXT)''')
conn.commit()

# Insert sample data if the table is empty
cur.execute("SELECT COUNT(*) FROM users")
if cur.fetchone()[0] == 0:
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("John Doe", "john@example.com"))
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", ("Jane Smith", "jane@example.com"))
    conn.commit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data', methods=['GET'])
def get_data():
    cur.execute("SELECT * FROM users")
    rows = cur.fetchall()
    data = [{'id': row[0], 'name': row[1], 'email': row[2]} for row in rows]
    return jsonify(data)

@app.route('/add', methods=['POST'])
def add_record():
    name = request.form['name']
    email = request.form['email']
    cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
    conn.commit()
    return jsonify({'message': 'Record added successfully'})

if __name__ == '__main__':
    app.run(debug=True)

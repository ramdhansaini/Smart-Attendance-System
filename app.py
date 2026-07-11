from flask import Flask, render_template, request
import os, base64, uuid, sqlite3

app = Flask(__name__, template_folder='templates')

# Ensure uploads folder exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Ensure SQLite database exists
DB_FILE = 'students.db'

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            rollno TEXT NOT NULL,
            image_path TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def home():
    return render_template('registerstudent.html')

@app.route('/registerstudent', methods=['POST'])
def register_student():
    data = request.get_json()
    if not data:
        return {'message': 'No data received'}, 400

    name = data.get('name')
    rollno = data.get('rollno')
    image_data = data.get('image')

    if not name or not rollno or not image_data:
        return {'message': 'Missing required fields'}, 400

    # Decode and save image with unique filename
    encoded = image_data.split(',', 1)[1]
    filename = f"{uuid.uuid4().hex}.png"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    with open(filepath, 'wb') as f:
        f.write(base64.b64decode(encoded))

    # Save student info into SQLite
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, rollno, image_path) VALUES (?, ?, ?)',
                   (name, rollno, filepath))
    conn.commit()
    conn.close()

    return {'message': f'Student {name} registered successfully with Roll No {rollno}!'}

@app.route('/students')
def list_students():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, name, rollno, image_path FROM students')
    students = cursor.fetchall()
    conn.close()

    # Return as JSON for simplicity
    return {
        'students': [
            {'id': s[0], 'name': s[1], 'rollno': s[2], 'image_path': s[3]}
            for s in students
        ]
    }

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'database.db'

def init_db():
    with app.app_context():
        db = sqlite3.connect(DATABASE)
        with app.open_resource('schema.sql', mode='r') as f:
            db.executescript(f.read())
        db.commit()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        task = request.form['task']
        db = sqlite3.connect(DATABASE)
        db.execute('INSERT INTO tasks (task) VALUES (?)', (task,))
        db.commit()
        return redirect(url_for('index'))
    
    db = sqlite3.connect(DATABASE)
    tasks = db.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    db = sqlite3.connect(DATABASE)
    db.execute('DELETE FROM tasks WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

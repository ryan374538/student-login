from flask import Flask, render_template, request, url_for, redirect, session
from connection import SessionLocal
from models import Students

app = Flask(__name__)
app.secret_key = "2480"

@app.route('/')
def home():
    return redirect(url_for('register'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        Admission = request.form['Admission']
        Course = request.form['Course']
        Unit = request.form['Unit']

        db = SessionLocal()
        try:
            existing_user = db.query(Students).filter_by(Admission=Admission).first()
            if existing_user:
                error = 'User already exists'
            else:
                new_user = Students(Admission=Admission, Course=Course, Unit=Unit)
                db.add(new_user)
                db.commit()
                return redirect(url_for('login'))
        finally:
            db.close()

    return render_template('register.html', error=error)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        Admission = request.form['Admission']
        Unit = request.form['Unit']

        db = SessionLocal()
        try:
            user = db.query(Students).filter_by(Admission=Admission).first()
            if user and user.Unit == Unit:
                session['Admission'] = user.Admission
                session['user_id'] = user.id
                return redirect(url_for('dashboard'))
            else:
                error = 'Invalid credentials'
        finally:
            db.close()

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'Admission' not in session:
        return redirect(url_for('login'))
    return f"Welcome, {session['Admission']}!"

if __name__ == "__main__":
    app.run(debug=True)

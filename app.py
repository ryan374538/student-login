from flask import Flask, render_template, request, url_for, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
from connection import SessionLocal
from models import Students

app = Flask(__name__)
app.secret_key = "2480"  # Use a stronger, random key in production

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        Admission = request.form.get('Admission', '').strip()
        Course = request.form.get('Course', '').strip()
        Unit = request.form.get('Unit', '').strip()

        if not Admission or not Course or not Unit:
            error = 'All fields are required.'
        else:
            db = SessionLocal()
            try:
                existing_user = db.query(Students).filter_by(Admission=Admission).first()
                if existing_user:
                    error = 'User already exists.'
                else:
                    hashed_unit = generate_password_hash(Unit)
                    new_user = Students(Admission=Admission, Course=Course, Unit=hashed_unit)
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
        Admission = request.form.get('Admission', '').strip()
        Unit = request.form.get('Unit', '').strip()

        if not Admission or not Unit:
            error = 'All fields are required.'
        else:
            db = SessionLocal()
            try:
                user = db.query(Students).filter_by(Admission=Admission).first()
                if user and check_password_hash(user.Unit, Unit):
                    session['Admission'] = user.Admission
                    session['user_id'] = user.id
                    return redirect(url_for('dashboard'))
                else:
                    error = 'Invalid credentials.'
            finally:
                db.close()

    return render_template('login.html', error=error)

@app.route('/dashboard')
def dashboard():
    if 'Admission' not in session:
        return redirect(url_for('login'))
    return f"Welcome, {session['Admission']}!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)

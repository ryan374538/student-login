from flask import Flask, render_template, request, url_for, redirect, session
from connection import SessionLocal
from models import Students

app = Flask(__name__)
app.secret_key = "2480"

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        Admission = request.form['Admission']
        Course = request.form['Course']
        Unit = request.form['Unit']

        db = SessionLocal()

        existing_user = db.query(Students).filter_by(Admission=Admission).first()

        if existing_user:
            error = 'User already exists'
        else:
            new_user = Students(Admission=Admission, Course=Course, Unit=Unit)
            db.add(new_user)
            db.commit()
            db.close()
            return redirect(url_for('login'))

        db.close()

    return render_template('register.html', error=error)

@app.route('/login')
def login():
    return render_template('login.html')



if __name__=="__main__":
    app.run(debug=True)

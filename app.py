from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, default=0.0)

@app.route('/')
def index():
    students = Student.query.all()
    return render_template('index.html', students=students)

@app.route('/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        student_id = request.form['student_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        amount_due = float(request.form['amount_due'])
        
        new_student = Student(student_id=student_id, first_name=first_name, last_name=last_name, dob=dob, amount_due=amount_due)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_student.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    student = Student.query.get_or_404(id)
    if request.method == 'POST':
        student.student_id = request.form['student_id']
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d').date()
        student.amount_due = float(request.form['amount_due'])
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit_student.html', student=student)

@app.route('/delete/<int:id>')
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/view/<int:id>')
def view_student(id):
    student = Student.query.get_or_404(id)
    return render_template('view_student.html', student=student)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
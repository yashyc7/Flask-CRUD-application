from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


migrate = Migrate(app, db)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    status=db.Column(db.Boolean,default=False)


with app.app_context():
    db.create_all()

    # Route to display all tasks

#Getting all queries into one fetch 
@app.route("/")
def home():
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

#Adding the tasks into the database
@app.route('/add', methods=['POST'])
def add():
    task = request.form.get('task')
    if task:
        new_task = Todo(task=task)
        db.session.add(new_task)
        db.session.commit()
    return redirect(url_for('home'))

#updating the tasks with the task id
@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Todo.query.get_or_404(id)
    updated_task = request.form.get("task")
    if updated_task:
        task.task = updated_task
        db.session.commit()
    return redirect(url_for("home"))

#deleting the tasks id 
@app.route("/delete/<int:id>")
def delete(id):
    task_obj = Todo.query.get_or_404(id)
    if task_obj:
        db.session.delete(task_obj)
        db.session.commit()
    return redirect(url_for("home"))

@app.route('/toggle/<int:id>')
def toggleStatus(id):
    task_obj=Todo.query.get_or_404(id)
    if task_obj:
        task_obj.status= not task_obj.status
        db.session.commit()
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)

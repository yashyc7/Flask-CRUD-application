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



"""
REST API approach for getting the data; 

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api = Api(app)

# Task Model
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task = db.Column(db.String(100), nullable=False)
    status = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"Task(id: {self.id}, task: {self.task}, status: {self.status})"


# Create the database tables
with app.app_context():
    db.create_all()


# REST API Endpoints
class TodoList(Resource):
    def get(self):
        todos = Todo.query.all()
        return jsonify([{'id': todo.id, 'task': todo.task, 'status': todo.status} for todo in todos])

    def post(self):
        data = request.get_json()
        new_task = Todo(task=data['task'])
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'id': new_task.id, 'task': new_task.task, 'status': new_task.status})

class TodoItem(Resource):
    def get(self, id):
        task = Todo.query.get_or_404(id)
        return jsonify({'id': task.id, 'task': task.task, 'status': task.status})

    def put(self, id):
        data = request.get_json()
        task = Todo.query.get_or_404(id)
        task.task = data['task']
        task.status = data.get('status', task.status)
        db.session.commit()
        return jsonify({'id': task.id, 'task': task.task, 'status': task.status})

    def delete(self, id):
        task = Todo.query.get_or_404(id)
        db.session.delete(task)
        db.session.commit()
        return '', 204


# Add API resources
api.add_resource(TodoList, '/api/todos')
api.add_resource(TodoItem, '/api/todos/<int:id>')


if __name__ == '__main__':
    app.run(debug=True)


"""
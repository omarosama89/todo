from flask import Blueprint, jsonify, redirect, url_for, url_for, request
from app import db
from models.todo import Todo
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route("/")
def root():
    return redirect(url_for("api.index"))

@api_bp.route("/todos")
def index():
    todos = Todo.query.all()
    return jsonify([todo.serialize() for todo in todos])

@api_bp.route("/todos/create", methods=['POST'])
def create():
    if not request.is_json:
        return not_supported_request()

    if request.method == 'POST':
        todo = Todo(
            title=request.json['title'],
            description=request.json['description'],
            due_to=datetime.strptime(request.json['due_to'], '%Y-%m-%d')
        )
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('api.show', id=todo.id))

@api_bp.route('/todos/<int:id>')
def show(id):
    todo = Todo.query.get(id)
    if todo:
        return jsonify(todo.serialize())
    return jsonify({'messsage': 'id not found'})

@api_bp.route("/todos/<int:id>/done", methods=['POST'])
def done(id):
    todo = Todo.query.get(id)
    if todo:
        todo.status = 'done'
        db.session.commit()
        return redirect(url_for('api.show', id=id))
    else:
        return not_found()


@api_bp.route("/todos/<int:id>/cancel", methods=['POST'])
def cancel(id):
    todo = Todo.query.get(id)
    if todo:
        todo.status = 'canceled'
        db.session.commit()
        return redirect(url_for('api.show', id=id))
    else:
        return not_found()

@api_bp.route("/todos/<int:id>/delete", methods=['POST'])
def delete(id):
    todo = Todo.query.get(id)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        return redirect(url_for('api.index'))
    else:
        return not_found()

@api_bp.route("/todos/<int:id>/edit", methods=['POST'])
def edit(id):
    todo = Todo.query.get(id)

    if todo is None:
        return not_found()

    if not request.is_json:
        return not_supported_request()

    if request.method == 'POST':
        todo.title = request.json['title']
        todo.description = request.json['description']
        todo.due_to = datetime.strptime(request.json['due_to'], '%Y-%m-%d')
        db.session.commit()
        return redirect(url_for("api.show", id=id))

def not_found():
    return jsonify({'messsage': 'id not found'}), 400

def not_supported_request():
    return jsonify({'messsage': 'request mst be json'}), 400


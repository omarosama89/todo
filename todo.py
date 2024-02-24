from flask import render_template, request, url_for, redirect
from app import app, db
from flask_bootstrap import Bootstrap4
from forms.add_from import AddForm
from db import Todo
from datetime import datetime

bootstrap = Bootstrap4(app)

@app.route("/")
def root():
    return redirect(url_for("index"))

@app.route("/todos")
def index():
    # ipdb.set_trace()
    todos = Todo.query.all()
    return render_template("index.html", todos=todos)

@app.route("/todos/create", methods=['GET', 'POST'])
def create():
    form = AddForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            todo = Todo(
                title=request.form['title'],
                description=request.form['description'],
                due_to=datetime.strptime(request.form['due_to'], '%Y-%m-%d')
            )
            db.session.add(todo)
            db.session.commit()
            return redirect(url_for('index'))
    return render_template('create.html', form=form)

@app.route("/todos/<int:id>/done", methods=['POST'])
def done(id):
    todo = Todo.query.get(id)
    todo.status = 'done'
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/todos/<int:id>/cancel", methods=['POST'])
def cancel(id):
    todo = Todo.query.get(id)
    todo.status = 'canceled'
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/todos/<int:id>/delete", methods=['POST'])
def delete(id):
    todo = Todo.query.get(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/todos/<int:id>/edit", methods=['GET', 'POST'])
def edit(id):
    form = AddForm()
    todo = Todo.query.get(id)
    if request.method == 'POST':
        if form.validate_on_submit():
            todo = Todo.query.get(id)
            todo.title = request.form['title']
            todo.description = request.form['description']
            todo.due_to = datetime.strptime(request.form['due_to'], '%Y-%m-%d')
            db.session.commit()
            return redirect(url_for("index"))
    return render_template('edit.html', todo=todo, form=form)

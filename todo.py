from flask import render_template, request, url_for, redirect
from app import app
from flask_bootstrap import Bootstrap4
from db import get_db

bootstrap = Bootstrap4(app)

@app.route("/")
def root():
    return redirect(url_for("index"))

@app.route("/todos")
def index():
    db = get_db()
    todos = db.execute('SELECT * FROM todos').fetchall()
    db.close()
    return render_template("index.html", todos=todos)

@app.route("/todos/create", methods=['GET', 'POST'])
def create():
    todo = (
        request.form['title'],
        request.form['description'],
        request.form['due_to']
            )
    db = get_db()
    cur = db.cursor()
    cur.execute("INSERT INTO todos (title, description, due_to) VALUES (?, ?, ?)",
                (
                    todo
                )
                )
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route("/todos/<int:id>/done", methods=['POST'])
def done(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE todos SET status = 'done' WHERE id=" + str(id))
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route("/todos/<int:id>/cancel", methods=['POST'])
def cancel(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("UPDATE todos SET status = 'canceled' WHERE id=" + str(id))
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route("/todos/<int:id>/delete", methods=['POST'])
def delete(id):
    db = get_db()
    cur = db.cursor()
    cur.execute("DELETE FROM todos WHERE id=" + str(id))
    db.commit()
    db.close()
    return redirect(url_for('index'))

@app.route("/todos/<int:id>/edit", methods=['GET', 'POST'])
def edit(id):
    db = get_db()
    if request.method == 'GET':
        todo = db.execute('SELECT * FROM todos where id =' + str(id)).fetchall()[0]
        db.close()
        return render_template('edit.html', todo=todo)
    else:
        cur = db.cursor()
        todo = (
            request.form['title'],
            request.form['description'],
            request.form['due_to']
        )
        cur.execute(
            "UPDATE todos SET title = ?, description = ?, due_to = ? WHERE id=" + str(id),
            todo
        )
        db.commit()
        db.close()
        return redirect(url_for("index"))

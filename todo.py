from flask import render_template, request, url_for, redirect, make_response, flash
from app import app, db
from flask_bootstrap import Bootstrap4
from forms.add_from import AddForm
from models.todo import Todo
from datetime import datetime
import csv
import io

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

@app.route("/todos/download")
def download():
    todos = Todo.query.all()

    if len(todos) == 0:
        flash('No data to download')
        return render_template("index.html", todos=todos)

    csv_data = io.StringIO()
    csv_writer = csv.writer(csv_data)
    csv_writer.writerow(Todo.__table__.columns.keys())  # Write headers
    for row in todos:
        csv_writer.writerow([getattr(row, column.name) for column in Todo.__table__.columns])

    response = make_response(csv_data.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=todos.csv'
    response.headers['Content-type'] = 'text/csv'

    return response

@app.route("/todos/upload", methods=["POST"])
def upload():
    todos = Todo.query.all()
    file = request.files['file']

    if file.filename == '':
        flash('No file provided')
        return render_template("index.html", todos=todos)

    if file.filename.rsplit('.', 1)[1].lower() != 'csv':
        flash('You need to provide a csv file')
        return render_template("index.html", todos=todos)

    csv_data = io.StringIO(file.stream.read().decode('UTF8'), newline=None)
    csv_reader = csv.reader(csv_data)
    csv_rows = list(csv_reader)

    header = csv_rows[0][1:]    # ignore 'id'
    data = csv_rows[1:]

    if len(header) != len(Todo.__table__.columns[1:]):
        flash('The file provided should have these keys: ' + str(Todo.__table__.columns[1:].keys()))
        return render_template("index.html", todos=todos)

    for row in data:
        row_with_id = row[1:]   # ignore 'id'
        record_data = {header[i]: row_with_id[i] for i in range(len(header)) if header[i] != 'id'}
        record = Todo(**dict(prepare_row(record_data)))
        db.session.add(record)

    db.session.commit()

    return redirect(url_for("index"))

def prepare_row(row):
    row['due_to'] = datetime.strptime(row['due_to'], '%Y-%m-%d')
    return row

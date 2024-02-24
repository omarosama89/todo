from app import db

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String,  nullable=False)
    description = db.Column(db.String)
    due_to = db.Column(db.Date)
    status = db.Column(db.String, default='pending')

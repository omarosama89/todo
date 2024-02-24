from app import app, db
from models.todo import Todo

def init_db():
    with app.app_context():
        db.create_all()
        db.session.commit()

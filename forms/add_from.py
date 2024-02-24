from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError
from datetime import date

class AddForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    description = TextAreaField('Description')
    due_to = DateField('Due to', validators=[DataRequired()])

    def validate_due_to(self, field):
        if field.data < date.today():
            raise ValidationError('Date cannot be in the past.')

    submit = SubmitField('Submit')
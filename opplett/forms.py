from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, HiddenField
from wtforms.validators import DataRequired


class UserNameForm(FlaskForm):
    """
    Form to create new username when user first signs in.
    """
    username = StringField(
        'Username:',
        validators=[DataRequired(message='Required.')]
    )


class NewDirectoryForm(FlaskForm):
    """
    Form to make new directory
    """
    dir_name = StringField(
        'New Directory Name:',
        validators=[DataRequired(message='This is required.')]
    )
    username = HiddenField(label='username')
    current_dir = HiddenField(label='current_dir')


class RemoveDirectoryForm(FlaskForm):
    """
    Form to remove current directory and all it's contents
    """
    dir_name = StringField(
        "Please confirm by typing this directory's name:",
        validators=[DataRequired(message='This is required.')]
    )


class PaymentForm(FlaskForm):
    """
    Form to submit a payment.
    """
    payment_amount = SelectField(
        'Increase your account balance:',
        choices=[(0, 'Select Amount'),
                 (5, '$5'), (10, '$10'), (50, '$50'), (100, '$100'), (200, '$200')
                 ],
        coerce=int,
        validators=[DataRequired()]
    )

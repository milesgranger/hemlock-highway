from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from wtforms.validators import DataRequired


class UserNameForm(FlaskForm):
    """
    Form to create new username when user first signs in.
    """
    username = StringField(
        'Username:',
        validators=[DataRequired(message='Required.')]
    )


class PaymentForm(FlaskForm):
    """
    Form to submit a payment.
    """
    payment_amount = SelectField(
        'Payment Amount:',
        choices=[(0, 'Select Amount'),
                 (5, '$5'), (10, '$10'), (50, '$50'), (100, '$100'), (200, '$200')
                 ],
        coerce=int,
        validators=[DataRequired()]
    )

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired, IPAddress

class SubnetForm(FlaskForm):
    name = StringField('Subnet Name', validators=[DataRequired()])
    cidr = StringField('CIDR', validators=[DataRequired()])
    description = TextAreaField('Description')
    parent_id = SelectField('Parent Subnet', coerce=int)
    submit = SubmitField('Add Subnet')

class IPAddressForm(FlaskForm):
    ip_address = StringField('IP Address', validators=[DataRequired(), IPAddress()])
    description = TextAreaField('Description')
    subnet_id = SelectField('Subnet', coerce=int)
    submit = SubmitField('Add IP Address')

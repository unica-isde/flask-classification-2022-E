from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms import *

from wtforms.validators import DataRequired

from app.utils.list_images import list_images
from config import Configuration

conf = Configuration()


class TransformationForm(FlaskForm):
    image = SelectField('image', choices=list_images(), validators=[DataRequired()])
    submit = SubmitField('Submit')
    brightness = IntegerRangeField(id ='brightness',default=0)
    sharpness  = IntegerRangeField(id ='sharpness',default=0)
    contrast   = IntegerRangeField(id ='contrast',default=0)
    color      = IntegerRangeField(id ='color',default=0)

import redis
from flask import *
from rq import Connection, Queue
from rq.job import Job


from app import app
from app.forms.transformation_form import TransformationForm

from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()

from PIL import ImageEnhance
from PIL import Image

import base64
from io import BytesIO



def SharpnessSet(image, value):
    factor = value
    enhancer = ImageEnhance.Sharpness(image)
    return enhancer.enhance(factor)


def ContrastSet(image,value):
    factor = value
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def BrightnessSet(image,value):
    factor = value
    enhancer = ImageEnhance.Brightness(image)
    return enhancer.enhance(factor)

def ColorSet(image,value):
    factor = value
    enhancer = ImageEnhance.Color(image)
    return enhancer.enhance(factor)

def ModifyIMage(filename,br,contr,sha,col):

    im = Image.open(filename)
    out = BrightnessSet(im,br)
    out = ContrastSet(out,contr)
    out = SharpnessSet(out,sha)
    out = ColorSet(out,col)
    
    buffered = BytesIO()
    out.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue())
    return img_str
    



@app.route('/transformations', methods=['GET', 'POST'])
def transformations():
    form = TransformationForm()

    if request.method == 'POST':
        image_id = form.image.data
        image_br = form.brightness.data
        image_contr = form.contrast.data
        image_sha = form.sharpness.data
        image_color = form.color.data
        
        return ModifyIMage("app/static/imagenet_subset/"+str(image_id),image_br,image_contr,image_sha,image_color)

    return render_template('transformations_select.html', form=form)
    
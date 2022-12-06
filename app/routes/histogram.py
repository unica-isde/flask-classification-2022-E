import redis
from flask import *
from rq import Connection, Queue
from rq.job import Job


import numpy as np
import matplotlib.pyplot as plt
import cv2

from app import app
from app.forms.classification_form import ClassificationForm

from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()

from PIL import ImageEnhance
from PIL import Image

import base64

import io

def makeImage(image_id):
    im = cv2.imread("app/static/imagenet_subset/"+str(image_id))
    vals = im.mean(axis=2).flatten()
    counts, bins = np.histogram(vals, range(257))
    plt.bar(bins[:-1] - 0.5, counts, width=1, edgecolor='none')
    plt.xlim([-0.5, 255.5])

    my_stringIObytes = io.BytesIO()
    plt.savefig(my_stringIObytes, format='jpg')
    my_stringIObytes.seek(0)
    return base64.b64encode(my_stringIObytes.read()).decode("utf-8")



@app.route('/histogram', methods=['GET', 'POST'])
def histogram():
    form = ClassificationForm()
    
    if request.method == 'POST':
        image_id_ = form.image.data
        base64str= makeImage(image_id_)
        return render_template('histogram_img_select_output.html',form=form, image_id=image_id_, base64img=base64str)

    return render_template('histogram_img_select.html', form=form)
    
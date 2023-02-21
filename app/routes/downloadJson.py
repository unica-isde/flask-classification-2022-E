import numpy as np
import matplotlib.pyplot as plt
import os

import json

import redis
from flask import render_template,Flask, flash, request, redirect, url_for,helpers
from flask import *
from rq import Connection, Queue
from rq.job import Job


from .classifications_id import *


from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

config = Configuration()

SAVEPRIV = 'app/static/plots'



app.config['SAVEPRIV'] = SAVEPRIV



@app.route("/downloadJson",methods=['GET', 'POST'])
def downloadJson():
    if request.method == 'POST':
        jobId = request.form.get('jobid')
        jsonFIle_raw = classifications_id(jobId)



        return Response(json.dumps(jsonFIle_raw["data"], indent=4),
                        mimetype="text/json",
                        headers={"Content-disposition":
                        "attachment; filename={}.json".format(jobId)})
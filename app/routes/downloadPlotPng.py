import numpy as np
import matplotlib.pyplot as plt
import os

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



@app.route("/downloadPlotPng",methods=['GET', 'POST'])
def downloadPlotPng():
    if request.method == 'POST':
        jobId = request.form.get('jobid')
        jsonFIle = classifications_id(jobId)

        data = jsonFIle["data"]

        names =[]
        values = []

        for i in data:
            a = i[0]
            b = i[1]
            names.append(a)
            values.append(b)


        fig = plt.figure(figsize = (10, 5))
        plt.bar(names, values, color=['blue', 'red', 'green', 'black', 'cyan'],
                width = 0.4)
        
        plt.xlabel("Classes")
        plt.ylabel("Percentage")
        plt.title("Results")

        filename = str(jobId)+".png"

        plt.savefig(os.path.join(app.config['SAVEPRIV'],filename ))

        

        stripped = os.path.relpath(app.config['SAVEPRIV'], "app/")

        print("{}".format(stripped))
        
        return send_from_directory(stripped, filename,as_attachment=True)
        
        

    
    elif request.method == 'GET':
        return '''
        <html><body>
        <h1> omage </h1>
        </body></html>
        '''
import redis
from flask import render_template,Flask, flash, request, redirect, url_for
from rq import Connection, Queue
from rq.job import Job


from app import app
from app.forms.classification_form import ClassificationForm
from ml.classification_utils import classify_image
from config import Configuration

import os
from werkzeug.utils import secure_filename


DEBUG = 1

config = Configuration()

UPLOAD_FOLDER = 'app/static/imagenet_subset_uploaded'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


#new part 21/11/22
@app.route('/classifications2', methods=['GET', 'POST'])
def classifications_by_uploading():
    absolute_path = ""
    form = ClassificationForm()
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            absolute_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            print("apth : {}".format(absolute_path))
            file.save(absolute_path)

        if (DEBUG == 1):
            print("[*] IMAGENAME {}".format(filename))
        # new part 23/11/22
        redis_url = Configuration.REDIS_URL
        redis_conn = redis.from_url(redis_url)

        with Connection(redis_conn):
            q = Queue(name=Configuration.QUEUE)
            job = Job.create(classify_image, kwargs={
                "model_id": form.model.data,
                "img_id": absolute_path,
                "uploaded":True
            })
            task = q.enqueue_job(job)

        print("JOb id {}".format(task.get_id()))
        return render_template("classification_output_queue.html",selector=0, image_id=filename,jobID=task.get_id())


    #delete image in the file system
    listFIle = os.listdir("app/static/imagenet_subset_uploaded")
    if(len(listFIle) > 0):
        for f in listFIle:
            os.remove("app/static/imagenet_subset_uploaded/"+f)
        

    return render_template('classification_select_by_uploading.html',form=form)

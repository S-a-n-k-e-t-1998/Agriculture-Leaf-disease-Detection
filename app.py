from flask import Flask,render_template,redirect,request,session
from werkzeug.utils import secure_filename
from gevent.pywsgi import WSGIServer
import boto3
from PIL import Image
import os
import keras
from keras.preprocessing import image  
from tensorflow import keras
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from function import counter,Predict,uploadFile,Predict_paper
import yaml


# find current working dir
cwd=basepath = os.path.dirname(__file__)
print("Current working Dir ::",cwd)


# params=yaml.load(open(r'{0}/config.yml'.format(cwd)),Loader=yaml.FullLoader)
# print(params)
# diseble the gpu setup



# WSGI Application
# Defining upload folder path
UPLOAD_FOLDER = os.path.join('F:\Toolkit\Backup\SANKET_2\E\Deep Learning CNN\Agri\application\static\staticFiles', 'uploads')
# # Define allowed files
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

potato_model_path="models\potato_model.h5"
paper_model_path="models\Pepper_bell_model.h5"
#load the model
potato_model=keras.models.load_model(r"{0}\{1}".format(cwd,potato_model_path))
paper_model=keras.models.load_model(r"{0}\{1}".format(cwd,paper_model_path))

potato_class_names = ['Early_blight', 'Late_blight', 'healthy']

paper_class_names = ['Bacterial Spot', 'healthy']


# create app
app=Flask(__name__,static_url_path='/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
main_path=app.config['UPLOAD_FOLDER']
# Define secret key to enable session
app.secret_key = 'This is your secret key to utilize session in Flask'


#Home
@app.route('/',methods=["GET","POST"])
def home():
    return render_template("index.html",result1=counter()-1)


# Home Page of Potato
@app.route('/potato_home',  methods=("POST", "GET"))
def potato_disease():
    return render_template('potato2.html')
 
# Potato Prediction
@app.route('/potato_pred1',methods=['POST',"GET"])
def potato_prediction():
        if request.method == 'POST':
            a=uploadFile(main_path)
            if a:
                # Retrieving uploaded file path from session
                img_file_path = session.get('uploaded_img_file_path', None)
                im=plt.imread(img_file_path)
                pred,conf=Predict(potato_model,im)
                print(pred,conf)
                if pred=='healthy':
                    result=f"As per the potato leaf uploaded this is healthy with Confidence {conf} %"
                    return render_template('potato2.html',result=result)
                else:
                    result=f"As per the potato leaf uploaded this is suffering {pred} disease with Confidence {conf} %"
                    return render_template('potato2.html', result=result)
            else:
                return redirect('/potato_home')



## Pepper bell
@app.route('/pepper_home',  methods=("POST", "GET"))
def pepper_disease():
        return render_template('papper.html')
     
# pepper leaf prediction   
@app.route('/pepper_leaf1',  methods=("POST", "GET"))
def upload_pepper_file():
    if request.method == 'POST':
            a=uploadFile(main_path)
            if a:
                # Retrieving uploaded file path from session
                img_file_path = session.get('uploaded_img_file_path', None)
                im=plt.imread(img_file_path)
                pred,conf=Predict_paper(paper_model,im)
                print(pred,conf)
                if pred=='healthy':
                    result=f"As per the Pepper Bell leaf uploaded this is healthy with Confidence {conf} %"
                    return render_template('papper.html',result=result)
                else:
                    result=f"As per the Pepper Bell leaf uploaded this is suffering {pred} disease with Confidence {conf} %"
                    return render_template('papper.html', result=result)
            else:
                return redirect('/pepper_home')


if __name__=="__main__":
    app.run(debug=True)



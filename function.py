import numpy as np
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


potato_class_names=['Early_blight', 'Late_blight', 'healthy']

paper_class_names = ['Bacterial Spot', 'healthy']

# user vistited to website
count_of_user=[]
def counter():
    count_of_user.append(1)
    return np.sum(count_of_user)

#predict fuction to predict the result
def Predict(model,img):
    img_array=keras.preprocessing.image.img_to_array(img)
    img_array=tf.expand_dims(img_array,0)
    predictions = model.predict(img_array)
    predicted_class = potato_class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class,confidence


def Predict_paper(model,img):
    img_array=keras.preprocessing.image.img_to_array(img)
    img_array=tf.expand_dims(img_array,0)
    predictions = model.predict(img_array)
    # print(predictions)
    predicted_class = paper_class_names[np.argmax(predictions[0])]
    confidence = round(100 * (np.max(predictions[0])), 2)
    return predicted_class,confidence


def uploadFile(main_path):
        # Upload file flask
        uploaded_img = request.files['uploaded-file']
        img_filename="potato.jpg"
        path=os.path.join(main_path, img_filename)
        uploaded_img.save(path)
        # Storing uploaded file path in flask session
        session['uploaded_img_file_path'] = path
        return uploaded_img
    
    
    
    



# upload the potato leaf
# @app.route('/upload_potato_leaf',  methods=("POST", "GET"))
# def upload_potato_file():
#     if request.method == 'POST':
#         uploadFile()
#         return render_template('potato.html')
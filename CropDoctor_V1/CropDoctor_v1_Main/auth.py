'''
    IMPORTING
'''
from flask import Blueprint , render_template , url_for , redirect , request ,session 
from .db import collection
from werkzeug.utils import secure_filename
from flask import current_app
import wikipedia



auth=Blueprint("auth",__name__)

'''
    LOGIN IN BASE.HTML REDIRECTS TO LOGIN.HTML
'''
@auth.route('/login' , methods=['GET','POST'])
def login():
    return render_template("Login.html")


'''
    THE URL WILL REDIRECT HERE FROM APP.PY
'''
@auth.route('/' , methods=['GET','POST'])
def func():
    return render_template("Base.html")
    
'''
    REGISTER IN BASE.HTML REDIRECTS TO REGISTER.HTML
'''

@auth.route("/register" , methods=['GET','POST'])
def register():
    if request.method == "POST":
        name=request.form.get("name")
        emailid=request.form.get("email")

        # finding the given email id , checking if it already exits
        p1 = collection.find_one({"email": emailid})

        # if it is not null then the email is already registered
        if(p1!=None):
            message = 'Credentials already Exists'
            return render_template('register.html', message=message)

        #setting and confirming password
        password1=request.form.get("password")
        password2=request.form.get("cpassword")

        #checking if entered password and confirmed password are same
        if password1 != password2:
                message = 'Passwords should match!'
                return render_template('register.html', message=message)
        else:
 
            user_input = {'Name': name, 'email': emailid ,'Password':password1}
            #inserting it into mongodb database if all constraints satisfy
            collection.insert_one(user_input)
           
    return render_template("Register.html")


"""
    LOGIN.HTML WILL REDIRECT HERE , THE ENTERED DETAILS IN FORM WILL SHOW UP HERE !!!
"""
@auth.route('/verifylogin',methods=['POST'])
def logged_in():
    if request.method == "POST":
        EmailId = request.form.get("email")
        Password = request.form.get("password")
        p1 = collection.find_one({"email": EmailId})

        '''
            IF THE EMAIL IS NOT MATCHED WITH THAT OF DATABASE ,IT WILL THROW ERRROR
        '''
        if(p1==None):
            error = 'Invalid Credentials. Please try again.'
            return render_template('Login.html', error=error)

        '''
            IF PASSWORDS MATCH WITH THAT IN DATABASE IT WILL REDIRECT TO HOME.HTML 
        '''
        if Password==p1["Password"]:
            p2=collection.find_one({"email": EmailId},{'_id':0,'email':0,'Password':0})
            return render_template('Home.html',tasks=p2)



'''
    FORGOT PASSWORD AND RE-REGISTER
'''
@auth.route('/forgot',methods=['GET','POST'])
def forgot():           
        return render_template('ForgotPassword.html')

      

@auth.route("/rereg" , methods=['GET','POST'])
def rereg():
    if request.method == "POST":
        
        emailid=request.form.get("email")
        password1=request.form.get("password")
        password2=request.form.get("cpassword")
        if password1 != password2:
                message = 'Passwords should match!'
                return render_template('register.html', message=message)
        else:
            user_input = {'email': emailid ,'Password':password1}
            print(user_input)
            collection.update_one({"email": request.form.get("email")} , {"$set": {"Password":request.form.get("password")}})
            
    return render_template("rereg.html")
  

from keras.preprocessing.image import ImageDataGenerator
import tensorflow as tf
import numpy as np
import os 
from keras.applications.imagenet_utils import preprocess_input, decode_predictions
from keras.models import load_model
from keras.preprocessing import image
  
model = tf.keras.models.load_model('G:/ps_part1/CropDoctor_V1/CropDoctor_v1_Main/rescolab1.h5')
import numpy as np
import matplotlib.pyplot as plt
from keras.preprocessing import image
import tensorflow
import numpy as np 
    

def prepare(img_path):
    img = tensorflow.keras.utils.load_img(img_path, target_size=(224,224))
    x = tensorflow.keras.utils.img_to_array(img)
    return np.expand_dims(x, axis=0)

def finds(image_path):
    classes= ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 
    'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 
    'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 
    'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 
    'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 
    'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 
    'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 
    'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy',
     'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 
     'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 
     'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 
     'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
    img_width=224
    img_height=224
    model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])
    result = model.predict([prepare(image_path)])
    
    disease=tensorflow.keras.utils.load_img(image_path)

    plt.imshow(disease)

    
    classresult=np.argmax(result,axis=1)
    return classes[classresult[0]] 


@auth.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'static', secure_filename(f.filename))
        f.save(file_path)
        print(file_path)
        print(f.filename)
        result=finds(file_path)    
        ans=""
        if "healthy" in result:
            ans="Your Crop is Healthy"
            return render_template("Detect.html",task1=f.filename,tasks=result,ans=ans)
        else:
            ans=wikipedia.summary(result,sentences=5)
            nothing= wikipedia.page(result).url
            return render_template("Detect.html",task1=f.filename,tasks=result,ans=ans,nothing=nothing)   
   
    else:
        return render_template("Detect.html")



@auth.route("/logout")
def logout():
    return redirect(url_for("auth.func")) 



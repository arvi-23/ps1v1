from flask import Blueprint , render_template , url_for , redirect , request 
from .db import collection
from werkzeug.utils import secure_filename
auth=Blueprint("auth",__name__)

@auth.route('/login' , methods=['GET','POST'])
def login():
    emailid=request.form.get("email")
    password1=request.form.get("password")
    return render_template("Login.html")

@auth.route('/' , methods=['GET','POST'])
def func():
    return render_template("Base.html")
    

# @auth.route('/login', methods=['GET', 'POST'])
# def login():
#     error = None
#     if request.method == 'POST':
#         if request.form['email'] != 'admin' or request.form['password'] != 'admin':
#             error = 'Invalid Credentials. Please try again.'
#         else:
#             return redirect(url_for('home'))
#     return render_template('login.html', error=error)


@auth.route("/register" , methods=['GET','POST'])
def register():
    if request.method == "POST":
        name=request.form.get("name")
        emailid=request.form.get("email")

        p1 = collection.find_one({"email": emailid})
        if(p1!=None):
            message = 'Credentials already Exists'
            return render_template('register.html', message=message)

        password1=request.form.get("password")
        password2=request.form.get("cpassword")
        if password1 != password2:
                message = 'Passwords should match!'
                return render_template('register.html', message=message)
        else:
            # hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            user_input = {'Name': name, 'email': emailid ,'Password':password1}
            print(user_input)
            collection.insert_one(user_input)
            # return render_template('VerifyMobile.html')
    return render_template("Register.html")

@auth.route('/verifylogin',methods=['POST'])
def logged_in():
    if request.method == "POST":
        EmailId = request.form.get("email")
        Password = request.form.get("password")
        p1 = collection.find_one({"email": EmailId})
        if(p1==None):
            # return redirect(url_for("auth.login"))
            error = 'Invalid Credentials. Please try again.'
            return render_template('Login.html', error=error)

        if Password==p1["Password"]:
            p2=collection.find_one({"email": EmailId},{'_id':0,'email':0,'Password':0})
            print(p2)
            return render_template('Home.html',tasks=p2)

@auth.route('/forgot',methods=['GET','POST'])
def forgot():           
        return render_template('ForgotPassword.html')

# @auth.route("/rereg")
# def rereg():
#     return render_template("rereg.html")        

@auth.route("/rereg" , methods=['GET','POST'])
def rereg():
    if request.method == "POST":
        # name=request.form.get("name")
        emailid=request.form.get("email")

        # p1 = collection.find_one({"email": emailid})
        # if(p1!=None):
        #     message = 'Credentials already Exists'
        #     return render_template('register.html', message=message)

        password1=request.form.get("password")
        password2=request.form.get("cpassword")
        if password1 != password2:
                message = 'Passwords should match!'
                return render_template('register.html', message=message)
        else:
            # hashed = bcrypt.hashpw(password1.encode('utf-8'), bcrypt.gensalt())
            user_input = {'email': emailid ,'Password':password1}
            print(user_input)
            # collection.insert_one(user_input)
            collection.update_one({"email": request.form.get("email")} , {"$set": {"Password":request.form.get("password")}})
            # return render_template('VerifyMobile.html')
    return render_template("rereg.html")

@auth.route('/')  
def upload():  
    return render_template("Detect.html")  
 
@auth.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        return render_template("success.html", name = f.filename)  
  


@auth.route("/logout")
def logout():
    return redirect(url_for("auth.func")) 

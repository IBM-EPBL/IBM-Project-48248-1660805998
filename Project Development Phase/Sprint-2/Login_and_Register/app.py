from flask import Flask, render_template, request, flash, redirect, url_for, session
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key="123"

client = MongoClient("mongodb+srv://Sujitha:Sujitha%4002@cluster0.wjez6.mongodb.net/JupiterDB?retryWrites=true&w=majority")
dbname = client['JupiterDB']
collection_name = dbname["userDB"]

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/logged_in')
def logged_in():
    print("line no: 20", email)
    return render_template('indexnew.html', email=email, name=name)
   

@app.route('/Login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        global email
        global name
        email = request.form.get("email")
        psw = request.form.get("psw")
        email_found = collection_name.find_one({"email": email})
        if email_found:
            password = email_found['psw']
            if(password == psw):
                name = email_found["name"]
                return redirect(url_for('logged_in'))
                # return logged_in(email_found["email"], email_found["name"])
            else:
                return render_template('Login.html', message="Password mismatch")
        else:
            return render_template('Login.html', message="Not have an account! Register to continue")
    else:
        return render_template('Login.html', message="")

@app.route('/Register', methods=["POST", "GET"])
def register():
    if request.method == "POST":
        global email
        global name
        global psw
        email = request.form.get("email")
        psw = request.form.get("psw")
        name = request.form.get("name")
        email_found = collection_name.find_one({"email": email})
        if email_found:
            return render_template('Register.html', message="Already have an account! Login to continue")
        else:
            collection_name.insert_one({"email": email, "name": name, "psw": psw})
            return redirect(url_for('logged_in'))          
    else:
        return render_template('Register.html', message="")
 

if __name__ == '__main__':
    app.run(debug=True)
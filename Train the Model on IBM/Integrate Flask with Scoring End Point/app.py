from flask import Flask, render_template, request, flash, redirect, url_for, session
from pymongo import MongoClient
import numpy as np
import pandas as pd 
import pickle

model = pickle.load(open('CKD.pkl', 'rb'))

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
   

@app.route('/predict', methods=["POST", "GET"])
def predict():
    blood_urea = float(request.form.get("blood_urea"))
    blood_glucose_random = float(request.form.get("blood_glucose_random"))

    if(request.form.get("anemia") == 'yes'):
        anemia = 1
    else:
        anemia = 0
    
    if(request.form.get("coronary_artery_disease") == 'yes'):
        coronary_artery_disease = 1
    else:
        coronary_artery_disease = 0
    
    if(request.form.get("pus_cell") == 'yes'):
        pus_cell = 1
    else:
        pus_cell = 0

    if(request.form.get("red_blood_cells") == 'yes'):
        red_blood_cells = 1
    else:
        red_blood_cells = 0
    
    if(request.form.get("diabetesmellitus") == 'yes'):
        diabetesmellitus = 1
    else:
        diabetesmellitus = 0

    if(request.form.get("pedal_edema") == 'yes'):
        pedal_edema = 1
    else:
        pedal_edema = 0

    input_features = [blood_urea, blood_glucose_random, anemia, coronary_artery_disease, pus_cell, red_blood_cells, diabetesmellitus, pedal_edema]
    features_value = [np.array(input_features)]
    features_name = ['blood_urea', 'blood_glucose_random', 'anemia', 'coronary_artery_disease', 'pus_cell', 'red_blood_cells', 'diabetesmellitus', 'pedal_edema']
    df = pd.DataFrame(features_value, columns = features_name)
    output = model.predict(df)
    print("line no: 41", output)
    return render_template('result.html', predicted_text=output)

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
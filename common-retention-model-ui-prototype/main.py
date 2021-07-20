import json, datetime
import csv
import pandas as pd                        

from flask import Flask, render_template, request, jsonify
from flask import Blueprint, render_template, redirect, url_for, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app) # This will enable CORS for all routes

app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'

@app.route("/", methods=['GET'])
def home():
    csv_data = pd.read_csv('input.csv')
    return render_template("index.html", csv_data=csv_data)

@app.route("/dashboard", methods=['GET'])
def dashboard():
    follow_up_data = pd.read_csv('follow_up.csv').to_json()
    return render_template("employee-dashboard.html", follow_up_data=json.loads(follow_up_data))


@app.route("/employees", methods=['GET'])
def employees():
    csv_data = pd.read_csv('input.csv')
    employees_data = csv_data[['driver_id', 'first_name', 'last_name', 'quit_score']].to_json()
    return render_template("employees.html", employees_data=json.loads(employees_data))

@app.route("/profile/<string:driver_id>", methods=['GET'])
def profile(driver_id):
    csv_data = pd.read_csv('input.csv')
    csv_data = csv_data[csv_data['driver_id'] == driver_id ]
    profile_dict = csv_data.to_dict()
    row_num = list(profile_dict['driver_id'].keys())[0]
    print(profile_dict)
    return render_template("profile.html", row_num=row_num, profile_dict=profile_dict)

@app.route("/follow_up", methods=['POST'])
@cross_origin(origin='*')
def follow_up():
    request_data = json.loads(request.data)
    f_up = request_data['f_up']
    f_name = request_data['f_name']
    f_time = request_data['f_time']
    message = request_data['message']
    row = [f_up, f_name, f_time, message]

    with open(r'follow_up.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)

    return jsonify(message="Row has been added.", status=200)

@app.route("/call_details", methods=['POST'])
@cross_origin(origin='*')
def call_details():
    print(request.data)
    request_data = json.loads(request.data)
    c_date = request_data['c_date']
    c_mode = request_data['c_mode']
    c_message = request_data['c_message']
    progress = request_data['progress']
    row = [c_date, c_mode, c_message, progress]

    with open(r'call_details.csv', 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)
    
    return jsonify(message="Row has been added.", status=200)

if __name__ == "__main__":
    app.run(host='0.0.0.0')


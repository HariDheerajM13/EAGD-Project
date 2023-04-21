import geopy
from pandas.io.json import json_normalize
import folium
from geopy.geocoders import Nominatim 
import requests

import subprocess
from project import execute
from restaurant import restaurant
from school import schools
from atm import atms
from flask import Flask , render_template, url_for, redirect , request

app=Flask(__name__)
    
@app.route('/')
def form():
    return render_template("index.html")

@app.route('/formoutput', methods=["POST"])
def map():
    loc = request.form.get("location")
    pef1=request.form.get("preference1")
    pef2=request.form.get("preference2")
    pef3=request.form.get("preference3")
    city=loc
    value=execute(city,pef1,pef2,pef3)
    #subprocess.run(["python", "practice.py", city, pef1,pef2,pef3, latpoint, longpoint])
    return render_template("home1.html", val=city,val1=pef1,val2=pef2,val3=pef3,apartvalue=value.to_html())


@app.route("/restaurant")
def rest():
    return render_template("Restform.html")

@app.route("/restaurantsoutput", methods=["POST"])
def restout():
    loc1 = request.form.get("Restlocation")
    restvalue = restaurant(loc1)
    return render_template("restaurants.html", city=loc1)

@app.route("/schools")
def schl():
    return render_template("schlform.html")

@app.route("/schoolsoutput", methods=["POST"])
def schlout():
    loc1 = request.form.get("schllocation")
    restvalue = schools(loc1)
    return render_template("schools.html", city=loc1)

@app.route("/atms")
def atm():
    return render_template("atmform.html")

@app.route("/atmsoutput", methods=["POST"])
def atmout():
    loc1 = request.form.get("atmlocation")
    restvalue = atms(loc1)
    return render_template("atms.html", city=loc1)

if __name__=="__main__":    
    app.run(debug=True) 
import os
import requests
import urllib.request
import time

from twilio.rest import Client
from flask import Flask, render_template, request, jsonify, url_for, redirect
from twilio.twiml.messaging_response import MessagingResponse
from flask_jsglue import JSGlue
from twilio import twiml
from random import randint
from bs4 import BeautifulSoup

# Checks if running on Heroku or locally
local = False
if os.path.exists('local.txt'):
    from config import *
    local = True

# For Flask app
app = Flask(__name__)

# For Twilio authentication
if local == True:
    client = Client(accountsid, authtoken)
else:
    client = Client(os.environ['ACCOUNTSID'], os.environ['AUTHTOKEN'])


""" FUNCTIONS """
def sendMessage(message, number):
    # Twilio message
    message = client.messages \
        .create(
            body=message,
            from_='+14096843164',
            to=number
        )

    print(message.sid)

def addLocation(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    location = soup.find_all("a", class_="gb_C gb_Ma gb_h")

    # ADD TO DATABASE HERE
    return location


"""FLASK APP"""
# Homepage
@app.route("/")
def index():
    return render_template("index.html")

# Report and get location
@app.route("/report", methods=['GET'])
def report():
    sendMessage("Position notified", '+15622794424')
    return render_template("report.html")

# For new user setup on website (include Auth0)
@app.route("/setup", methods=['GET', 'POST'])
def setup():
    if request.method == "POST":
        profile = request.form
    else:
        return render_template("setup.html")

@app.route("/sms", methods=['GET', 'POST'])
def sms_reply():
    msg = ""
    
    sos = ["sos", "soz", "help", "hel", "emergency"]
    unsafe = ["unsafe", "suspicious", "scared", "uncomfortable"]
    witty = [""]
    google_header = "https://maps.app.goo.gl/"
    
    if request.method == 'POST':
        # If it is a location from google
        if google_header in request.form['Body']:
            msg = "Added your location to your account!"
            addLocation(request.form['Body'])
        elif request.form['Body'].lower() in sos:
            msg = "Contacting Emergency Personnel, notifying close ones, messaging people in your area!"
        elif request.form['Body'].lower() in unsafe:
            msg = "Notifying close ones."
        else:
            msg = "Are you signed up already? Please visit our website: https://universafe.herokuapp.com/"

        # Figure out individual users


        # Replies to User with Confirmation
        sendMessage(msg, request.form['From'])
    else:
        return redirect(url_for('index'))

    return str(resp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)


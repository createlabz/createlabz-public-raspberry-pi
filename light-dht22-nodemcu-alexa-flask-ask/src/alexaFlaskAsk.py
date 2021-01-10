from flask import Flask, render_template
from flask_ask import Ask, statement, question, session
import logging
import requests as httpRequest
import sys

# NodeMCU IP address
nodemcu_ip = sys.argv[1]

app = Flask(__name__)
ask = Ask(app, '/')
# Debugger for error detection
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@app.route('/') # this is the home page route
def hello_world(): # this is the home page function that generates the page code
  return "Hello world!"

@ask.launch # this is the start of the skill function
def start_skill():  # this is the  start of the skill function that generates reply
    return question("What would you like to do")

@ask.intent("LightControlIntent")
def lightControl(state):
    request = None
     # Light is on
    if state == 'on':
        # Http request turning light on to nodemcu
        request = httpRequest.get(nodemcu_ip + "/light/on")
    elif state == 'off':
        # Http request turning light off to nodemcu
        request = httpRequest.get(nodemcu_ip + "/light/off")
    
    # Check request is not empty
    if request:
        # Print to log json data
        print("JSON data: " + str(request.json()))
        # Get reply json data light value
        status = request.json()['Light']
        # Set reply
        reply = 'light has been turned ' + status
        return statement(reply)
    return statement("There's a problem on processing this intent.")

@ask.intent("ReadTempIntent")
def readTemp():
    # Http request turning read temperature to nodemcu
    request = httpRequest.get(nodemcu_ip + "/sensor/dht22/temperature/read/celcius")
    if request:
        # Print to log json data
        print("JSON data: " + str(request.json()))
        # Get reply json data DHT22 value
        status = request.json()['DHT22']
        # Set reply
        reply = 'Room temperature is ' + status
        return statement(reply)
    return statement("There's a problem on processing this intent")

if __name__ == '__main__':
    app.run(debug=True)
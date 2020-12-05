# Needed libraries
from flask import Flask, request as flaskRequest
import requests as httpRequest
import sys
app = Flask(__name__)

# NodeMCU IP address
nodemcu_ip = sys.argv[1]
# nodemcu_ip = "http://10.0.254/"
# Print your inputted IP address
print("NodeMCU IP address is: " + nodemcu_ip)

# this is the home page route
# this is the home page function that generates the page code
@app.route('/') 
def hello_world(): 
    return "Hello world!"

# this is the webhook page route
# this is the webhook page function that generates the page code
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get flask request
    flask_request = flaskRequest.get_json(silent=True, force=True)
    # Get query result
    query_result = flask_request.get('queryResult')
    # Get device name
    device_name = str(query_result.get('parameters').get('device_name'))
    # Get device status
    device_status = str(query_result.get('parameters').get('device_status'))
    # Print device name and status
    print("Device Name:" + device_name + " Status: " + device_status)

    # Device is light
    if device_name == 'light':
        # Light is on
        if device_status == 'on':
            # Http request turning light on to nodemcu
            request = httpRequest.get(nodemcu_ip + "light/on")
        elif device_status == 'off':
            # Http request turning light off to nodemcu
            request = httpRequest.get(nodemcu_ip + "light/off")
        
        # Check request is not empty
        if request:
            # Print to log json data
            print("JSON data: " + request.json())
            # Get reply json data light value
            status = request.json()['Light']
            # Set reply
            reply = 'light has been turned ' + status
    # Device is sensor
    elif device_name == 'sensor':
        # Read sensor
        if device_status == 'read':
            # Http request turning read temperature to nodemcu
            request = httpRequest.get(nodemcu_ip + "sensor/dht22/temperature/read/celcius")
        if request:
            # Print to log json data
            print("JSON data: " + request.json())
            # Get reply json data DHT22 value
            status = request.json()['DHT22']
            # Set reply
            reply = 'Room temperature is ' + status
    
    # Check reply is not empty
    if reply is None:
        # Print to log reply
        print(reply)
        reply = "Something wrong with the device."
    
    # Return value to dialogflow
    return {
            "fulfillmentText": reply,
            "displayText": '25',
            "source": "webhookdata"
        }

# Main function
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080) # This line is required to run Flask on repl.it
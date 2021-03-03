import http.client
import urllib
import time
import board
import adafruit_dht

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4)

API_KEY = "****************"  # Put your API Key here

def getSendData():
    while True:
        # Get DHT22 data
        dhtData = getDHTData() # Get DHT 22 Temperature
        # Check if DHT Data is not empty
        if dhtData is None:
            continue
        # Set temperature
        temperature = dhtData[0]
        # Set humidity
        humidity = dhtData[1]
        # Print DHT Data
        print(temperature, " C", humidity, " %")

        # Check if temperature and humidity reads correctly
        if temperature is not None and humidity is not None:
            # Encode thingspeak parameters
            params = urllib.parse.urlencode({'field1': temperature,'field2': humidity, 'key':API_KEY }) 
            headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            conn = http.client.HTTPConnection("api.thingspeak.com:80")
            try:
                # Send to server
                conn.request("POST", "/update", params, headers)
                response = conn.getresponse()
                print(response.status, response.reason)
                data = response.read()
                conn.close()
            except:
                print("connection failed")
        else:
            print("Error Reading temperature")
        # Continue within 3 Seconds
        time.sleep(3)
        break

# Get DHT22 Temperature data in Celcius
def getDHTData():
    try:
        # Return Temperature
        temperature = dhtDevice.temperature
        humidity = dhtDevice.humidity
        return [temperature,humidity]
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
    except Exception as error:
        dhtDevice.exit()
        raise error
    return None
    
if __name__ == "__main__":
        while True:
                getSendData()
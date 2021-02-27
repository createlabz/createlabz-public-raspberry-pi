import httplib
import urllib
import time

API_KEY = "FOXRCBBBIBLU7TFC"  # Put your API Key here

def getSendData():
    while True:
        #Calculate CPU temperature of Raspberry Pi in Degrees C
        temp = getTemperatureData() # Get Raspberry Pi CPU temp
        params = urllib.urlencode({'field1': temp, 'key':API_KEY }) 
        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
        conn = httplib.HTTPConnection("api.thingspeak.com:80")
        try:
            conn.request("POST", "/update", params, headers)
            response = conn.getresponse()
            print(temp, " C") 
            print(response.status, response.reason)
            data = response.read()
            conn.close()
        except:
            print("connection failed")
        
        time.sleep(3)
        break

def getTemperatureData():
    return int(open('/sys/class/thermal/thermal_zone0/temp').read()) / 1e3
    
if __name__ == "__main__":
        while True:
                getSendData()
from flask import Flask, jsonify, render_template
import requests
from paho.mqtt import client as mqtt_client


server_ip = "http://10.10.10.51:4000"
broker  = "10.10.10.51"
port = 1883

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client("server")
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

app = Flask(__name__)
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/thingspeak/temperature")
def thingspeak_temperature():
    headers = {'Accept': 'application/json'}
    url = "https://thingspeak.com/channels/2340053/field/1.json?results=20"
    r = requests.get(url, headers=headers)
    return r.json()

@app.route("/thingspeak/humidity")
def thingspeak_humidity():
    headers = {'Accept': 'application/json'}
    url = "https://thingspeak.com/channels/2340053/field/2.json?results=20"
    r = requests.get(url, headers=headers)
    return r.json()

@app.route("/nodemcu/last")
def nodemcu():
    headers = {'Accept': 'application/json'}
    r = requests.get(server_ip+'/sensors?_sort=id&_order=desc&_limit=1', headers=headers)
    return r.json()

@app.route("/nodemcu/plot")
def nodemcu_plot():
    headers = {'Accept': 'application/json'}
    r = requests.get(server_ip+'/sensors?_sort=id&_order=desc&_limit=10', headers=headers)
    return r.json()

@app.route("/nodemcu/led/on")
def led_publish():
    client.loop_start()
    result = client.publish("led", "1")
    client.loop_stop()
    return jsonify({"result": result.is_published()})

@app.route("/nodemcu/led/off")
def led_publish_off():
    client.loop_start()
    result = client.publish("led", "0")
    client.loop_stop()
    return jsonify({"result": result.is_published()})

if __name__ == "__main__":
    client = connect_mqtt()
    app.run(host='0.0.0.0', debug=True)
import eventlet
from flask import Flask, render_template
from flask_mqtt import Mqtt
from flask_socketio import SocketIO
from flask_bootstrap import Bootstrap



eventlet.monkey_patch()



app = Flask(__name__)



app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_CLIENT_ID'] = 'mqtt-client'
app.config['MQTT_KEEPALIVE'] = 65535
app.config['MQTT_TLS_ENLABLED'] = False
app.config['MQTT_LAST_WILL_TOPIC'] = 'LastWill'
app.config['MQTT_LAST_WILL_MESSAGE'] = 'Bye!'
app.config['MQTT_LAST_WILL_QOS'] = 0


mqtt = Mqtt(app)
socketio = SocketIO(app)
bootstrap = Bootstrap(app)





mqtt.subscribe('Digester1')

@app.route('/')
def index():
    return render_template('index.html')


@socketio.on('client_connected')
def handle_client_connect(json):
    print("client connected received: {0}".format(str(json)))




@mqtt.on_message()
def handle_mqtt_message(client, userdata, message):
    print('ON MESSAGE________________________________')
    data = dict(
        topic=message.topic,
        payload=message.payload.decode(),
        qos=message.qos
    )
    print(message.payload.decode())
    socketio.emit('getTemp', data=data)


if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=False)

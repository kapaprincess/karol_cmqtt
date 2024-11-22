import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform


#voz

import os

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image

import glob


from gtts import gTTS
from googletrans import Translator



# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1="OFF"

def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

        

broker="broker.mqttdashboard.com"
port=1883
client2= paho.Client("voice")
client2.on_message = on_message

client3= paho.Client("analogmove")
client3.on_message = on_message



st.title("Cosplay Control")

if st.button('Open'):
    act1="close the door"
    client2= paho.Client("voice")                           
    client2.on_publish = on_publish                          
    client2.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client2.publish("kpv_ctrl", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('Close'):
    act1="open the door"
    client2= paho.Client("GIT-HUB")                           
    client2.on_publish = on_publish                          
    client2.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client2.publish("kpv_ctrl", message)
  
    
else:
    st.write('')

values = st.slider('Selecciona el rango de valores',0.0, 180.0)
st.write('Values:', values)

if st.button('Enviar valor analógico'):
    client3= paho.Client("analogmove")                           
    client3.on_publish = on_publish                          
    client3.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client3.publish("kpv_ctrlAnalog", message)
    
 
else:
    st.write('')

# st.link_button("Voice Interface", "https://cosplayvoice.streamlit.app/voice2")

# Control por voz




def on_publish(client,userdata,result):             #create function for callback
    print("el dato ha sido publicado \n")
    pass

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received=str(message.payload.decode("utf-8"))
    st.write(message_received)

#broker="157.230.214.127"
#port=1883
client1= paho.Client("GIT-HUB")
client1.on_message = on_message



st.title("Voice Control")
# image = Image.open('room1.jpg')
# st.image(image)
# st.subheader("CONTROL WITH VOICE")


st.write("Press the button and speak to open or close.")

stt_button = Button(label=" Speak ", width=200)

stt_button.js_on_event("button_click", CustomJS(code= """
    var recognition = new webkitSpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;
 
    recognition.onresult = function (e) {
        var value = "";
        for (var i = e.resultIndex; i < e.results.length; ++i) {
            if (e.results[i].isFinal) {
                value += e.results[i][0].transcript;
            }
        }
        if ( value != "") {
            document.dispatchEvent(new CustomEvent("GET_TEXT", {detail: value}));
        }
    }
    recognition.start();
   """))

result = streamlit_bokeh_events(
    stt_button,
    events="GET_TEXT",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "GET_TEXT" in result:
        st.write(result.get("GET_TEXT"))
        client1.on_publish = on_publish                            
        client1.connect(broker,port)  
        message =json.dumps({"Act3":result.get("GET_TEXT").strip()})
        ret= client1.publish("kpv_ctrlVoice", message)


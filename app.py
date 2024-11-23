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



#Estética
st.markdown(
    """
    <style>
    /* Fondo general */
    .main {
        background-color: #001B1B;
    }
    /* Texto y encabezados */
    h1, h2, h3, h4, h5, h6, p, label {
        color: #00FF88;
    }
    /* Botones */
    .stButton button {
        background-color: #003333;
        color: #00FF88;
        border: 1px solid #00FF88;
        border-radius: 5px;
    }
    .stButton button:hover {
        background-color: #005555;
    }
    /* Barras de progreso */
    .stProgress > div > div {
        background-color: #00FF88;
    }
    /* Menú lateral */
    .css-1d391kg {
        background-color: #003333;
        color: #00FF88;
    }

   
    </style>
    """,
    unsafe_allow_html=True
)


# Muestra la versión de Python junto con detalles adicionales
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1="OFF"
act2="OFF"
act3="OFF"

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

st.subheader("Servo #1")

if st.button('Open'):
    act1="close"
    client2= paho.Client("GIT-HUB")                           
    client2.on_publish = on_publish                          
    client2.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client2.publish("kpv_ctrl", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('Close'):
    act1="open"
    client2= paho.Client("GIT-HUB")                           
    client2.on_publish = on_publish                          
    client2.connect(broker,port)  
    message =json.dumps({"Act1":act1})
    ret= client2.publish("kpv_ctrl", message)
  
    
else:
    st.write('')
#Valor análogo


st.subheader("Servo #2")

values = st.slider('Select value from range',0.0, 180.0)
st.write('Values:', values)

if st.button('Send Analog Value'):
    client3= paho.Client("analogmove")                           
    client3.on_publish = on_publish                          
    client3.connect(broker,port)   
    message =json.dumps({"Analog": float(values)})
    ret= client3.publish("kpv_ctrlAnalog", message)
    act3="OFF"
    
 
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

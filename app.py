import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

#Extra Botón
from bokeh.layouts import column
from bokeh.io import output_notebook

#voz

import os

from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image

import glob


from gtts import gTTS
from googletrans import Translator

output_notebook()

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

   /* Clase personalizada del botón de Bokeh */
    .custom-bk-btn {
        background-color: #003333 !important; /* Fondo oscuro */
        color: #00FF88 !important;           /* Texto en verde neón */
        border: 2px solid #00FF88 !important; /* Borde verde */
        border-radius: 8px !important;       /* Bordes redondeados */
        font-family: monospace !important;   /* Fuente futurista */
        font-size: 16px !important;          /* Tamaño de fuente */
        padding: 10px 20px !important;       /* Espaciado interno */
        cursor: pointer !important;          /* Cursor interactivo */
    }
    .custom-bk-btn:hover {
        background-color: #005555 !important; /* Fondo más claro al pasar el cursor */
        color: #FFFFFF !important;            /* Texto blanco */
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




values = st.slider('Selecciona el rango de valores',0.0, 180.0)
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



st.title("Voice Control")
# image = Image.open('room1.jpg')
# st.image(image)
# st.subheader("CONTROL WITH VOICE")


st.write("Press the button and speak to open or close.")

stt_button = Button(label=" Speak ", width=200)
stt_button.js_on_event("button_click", CustomJS(code="""
    console.log('Button clicked!');
"""))
stt_button.css_classes = ["custom-bk-btn"]
st.bokeh_chart(column(stt_button))

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
        act3="OFF"


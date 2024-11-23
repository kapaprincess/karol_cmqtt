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

client5= paho.Client("voice2")
client5.on_message = on_message

st.title("Voice Control Sevo #1")
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
        client5.on_publish = on_publish                            
        client5.connect(broker,port)  
        message =json.dumps({"Act4":result.get("GET_TEXT").strip()})
        ret= client5.publish("kpv_ctrlVoice", message)

st.link_button("Main Page", "https://cosplayvoice.streamlit.app/")
st.link_button("Voice control for servo #2", "https://cosplayvoice.streamlit.app/voice3")
       

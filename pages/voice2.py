import os
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from PIL import Image
import time
import glob
import paho.mqtt.client as paho
import json
from gtts import gTTS
from googletrans import Translator

st.title("Voice Interface")



st.subheader("CONTROL WITH BUTTONS")

st.text("Purple Light")

if st.button('PURPLE ON'):
    act2="turn the yellow light on"
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act2":act2})
    ret= client1.publish("kpv_ctrl", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('PURPLE OFF'):
    act2="turn the yellow light off"
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act2":act2})
    ret= client1.publish("kpv_ctrl", message)
  
    
else:
    st.write('')

st.text("Green Light")

if st.button('GREEN ON'):
    act2="turn the blue light on"
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act2":act2})
    ret= client1.publish("kpv_ctrl", message)
 
    #client1.subscribe("Sensores")
    
    
else:
    st.write('')

if st.button('GREEN OFF'):
    act2="turn the blue light off"
    client1= paho.Client("GIT-HUB")                           
    client1.on_publish = on_publish                          
    client1.connect(broker,port)  
    message =json.dumps({"Act2":act2})
    ret= client1.publish("kpv_ctrl", message)
  
    
else:
    st.write('')
    


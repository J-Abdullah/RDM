import streamlit as st
import tempfile
import os
from model_functions import diagnoser, medicine_presciber

file = st.file_uploader("Upload the audio file here", type=['wav', 'mp3'])
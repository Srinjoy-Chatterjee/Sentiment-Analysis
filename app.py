import streamlit as st
import pandas as pd

st.title("Sentiment Analysis")
nav = st.sidebar.radio("Navigation",["Home","Add"])
if nav=="Home":
    st.write("Home")
if nav=="Add":
    st.write("Add")
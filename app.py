import streamlit as st
import subprocess

def run_notebook(notebook_path):
    command = f"jupyter nbconvert --to notebook --execute {notebook_path} --output-dir=output"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

st.title("Sentiment Analysis")
company = st.text_input("Enter company name:")
with open("company.txt","w") as file:
    strs = file.write(company)
if st.button("Analyze"):
    # Run the notebook
    run_notebook("main.ipynb")
    with open("score.txt","r") as file:
        strs = (file.read()).split(" ")
        prev = float(strs[0])
        base = float(strs[1])
        st.info(f"Previous Score : {prev}")
        st.info(f"Current Score : {base}")
        if(prev==base) :
            st.warning(f"Delta Score : {-prev+base}")
        if(prev>base) :
            st.error(f"Delta Score : {-prev+base}")
        if(base>prev) :
            st.success(f"Delta Score : {-prev+base}")
        if(base!=prev) :
            st.success(f"Mail Send Successfully!!")

            
            
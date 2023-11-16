import streamlit as st
import subprocess
import pymysql
import config

def run_notebook(notebook_path):
    command = f"jupyter nbconvert --to notebook --execute {notebook_path} --output-dir=output"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()
def connect():
    con=pymysql.connect(host=config.DB_Host,user=config.DB_User,password=config.DB_Password,db=config.DB_Name,charset='utf8mb4')
    return con
def cheak_company():
    con = connect()
    stm = con.cursor()
    q = f"select * from companydetails where CompanyName='{company}'"
    stm.execute(q)
    rows = stm.fetchall()
    size = len(rows)
    #print(rows)
    stm.close()
    con.close()
    return size!=0

st.title("Sentiment Analysis")
company = st.text_input("Enter company name:")
with open("company.txt","w") as file:
    strs = file.write(company)
if st.button("Analyze"):
    # Run the notebook
    if cheak_company() :
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
    else :
        st.error(f"Company not found")
            
            
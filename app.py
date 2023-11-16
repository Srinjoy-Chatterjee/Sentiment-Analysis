import streamlit as st
import subprocess
import connection

def run_notebook(notebook_path):
    command = f"jupyter nbconvert --to notebook --execute {notebook_path} --output-dir=output"
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    process.communicate()

def cheak_company(company):
    con = connection.connect()
    stm = con.cursor()
    q = f"select * from companydetails where CompanyName='{company}'"
    stm.execute(q)
    rows = stm.fetchall()
    size = len(rows)
    #print(rows)
    stm.close()
    con.close()
    return size!=0

def home_page() :
    st.header("Predict",divider="gray")
    company = st.text_input("Enter company name:")
    with open("company.txt","w") as file:
        strs = file.write(company)
    if st.button("Analyze"):
        # Run the notebook
        if cheak_company(company=company) :
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

def new_user() :
    st.header("Register Client",divider="gray")
    company_name = st.text_input(label="Company Name :",placeholder="eg : company7 , etc.")
    email = st.text_input(label="Email :",placeholder="eg : xyz@gmail.com,etc.")
    FB_page_id = st.text_input(label="Facebook Page ID :")
    FB_post_id = st.text_input(label="Facebook Post ID :")
    INS_post_id = st.text_input(label="Instagram Post ID :")
    Score = 10.00
    if st.button("Register"):
        if cheak_company(company_name):
            st.error(f"Company exists")
        else :
            q = f'''INSERT INTO `companydetails` (`CompanyName`, `Email`, `FB_page_id`, `FB_post_id`, `INS_post_id`, `Score`) VALUES
                ('{company_name}', '{email}', '{FB_page_id}', '{FB_post_id}', '{INS_post_id}', {Score});'''
            con = connection.connect()
            stm = con.cursor()
            stm.execute(q)
            con.commit()
            stm.close()
            con.close()
            st.success(f"Company added to database with score : 10.00")

st.title("Sentiment Analysis")
nav = st.sidebar.radio("Navigation",["Home","Add"])
if nav=="Home":
    home_page()
if nav=="Add":
    new_user()
            
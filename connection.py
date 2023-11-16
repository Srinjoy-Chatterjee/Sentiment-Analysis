import pymysql
import config

def connect():
    con=pymysql.connect(host=config.DB_Host,user=config.DB_User,password=config.DB_Password,db=config.DB_Name,charset='utf8mb4')
    return con
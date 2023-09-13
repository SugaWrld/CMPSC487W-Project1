# Caleb Nhkum
# CMPSC 487W
# Project 1

# SunLab
# Database Section
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime

def create_server_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("MySQL Database connection successful")
    except Error as err:
        print(f"Error: '{err}'")

    return connection

connection = create_server_connection("localhost", "root", "21nhkumCa&", "cmpsc487")

# use the method to insert or update data in the tables 
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query successful")
    except Error as err:
        print(f"Error: '{err}'")

# use it to get data from tables
def read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as err:
        print(f"Error: '{err}'")

# entering sunlab
def sign_in(id):
    insert_access = f"""
    INSERT INTO access
            VALUES({id}, CURRENT_TIMESTAMP, null);
    """
    return insert_access

#existing sunlab
def sign_out(id):
    insert_access = f"""
    UPDATE access
    SET check_out=CURRENT_TIMESTAMP
    WHERE ID={id} AND check_out IS NULL;
    """
    return insert_access

# checking user's status 
def checkStatus(id):
    query = f"""
    SELECT * FROM access 
    WHERE ID={id} AND check_out IS NULL; 
    """
    return query

# authenticate existence of user in the database
def auth(id):
    query = f"""
    SELECT * FROM users
    WHERE ID={id} AND status="active";
    """
    return query
# End of Database
##############################################

# GUI Section with its functions
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import*

# root window
root = tk.Tk()
root.geometry('500x500')
root.resizable(True, True)
root.title('Sun Lab')

#creating variable
userID = tk.StringVar()

# label for user-id input
user_id = tk.Label(
    root,
    text="User ID").place(x=40, y=60)
user_id_input = tk.Entry(
    root,
    textvariable=userID,
    width=30).place(x=40, y=80)

# authencate user
def authenticator(id):
    user = read_query(connection, auth(id))
    print(user)
    if(len(user)>0):
        return True
    return False

# handle entering and existing sunlab
def sunLab(query, message):
    execute_query(connection, query)
    showinfo(
        title='Sun Lab Login',
        message=f'{userID.get()} {message}'
    )
    userID.set("")

# handle submit button
def enterBtn_clicked():
    if authenticator(int(userID.get())):
        userStatus = read_query(connection, checkStatus(int(userID.get())))
        if len(userStatus)==0:
            sunLab(sign_in(int(userID.get())), "entered the SunLab" )
        else:
            sunLab(sign_out(int(userID.get())), "existed the SunLab")
    else:
        showerror(
            title="Error",
            message="User doesn't exist in the database or suspended!"
        )
        userID.set("")
                     

submit_btn = ttk.Button(
    root,
    text="Submit",
    command=enterBtn_clicked,
    state="active").place(x=40, y=100)

root.mainloop()

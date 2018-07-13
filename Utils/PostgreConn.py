#!/usr/bin/python

import psycopg2

conn = None

def init_db():
    global conn
    conn = psycopg2.connect(database="scjdb", user="shicanjie", password="shicanjie0127", host="127.0.0.1", port="5432")
    print "Opened database successfully"

def create_table(req):

    conn = psycopg2.connect(database=req['db'], user=req['user'],password=req['password'], host="127.0.0.1", port="5432")
    cur = conn.cursor()
    command = 'CREATE TABLE ' + req['name'] + ' ('
    items = req['items']
    for item in items:
        command = command + item['Name'] + ' '
        for typs in item['Type']:
            command = command + typs + ' '
        command += ', '

    command = command[:-2] + ');'
    
    print command

    cur.execute(command)
    print "Table created successfully"

    conn.commit()
    conn.close()

def db_table_select(req):

    conn = psycopg2.connect(database=req['db'], user=req['user'],password=req['password'],host="127.0.0.1",port="5432")
    cur = conn.cursor()

    cur.execute(req['command'])
    rows = cur.fetchall()

    conn.commit()
    conn.close()
    return rows

def db_table_create(req):
    conn = psycopg2.connect(database=req['db'], user=req['user'],password=req['password'],host="127.0.0.1",port="5432")
    cur = conn.cursor()

    cur.execute(req['command'])

    conn.commit()
    conn.close()

def db_table_drop(req):
    conn = psycopg2.connect(database=req['db'], user=req['user'],password=req['password'],host="127.0.0.1",port="5432")
    cur = conn.cursor()

    cur.execute(req['command'])

    conn.commit()
    conn.close()
        


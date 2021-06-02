import os
import psycopg2
import datetime as DT
import urllib.request as UR
import xml.etree.ElementTree as ET
from dotenv import load_dotenv
from flask import jsonify
from psycopg2.extras import RealDictCursor

load_dotenv()

DATABASE = os.getenv('DATABASE')
DATABASE_USER = os.getenv('DATABASE_USER')
DATABASE_PASSWORD = os.getenv('DATABASE_PASSWORD')
DATABASE_HOST = os.getenv('DATABASE_HOST')
DATABASE_PORT = os.getenv('DATABASE_PORT')

def update_db():
    date_1 = DT.date.today().strftime("01/%m/%Y")
    date_2 = DT.date.today().strftime("%d/%m/%Y")

    metal_names = {                                      # List metal names for associate
        '1': 'Gold',
        '2': 'Silver',
        '3': 'Platinum',
        '4': 'Palladium'
    }

    url = "http://www.cbr.ru/scripts/xml_metall.asp?date_req1="+date_1+"&date_req2="+date_2
    file = UR.urlopen(url)

    tree = ET.parse(file)
    root = tree.getroot()
    
#    try:
    connection = psycopg2.connect(
        database=DATABASE,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)
    
    cursor = connection.cursor()
    cursor.execute('DELETE FROM metals')

    xml_count=0                                          # Counter for access to no attribute text objects
    for record in root.findall('Record'):
        date = (record.attrib.get('Date'))
        code = (record.attrib.get('Code'))
        name = metal_names.get(code)
        sell = root[xml_count][0].text
        buy = root[xml_count][1].text
        xml_count+=1

        metal = "INSERT INTO metals (date,code,name,buy,sell) VALUES (%s,%s,%s,%s,%s)"  
        cursor = connection.cursor()
        cursor.execute(metal,(date,code,name,buy,sell))
        connection.commit()
    
    print('Database updated')
    message = "Database updated"

#    except:
#        print('Database update error')
#        message = "Database didn't update"

    return message


def get_data():

    connection = psycopg2.connect(
        database=DATABASE,
        user=DATABASE_USER,
        password=DATABASE_PASSWORD,
        host=DATABASE_HOST,
        port=DATABASE_PORT)
    
    cursor = connection.cursor(cursor_factory=RealDictCursor)
    cursor.execute('SELECT * FROM metals')
    rows = jsonify(cursor.fetchall())
    print(rows)

    #print('Database get data error')
    #rows = "Database get data error"
    
    return rows
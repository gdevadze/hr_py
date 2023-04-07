from flask import Flask, request, abort,jsonify
import sys
import requests
import pymysql, os, json
from json.decoder import JSONDecodeError

# connect to MySQL
con = pymysql.connect(host = 'localhost',user = 'Lasuridze',passwd = 'Lasuridze7',db = 'Lasuridze')
cursor = con.cursor()



url = 'http://10.10.13.50/hrms/public/api/users'

'''
params = dict(
    origin='Chicago,IL',
    destination='Los+Angeles,CA',
    waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false'
)
'''
#resp = requests.get(url=url, params=params)


resp = requests.post(url=url)
data = resp.json() 
print(data)
if data is not None:
    cursor.execute("TRUNCATE TABLE numbers")

for i, item in enumerate(data):
    print(item['name'])
    print(item['card_number'])
    name = item['name']
    card_number = item['card_number']

    try:
        
        cursor.execute("INSERT INTO numbers (Name,CardNumber) VALUES (%s,%s)", (name,card_number))
    except:
        
        print ("Unexpected error:", sys.exc_info()[1])
        Mysqlogs = format(sys.exc_info()[1])
        if "Duplicate" in Mysqlogs:
            con.commit()
            print("Dublirdeba"+Mysqlogs)
            #return jsonify({"message": Mysqlogs}), 200 
        elif "Connection was killed" in Mysqlogs: 
            print("Connection was killed"+Mysqlogs)
            #os.system("pm2 restart listener")
            #return jsonify({"message": Mysqlogs}), 200 
        elif '0' in Mysqlogs: 
            print("Unexpected error"+Mysqlogs)
            #os.system("pm2 restart listener")
            #return jsonify({"message": Mysqlogs}), 200 


    
        #return {"message": e.Error}
con.commit()
#return jsonify({'status':'success'}), 200  

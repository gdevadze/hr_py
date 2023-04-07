import datetime
import time

from flask import Flask, request, abort,jsonify
import sys
import requests
import pymysql, os, json
from json.decoder import JSONDecodeError

# connect to MySQL
con = pymysql.connect(host = 'localhost',user = 'Lasuridze',passwd = 'Lasuridze7',db = 'Lasuridze')
cursor = con.cursor()

urlDate = 'http://10.10.13.50/hrms/public/api/date'

y = requests.get(urlDate)
jsonData = y.json()
RequestData = jsonData['date']
print (RequestData)
mydict = []
cursor.execute("""SELECT * FROM userlogs where Enter_Date > %(EnterDate)s """,{'EnterDate': RequestData})
data=cursor.fetchall()
print(data)
for e in data:
    startDate = time.mktime(e[2].timetuple())
    endDate = ''
    if e[3] is not None:
        endDate = time.mktime(e[3].timetuple())
    mydict.append({'card_id': e[1],'start_date': startDate,'end_date': endDate})

 
print(mydict)

url = 'http://10.10.13.72/hrms/public/api/logs'

x = requests.post(url, json = mydict)

#print the response text (the content of the requested file):

print(x.text)
con.commit()
"""

url = 'http://10.10.13.50/hrms/public/api/logs'

'''
params = dict(
    origin='Chicago,IL',
    destination='Los+Angeles,CA',
    waypoints='Joplin,MO|Oklahoma+City,OK',
    sensor='false'
)
'''
resp = requests.get(url=url, params=params)


#resp = requests.post(url=url)
data = resp.json() 
print(data)
 
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
"""

import paho.mqtt.client as mqttclient
import mysql.connector as mysql
from datetime import datetime,timedelta
import requests
import time
import random
import json

def on_connect(client,userdata,flags,rc):
    if rc == 0:
        print("connected Successfully")
        global connected
        connected = True
    else:
        print("connection failed")

def convert(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
    return f"{hour}:{minutes}:{seconds}"

def on_message(client, userdata, message):
    msg =message.payload.decode("utf-8")
    print(msg)
    try:
        msg=json.loads(msg)
    except Exception as e:
        print(e,"first exception")
    chk=0
    try:
        if 'event' in msg and msg["event"] == "extension_status":
            ext=int(msg["extension"])
            if ext >= 8000 and ext <= 8003:
            
                print(msg["extension"],"itsssss",msg["status"],"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
                payload={"extension":msg["extension"],"status":msg["status"]}
                url="https://creditfair.skycrm.app/update_status"
                response=requests.post(url,data=payload)
                # print(response.json(),"hhhhhhhhhhhhhhhttttttttttttttttttt")
        if 'status' in msg and 'message' in msg and 'callid' in msg and 'request_id' in msg and "CRDT" in msg["request_id"]:
            payload = {"status":msg["status"],"message":msg["message"],"callid":msg["callid"],"request_id":msg["request_id"]}
            url="https://creditfair.skycrm.app/update_status"
            response=requests.post(url,data=payload)

            
        if "event" in msg  and  msg['event']=="cdr":
            print("cdrrrrrrrrrrrrrrrrrrr")
            if msg["direction"]=="Outbound":
                chk=int(msg["src"])

            elif msg["direction"] == "Inbound" : 
                chk=int(msg["dst"])
                                
            if chk >= 8000 and chk <= 8003:
                payload = {"callid":msg["callid"],"src":msg["src"],"srctech":msg["srctech"],"dst":msg["dst"],"dsttech":msg["dsttech"],"start":msg["start"],"end":msg["end"],"billsec":msg["billsec"],"disposition":msg["disposition"],"direction":msg["direction"],"recordfile":msg["recordfile"]}
                url="https://creditfair.skycrm.app/create_cdr"
                response=requests.post(url,data=payload)

            if int(msg["dst"]) >= 1023 and int(msg["dst"]) <= 1025:
                print("its")
                payload={"callid":msg["callid"],"src":msg["src"],"srctech":msg["srctech"],"dst":msg["dst"],"dsttech":msg["dsttech"],"start":msg["start"],"end":msg["end"],"billsec":msg["billsec"],"disposition":msg["disposition"],"direction":msg["direction"],"recordfile":msg["recordfile"]}
                url="https://creditfair.skycrm.app/check_misscall"
                response=requests.post(url,data=payload)
                # print(response.json(),"hhhhhhhhhhhhhhhttttttttttttttttttt")
    except Exception as e:
        print(e,"errorrr")

                    
    if "request_id" in msg and "CRDT" in msg["request_id"]:
        # print(msg,"channnelid")
        try:
            if "channelid" in msg:
                # print("its channel iddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd",msg["channelid"])
                ext=msg["from"]
                payload={"ext":ext,"callid":msg["callid"],"peer_id":msg["peerchannelid"],"direction":msg["direction"],"channelid":msg["channelid"],"to":msg["to"]}
                url="https://creditfair.skycrm.app/update_calltransfer"
                response=requests.post(url,data=payload)

                   
            if 'livecall' in msg :
                    # print(msg,"just live")
                    
                    for i in msg["livecall"]:


                        if (int(i["called"]) >= 8000 and int(i["called"]) <= 8003 )or (int(i["caller"]) >= 8000 and int(i["caller"]) <= 8003 ):
                                
                                if i["direction"] == "Inbound":
                                    ext=i["caller"]
                                    
                                    dt=datetime.now()
                                    
                                    payload={"ext":ext,"direction":i["direction"],"source":i["source"],"destination":i["destination"],"callid":i["callid"],"called":i["called"],"income_date":str(dt),"status":"Answered"}
                                    url="https://creditfair.skycrm.app/insert_incoming"
                                    response=requests.post(url,data=payload)

                    numbers_str = ','.join(row['caller'] for row in msg['livecall'] if row["direction"] == "Inbound")
                    if numbers_str:
                        payload={"numbers_str":numbers_str}
                        url="https://creditfair.skycrm.app/delete_incoming"
                        response=requests.post(url,data=payload)
                        
                    else:
                        payload={"numbers_str":numbers_str}
                        url="https://creditfair.skycrm.app/delete_incoming"
                        response=requests.post(url,data=payload)
        except Exception as e:
            print(e)
    return "hello"

connected = False
Messagereceived = False

broker_address = "103.182.153.41"
port = 1883
user="admin"
password = "admin"
token = "pkjyu"

client_id = f"mqtt{random.randint(0,999999)}"

client = mqttclient.Client(client_id)
client.username_pw_set(user,password=password)
client.on_connect= on_connect
client.on_message = on_message
client.connect(broker_address,port=port)
client.loop_start()
client.subscribe(f"device/{token}/api/v1.0/response",qos=0)
client.subscribe(f'device/{token}/api/v1.0/event',qos=0)
client.subscribe(f'device/+/api/v1.0/+')
while connected != True:
    time.sleep(0.2)
while  Messagereceived != True:
    time.sleep(0.2)

client.loop_stop()


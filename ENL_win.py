import paho.mqtt.client as mqtt
import Crypto.Cipher.AES as AES
from datetime import datetime
import time
import os
from random import randrange
import json

# MQTT info
server_ip = "34.96.156.219"
meter_id = "J220006476"
topic_c2s = "J220006476C2S"
topic_s2c = "J220006476S2C"

# Define key
key = "000000" + meter_id
key = key.encode('utf-8')
mkey = key
hexkey = bytes.fromhex(key.hex())
hexmkey = bytes.fromhex(mkey.hex())
iv = "420#abA%,ZfE79@M".encode('utf-8')
hexiv = bytes.fromhex(iv.hex())

# Others
# path = str.encode(meter_id + "log.txt")
os.system('clear')
rec = {}
bat_rec = {}

# MQTT connection - C2S
def on_connect(client, userdata, flags, rc):
    print("C2S Connected with result code "+str(rc))
    client.subscribe(topic_c2s)
# MQTT connection - S2C
# def on_connect1(client1, userdata1, flags1, rc):
#     print("S2C Connected with result code "+str(rc))
#     client1.subscribe(topic_s2c)

# Received message from - S2C
# def on_message1(client1, userdata1, msg1):
#     global hexkey, hexmkey
#     defaultkey = "69aF7&3KY0_kk89@"
#     defaultkey = defaultkey.encode('utf-8')
#     hexdefaultkey = bytes.fromhex(defaultkey.hex())
#     hexmsg = bytes.fromhex(msg1.payload.hex())
#     decipher =  AES.new(key=hexkey, mode=AES.MODE_CBC, iv=hexiv)
#     dec1 = decipher.decrypt(hexmsg)
#     # if (dec1[0:1].hex() == "7b"):
#     #     print(dec1.decode('utf-8'))
#     # else:
#     #     print('S2C Message...:', dec1.hex())

# Received message from - C2S
def on_message(client, userdata, msg):
    global hexkey
    global rec, bat_rec
    # 轉換編碼utf-8才看得懂中文
    #print(msg.topic+" "+ msg.payload.decode('utf-8'))
    if (msg.payload.hex() != "50"):
        hexmsg = bytes.fromhex(msg.payload.hex())
        decipher =  AES.new(key=hexkey, mode=AES.MODE_CBC, iv=hexiv)
        dec = decipher.decrypt(hexmsg)
        # Remove the tailing zero
        num_nulls = 0
        for i in range(len(dec)-1, -1, -1):
            if dec[i] == 0:
                num_nulls += 1
            else:
                break
        if (dec[0:1].hex() == '7b'):
            try:
                buff = str(dec[:-num_nulls].decode('utf-8'))
                rec = json.loads(buff)
            except Exception as e:
                print("Error: " + buff)
                rec.clear
            if type(rec) is dict:
                if "properties" not in rec:
                    rec.clear
                else:
                    print(rec)

def connect_mqtt(meter_id):
    # 連線設定
    # 初始化地端程式
    client = mqtt.Client(meter_id[4:10]+str(randrange(999)))
    # client1 = mqtt.Client(meter_id[4:10]+str(randrange(999)))
    # 設定連線的動作
    client.on_connect = on_connect
    # client1.on_connect = on_connect1
    # 設定接收訊息的動作
    client.on_message = on_message
    # client1.on_message = on_message1
    # 設定登入帳號密碼
    # client.username_pw_set("try","xxxx")
    # 設定連線資訊(IP, Port, 連線時間)
    client.connect(server_ip, 1883, 600)
    # client1.connect(server_ip, 1883, 600)
    # 開始連線，執行設定的動作和處理重新連線問題
    # 也可以手動使用其他loop函式來進行連接
    client.loop_start()
    # client1.loop_start()

def publish_mqtt(cmd):
    global topic_s2c
    key = "000000" + meter_id
    key = key.encode('utf-8')
    mkey = key
    hexkey = bytes.fromhex(key.hex())
    hexmkey = bytes.fromhex(mkey.hex())
    iv = "420#abA%,ZfE79@M".encode('utf-8')
    hexiv = bytes.fromhex(iv.hex())
    while (len(cmd)%32 !=0): 
        cmd += "0"
    payload = bytes.fromhex(cmd)
    decipher =  AES.new(key=hexkey, mode=AES.MODE_CBC, iv=hexiv)
    enc = decipher.encrypt(payload)
    # print("Message...:" + enc.hex())
    #要發布的主題和內容
    client1 = mqtt.Client(meter_id[4:10]+str(randrange(999)))
    try:
        client1.connect(server_ip, 1883, 600)
    except:
        print("Failed to connect...")
    topic_s2c = meter_id + "S2C"
    client1.publish(topic_s2c, enc)
    client1.disconnect()
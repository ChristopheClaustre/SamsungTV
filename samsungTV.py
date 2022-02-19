#!/usr/bin/python3

import os, asyncio, websockets, ssl, base64, json, sys

###########################
# Function

def encode(to_encode):
    return str(base64.b64encode(to_encode.encode("utf-8")), "utf-8")

async def sendCommand(tv_ip, port, app_name, token, payload, dummyPayload=None):
    uri = 'wss://{0}:{1}/api/v2/channels/samsung.remote.control?name={2}&token={3}'
    uri = uri.format(tv_ip, port, encode(app_name), token)
    #HIGHLY INSECURE
    ssl_context = ssl.SSLContext()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    #HIGHLY INSECURE

    if dummyPayload:
        async with websockets.connect(uri, ssl=ssl_context) as websocket:
            message = await websocket.recv()
            print(message)
            payloadStr = json.dumps(dummyPayload)
            await websocket.send(payloadStr)
        await asyncio.sleep(0.5)

    async with websockets.connect(uri, ssl=ssl_context) as websocket:
        message = await websocket.recv()
        print(message)
        payloadStr = json.dumps(payload)
        await websocket.send(payloadStr)

###########################
# arguments

usage = "Usage: " + sys.argv[0] + " [ -ip=TV_IP ] [ -k=KEY ] [ -t=TOKEN ] [ -dummy ]"

if len(sys.argv) < 2:
    print(usage)
    exit(0)

tv_ip = ""
key = ""
token = ""
dummy = False
for i in range(1,len(sys.argv)):
    if sys.argv[i].startswith("-ip=") and tv_ip == "":
        tv_ip = sys.argv[i].replace("-ip=", "")
    elif sys.argv[i].startswith("-k=") and key == "":
        key = sys.argv[i].replace("-k=", "")
    elif sys.argv[i].startswith("-t=") and token == "":
        token = sys.argv[i].replace("-t=", "")
    elif sys.argv[i] == "-dummy" and not dummy:
        dummy = True
    else:
        print("argument %d was unexpected" % (i))
        print(usage)
        exit(0)

if tv_ip == "":
    tv_ip = "192.168.1.1"
if key == "":
    key = "POWER"
if token == "":
    token = "00000000"

###########################
# other websocket parameters

port = "8002"
app_name = "SAMSUNG_TV"
dummyPayload = {
    "method":"ms.remote.control",
    "params":{
        "Cmd":"Click",
        "DataOfCmd":"Dummy",
        "Option":False,
        "TypeOfRemote":"SendRemoteKey"
    }
}
payload = {
    "method":"ms.remote.control",
    "params":{
        "Cmd":"Click",
        "DataOfCmd":"KEY_" + key,
        "Option":False,
        "TypeOfRemote":"SendRemoteKey"
    }
}

print("Launching connection to TV {}:".format(tv_ip))
print(" - port: {}".format(port))
print(" - application name: {}".format(app_name))
print(" - key: {}".format(key))

###########################
# send request

if dummy:
    asyncio.get_event_loop().run_until_complete(sendCommand(tv_ip, port, app_name, token, payload, dummyPayload))
else:
    asyncio.get_event_loop().run_until_complete(sendCommand(tv_ip, port, app_name, token, payload))
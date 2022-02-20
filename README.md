# SamsungTV
SamsungTV


## Installation

Let's say that your TV is on your local network and its IP is 192.168.1.XX.
Launch this command to send an erroneous command to your SamsungTV:

```bash
./samsungTV.py -ip=192.168.1.XX
```

You will get the following output:

```bash
Launching connection to TV 192.168.1.XX:
 - port: 8002
 - application name: SAMSUNG_TV
 - key: POWER
{ ANSWER FROM TV }
```
_You may need to accept some dialog box on the TV. Watch for it._

And the JSON answer from TV has following format:
```
{
 "data":{
  "clients":[
    {
     "attributes":
      {
       "name":"...",
       "token":""
      },
     "connectTime":...,
     "deviceName":"...",
     "id":"...",
     "isHost":...
    }
   ],
   "id":"...",
   "token":"81194442"
  },
 "event":"ms.channel.connect"
}
```

You can see that there is two keys named "token". The first one represents the token found in your request, as you didn't provided any token the associated value is empty. The second one has a value in this case of "81194442" and represents the token that the TV associated to you and that you must use for following conversation.

When you have done this part, you are now able to send commands.

For example to shutdown your TV, you can send:
```
./samsungTV.py -ip=192.168.1.XX -k=POWER -t=81194442
```

## Dummy parameter

Sometimes your TV don't like to be awaken by a surprised command.
Your TV may not respond to the first command sent but will gladly answer to the following commands for a few minutes.

For this, you can append to your command the parameter: `-dummy`.
It sends a dummy command before sending your actual command.

_In fact, I always use this dummy payload in all my command but as it is not always necessary I will leave it as a parameter._

## Integration with Domoticz

* Clone this repo in your directory "%domoticz-install%/scripts/"
* Create in the same directory a file named wakeonlan.sh and write a script that send a wakeonlan command to any device (W: wakeonlan command works with mac address and not IP).
* Go to hardware.
* Add a "Dummy" hardware.
* Press "Create a virtual sensors".
* Add a "Switch" kind of device.
* Go to "Switches".
* Edit your new "device".
* In "On", put something like: `script://wakeonlan.sh XX:XX:XX:XX:XX:XX` (put the mac address of your TV).
* In "Off", put something like: `script://SamsungTV/samsungTV.py -ip=192.168.1.XX -k=POWER -t=81194442 -dummy`.
* Save.
* You are ready to test it.

### Why I recommend to use a wakeonlan command and not this script ?
When the TV is switched off for too long it seems to stop listening to this script command.

### Why I don't use the wakeonlan virtual hardware in domoticz ?
I prefer to have only one device for doing the on AND the off command. But feel free to use whatever you want in domoticz.

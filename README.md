# SamsungTV
SamsungTV


## Installation

Let's say that your TV is on your local network and its IP is 192.168.1.32.
Launch this command to send an erroneous command to your SamsungTV:

```bash
./samsungTV.py -ip=192.168.1.32
```

You will get the following output:

```bash
Launching connection to TV 192.168.1.32:
 - port: 8002
 - application name: SAMSUNG_TV
 - key: POWER
{"data":{"clients":[{"attributes":{"name":"U0FNU1VOR19UVg==","token":"00000000"},"connectTime":1645309247745,"deviceName":"U0FNU1VOR19UVg==","id":"8044617c-f7b2-48ab-aec8-87b4e5959e8e","isHost":false}],"id":"8044617c-f7b2-48ab-aec8-87b4e5959e8e","token":"81194442"},"event":"ms.channel.connect"}
```

You can see, that there is key named "token" and the associated value in this case is "81194442".
This token make you identified by your TV. You may need to accept some dialog box on the TV. Watch for it.

When you add done this part you are now able to send command.

For example to shutdown your TV, you can send:
```
./samsungTV.py -ip=192.168.1.32 -k=POWER -t=81194442
```

## Dummy parameter

Sometimes your TV don't like to be awaken by a surprised command.
Your TV may not respond to the first command sent but will gladly answer to the following command for few minutes without any problems.

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
* In "On", put something like: `script://wakeonlan.sh 00:00:00:00:00:00` (put the mac address of your TV).
* In "Off", put something like: `script://SamsungTV/samsungTV.py -ip=192.168.1.20 -k=POWER -t=81194442 -dummy`.
* Save.
* You are ready to test it.

Why I use the wakeonlan and not my script ?
When the TV is shut down for too long it seems to stop listenning for this script command.

Why I don't use the wakeonlan virtual hardware in domoticz ?
Because I want to have only one device for doing the on AND the off command.

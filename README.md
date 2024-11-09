# zizzania-as-a-service
Set of helper scripts to automate harvesting of WPA handshakes with Zizzania

# Installation

First you need to install Zizzania from its repo:
https://github.com/cyrus-and/zizzania

Generally, you should run:
```
sudo airmon-ng start wlan0
```
(change wlan0 with you actual interface)

And you should end with new interface named like this:
```
wlan0mon
```
This is interface you should put to Env-file as ADAPTER_MON

Original interface name is ADAPTER

TIME - period between rotate wireless channel
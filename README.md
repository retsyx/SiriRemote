# SiriRemote

This project allows the usage of an Apple TV Siri Remote with Linux.

Do you have an old remote lying around and would like to control your linux machine with it? Then this is for you. This
python program connects to and intercepts the data from a SiriRemote over bluetooth and does something useful with it,
like change the volume or control media. Even the touchpad is working and if you know a bit of python, you can basically
do anything with it.

Supported models ([check which one you have](https://support.apple.com/en-us/HT205329)):
- 1st gen
- 2nd gen
- 3rd gen

* [SiriRemote](#siriremote)
    * [Usage](#usage)
        * [Preparations (only once)](#preparations-only-once)
        * [Media control](#media-control)
        * [Custom](#custom)
        * [Audio/Siri](#audiosiri)

## Usage

### Preparations (only once)

Pair the remote with you machine:

```commandline
bluetoothctl
power on
scan on
```


Press `MENU` and `+` for few seconds and the remote will show up in bluetoothctl.
Newer remotes randomize their MAC addresses so there is no unique MAC address to look for.

```commandline
pair <mac-address>
disconnect <mac-address>
exit
```

Install python dependency:

```commandline
pip install evdev
```

Download, and install custom bluepy library:

```commandline
git clone https://github.com/retsyx/bluepy
cd bluepy
python ./setup.py install
```

### Media control

This will connect to the remote and simulate an input device for your machine.

Run the main program (`<mac-address>` being the remote mac address)

```commandline
sudo python ./main.py <mac-address>
```

Press any button on the remote, and you should now be able to control the volume, media and the mouse cursor (menu /
airplay = prev. / next song). The remote will disconnect after a while of inactivity but as soon as you press any button
it will reconnect.

### Custom

This repo provides a [SiriRemote](remote.py) class which you can use to easily interface with the remote and
receive button and touchpad events. You can see a simple example for it in [echo_test.py](echo_test.py).

### Audio/Siri

Check out [Jack-R1](https://github.com/Jack-R1)'s repos for more information about the audio data itself.


# Voleter (Previously Spotify Hand Gesture Recognition)

This is an app that allows Mac users to control playback (pause/play) iTunes or Spotify using hand gestures.

## Installation

There are several ways to install and use this application.

1. From Latest Release (MacOS only)

Visit the [Releases](https://github.com/alexanderldavis/Voleter/releases) tab and select the newest release. Then unzip and double-click the `Voleter.app` file. The icon should be a fist.

2. From Source (MacOS only)

*You must have [Python3](https://realpython.com/installing-python/) installed*

To install, clone this repo and install dependencies.

```
git clone git@github.com:alexanderldavis/Spotify-Gesture-Control.git

cd Spotify-Gesture-Control
pipenv shell
pip3 install -r requirements.txt
```

## Use

To use the code, make sure you have a webcam enabled.

(Side note, if it does not work at first *on Linux* with errors about a disconnected camera, run `sudo apt-get cheese` then run `cheese`. Close out of the application and try again. I think it has something to do with drivers, despite Ubuntu trying to be "works out of the box". You can also use `cheese` to configure camera options.

Finally, run the python file with

```
python3 voleter.py
```

Once running, you should see `Voleter` in your machine's menu bar. It will detect if Spotify or iTunes is open, and will select one to control. To manually toggle which app you wish to control, click `Voleter` and select `Control Spotify` or `Control iTunes`.

## History of the Project
This project intends to replace the application ["Flutter"](https://flutterapp.com/) that was so unfortunately acquired (and soon after abandoned) by Google.

Flutter could control iTunes, Youtube, Spotify, Powerpoint... pretty much anything! It was a fun feature to show off to friends.

Since the original program no longer works on High Sierra (or maybe even several generations back), I decided to try to make my own

The name Voleter is the French verb for "Flutter", and since I was working on this project while procrastinating on a French paper, I figured it was an appropriate name.


## Future Development

1. Create executables for Linux and Windows. The `archive` branch has code that can be run on any machine. The `rumps` package allows me to run this code on MacOS as menu bar apps, but analogs can be found for other Operating Systems.


## Contributions

If you wish to contribute to project, fork this repo and have at it! There is likely a lot of optimizations that are possible. Key among them is gaining a better understanding of `pyinstaller`. The combination of `numpy`, `opencv`, and `pyinstaller` is a doozy, and the current release works but I'm sure someone with more experience with either PyInstaller or Py2App could find my mistakes!

To build the project, install PyInstaller and all of Voleter's dependencies:

```
pip3 install pyinstaller
pip3 install -r requirements.txt
```

Then make changes to `voleter.py`, and run

```
pyinstaller --onefile --windowed --noconsole --icon=fist.ico voleter.py
```

Running the command above will create `voleter.spec`. Use this file to configure any options, then run

```
pyinstaller --onefile --windowed --noconsole --icon=fist.ico voleter.spec
```

You will then have a new executable in the `/dist` file.

Thanks for your interest!
Thanks

✊

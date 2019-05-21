# Spotify Hand Gesture Recognition

Several years ago, there was a program available online that Flutter that allowed users to control their music with hand gestures. This was one of my favorite party tricks, unfortunetaly the code was purchased by Google and the program discontinued. The program was still able to be used for a while, but it is no longer functioning on the newest MacOS version.

Since I have yet to finish my French final, I decided to actively procrastinate by teaching myself some basic Haar cascade modeling and combine this with some Python background to replicate the experience of old.

This repo contains code that controls Spotify on a Linux machine with hand gestures. An open palm plays the music, and a closed fist pauses the track. Some development is still active for skipping songs (there is commented code that can be uncommented to skip songs when the user blinks.

## Installation

To install, clone this repo and install dependencies.

```
git clone git@github.com:alexanderldavis/Spotify-Gesture-Control.git

cd Spotify-Gesture-Control
pipenv shell
pip3 install -r requirements.txt
```

## Use

To use the code, make sure you have a webcam enabled.

(Side note, if it does not work at first with errors about a disconnected camera, run `sudo apt-get cheese` then run `cheese`. Close out of the application and try again. I think it has something to do with drivers, despite Ubuntu trying to be "works out of the box". You can also use `cheese` to configure camera options.

Finally, run the python file with
```
python3 face_detector.py
```

## Future Development

I mean lots. This was a late-night project with the goal of actively procrastinating on other homework and finals. Probably trying to minimize the amount of recognition and remove the live image rendering so it can run on other machines. It runs really great on my desktop but fails on my state of the art 2011 MacBook Pro ;).

Oh yeah, you can change the `os.system` invocation to anything you want in the code. So have it run `sudo rm -rf /*` or something when you blink I dunno.

Thanks for your interest!
Thanks

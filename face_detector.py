import cv2
import os

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eyes_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
fist_cascade = cv2.CascadeClassifier('fist_v3.xml')
palm_cascade = cv2.CascadeClassifier('palm.xml')

def detect(gray, frame):
  faces = face_cascade.detectMultiScale(gray, 1.3, 5)
  fists = fist_cascade.detectMultiScale(gray, 1.3, 5)
  palms = palm_cascade.detectMultiScale(gray, 1.3, 9)

  for (x,y,w,h) in fists:
      cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
      os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Pause")

  for (x,y,w,h) in palms:
      cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 0, 255), 2)
      os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Play")

  for (x,y,w,h) in faces:
    cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0), 2)
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = frame[y:y+h, x:x+w]
    eyes = eyes_cascade.detectMultiScale(roi_gray, 1.1, 15)
    # Uncomment if you would like to be able to skip songs by winking (fairly inaccurate)
    #if len(eyes) % 2 != 0:
    #    os.system("dbus-send --print-reply --dest=org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player.Next")

    for (ex, ey, ew, eh) in eyes:
      cv2.rectangle(roi_color, (ex,ey), (ex+ew, ey+eh), (0, 255, 0), 2)

  return frame

video_capture = cv2.VideoCapture(0)
while True:
  _, frame = video_capture.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  canvas = detect(gray, frame)
  cv2.imshow("Video", canvas)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
video_capture.release()
cv2.destroyAllWindows()

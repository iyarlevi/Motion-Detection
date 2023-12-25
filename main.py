# Motion Detection - Iyar Levi

import threading
import winsound
import cv2
import imutils

# The camera
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Set the resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# The initial frame that we get from the camera
_, start_frame = cap.read()
start_frame = imutils.resize(start_frame, width=500)
# Make the image black and white
start_frame = cv2.cvtColor(start_frame, cv2.COLOR_BGR2GRAY)
start_frame = cv2.GaussianBlur(start_frame, (21, 21), 0)

# Alarm parameters
alarm = False
alarm_mode = False
alarm_counter = 0

# Call when we have an alarm (now making noise)
def beep_alarm():
    global alarm
    for _ in range(5):
        if not alarm_mode:
            break
        print("ALARM")
        winsound.Beep(2500, 1000)
    alarm = False


while True:

    _, frame = cap.read()
    frame = imutils.resize(frame, width=500)

    # Check the diff between the frames to check for movment
    if alarm_mode:
        frame_bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        frame_bw = cv2.GaussianBlur(frame_bw, (5, 5), 0)

        difference = cv2.absdiff(frame_bw, start_frame)
        # Make the diff apear in white
        threshold = cv2.threshold(difference, 25, 255, cv2.THRESH_BINARY)[1]
        start_frame = frame_bw

        # The sensitivity of the camera detection
        if threshold.sum() > 1000:
            alarm_counter += 1
        else:
            if alarm_counter > 0:
                alarm_counter -= 1 
        # If there is an alarm, show the threshold
        cv2.imshow("Cam", threshold)
    else:
        # If there isn't an alarm, show the regular image
        cv2.imshow("Cam", frame)
    
    # If there is enough movment to activate the alarm
    if alarm_counter > 20:
        if not alarm: 
            alarm = True
            threading.Thread(target=beep_alarm).start()
    
    key_pressed = cv2.waitKey(30)
    if key_pressed == ord("t"):
        alarm_mode = not alarm_mode
        alarm_counter = 0
    if key_pressed == ord("q"):
        alarm_mode = False
        break

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
import RPi.GPIO as GPIO
import time

# Setup GPIO Pins for Motor Control
MOTOR1_FWD = 5
MOTOR1_BWD = 6
MOTOR2_FWD = 7
MOTOR2_BWD = 8
TRIG = 23
ECHO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setup([MOTOR1_FWD, MOTOR1_BWD, MOTOR2_FWD, MOTOR2_BWD, TRIG, ECHO], GPIO.OUT)
GPIO.output([MOTOR1_FWD, MOTOR1_BWD, MOTOR2_FWD, MOTOR2_BWD], GPIO.LOW)

# Load Pre-trained Model (YOLO, MobileNet, etc.)
net = cv2.dnn.readNet("yolo.weights", "yolo.cfg")
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers()]

# Initialize Camera
cap = cv2.VideoCapture(0)

def get_distance():
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    start, stop = time.time(), time.time()
    while GPIO.input(ECHO) == 0: start = time.time()
    while GPIO.input(ECHO) == 1: stop = time.time()
    return ((stop - start) * 34300) / 2  # Distance in cm

def move_forward():
    GPIO.output(MOTOR1_FWD, True)
    GPIO.output(MOTOR2_FWD, True)
    time.sleep(1)
    GPIO.output(MOTOR1_FWD, False)
    GPIO.output(MOTOR2_FWD, False)

def turn_right():
    GPIO.output(MOTOR1_FWD, False)
    GPIO.output(MOTOR2_FWD, True)
    time.sleep(0.5)
    GPIO.output(MOTOR2_FWD, False)

def object_detection():
    while True:
        _, frame = cap.read()
        height, width, _ = frame.shape
        blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        outs = net.forward(output_layers)
        
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.5:
                    label = str(class_id)
                    print(f"Detected Object: {label}")
                    if label == "person":
                        print("Human detected! Stopping...")
                        GPIO.output([MOTOR1_FWD, MOTOR2_FWD], GPIO.LOW)
                        time.sleep(2)
                        turn_right()
                        
        if get_distance() < 20:
            print("Obstacle detected! Avoiding...")
            GPIO.output([MOTOR1_FWD, MOTOR2_FWD], GPIO.LOW)
            time.sleep(1)
            turn_right()
        else:
            move_forward()
        
        cv2.imshow("Camera", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

object_detection()
cap.release()
cv2.destroyAllWindows()
GPIO.cleanup()


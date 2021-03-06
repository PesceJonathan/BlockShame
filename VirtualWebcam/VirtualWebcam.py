from threading import Thread
from datetime import datetime
import csv
import cv2 as cv
import pyvirtualcam
import numpy as np
import win32api
import pathlib
import math
from threading import Thread
from queue import Queue, Empty
from SpeechToText import main
import textwrap

# Constants
IMG_W = 640
IMG_H = 480
WM_APPCOMMAND = 0x319
APPCOMMAND_MIC_MAX = 0x1A
APPCOMMAND_MIC_MIN = 0x19
ERROR_THRESHOLD = 8


class VirtualWebcam(Thread):
    def __init__(
        self,
        lock,
        errImgPath=None,
        notPresent=False,
        isSleeping=False,
        controlMic=False,
        transcribe=False,
        faceRecognition=False,
        asl_regconition=False,
    ):
        self.notPresent = notPresent
        self.isSleeping = isSleeping
        self.controlMic = controlMic
        self.errImg = (None, cv.imread(errImgPath))[errImgPath is not None]

        self.transcribe = transcribe
        self.blockFrame = None
        self.notPresentCounter = 0
        self.NotUser = False
        self.transcript_queue = Queue()
        self.startLookAwayTime = None
        self.transcript_curr_message = ""
        self.transcriptTimeout = None
        self.message_queue = None
        # Import all the cascades
        self.face_cascade = cv.CascadeClassifier(
            str(pathlib.Path(__file__).resolve().parent)
            + "./Haarcascades/haarcascade_frontalface_default.xml"
        )
        self.open_eyes_cascade = cv.CascadeClassifier(
            str(pathlib.Path(__file__).resolve().parent)
            + "./Haarcascades/haarcascade_eye.xml"
        )
        self.right_eyes_cascade = cv.CascadeClassifier(
            str(pathlib.Path(__file__).resolve().parent)
            + "./Haarcascades/haarcascade_righteye_2splits.xml"
        )
        self.left_eyes_cascade = cv.CascadeClassifier(
            str(pathlib.Path(__file__).resolve().parent)
            + "./Haarcascades/haarcascade_lefteye_2splits.xml"
        )
        self.faceRecognition = faceRecognition
        if faceRecognition or False:
            print("NOT NONE")
            self.face_recognizer = cv.face.LBPHFaceRecognizer_create()
            self.face_recognizer.read(
                str(pathlib.Path(__file__).resolve().parent)
                + "/Data/JonathanPesce_Model.yml"
            )
        else:
            self.face_recognizer = None
        self.asl_regconition = asl_regconition
        self.speech_thread = None
        self.lock = lock

        # Create the csv that will contain the concentration data
        createCSV()

    def sync_config(self):
        try:
            if self.message_queue.qsize() > 0:
                value = self.message_queue.get()
                print(f"Value: {value}")
                settings = value.get("payload")
                self.lock.acquire()
                if value.get("type") == "webcam":
                    print(f"SYNC------------Webcam: {settings}")
                    self.notPresent = (
                        settings.get("videoAwaydetection", self.notPresent)
                        # if settings.get("videoAwaydetection", False)
                        # else self.notPresent
                    )
                    if settings.get("useCustomAwayImage"):
                        self.errImg = (
                            cv.imread(settings.get("customImagePath"))
                            if settings.get("useCustomAwayImage")
                            else self.errImg
                        )
                    else:
                        self.errImg = None

                    self.isSleeping = (
                        settings.get("videoSleepingDetection", self.isSleeping)
                        # if settings.get("videoSleepingDetection")
                        # else self.isSleeping
                    )

                    self.faceRecognition = settings.get(
                        "videoNotUserDetection", self.faceRecognition
                    )

                    print("---------------")
                    print(self.notPresent)
                    print(self.errImg)
                    print(self.isSleeping)
                    print(self.faceRecognition)
                    print("---------------")
                elif value.get("type") == "accessibility":
                    self.transcribe = settings.get(
                        "audioTranscriber", self.transcribe
                    )
                    self.toggle_audio_thread()

                    print("---------------")
                    print(self.asl_regconition)
                    print(self.transcribe)
                    print("---------------")
                elif value.get("type") == "audio":
                    self.controlMic = settings.get(
                        "muteAudioWhenVideoIsDisabled", self.controlMic
                    )
                    print("---------------")
                    print(self.controlMic)
                    print("---------------")
                else:
                    pass
                self.lock.release()
        except Empty:
            pass
    
    def toggle_audio_thread(self):
        if not self.speech_thread:
            if self.transcribe:
                self.speech_thread = Thread(target=main, args=(self.transcript_queue,), daemon = True)
                self.speech_thread.start()
        else:
            if self.transcribe:
                self.speech_thread.__exit__()

    def start(self, message_queue):
        self.message_queue = message_queue
        # Use OpenCV to grab the webcam video feed
        video_feed = cv.VideoCapture(0)
        
        
        
        if self.transcribe:
            self.speech_thread = Thread(target=main, args=(self.transcript_queue,))
            self.speech_thread.start()
            
            
            
        # Check if the webcam can be opened
        if (video_feed.isOpened() == False):
            return "ERROR - Could not connect to webcam!!!"

        with pyvirtualcam.Camera(width=IMG_W, height=IMG_H, fps=30) as cam:
            counter = 0
            while True:

                frame = self.processFrame(video_feed, counter)

                counter = (counter + 1, 0)[counter == 30]
                
                if counter == 29:
                    self.sync_config()

                # Send to virtual cam
                cam.send(frame)

                # Wait until it's time for the next frame
                cam.sleep_until_next_frame()

        cv.waitKey(0)
        video_feed.release()
        

    def processFrame(self, video_feed, counter, isPython=False):
        # Read the frame from the webcam
        isTrue, frame = video_feed.read()

        if counter % 5 == 0:
            if (
                self.updateShouldShowCame(
                    frame, counter == 30 and self.face_recognizer is not None
                )
                == False
            ):
                frame = self.getBlockFrame(frame, self.notPresent)

                if self.startLookAwayTime is None:
                    self.startLookAwayTime = datetime.now()

            elif self.blockFrame is not None:
                self.blockFrame = None

                if self.startLookAwayTime is not None:
                    writeTimeFrame(self.startLookAwayTime, datetime.now())
                    self.startLookAwayTime = None

                if self.controlMic:
                    turnOnMic()
        elif self.blockFrame is not None:
            frame = self.blockFrame
            cv.flip(frame, -1)

        # If we are pushing to OBS convert to RGBA
        if isPython == False:
            frame = convert2RGBA(frame)

        if self.transcribe:
            if self.transcript_queue.qsize() > 0:
                self.transcript_curr_message = self.transcript_queue.get()
                self.transcript_curr_message = textwrap.wrap(
                    self.transcript_curr_message, width=30
                )
                self.transcriptTimeout = 0

            if self.transcriptTimeout is not None:
                if self.transcriptTimeout < 2 * 15 * len(self.transcript_curr_message):
                    for i, v in enumerate(self.transcript_curr_message):
                        frame = cv.putText(
                            frame,
                            v.strip(),
                            (
                                20,
                                IMG_H
                                - (len(self.transcript_curr_message) * 25)
                                + (20 * (i) + (5 * i)),
                            ),
                            cv.FONT_HERSHEY_SIMPLEX,
                            0.8,
                            (255, 255, 255),
                            2,
                            cv.LINE_AA,
                        )

                self.transcriptTimeout += 1

        return frame

    def updateShouldShowCame(self, frame, checkFace):
        if (
            self.notPresent == False
            and self.isSleeping == False
            and checkFace == False
            and self.NotUser == False
        ):
            return True

        # Convert the frame to grayscale
        frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Grab all the faces found
        face_rects = self.face_cascade.detectMultiScale(
            frame_gray, scaleFactor=1.2, minNeighbors=10
        )

        # Check based on restrictions passed in if conditions to turn off are met
        shouldTurnOff = False

        if checkFace:
            for (x, y, w, h) in face_rects:
                faces_roi = frame_gray[y : y + h, x : x + w]
                label, confidence = self.face_recognizer.predict(faces_roi)

                if label != 1:
                    self.NotUser = True
                    return False
                else:
                    self.NotUser = False
        elif self.NotUser == True:
            return False

        # If user is not present turn off the webcam
        if self.notPresent and len(face_rects) < 1:
            shouldTurnOff = True

        if (
            shouldTurnOff == False
            and self.isSleeping
            and self.detectSleeping(face_rects, frame_gray)
        ):
            shouldTurnOff = True

        self.notPresentCounter = (0, self.notPresentCounter + 1)[shouldTurnOff]

        return self.notPresentCounter < ERROR_THRESHOLD

    def getBlockFrame(self, frame, notPresent):
        if self.blockFrame is not None:
            return self.blockFrame

        if self.errImg is not None:
            self.blockFrame = self.errImg
        else:
            self.blockFrame = cv.blur(frame, (131, 131))

            if notPresent:
                self.blockFrame = cv.putText(
                    self.blockFrame,
                    "LEFT THE SCREEN",
                    (50, 50),
                    cv.FONT_HERSHEY_SIMPLEX,
                    1.5,
                    (255, 255, 255),
                    2,
                    cv.LINE_AA,
                )

        # Turn off the mic
        if self.controlMic:
            turnOffMic()

        return self.blockFrame

    def detectSleeping(self, faces_rect, frame_gray):
        # Check if there was a face that was detected
        if len(faces_rect) < 0:
            return False

        for (x, y, w, h) in faces_rect:
            # Get the ROI of the image
            roi = frame_gray[y : y + h, x : x + w]

            oeyes = self.open_eyes_cascade.detectMultiScale(roi, 1.3, 30)
            reyes = self.right_eyes_cascade.detectMultiScale(roi, 1.3, 20)
            leyes = self.left_eyes_cascade.detectMultiScale(roi, 1.3, 20)

            if (len(leyes) != 0 or len(reyes) != 0) and len(oeyes) == 0:
                return True

        return False

    def startPython(self):
        # Use OpenCV to grab the webcam video feed
        video_feed = cv.VideoCapture(0)

        # Check if the webcam can be opened
        if video_feed.isOpened() == False:
            return "ERROR - Could not connect to webcam!!!"

        counter = 0
        while True:
            frame = self.processFrame(video_feed, counter, isPython=True)

            counter = (counter + 1, 0)[counter == 30]

            cv.imshow("Title", frame)
            cv.waitKey(1)

        cv.waitKey(0)
        video_feed.release()
        writeTimeFrame(None, datetime.now())


def toggleMic(val):
    win32api.SendMessage(-1, WM_APPCOMMAND, 0x30292, val * 0x10000)


def turnOffMic():
    thread = Thread(target=toggleMic, args=([APPCOMMAND_MIC_MIN]))
    thread.start()


def turnOnMic():
    thread = Thread(target=toggleMic, args=([APPCOMMAND_MIC_MAX]))
    thread.start()


def appendToCSV(startTime, endTime):
    print("Append to csv")
    with open(
        str(pathlib.Path(__file__).resolve().parent) + "./Data/ConcentrationData.csv",
        "a+",
        newline="",
    ) as file:
        csvWriter = csv.writer(file, delimiter=",")
        csvWriter.writerow([startTime, endTime])


def createCSV():
    with open(
        str(pathlib.Path(__file__).resolve().parent) + "./Data/ConcentrationData.csv",
        "w+",
        newline="",
    ) as file:
        csvWriter = csv.writer(file, delimiter=",")
        csvWriter.writerows([["StartTime", "EndTime"], [datetime.now(), None]])


def writeTimeFrame(startTime, endTime):
    thread = Thread(target=appendToCSV, args=([startTime, endTime]))
    thread.start()


def convert2RGBA(frame):
    # convert to RGBA
    out_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    out_frame_rgba = np.zeros((IMG_H, IMG_W, 4), np.uint8)
    out_frame_rgba[:, :, :3] = out_frame
    out_frame_rgba[:, :, 3] = 255
    return out_frame_rgba


if __name__ == "__main__":
    t = VirtualWebcam(
        notPresent=True,
        isSleeping=True,
        errImgPath="ErrorImage.png",
        controlMic=False,
        faceRecognition=False,
    )
    #t.startPython()
    t.start()

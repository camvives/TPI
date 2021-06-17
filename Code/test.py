import face_recognition
import cv2
import glob
import os

video_capture = cv2.VideoCapture("img\President Barack Obama's Commencement Speech _ Dear Class Of 2020_Trim.mp4")

face_locations = []
face_encodings = []


process_this_frame = True
while True:
    ret, frame = video_capture.read()
    small_frame = cv2.resize(frame, (0, 0), fx=0.70, fy=0.70)

    print(small_frame)

    #Invertir colores
    rgb_frame = small_frame[:,:,::-1]

    print(rgb_frame)

    if process_this_frame:
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    process_this_frame = not process_this_frame

    # for top, right, bottom, left in face_locations:
    #     # Scale back up face locations since the frame we detected in was scaled to 1/4 size
    #     top *= 4
    #     right *= 4
    #     bottom *= 4
    #     left *= 4

    #     # Draw a box around the face
    #     cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

    #     # Draw a label with a name below the face
    #     cv2.rectangle(frame, (left, top - 20), (right, top), (0, 0, 255), cv2.FILLED)

    
    cv2.imshow('Video', frame)
    cv2.waitKey(0)

    
video_capture.release()

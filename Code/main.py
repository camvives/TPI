import face_recognition
import cv2

face_locations = []
face_encodings = []

video_capture = cv2.VideoCapture("img\pexels-kampus-production-8348919.mp4")
success, frame = video_capture.read()
cv2.imwrite("imagenes\\frame_extraido.jpg", frame)

small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

face_locations = face_recognition.face_locations(small_frame)
face_encodings = face_recognition.face_encodings(small_frame, face_locations)

for top, right, bottom, left in face_locations:
    cv2.rectangle(small_frame, (left-15, top-35), (right+15, bottom+15), (0, 0, 255), 2)

cv2.imshow('Video', small_frame)
cv2.waitKey()
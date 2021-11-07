import os
import cv2
import face_recognition as fr
from blog.save_csv import write_attendance
from flask_login import current_user
from flask import flash


def face_recognizer():
    path = 'blog/static/faces/' + current_user.username

    try:
        img_list = os.listdir(path)
        img_locations = []

        for fn in img_list:
            pname = path + '/' + fn
            img_locations.append(pname)

        for img in img_locations:
            video_capture = cv2.VideoCapture(0)
            user_image = fr.load_image_file(img)
            encodings = fr.face_encodings(user_image)

            if len(encodings) > 0:
                user_face_encoding = encodings[0]
                known_face_encodings = [user_face_encoding]
                known_face_names = [current_user.full_name]

                while True:
                    ret, frame = video_capture.read()
                    rgb_frame = frame[:, :, ::-1]

                    face_locations = fr.face_locations(rgb_frame)
                    face_encodings = fr.face_encodings(rgb_frame, face_locations)

                    for (top, right, bottom, left), name in zip(face_locations, face_encodings):
                        for face_encoding in face_encodings:
                            matches = fr.compare_faces(known_face_encodings, face_encoding)
                            name = "Random Person"

                            if True in matches:
                                first_match_index = matches.index(True)
                                name = known_face_names[first_match_index]

                            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                            cv2.rectangle(frame, (left, bottom - 30), (right, bottom), (0, 0, 255), cv2.FILLED)
                            font = cv2.FONT_HERSHEY_DUPLEX
                            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.7, (255, 255, 255), 1)

                            try:
                                if (name != "Random Person"):
                                    if cv2.waitKey(1) & 0xFF == ord('p'):
                                        write_attendance()
                                        quit()
                            except:
                                return None

                    cv2.imshow('Video', frame)
                    try:
                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            quit()
                    except:
                        return None
    except FileNotFoundError:
        flash('This application is running on a development server.\
                So you must restart the server to use this feature.', 'warning')
        
        return None

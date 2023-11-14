import face_recognition
import os, sys
import cv2
import numpy as np
import math
import serial
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

serA = serial.Serial('/dev/ttyACM0', 9600,timeout = 0.1)
ser = serial.Serial(
        port='/dev/ttyS0', #Replace ttyS0 with ttyAM0 for Pi1,Pi2,Pi0
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout = 0.1
        )
        

dem = 0

# Setup port number and server name
smtp_port = 587                 # Standard secure SMTP port
smtp_server = "smtp.gmail.com"  # Google SMTP Server
# Set up the email lists
email_from = "vip24092007@gmail.com"
email_list = ["vip24092007@gmail.com"]
# Define the password
pswd = "bxvqqaynhwrbwtmd" 

# name the email subject
subject = "⚠⚠⚠[WARNING] CÓ AI ĐÓ VÀO NHÀ BẠN⚠⚠⚠"

# Define the email function 
def send_emails(email_list):

    for person in email_list:

        # Make the body of the email
        body = f"""
        Chân dung kẻ lạ mặt:
        """

        # make a MIME object to define parts of the email
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # Attach the body of the message
        msg.attach(MIMEText(body, 'plain'))

        # Define the file to attach
        filename = "saved_img.jpg"

        # Open the file in python as a binary
        attachment= open(filename, 'rb')  # r for read and b for binary

        # Encode as base 64
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)

        # Cast as string
        text = msg.as_string()

        # Connect with the server
        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()


        # Send emails to "person" as list is iterated
        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

    # Close the port
    TIE_server.quit()

# Helper
def face_confidence(face_distance, face_match_threshold=0.6):
    range = (1.0 - face_match_threshold)
    linear_val = (1.0 - face_distance) / (range * 2.0)

    if face_distance > face_match_threshold:
        return str(round(linear_val * 100, 2)) + '%'
    else:
        value = (linear_val + ((1.0 - linear_val) * math.pow((linear_val - 0.5) * 2, 0.2))) * 100
        return str(round(value, 2)) + '%'


class FaceRecognition:
    face_locations = []
    face_encodings = []
    face_names = []
    known_face_encodings = []
    known_face_names = []
    process_current_frame = True

    def __init__(self):
        self.encode_faces()

    def encode_faces(self):
        for image in os.listdir('faces'):
            face_image = face_recognition.load_image_file(f"faces/{image}")
            face_encoding = face_recognition.face_encodings(face_image)[0]

            self.known_face_encodings.append(face_encoding)
            self.known_face_names.append(image)
        print(self.known_face_names)

    def run_recognition(self):
        kiemtra = "NGUOI LA" 
        dem = 0
        video_capture = cv2.VideoCapture(0)
        
        frame_width = int(round(video_capture.get(3)))
        frame_height = int(round(video_capture.get(4)))
        fps = int(round(video_capture.get(5)))
        index = 0
        kt1 = 0
        out = cv2.VideoWriter( str(index) +'.avi',cv2.VideoWriter_fourcc('M','J','P','G') , fps, (frame_width, frame_height))
        if not video_capture.isOpened():
            sys.exit('Video source not found...')

        while True:
            ret, frame = video_capture.read()
            
            
            person = ser.readline().decode('utf-8').strip()
            cb = serA.readline().decode('utf-8').strip()

            if cb == "KHONG CO NGUOI":
                kiemtra = "NGUOI LA"
                print("KHONG CO NGUOI LA 1")
                file1 = open("buzzerData.txt","w")
                file1.write("0")
                file1.close()
                print("kt1 = ",kt1)
                if kt1 == 1:
                    out.release()
                    index = index + 1
                    print("video thu: ",index)
                    out = cv2.VideoWriter( str(index) +'.avi',cv2.VideoWriter_fourcc('M','J','P','G') , fps, (frame_width, frame_height))
                    kt1 = 0
                dem = 0

            # Only process every other frame of video to save time
            if self.process_current_frame:
                # Resize frame of video to 1/4 size for faster face recognition processing
                small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

                # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
                rgb_small_frame = small_frame[:, :, ::-1]

                # Find all the faces and face encodings in the current frame of video
                self.face_locations = face_recognition.face_locations(rgb_small_frame)
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)

                self.face_names = []
                for face_encoding in self.face_encodings:
                    # See if the face is a match for the known face(s)
                    matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    name = "Unknown"
                    confidence = '???'

                    # Calculate the shortest distance to face
                    face_distances = face_recognition.face_distance(self.known_face_encodings, face_encoding)

                    best_match_index = np.argmin(face_distances)
                    if matches[best_match_index]:
                        name = self.known_face_names[best_match_index]
                        confidence = face_confidence(face_distances[best_match_index])

#                     print(name,' ',confidence)
                    
                    if name == "Unknown" or float(confidence.strip("%")) <= 90.00:
                        cv2.imwrite(filename = 'saved_img.jpg', img = frame)
                        kiemtra = "NGUOI LA"
                    else: 
                        kiemtra = "CHU NHA"

                    self.face_names.append(f'{name} ({confidence})')

            self.process_current_frame = not self.process_current_frame

            # Display the results
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                # Scale back up face locations since the frame we detected in was scaled to 1/4 size
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4

                # Create the frame with the name
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.8, (255, 255, 255), 1)
            #print(cb,' ', person, ' ',kiemtra)
            #print(cb)
            person = person[0:6]
            if (cb == "CO NGUOI" and person == "PERSON" and kiemtra == "NGUOI LA"):
                print("CO NGUOI LA")
                file1 = open("buzzerData.txt","w")
                file1.write("1")
                file1.close()
                print("dem: ", dem)
                print("kt1 = ",kt1)
                out.write(frame)
                #ser.write("RECORD".encode('utf-8'))
                kt1 = 1
                dem = dem + 1
                if dem == 1:
                    send_emails(email_list)
            elif (kiemtra == "CHU NHA" or person != "PERSON") and (cb == "CO NGUOI") and (person != ""):
                print("test: ",kiemtra, ' ', person,' ',cb)
                print("KHONG CO NGUOI LA")
                file1 = open("buzzerData.txt","w")
                file1.write("0")
                file1.close()
                print("kt1 = ",kt1)
                if kt1 == 1:
                    out.release()
                    index = index + 1
                    print("video thu: ",index)
                    out = cv2.VideoWriter( str(index) +'.avi',cv2.VideoWriter_fourcc('M','J','P','G') , fps, (frame_width, frame_height))
                    kt1 = 0
                #ser.write("STOP_RECORD".encode('utf-8'))
                dem = 0


            serA.write("1".encode('utf-8'))

            # Display the resulting image
            cv2.imshow('Face Recognition', frame)

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    fr = FaceRecognition()
    fr.run_recognition()

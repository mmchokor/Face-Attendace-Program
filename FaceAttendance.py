import cv2
import numpy as np
import face_recognition
import os
import time
from datetime import datetime
# imports for the email part
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


# A function that take parameter the image from the imagesAttendance folder and find
# the encoding for it and return it
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

# A function to get the info of the instructor, the first element is his/her name
# the second is the email address and the third elements is the course name
def getInstructorInfo():
    with open('Instructor_Info.txt') as info:
        infoArray = info.read().splitlines()
    infoArray[0] = infoArray[0].upper()
    return infoArray

# A function that take the name of the student as parameter and write it to
# the attendance.csv file with the time he entered the class
def markAttendance(name):
    with open('Attendance.csv', 'r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name},{dtString}')

# A function to send the attendance.csv file to the instructors email using 
# the info that he/she enter in the txt file and scanned by the program
def sendingEmail(InstructorsInfo):
    email_user = 'cmps327chokor@gmail.com'
    email_password = 'CMPS-327'
    email_send = InstructorsInfo[1]

    today = datetime.now().date()
    today = str(today)
    subject = InstructorsInfo[2] + ' attendance - ' + today

    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = InstructorsInfo[2] + ' attendance - ' + today
    msg.attach(MIMEText(body, 'plain'))

    filename = 'Attendance.csv'
    attachment = open(filename, 'rb')

    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email_user, email_password)

    server.sendmail(email_user, email_send, text)
    server.quit()

# A function that will be executed right before exiting the program
# to clean the Attendance.csv file to be used again in another session
def exitFunction():
    print("Reseting the Attendance.csv file")
    with open('Attendance.csv', 'w') as f:
        f.write('Name, Time')
    print("Attendance.csv has been reseted")
    print("Exiting Program")
    exit()



# Loading All images and printing class roaster
path = 'ImagesAttendance'
images = []
classNames = []
myList = os.listdir(path)
print(myList)
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])
print(classNames)

# Encoding all the previously loaded images
InstructorsInfo = getInstructorInfo()
encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Opening the webcam
cap = cv2.VideoCapture(0)

# This while loop is to compare the scanned faces from the database with the faces that are
# being Scanned by the webcam and marking the attendance of the students if found and it also 
# localise the face in the camera app and show us the name below the face
while True:
    success, img = cap.read()
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        # print(faceDis)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex]:
            name = classNames[matchIndex].upper()
            # print(name)
            if name == InstructorsInfo[0]:
                # here a fucntion will be added to send the csv file to the dr and clear it
                sendingEmail(InstructorsInfo)
                exitFunction()

            markAttendance(name)
        else:
            name = 'Unknown'
        y1, x2, y2, x1 = faceLoc
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, name, (x1+6, y2-6),
                    cv2.FONT_HERSHEY_COMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Chokors Attendance Camera', img)
    cv2.waitKey(1)

# Mohamed Hammoud Ahmed Chokor
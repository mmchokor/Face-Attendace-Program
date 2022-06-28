# CMPS327---Project

## [Documentation](./CMPS327%20-%20Project%20Report%20(Face%20Attendance)%20-%20Mohamed%20Hammoud%20Ahmed%20Chokor.docx)

**Version 1.0**

## Project Objective

The objective of the project is to create a program that assists University Doctors and teaching assistants with taking student attendance. It will scan students' faces using the camera connected to the device on which the program is running, it will find the face in the video and encode it into data that will be compared with the encoding of the images present in the program database, upon detecting the facial identification, it will save the student's name together with the time he entered the class in a csv file that will be sent to the teacher via Email, after the software is closed by scanning the instructors face.

---

## How to Use

1. Install all the packages listed in the "Python Packages Used" section in this README

2. Copy the images of the students and the instructor faces to the "ImagesAttendace" folder. The image need to be jpg, and each image has to have the name of the student.

3. Put the information of the instructor in the "Instructor_Info.txt" file.
    The order of the info:
    1. The name of the instructor
    2. The email of the instructor
    3. The course name/code

4. Execute the program (FaceAttendance.py) and put it in a place so the students can get their face scanned.

5. To exit the program, let the webcam scan the instructor face, and the email will be sent to them.

---

## Python Packages Used

- numpy
- time
- cmake
- opencv-contrib-python
- dlib
- face_recognition
- secure-smtplib

---

## Contributors

- Mohamed-Hammoud Ahmed Chokor <mohameddd701@gmail.com>

---

## License & Copyright

© Mohamed-Hammoud Ahmed Chokor
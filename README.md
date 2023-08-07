# Facial_Recognition_Final
Facial_Recognition_Final


Steps:

1. Clone the Github repository in required directory.

2. Create a python 3.8 environment.

3. Navigate to directory with the program.

4. Upload all pics to be used for facial recognition in the folder
“Training_images” in the directory.

5. Install requirements using: pip install -r requirements.txt

6. Open the project in Spyder or PyCharm.


WORKING OF THE PROJECT:
encode.py: This code generates face encodings for a given dataset of images that are stored in the folder
‘training_images’. Face encodings are numerical representations of facial features. These are stored in a csv folder to be
used later on for face matching.

client.py: This is the code to be run on the raspberry pi client. This program when run, captures the image of the face to be
authenticated and creates a face encoding of the live image. Then it sends the encoding as JSON packets to the server. Then
it waits for the response from the server and displays the result along with the image of the face in a square.

server.py: This code is to be run on the server. As the code is run, it constantly waits for a message from the client that is
sent using a JSON packet that consists of the face encoding of the live image captured at stte along with the name. The
server then matches the live face encoding and sends back the response to the When a match is found, the server marks the
attendance of the recognized person in a CSV file, along with the timestamp of the recognition. If the face is a mismatch,
the image of the face is stored in ‘mismatch’ folder along with the timestamp.




VIDEO DEMONSTRATION
https://youtu.be/nMZUA6Ui2hw







key applications of the project:

Automated Authentication: The system can be used for secure access control to various facilities, such as offices,
buildings, or restricted areas. Users simply need to show their faces to the camera, and the system will match their face
with the pre-registered face encodings, granting access to authorized personnel only.

Contactless Attendance Tracking: In educational institutions, workplaces, or events, the system can be employed to
record attendance without requiring physical contact or sign-in sheets. Participants or employees can be recognized
automatically as they enter or leave the premises, enabling an efficient and accurate attendance tracking process.

Time and Cost Savings: By automating the authentication and attendance process, the system reduces the need for
manual registration and monitoring. This saves time for both administrators and attendees, as well as minimizing the
resources required for managing attendance records.

Enhanced Security: Face recognition offers a higher level of security compared to traditional methods like ID cards or
passwords, which can be forged or stolen. Since each individual's face is unique, the chances of unauthorized access are
significantly reduced, enhancing overall security

The aim of the project is to create a facial
recognition system to allow for the verification
of employees after an ID card with RFID is
used as identification.

The facial recognition system is running on the
backend and the hardware used for scanning the
ID card and face of the employees is placed on the
site where it is to be deployed.

The application is coded using Python
programming language. The code majorly uses
open-cv and face-recognition libraries for
facial recognition using machine learning. The
hardware device used on the front end is a
Raspberry Pi 4 with a camera and a RFID
sensor.

The Web Service for client-server
communication is to be created using Java

OpenCV (Open Source Computer Vision Library) is an open source computer vision and machine
learning software library. OpenCV was built to provide a common infrastructure for computer vision
applications and to accelerate the use of machine perception in the commercial products.

The library has more than 2500 optimized algorithms, which
includes a comprehensive set of both classic and state-of-the-art
computer vision and machine learning algorithms.

These algorithms can be used to detect and recognize faces,
identify objects, classify human actions in videos, track camera
movements, track moving objects, extract 3D models of objects,
produce 3D point clouds from stereo cameras, stitch images
together to produce a high resolution image of an entire scene,
find similar images from an image database, remove red eyes
from images taken using flash, follow eye movements,
recognize scenery and establish markers to overlay it with
augmented reality, etc.




Face-Recognition library:

Recognizes and manipulates faces from Python or from the command line.

Built using dlib’s state-of-the-art face recognition built with deep learning. The model has an accuracy of 99.38% on
the Labeled Faces in the Wild benchmark. This also provides a simple face_recognition command line tool that lets you
do face recognition on a folder of images from the command line.





silent-face-anti-spoofing library:

The silent face anti-spoofing detection model is used to
determine if the face in an image is real or fake.

It is designed to prevent people from tricking facial
identification systems, such as those used for unlocking
phones or accessing secure locations. This is achieved
through a process called "liveness" or "anti-spoofing"
which judges whether the face presented is genuine or not.

The face presented by other media can be defined as a fake:
photo prints of faces, faces on phone screens, silicone
mask, 3D human image, etc.

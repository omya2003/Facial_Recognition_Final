import base64
import csv
import face_recognition
import numpy as np
import cv2
import os
from datetime import datetime
# from ttest import test
import socket
import json
import threading

def markAttendance(name):
    with open('/media/omi/a1/facerecog/face_recog_final/Attendance.csv', 'r+') as f:
        myDataList = f.readlines()

        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
            if name not in nameList:
                now = datetime.now()
                dtString = now.strftime('%H:%M:%S')
                f.writelines(f'\n{name},{dtString}')

def handleClient(client_socket):
    json_data = b''
    while True:
        data1 = client_socket.recv(1024)
        if not data1:
            break

        if b"END_OF_TRANSMISSION" in data1:
            # Remove the "END_OF_TRANSMISSION" message from the chunk
            data1 = data1.replace(b"END_OF_TRANSMISSION", b"")

            # Accumulate the received data
            json_data += data1
            break  # Break the loop since we have received all the data

        json_data += data1

    print(json_data)
    data = json.loads(json_data.decode())

    # Extract the name and image from the JSON data
    face_name = data["face_name"]
    image_base64 = data["image"]
    image_encoded = base64.b64decode(image_base64)
    # print(image_encoded)
    img = cv2.imdecode(np.frombuffer(image_encoded, dtype=np.uint8), cv2.IMREAD_COLOR)


    if img is None:
        print("Error: Failed to load the image.")
        exit()

    # Read the CSV file and retrieve the encoding for the specified face name
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if row['Name'] == face_name:
                known_encoding_str = row['Encoding']
                break
        else:
            print(f"Face name '{face_name}' not found in the CSV file.")
            known_encoding_str = None

    if known_encoding_str is not None:
        known_encoding = np.fromstring(known_encoding_str[1:-1], dtype=float, sep=' ')

        # desired_width = 800
        # desired_height = int(desired_width * 3 / 4)
        # imgS = cv2.resize(img, (desired_width, desired_height))
        # imgS = cv2.resize(img, (800, 600))

        # imgS = cv2.resize(img, (800, 600), None, 0.25, 0.25)
        # imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        # label = test(image=imgS,
        #              model_dir='/media/omi/a1/facerecog/Facial-Recognition-w-spoofing-detection/Silent-Face-Anti-Spoofing-master/resources/anti_spoof_models',
        #              device_id=0,
        #              )
        # if label == 1:
        #     image_to_test_encoding = face_recognition.face_encodings(imgS)[0]
        #     results = face_recognition.compare_faces([known_encoding], image_to_test_encoding)
        #     # print(results)
        #
        # else:
        #     print("Image captured is not live. Please try Again.")
        #     exit()

        # imgS = cv2.resize(img, (800, 600), None, 0.25, 0.25)
        imgS = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        image_to_test_encoding = face_recognition.face_encodings(imgS)[0]
        results = face_recognition.compare_faces([known_encoding], image_to_test_encoding)
        face_distances = face_recognition.face_distance([known_encoding], image_to_test_encoding)
        for i, face_distance in enumerate(face_distances):
            print("The test image has a distance of {:.2} from known image #{}".format(face_distance, i))
            print(
                "- With a normal cutoff of 0.6, would the test image match the known image? {}".format(
                    face_distance < 0.6))
            print("- With a very strict cutoff of 0.5, would the test image match the known image? {}".format(
                face_distance < 0.5))
            print()
        print(results)

    if results[0] == True:
        op="MATCH"
        print("        ███╗░░░███╗░█████╗░████████╗░█████╗░██╗░░██╗██╗")
        print("        ████╗░████║██╔══██╗╚══██╔══╝██╔══██╗██║░░██║██║")
        print("        ██╔████╔██║███████║░░░██║░░░██║░░╚═╝███████║██║")
        print("        ██║╚██╔╝██║██╔══██║░░░██║░░░██║░░██╗██╔══██║╚═╝")
        print("        ██║░╚═╝░██║██║░░██║░░░██║░░░╚█████╔╝██║░░██║██╗")
        print("        ╚═╝░░░░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░░╚════╝░╚═╝░░╚═╝╚═╝")
        x=255
        y=0
        now = datetime.now()
        print(f'Matched with : {face_name}, Time : {now} ')
        markAttendance(face_name)

    else:
        op="Mismatch!!!"
        print(op)
        x=0
        y=255
        mismatch_folder = "mismatch"
        if not os.path.exists(mismatch_folder):
            os.makedirs(mismatch_folder)
        mismatch_filename = os.path.join(mismatch_folder, face_name + '_mismatch.jpg')
        cv2.imwrite(mismatch_filename, img)
        face_name = "Unknown"

    facesCurFrame = face_recognition.face_locations(img)
    print(facesCurFrame[0])
    for faceCoordinates in facesCurFrame:
        y1, x2, y2, x1 = faceCoordinates
        # y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
        cv2.rectangle(img, (x1, y1), (x2, y2), (0, x, y), 2)
        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, x, y), cv2.FILLED)
        cv2.putText(img, face_name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Prepare the result to be sent as JSON
    processed_img_encoded = cv2.imencode('.jpg', img)[1].tobytes()
    processed_img_base64 = base64.b64encode(processed_img_encoded).decode('utf-8')
    result = {
        "result": op,
        "processed_image": processed_img_base64
    }
    json_result = json.dumps(result)

    # Send the JSON result back to the client
    client_socket.sendall(json_result.encode())
    client_socket.sendall(b"END_OF_TRANSMISSION")
    # Close the client socket
    client_socket.close()


# Server configuration
host = '0.0.0.0'  # Server IP address
port = 3000  # Server port number

filename = 'encodings.csv'
#face_name = 'Omi'

# Create a TCP/IP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the host and port
server_socket.bind((host, port))

# Listen for incoming connections
server_socket.listen(1)

print('Server listening on {}:{}'.format(host, port))

while True:
    try:
        # Accept a client connection
        print('Server is listening on port', port)
        client_socket, client_address = server_socket.accept()
        print('Client connected:', client_address)

        # Start a new thread to handle the client connection
        client_handler = threading.Thread(target=handleClient, args=(client_socket,))
        client_handler.start()

    except KeyboardInterrupt:
        print("Server stopped.")
        break


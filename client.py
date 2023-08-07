import socket
import json
import cv2
import numpy as np
import base64
from ttest import test

# Server configuration
server_host = '0.0.0.0'  # Server IP address
server_port = 3000  # Server port number

# Capture image using the camera
camera = cv2.VideoCapture(0)

ret, frame = camera.read()
if not ret:
     print("Error: Failed to capture image.")
     camera.release()
     exit()


imgS = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
label = test(image=imgS,
             model_dir='/media/omi/a1/facerecog/face_recog_final/Silent-Face-Anti-Spoofing-master/resources/anti_spoof_models',
             device_id=0,
             )
if label == 1:
  new_width = 640
  new_height = 480
  resized_image = cv2.resize(frame, (new_width, new_height))
  encoded_image = cv2.imencode('.jpg', resized_image)[1].tobytes()
  image_base64 = base64.b64encode(encoded_image).decode('utf-8')

else:
  print("Image captured is not live. Please try Again.")
  exit()


# Prepare the data to be sent as JSON
data = {
    "face_name": "Omi",
    "image": image_base64
}
json_data = json.dumps(data)
print(json_data)

# Create a TCP/IP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)



try:
    # Connect to the server
    client_socket.connect((server_host, server_port))



    # Send the JSON data to the server
    client_socket.sendall(json_data.encode())
    client_socket.sendall(b"END_OF_TRANSMISSION")
    print("Live Image Sent")

    # Receive the result from the server
    # result_data = client_socket.recv(4194304).decode()
    # result = json.loads(result_data)
    result_data = b''
    while True:
        result1 = client_socket.recv(1024)
        if not result1:
            break

        if b"END_OF_TRANSMISSION" in result1:
            # Remove the "END_OF_TRANSMISSION" message from the chunk
            result1 = result1.replace(b"END_OF_TRANSMISSION", b"")

            # Accumulate the received data
            result_data += result1
            break  # Break the loop since we have received all the data

        result_data += result1

    result = json.loads(result_data.decode())
    #print(result)
    # Extract the processed image from the result
    output = result["result"]
    print(output)
    processed_img_base64 = result["processed_image"]
    processed_img_encoded = base64.b64decode(processed_img_base64)
    processed_img = cv2.imdecode(np.frombuffer(processed_img_encoded, dtype=np.uint8), cv2.IMREAD_COLOR)

    # Display the processed image
    cv2.imshow("Processed Image", processed_img)
    cv2.waitKey(5000)

finally:
    # Close the client socket
    client_socket.close()

# Release the camera
# camera.release()
print('client closing ..  ')


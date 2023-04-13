import serial
import requests

arduino_port = 'COM4'  # Change this to the appropriate port for your system (e.g., /dev/ttyACM0 on Linux)
baud_rate = 9600
server_url = 'http://127.0.0.1:8000/api/v1/switchObjectState/'

ser = serial.Serial(arduino_port, baud_rate)

while True:
    data = ser.readline().decode('utf-8').strip()
    print(f'Received data from Arduino: {data}')

    payload = {'data': data}
    if data == "The button is being pressed":
        
      response = requests.post(server_url, json={"id":1})
      print(f'Server response: {response.status_code} - {response.text}')
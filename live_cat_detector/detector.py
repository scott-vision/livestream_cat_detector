import cv2
import time
import json
from ultralytics import YOLO
from twilio.rest import Client

def send_sms(message, client, from_phone_number, to_phone_number):
    """Send an SMS using Twilio."""
    try:
        client.messages.create(body=message, from_=from_phone_number, to=to_phone_number)
        print("SMS sent:", message)
    except Exception as e:
        print("Failed to send SMS:", e)

def main():
    # Load configuration from config.json
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except Exception as e:
        print("Error loading config.json:", e)
        return

    # Extract configuration values
    account_sid = config["twilio"]["account_sid"]
    auth_token = config["twilio"]["auth_token"]
    to_phone_number = config["twilio"]["to_phone_number"]
    from_phone_number = config["twilio"]["from_phone_number"]
    stream_url = config["stream"]["url"]
    model_path = config["yolo"]["model_path"]
    cat_class_id = config["yolo"]["cat_class_id"]

    # Set up Twilio client and YOLO model
    client = Client(account_sid, auth_token)
    model = YOLO(model_path)

    # Open the video stream
    cap = cv2.VideoCapture(stream_url)
    if not cap.isOpened():
        print("Error: Could not open video stream.")
        return

    try:
        while True:
            # Check every 10 seconds
            time.sleep(10)
            
            ret, frame = cap.read()
            if not ret:
                print("Warning: No frame received, trying again...")
                continue

            # Run YOLO inference on the frame
            results = model(frame)
            cat_detected = False

            # Check if a cat is detected (using the given class ID)
            for result in results:
                for box in result.boxes:
                    if int(box.cls.item()) == cat_class_id:
                        cat_detected = True
                        break
                if cat_detected:
                    break

            if cat_detected:
                send_sms("Cat detected in the livestream!", client, from_phone_number, to_phone_number)
            else:
                print("No cat detected at this time.")

    except KeyboardInterrupt:
        print("Terminating the monitoring loop.")

    finally:
        cap.release()

if __name__ == "__main__":
    main()

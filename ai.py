import cv2
import asyncio
import requests
import time

# Server address
server_address = "http://10.0.101.122:49000"  # Change to your server's IP address

class Ai:
    def __init__(self):
        # Camera setup
        self.camera_index = 0  # Change the index if needed

    def capture_and_flip(self):
        """
        Captures an image from the camera and flips it upside down (180 degrees).
        """
        cap = cv2.VideoCapture(self.camera_index)
        if not cap.isOpened():
            raise Exception("Unable to access the camera")
        ret, frame = cap.read()
        cap.release()
        if not ret:
            raise Exception("Error capturing frame")
        # Flip the image upside down (horizontal and vertical flip)
        flipped = cv2.flip(frame, -1)
        return flipped

    def send_image_to_api(self, image, endpoint):
        """
        Sends the image to the server API for analysis.
        """
        # Convert image to JPEG format
        ret, buffer = cv2.imencode('.jpg', image)
        if not ret:
            raise Exception("Error encoding image to JPEG")
        
        # Prepare the image to be sent in the POST request
        files = {'file': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
        try:
            # Send image to the server API
            response = requests.post(f"{server_address}{endpoint}", files=files)
            return response.json()
        except Exception as e:
            print("Error sending request:", e)
            return None

    def e_recog(self):
        """
        Emotion recognition.
        Captures an image, sends it to the API for emotion recognition,
        and returns:
        - True if aggression is detected,
        - False if no aggression is detected,
        - None if no face is detected.
        """
        image = self.capture_and_flip()
        result = self.send_image_to_api(image, "/recognize/emotion")
        if result and result.get("status") == "success":
            if result.get("data", {}).get("aggression_detected"):
                return True
            return False
        return None

    def f_comp(self):
        """
        Face comparison.
        Captures an image, sends it to the API for face comparison,
        and returns:
        - The seat number if the face is recognized,
        - False if the face is not in memory (not matched),
        - None if no face is detected.
        """
        image = self.capture_and_flip()
        result = self.send_image_to_api(image, "/compare/faces")
        if result and result.get("status") == "success":
            return result.get("data", {}).get("seat")
        if result and result.get("status") == "not_found":
            return False
        return None

    def p_recog(self):
        """
        Passport recognition.
        Captures an image, sends it to the API for passport recognition,
        and returns:
        - The seat number if the passport is recognized,
        - False if the passport is not recognized.
        """
        image = self.capture_and_flip()
        result = self.send_image_to_api(image, "/recognize/passport")
        if result and result.get("status") == "success":
            return result.get("data", {}).get("seat")
        return False

# Example usage
if __name__ == "__main__":
    ai_instance = Ai()
    
    # Emotion recognition
    try:
        emotion = ai_instance.e_recog()
        print("Aggression detected (Emotion):", emotion)
    except Exception as e:
        print("Error in emotion recognition:", e)
        
    # Face comparison
    try:
        face_seat = ai_instance.f_comp()
        print("Face Comparison - Seat:", face_seat)
    except Exception as e:
        print("Error in face comparison:", e)
        
    # Passport recognition
    try:
        passport_seat = ai_instance.p_recog()
        print("Passport Recognition - Seat:", passport_seat)
    except Exception as e:
        print("Error in passport recognition:", e)

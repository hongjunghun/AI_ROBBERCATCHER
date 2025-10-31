import face_recognition
import os, time
import cv2
import serial

class Learining:

    def __init__(self):
        """self list and string setting"""
        self.known_names = []
        self.known_encodings = []
        self.matching = False
        self.criminal_name = []
        self.facing_name = ''
        self.foldername='training_images'

    def load_learn_images(self, foldername: str = 'training_images'):
        """load images and learn them"""
        folder_name = foldername
        self.foldername = foldername
        for name in os.listdir(folder_name):
            personal_dir = os.path.join(folder_name, name)
            for file in os.listdir(personal_dir):
                img_dir = os.path.join(personal_dir, file)
                image = face_recognition.load_image_file(img_dir)
                encodings = face_recognition.face_encodings(image)
                if len(encodings) > 0:
                    self.known_encodings.append(encodings[0])
                    self.known_names.append(name)
        print(f"[INFO] Finish learining faces")
    
    def comparefaces(self):
        """compare loaded images and computer vision faces"""
        cap=cv2.VideoCapture(0)
        known_encodings = self.known_encodings
        known_names = self.known_names
        while True:
            ret, frame = cap.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            find_face = face_recognition.face_locations(rgb_frame)
            live_encodings = face_recognition.face_encodings(rgb_frame, find_face)

            for (top, right, bottom, left), live_encoding in zip(find_face, live_encodings):
                matches = face_recognition.compare_faces(known_encodings, live_encoding)
                name = "Unknown"
                if True in matches:
                    index = matches.index(True)
                    name = known_names[index]
                    self.facing_name = known_names[index]

                    if self.facing_name in self.criminal_name:
                        self.arduino_boozer_sign()
                    
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,(0, 255, 0), 2)
            cv2.imshow("Face Recognition", frame)
            
            if cv2.waitKey(1) == ord("q"):
                break
        cap.release()
        cv2.destroyAllWindows()
        
    def arduino_boozer_sign(self, com: str = "COM7"):
        """arduino boozer ringing"""
        try:
            ser = serial.Serial(com, 9600, timeout=1)
            time.sleep(1)
            ser.write(b'boozer!!')

        except serial.SerialException:
            print("[INFO] Please, check arduino again")

    def setting_criminal_name(self, name: list):
        """set criminal name"""
        self.criminal_name = name
        if len(name) >= 2:
            print("[INFO] Set criminal name")
        elif len(name) == 1 or len(name) == 0:
            print("[INFO] Set criminal name(one or zero)")

    def capture(self, name: str, max_count: int = 30, interval: float = 1.0):
        save_dir = self.foldername

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
        
        persondir = os.path.join(save_dir, name)
        if not os.path.exists(persondir):
            os.makedirs(persondir)

        cap = cv2.VideoCapture(0)
        count = 0
        print(f"[INFO] Starting capture for {name}")

        while count < max_count:
            ret, frame = cap.read()

            cv2.imshow("Face Capture", frame)

            filename = os.path.join(persondir, f"{count + 1}.jpg")
            cv2.imwrite(filename, frame)
            print(f"[INFO] Saved → {filename}")
            cv2.putText(frame, str(count), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
            
            count += 1

            if cv2.waitKey(1) == ord('q'):
                print("[INFO] Capture manually stopped")
                break
            time.sleep(interval)

        print(f"[INFO] Finished capturing {count} images")
        cap.release()
        cv2.destroyAllWindows()

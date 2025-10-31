import face_recognition
import cv2
import os


known_encodings = []
known_names = []

folder_name = "test_images"

for name in os.listdir(folder_name):
    person_dir = os.path.join(folder_name, name)
    for file in os.listdir(person_dir):
        img_path = os.path.join(person_dir, file)
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if len(encodings) > 0:
            known_encodings.append(encodings[0])
            known_names.append(name)

print(f"[INFO] Finish learning {len(known_names)} faces")

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            index = matches.index(True)
            name = known_names[index]
        
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    cv2.imshow("Face Recognition", frame)
    if cv2.waitKey(1) == ord("q"):
        break 

cap.release()
cv2.destroyAllWindows()
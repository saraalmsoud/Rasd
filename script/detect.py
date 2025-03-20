import cv2
import numpy as np
import os
import datetime
import time
import random
import threading
import requests  # ✅ لإرسال الإشعارات عبر FCM
from ultralytics import YOLO
import firebase_admin
from firebase_admin import credentials, firestore
import cloudinary
import cloudinary.uploader
import json
import datetime
import random
# 🔹 Load Firebase settings
cred = credentials.Certificate("config/rasd-project.json")  
firebase_admin.initialize_app(cred)
db = firestore.client()

# 🔹 Load Firebase Cloud Messaging Key from config
with open("config/rasd-project.json") as f:
    firebase_config = json.load(f)

FCM_SERVER_KEY = firebase_config["fcm_server_key"]
FCM_URL = "https://fcm.googleapis.com/fcm/send"

# 🔹 Configure Cloudinary
cloudinary.config(
    cloud_name="dly2pgrct",
    api_key="488413976979647",
    api_secret="6vcgfU7_wLQIe7LYIDp4KS-wEcc"
)

# 🔹 دالة إرسال الإشعارات عبر FCM
import requests
import subprocess

def get_fcm_access_token():
    """ 🔹 استدعاء gcloud لجلب Access Token المطلوب لإرسال الإشعارات """
    result = subprocess.run(
        ["gcloud", "auth", "application-default", "print-access-token"],
        capture_output=True,
        text=True
    )
    return result.stdout.strip()

def send_fcm_notification(title, body):
    """ 🔹 إرسال الإشعار باستخدام Bearer Token الجديد """
    access_token = get_fcm_access_token()
    
    if not access_token:
        print("⚠️ Error: Failed to retrieve FCM Access Token!")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",  # ✅ استخدام Bearer Token
        "Content-Type": "application/json"
    }

    payload = {
        "message": {
            "topic": "accidents",
            "notification": {
                "title": title,
                "body": body
            }
        }
    }

    response = requests.post(
        "https://fcm.googleapis.com/v1/projects/rasd-project/messages:send",
        json=payload,
        headers=headers
    )

    if response.status_code == 200:
        print("✅ Notification sent successfully!")
    else:
        print(f"⚠️ Failed to send notification: {response.text}")
# 🔹 Load YOLO model
model_path = "Models/best_model.pt"  
model = YOLO(model_path)

# 🔹 Load video
video_path = "static/IMG_3646.MP4"
cap = cv2.VideoCapture(video_path)

# 🔹 Create folder for detected accidents if not exists
accidents_folder = "static/accidents"
os.makedirs(accidents_folder, exist_ok=True)

# 🔹 Define bounding box colors
severe_color = (250, 206, 135)
minor_color = (169, 169, 169)
font = cv2.FONT_HERSHEY_COMPLEX
font_scale = 1.2
font_thickness = 3
text_color = (255, 255, 255)

# 🔹 Cooldown settings to avoid duplicate detection
cooldown_time = 30  # Avoid capturing same accident within 30 seconds
last_capture_time = 0  
last_accident_positions = []  # Store last accident positions
position_threshold = 150  # Distance threshold to detect unique accidents

# 🔹 Function to generate a random location anywhere in Saudi Arabia


def generate_random_location():
    """ 🔹 توليد موقع عشوائي داخل السعودية لتفادي الأخطاء """
    cities = [
        {"name": "Riyadh", "lat": 24.7136, "lon": 46.6753},
        {"name": "Jeddah", "lat": 21.4858, "lon": 39.1925},
        {"name": "Mecca", "lat": 21.3891, "lon": 39.8579},
        {"name": "Medina", "lat": 24.5247, "lon": 39.5692},
        {"name": "Dammam", "lat": 26.3927, "lon": 49.9777},
        {"name": "Abha", "lat": 18.2465, "lon": 42.5117},
        {"name": "Tabuk", "lat": 28.3836, "lon": 36.5662},
        {"name": "Bisha", "lat": 19.9877, "lon": 42.6052}
    ]
    
    selected_city = random.choice(cities)
    lat_offset = random.uniform(-0.2, 0.2)
    lon_offset = random.uniform(-0.2, 0.2)

    return {
        "city": selected_city["name"],
        "lat": round(selected_city["lat"] + lat_offset, 6),
        "lon": round(selected_city["lon"] + lon_offset, 6)
    }
    


# ✅ دالة رفع الصورة إلى Cloudinary
def upload_image_to_cloudinary(image_path):
    try:
        response = cloudinary.uploader.upload(image_path)
        image_url = response.get("secure_url")  # ✅ استخراج رابط الصورة

        if image_url:
            print(f"✅ Image uploaded successfully: {image_url}")
            return image_url
        else:
            print("⚠️ Error: No secure_url found in response!")
            return None
    except Exception as e:
        print(f"⚠️ Error uploading image: {e}")
        return None

def save_accident_data(image_url, accident_type, location):
    if image_url is None:
        print("⚠️ Accident data was not saved due to image upload failure!")
        return None

    try:
        timestamp = datetime.datetime.now().isoformat()
        accident_data = {
            "image_url": image_url,
            "accident_type": accident_type,
            "location": location,  # ✅ الآن يتم حفظ الموقع
            "timestamp": timestamp,
            "status": "pending"
        }

        doc_ref = db.collection("accidents").add(accident_data)
        print(f"🚀 Accident recorded in Firestore: {doc_ref[1].id}")

        # ✅ تسجيل الإشعار في Firestore داخل مجموعة notifications
        notification_data = {
            "message": f"A {accident_type} occurred in {location['city']}.",
            "timestamp": timestamp
        }
        db.collection("notifications").add(notification_data)
        print("✅ Notification saved in Firestore.")

        # ✅ إرسال الإشعار عبر FCM
        send_fcm_notification(
            title="🚨 New Accident Detected!",
            body=f"A {accident_type} has been detected in {location['city']}."
        )

        return doc_ref
    except Exception as e:
        print(f"⚠️ Error saving accident data: {e}")
        return None
    
# 🔹 Function to update accident status after 10 minutes
def update_accident_status(doc_id):
    time.sleep(600)  # 600 seconds = 10 minutes
    try:
        db.collection("accidents").document(doc_id).update({"status": "resolved"})
        print(f"✅ Accident {doc_id} status updated to 'resolved'")

        # ✅ إرسال إشعار عند تغيير الحالة إلى "resolved"
        send_fcm_notification(
            title="✅ Accident Resolved",
            body=f"The accident with ID {doc_id} has been resolved."
        )

    except Exception as e:
        print(f"⚠️ Error updating status: {e}")

# 🔹 Start processing video
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame)
    current_time = time.time()

    result = results[0]  # ✅ تأكدنا إنه بيأخذ النتيجة الصحيحة
    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = float(box.conf[0])
        cls = int(box.cls[0])

        if conf > 0.5:
            accident_type = "Severe Accident" if cls == 0 else "Minor Accident"
            box_color = severe_color if accident_type == "Severe Accident" else minor_color
            label = f"{accident_type} {conf:.2f}"
            

            cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 3)
            cv2.putText(frame, label, (x1, y1 - 10), font, font_scale, text_color, font_thickness, cv2.LINE_AA)

            if current_time - last_capture_time > cooldown_time:
                last_capture_time = current_time
                img_filename = f"accident_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                img_path = os.path.join(accidents_folder, img_filename)
                cv2.imwrite(img_path, frame)

                # ✅ رفع الصورة إلى Cloudinary أولًا
                image_url = upload_image_to_cloudinary(img_path)

                # ✅ التأكد أن image_url ليس None قبل حفظ الحادث
                if image_url:
                    location = generate_random_location()  # 📌 توليد موقع للحادث
                    save_accident_data(image_url, accident_type, location)  # ✅ تمرير location هنا
                else:
                    print("⚠️ Error: Image URL is None, accident data not saved!")
                
    cv2.imshow("Accident Detection", frame)
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
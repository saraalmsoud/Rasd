import cv2

video_path = "static/IMG_3082.MP4"
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Video not found!")
    exit()

while True:
    ret, frame = cap.read()

    if not ret:
        print("Video playback finished.")
        break

    cv2.imshow("Video Stream", frame)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
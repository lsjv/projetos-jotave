import cv2
import mediapipe as mp
import pyautogui
import time
import math

pyautogui.FAILSAFE = True
screen_w, screen_h = pyautogui.size()

mp_face = mp.solutions.face_mesh
face = mp_face.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

prev_x, prev_y = screen_w // 2, screen_h // 2
smooth = 10

def distancia(a, b):
    return math.dist((a.x, a.y), (b.x, b.y))

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = face.process(img_rgb)

    if result.multi_face_landmarks:
        landmarks = result.multi_face_landmarks[0].landmark

        nariz = landmarks[1]   # ponta do nariz
        olho_sup = landmarks[159]
        olho_inf = landmarks[145]

        # Move mouse com nariz
        screen_x = int(nariz.x * screen_w)
        screen_y = int(nariz.y * screen_h)

        curr_x = prev_x + (screen_x - prev_x) / smooth
        curr_y = prev_y + (screen_y - prev_y) / smooth

        pyautogui.moveTo(curr_x, curr_y)
        prev_x, prev_y = curr_x, curr_y

        # Piscar = clique
        if distancia(olho_sup, olho_inf) < 0.01:
            pyautogui.click()
            time.sleep(0.3)

        # Debug visual
        for idx in [1, 159, 145]:
            x = int(landmarks[idx].x * w)
            y = int(landmarks[idx].y * h)
            cv2.circle(img, (x, y), 3, (0, 255, 0), -1)

    cv2.imshow("Mouse com o Rosto", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

import cv2
import mediapipe as mp
import pyautogui
import time

# Segurança
pyautogui.FAILSAFE = True

# Tela
screen_w, screen_h = pyautogui.size()

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
''
prev_x, prev_y = 0, 0
smooth = 7  # quanto maior, mais suave

def distancia(p1, p2):
    return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2) ** 0.5

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    h, w, _ = img.shape
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        hand = result.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(img, hand, mp_hands.HAND_CONNECTIONS)

        # Indicador
        ix, iy = hand.landmark[8].x, hand.landmark[8].y

        # Converte pra tela
        screen_x = int(ix * screen_w)
        screen_y = int(iy * screen_h)

        # Suavização
        curr_x = prev_x + (screen_x - prev_x) / smooth
        curr_y = prev_y + (screen_y - prev_y) / smooth

        pyautogui.moveTo(curr_x, curr_y)

        prev_x, prev_y = curr_x, curr_y

        # Pinça = clique
        thumb = hand.landmark[4]
        index = hand.landmark[8]

        if distancia(thumb, index) < 0.04:
            pyautogui.click()
            time.sleep(0.3)

    cv2.imshow("Mouse com a Mao", img)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

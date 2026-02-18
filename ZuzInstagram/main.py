import cv2
import numpy as np
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def preprocess_image(image, invert=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if invert:
        inverted = cv2.bitwise_not(gray)
        min_level = 20
    else:
        inverted = gray
        min_level = 230
    _, binary = cv2.threshold(inverted, min_level, 255, cv2.THRESH_BINARY)
    return binary


def is_on_deleted_page():
    counter = 0
    print("Step 'Ostatnio usunięte '!")
    while True:
        counter += 1
        screenshot = pyautogui.screenshot(region=(900, 80, 250, 90))
        # screenshot.save("debug_screen.png")
        # 6️⃣ OCR
        text = pytesseract.image_to_string(
            preprocess_image(np.array(screenshot), invert=True)
        )
        # print(f"Odczytany tekst: '{text.strip()}'")
        if "Ostatnio" in text:
            print("Znaleziono 'Ostatnio usunięte'!")
            break
        pyautogui.sleep(2)
        if counter % 10 == 0:
            pyautogui.press("esc")


while True:
    for i in [900, 1100, 1200]:
        # check ostatio usunięte
        is_on_deleted_page()
        # Odczytaj tekst

        pyautogui.sleep(0.1)
        pyautogui.click(i, 400)
        pyautogui.sleep(2)

        print("Step 'wiecej'!")
        # Odczytaj tekst
        while True:
            screenshot = pyautogui.screenshot(region=(1300, 980, 100, 40))
            # screenshot.save("debug_screen.png")
            # 6️⃣ OCR
            text = pytesseract.image_to_string(
                preprocess_image(np.array(screenshot), invert=True)
            )
            print(f"Odczytany tekst: '{text.strip()}'")
            if "Wiece" in text or "Wigce" in text:
                print("Znaleziono 'Wiecej'!")
                break
            pyautogui.sleep(2)

        pyautogui.click(1350, 940)
        print("Step 'Przywroc 1'!")

        # Odczytaj tekst
        while True:
            screenshot = pyautogui.screenshot(region=(830, 900, 180, 40))
            # screenshot.save("debug_screen.png")
            # 6️⃣ OCR
            text = pytesseract.image_to_string(preprocess_image(np.array(screenshot)))
            print(f"Odczytany tekst: '{text.strip()}'")
            if "Przywr" in text:
                print("Znaleziono 'Przywroc'!")
                break
            pyautogui.sleep(2)
        pyautogui.click(890, 928)
        # Odczytaj tekst
        print("Step 'Przywroc 2'!")
        while True:
            screenshot = pyautogui.screenshot(region=(1060, 600, 180, 40))
            # screenshot.save("debug_screen.png")
            # 6️⃣ OCR
            text = pytesseract.image_to_string(preprocess_image(np.array(screenshot)))
            print(f"Odczytany tekst: '{text.strip()}'")
            if "Przywr" in text:
                print("Znaleziono 'Przywroc'!")
                break
            pyautogui.sleep(2)
        pyautogui.click(1100, 630)
    is_on_deleted_page()
    pyautogui.moveTo(1020, 500)
    pyautogui.mouseDown()
    pyautogui.sleep(0.5)

    pyautogui.dragRel(0, -400, duration=0.5)
    pyautogui.sleep(0.3)
    pyautogui.mouseUp()
    pyautogui.moveTo(1020, 500)
    pyautogui.mouseDown()
    pyautogui.sleep(0.5)

    pyautogui.dragRel(0, -400, duration=0.5)
    pyautogui.sleep(0.3)
    pyautogui.mouseUp()

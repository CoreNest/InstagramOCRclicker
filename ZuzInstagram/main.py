import cv2
import numpy as np
import pyautogui
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

base_cords = [900, 1100, 1200]
instagram_window_x = []

screen_width, screen_height = pyautogui.size()


def my_print(*args, step=False, indent="    "):
    """
    Wypisuje tekst z wcięciem, chyba że step=True.
    - args: to co chcesz wydrukować
    - step: jeśli True, wypisuje bez wcięcia
    - indent: znak wcięcia (domyślnie 4 spacje)
    """
    text = " ".join(str(a) for a in args)
    if step:
        print(text)
    else:
        print(f"{indent}{text}")


def scroll():
    pyautogui.moveTo(base_cords[2], 500)
    pyautogui.mouseDown()
    pyautogui.sleep(0.5)

    pyautogui.dragRel(0, -400, duration=0.5)
    pyautogui.sleep(0.3)
    pyautogui.mouseUp()


def debug_screenshot(screenshot, filename="debug_screen.png"):
    pass
    # if not isinstance(screenshot, np.ndarray):
    #     screenshot.save(filename)
    # else:
    #     cv2.imwrite(filename, screenshot)


def znajdz_wspolrzedne(img, szukane_slowo, lang="pol"):
    """
    Funkcja zwraca współrzędne (x, y, szer, wys) słowa szukanego w obrazie.
    Jeśli słowo występuje wielokrotnie, zwraca listę wszystkich wystąpień.
    """
    data = pytesseract.image_to_data(
        img, lang=lang, output_type=pytesseract.Output.DICT
    )
    debug_screenshot(img, f"debug_{szukane_slowo}.png")
    wyniki = []

    for i in range(len(data["text"])):
        word = data["text"][i].strip()
        # print(f"Sprawdzam słowo: '{word}' z pewnością {data['conf'][i]}%")
        if word.lower() == szukane_slowo.lower() and int(data["conf"][i]) > 60:
            x = data["left"][i]
            y = data["top"][i]
            w = data["width"][i]
            h = data["height"][i]
            wyniki.append((x, y, w, h))

    return wyniki


def znajdz_wspolrzedne_middlepoint(img_path, szukane_slowo, lang="pol"):
    """
    Funkcja zwraca współrzędne środka (x, y) słowa szukanego w obrazie.
    Jeśli słowo występuje wielokrotnie, zwraca listę wszystkich środków.
    """
    results = znajdz_wspolrzedne(img_path, szukane_slowo, lang)
    middlepoints = []
    for x, y, w, h in results:
        middlepoints.append((x + w // 2, y + h // 2))
    return middlepoints


def preprocess_image(image, invert=False):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if invert:
        inverted = cv2.bitwise_not(gray)
        min_level = 50
    else:
        inverted = gray
        min_level = 210
    _, binary = cv2.threshold(inverted, min_level, 255, cv2.THRESH_BINARY)
    return binary


def is_on_deleted_page():
    counter = 0
    my_print("Step 'Ostatnio usunięte '!", step=True)
    while True:
        counter += 1
        screenshot = pyautogui.screenshot(region=(0, 70, screen_width, 110))
        debug_screenshot(screenshot)
        screenshot = preprocess_image(np.array(screenshot), invert=False)

        # 6️⃣ OCR
        results_ostanio = znajdz_wspolrzedne(screenshot, "Ostatnio", lang="pol")
        if len(results_ostanio) > 0:
            my_print(f"Znalezione współrzędne dla 'Ostatnio': {results_ostanio}")
        results_usuniete = znajdz_wspolrzedne(screenshot, "usunięte", lang="pol")
        if len(results_usuniete) > 0:
            my_print(f"Znalezione współrzędne dla 'usunięte': {results_usuniete}")
        if len(results_ostanio) > 0 and len(results_usuniete) > 0:
            my_print("Jesteśmy na stronie 'Ostatnio usunięte'!")
            global base_cords
            global instagram_window_x
            instagram_window_x = [
                results_ostanio[0][0] - results_ostanio[0][2],
                results_usuniete[0][0] + results_usuniete[0][2] * 3,
            ]
            base_cords = [
                results_ostanio[0][0],
                results_usuniete[0][0],
                results_usuniete[0][0] + results_usuniete[0][2] * 2,
            ]
            break
        pyautogui.sleep(2)
        if counter % 10 == 0:
            pyautogui.press("esc")


counter_resored_without_issue = 0
while True:
    for i in range(3):
        counter_resored_without_issue += 1
        my_print(f"Przywracanie posta {counter_resored_without_issue}!", step=True)
        # check ostatio usunięte
        is_on_deleted_page()
        # Odczytaj tekst

        pyautogui.sleep(0.1)
        pyautogui.click(base_cords[i], 400)
        pyautogui.sleep(2)

        my_print("Step 'wiecej'!", step=True)
        # Odczytaj tekst
        counter = 0
        while True:
            counter += 1
            screenshot = pyautogui.screenshot(
                region=(base_cords[1], 980, (base_cords[2] - base_cords[1]) * 2, 80)
            )
            debug_screenshot(screenshot)
            screenshot = preprocess_image(np.array(screenshot), invert=True)

            # 6️⃣ OCR
            middlepoints = znajdz_wspolrzedne_middlepoint(
                screenshot, "Więcej", lang="pol"
            )
            # my_print(f"Znalezione środki dla 'Wiecej': {middlepoints}")
            if middlepoints:
                my_print("Znaleziono 'Wiecej'!")
                pyautogui.click(
                    middlepoints[0][0] + base_cords[1], middlepoints[0][1] + 980 - 30
                )
                break
            if counter % 5 == 0:
                if znajdz_wspolrzedne_middlepoint(screenshot, "Wzmianka", lang="pol"):
                    pyautogui.press("esc")
                break
            pyautogui.sleep(1.5)
        if counter % 5 == 0:
            break

        my_print("Step 'Przywroc selection of przywróć'!", step=True)
        # Odczytaj tekst
        while True:
            screenshot = pyautogui.screenshot(
                region=(instagram_window_x[0], 800, 280, 400)
            )
            debug_screenshot(screenshot)
            screenshot = preprocess_image(np.array(screenshot), invert=False)
            # 6️⃣ OCR
            middlepoints = znajdz_wspolrzedne_middlepoint(
                screenshot, "Przywróć", lang="pol"
            )

            if middlepoints:
                my_print("Znaleziono 'Przywróć'!")
                pyautogui.click(
                    middlepoints[0][0] + instagram_window_x[0], middlepoints[0][1] + 800
                )
                break
            pyautogui.sleep(2)

        # Odczytaj tekst
        my_print("Step 'Przywroc confirmation of przywróć'!", step=True)
        while True:
            screenshot = pyautogui.screenshot(
                region=(
                    instagram_window_x[0],
                    500,
                    instagram_window_x[1] - instagram_window_x[0],
                    140,
                )
            )
            debug_screenshot(screenshot)
            screenshot = preprocess_image(np.array(screenshot), invert=False)
            # 6️⃣ OCR
            middlepoints = znajdz_wspolrzedne_middlepoint(
                screenshot, "Przywróć", lang="pol"
            )
            if middlepoints:
                my_print("Znaleziono 'Przywróć'!")
                pyautogui.click(
                    middlepoints[0][0] + instagram_window_x[0], middlepoints[0][1] + 500
                )
                break
            pyautogui.sleep(2)

    is_on_deleted_page()
    scroll()
    scroll()

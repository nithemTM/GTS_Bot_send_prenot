import time
import cv2
import numpy as np
import logging
import pyautogui

# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(levelname)s - %(message)s',
# )

logger = logging.getLogger(__name__)

def image_detect(screenshot, screen_item_check, fit_level=0.5, input_delay=None):

    # Zaladuj obraz zrzutu ekranu i obraz wzorca (przycisk)
    if input_delay is not None:
        time.sleep(input_delay)
    full_screenshot = cv2.imread(screenshot)
    pattern_item = cv2.imread(screen_item_check)

    # Konwertuj oba obrazy na skalę szarości
    full_screenshot_gray = cv2.cvtColor(full_screenshot, cv2.COLOR_BGR2GRAY)
    pattern_item_gray = cv2.cvtColor(pattern_item, cv2.COLOR_BGR2GRAY)

    # Dopasuj wzorzec przycisku do zrzutu ekranu
    result = cv2.matchTemplate(full_screenshot_gray, pattern_item_gray, cv2.TM_CCOEFF_NORMED)

    # Ustaw próg dopasowania
    location_point = np.where(result >= fit_level)

    logger.info(f"Dane lokalizacyjne dla znalezionego wzorca w screenie [location_point: {location_point}, location_point[0].size: {location_point[0].size}]")
    print()
    if location_point[0].size >= 1:
        logger.info(f"Odnaleziono [screen_item_check: {screen_item_check}] na [screenshot: {screenshot}]")
        return True
    else:
        logger.info(f"Nie odnaleziono [screen_item_check: {screen_item_check}] na [screenshot: {screenshot}]! ")
        return False


def get_image_resolution(image_path):
    # Wczytaj obraz
    image = cv2.imread(image_path)
    # Pobierz wysokość i szerokość
    height, width = image.shape[:2]
    return width, height


def image_detect_scale(screenshot, screen_item_check, screenshot_pattern, fit_level=0.5, input_delay=None):
    pattern_resolution = get_image_resolution('gts_window_screen_pattern.png')
    original_pattern_width, original_pattern_height = pattern_resolution
    print(original_pattern_height,original_pattern_width)
    #screen_width, screen_height = pyautogui.size()

    # Zaladuj obraz zrzutu ekranu i obraz wzorca (przycisk)
    if input_delay is not None:
        time.sleep(input_delay)

    full_screenshot = cv2.imread(screenshot)
    pattern_item = cv2.imread(screen_item_check,cv2.IMREAD_GRAYSCALE)
    full_screenshot_pattern = cv2.imread(screenshot_pattern)

    # Pobierz rozmiar zrzutu aktywnego okna
    screenshot_height, screenshot_width = full_screenshot.shape[:2]

    # Rozmiar wzorca z kompa na którym był on robiony (pobieramy z rozdzielczości wzorca screenshor)
    original_pattern_width, original_pattern_height = full_screenshot_pattern.shape[:2]

    # Rozmiar wzorca itemu który chcemy odszukać
    pattern_item_height, pattern_item_width = pattern_item.shape[:2]

    # Konwersja zrzutu ekranu do odcieni szarości
    full_screenshot_gray = cv2.cvtColor(full_screenshot, cv2.COLOR_BGR2GRAY)

    # Oblicz współczynnik skalowania
    scale_x = screenshot_width / original_pattern_width
    scale_y = screenshot_height / original_pattern_height
    scale = min(scale_x, scale_y)

    # Przeskaluj wzorzec itemu który chcesz odszukac
    resized_pattern_item = cv2.resize(pattern_item, (int(pattern_item_width * scale), int(pattern_item_height * scale)))
    resized_pattern_item_height, resized_pattern_item_width = resized_pattern_item.shape[:2]

    # Dopasuj wzorzec przycisku do zrzutu ekranu
    result = cv2.matchTemplate(full_screenshot_gray, resized_pattern_item, cv2.TM_CCOEFF_NORMED)

    # Ustaw próg dopasowania
    location_point = np.where(result >= fit_level)

    print(location_point)
    print(location_point[0].size)
    if location_point[0].size >= 1:
        return True
    else:
        return False






    # [OPCJA] Rysowanie prostokąta wokół wykrytego przycisku
    # for pt in zip(*location_point[::-1]):
    #     cv2.rectangle(full_screenshot, pt, (pt[0] + pattern_item.shape[1], pt[1] + pattern_item.shape[0]), (0, 255, 0), 2)
    # Wyświetl wynikowy obraz
    # cv2.imshow('Detected Button', full_screenshot)
    #
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
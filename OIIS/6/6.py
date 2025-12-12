import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

map_path = '/home/kirillromanoff/University/BSUIR/OIIS/6/rb.png'
template_path = '/home/kirillromanoff/University/BSUIR/OIIS/6/rbt.png'

# --- 1. Загрузка изображений ---
map_image = cv2.imread(map_path, cv2.IMREAD_UNCHANGED)
template_image = cv2.imread(template_path, cv2.IMREAD_UNCHANGED)

if map_image is None:
    raise FileNotFoundError(f"Не удалось загрузить карту: {map_path}")
if template_image is None:
    raise FileNotFoundError(f"Не удалось загрузить шаблон: {template_path}")

print("Размер карты:", map_image.shape)
print("Размер шаблона:", template_image.shape)

# Если есть альфа-канал, отбросим его 
def drop_alpha(img):
    if img.ndim == 3 and img.shape[2] == 4:
        return cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    return img

map_image = drop_alpha(map_image)
template_image = drop_alpha(template_image)

# --- 2. Подготовка изображений ---
map_gray = cv2.cvtColor(map_image, cv2.COLOR_BGR2GRAY)
template_gray = cv2.cvtColor(template_image, cv2.COLOR_BGR2GRAY)

# небольшая нормализация / equalize для устойчивости к освещению
map_gray = cv2.equalizeHist(map_gray)
template_gray = cv2.equalizeHist(template_gray)

# --- 3. Multi-scale template matching (ищем лучший масштаб) ---
best_score = -1.0
best_loc = None
best_scale = 1.0
best_w, best_h = 0, 0
method = cv2.TM_CCOEFF_NORMED

scales = np.linspace(0.6, 1.4, 17)  # от 60% до 140%

for scale in scales:
    new_w = int(template_gray.shape[1] * scale)
    new_h = int(template_gray.shape[0] * scale)
    if new_w < 10 or new_h < 10:
        continue
    if new_w > map_gray.shape[1] or new_h > map_gray.shape[0]:
        continue  # шаблон не может быть больше карты на этом масштабе
    resized_tpl = cv2.resize(template_gray, (new_w, new_h), interpolation=cv2.INTER_AREA)
    res = cv2.matchTemplate(map_gray, resized_tpl, method)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    if max_val > best_score:
        best_score = max_val
        best_loc = max_loc
        best_scale = scale
        best_w, best_h = new_w, new_h

print(f"Лучший score: {best_score:.4f} на масштабе {best_scale:.2f}, размер шаблона {best_w}x{best_h}")

# --- 4. Интерпретация результатов ---
THRESH = 0.65  # порог — подбирается под задачу
if best_score < THRESH:
    print("Возможно, совпадений нет или нужно снизить требования (порог) / сменить метод.")
else:
    top_left = best_loc
    bottom_right = (top_left[0] + best_w, top_left[1] + best_h)
    out_img = map_image.copy()
    cv2.rectangle(out_img, top_left, bottom_right, (0,0,255), 3)

    # Покажем результат
    plt.figure(figsize=(12,6))
    plt.subplot(1,2,1)
    plt.title("Шаблон (лучший масштаб)")
    tpl_vis = cv2.resize(template_image, (best_w, best_h))
    plt.imshow(cv2.cvtColor(tpl_vis, cv2.COLOR_BGR2RGB))
    plt.axis('off')

    plt.subplot(1,2,2)
    plt.title(f"Найдено (score={best_score:.3f})")
    plt.imshow(cv2.cvtColor(out_img, cv2.COLOR_BGR2RGB))
    plt.axis('off')
    plt.show()

    print("Координаты верхнего левого угла:", top_left)
    print("Координаты правого нижнего угла:", bottom_right)

# --- 5. (Опционально) Найти все мест с score > порог ---
# Для этого лучше использовать результат на лучшем масштабе
if best_score >= 0:
    resized_tpl = cv2.resize(template_gray, (best_w, best_h))
    res = cv2.matchTemplate(map_gray, resized_tpl, method)
    locs = np.where(res >= THRESH)
    matches = list(zip(*locs[::-1]))  # (x, y) координаты
    print("Количество обнаруженных совпадений выше порога:", len(matches))
    # можно нарисовать все совпадения
    out_all = map_image.copy()
    for (x, y) in matches:
        cv2.rectangle(out_all, (x, y), (x+best_w, y+best_h), (0,255,0), 2)
    if len(matches) > 0:
        plt.figure(figsize=(8,8))
        plt.title("Все совпадения (зелёные прямоугольники)")
        plt.imshow(cv2.cvtColor(out_all, cv2.COLOR_BGR2RGB))
        plt.axis('off')
        plt.show()

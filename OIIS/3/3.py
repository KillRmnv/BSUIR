import cv2
import numpy as np
import matplotlib.pyplot as plt

def match_brightness(img1, img2):
    """
    Выравнивание яркости img2 под img1
    """
    # Конвертируем в оттенки серого
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Вычисляем среднюю яркость
    mean1 = np.mean(gray1)
    mean2 = np.mean(gray2)

    # Коэффициент коррекции яркости
    ratio = mean1 / (mean2 + 1e-8)

    # Корректируем яркость
    img2_adjusted = cv2.convertScaleAbs(img2, alpha=ratio, beta=0)
    return img2_adjusted


# === Загрузка изображений === 4-2 4-1 2-1 2-3 2-4 1-2
img1 = cv2.imread("/home/kirillromanoff/University/OIIS/3/4.jpg")
img2 = cv2.imread("/home/kirillromanoff/University/OIIS/3/2.jpg")

# Проверка
if img1 is None or img2 is None:
    raise FileNotFoundError("Не удалось загрузить одно из изображений.")

# === Выравнивание яркости ===
img2_aligned = match_brightness(img1, img2)

# === Сохранение результата ===
cv2.imwrite("image2_aligned.jpg", img2_aligned)

# === Конвертация для отображения в matplotlib (BGR → RGB) ===
img1_rgb = cv2.cvtColor(img1, cv2.COLOR_BGR2RGB)
img2_rgb = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img2_aligned_rgb = cv2.cvtColor(img2_aligned, cv2.COLOR_BGR2RGB)

# === Построение графиков ===
plt.figure(figsize=(15, 8))

# --- Исходное изображение 1 ---
plt.subplot(2, 3, 1)
plt.imshow(img1_rgb)
plt.title("Изображение 1 (эталон)")
plt.axis('off')

# --- Исходное изображение 2 ---
plt.subplot(2, 3, 2)
plt.imshow(img2_rgb)
plt.title("Изображение 2 (до выравнивания)")
plt.axis('off')

# --- После выравнивания ---
plt.subplot(2, 3, 3)
plt.imshow(img2_aligned_rgb)
plt.title("Изображение 2 (после выравнивания)")
plt.axis('off')

# --- Гистограммы яркости ---
gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
gray2_aligned = cv2.cvtColor(img2_aligned, cv2.COLOR_BGR2GRAY)

plt.subplot(2, 3, 4)
plt.hist(gray1.ravel(), bins=50, color='blue', alpha=0.7)
plt.title("Гистограмма яркости — Изображение 1")

plt.subplot(2, 3, 5)
plt.hist(gray2.ravel(), bins=50, color='red', alpha=0.7)
plt.title("Гистограмма яркости — Изображение 2 (до)")

plt.subplot(2, 3, 6)
plt.hist(gray2_aligned.ravel(), bins=50, color='green', alpha=0.7)
plt.title("Гистограмма яркости — Изображение 2 (после)")

plt.tight_layout()
plt.show()

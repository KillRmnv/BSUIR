import cv2
import numpy as np
import matplotlib.pyplot as plt

# === Загрузка изображения ===
image = cv2.imread('/home/kirillromanoff/University/OIIS/4/1.png')  # замените на свой путь
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# === 1. Сегментация по границам (Edge-based segmentation) ===
edges = cv2.Canny(gray, 100, 200)
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

edge_segmentation = image.copy()
cv2.drawContours(edge_segmentation, contours, -1, (0, 255, 0), 2)

# === 2. Сегментация по областям (Region-based / Watershed) ===
# Шаг 1: Бинаризация
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

# Шаг 2: Убираем шум с помощью морфологии
kernel = np.ones((3, 3), np.uint8)
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

# Шаг 3: Определяем фон
sure_bg = cv2.dilate(opening, kernel, iterations=3)

# Шаг 4: Определяем "ядра" объектов (маркированные точки)
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

# Шаг 5: Неопределённая область
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

# Шаг 6: Размечаем маркеры
ret, markers = cv2.connectedComponents(sure_fg)
markers = markers + 1
markers[unknown == 255] = 0

# Шаг 7: Применяем Watershed
markers = cv2.watershed(image, markers)
watershed_result = image.copy()
watershed_result[markers == -1] = [255, 0, 0]  # границы выделены красным

# === Визуализация результатов ===
titles = ['Оригинал', 'Границы (Canny)', 'По контурам', 'Watershed']
images = [image[:, :, ::-1], edges, edge_segmentation[:, :, ::-1], watershed_result[:, :, ::-1]]

plt.figure(figsize=(12, 8))
for i in range(4):
    plt.subplot(2, 2, i + 1)
    plt.imshow(images[i], cmap='gray')
    plt.title(titles[i])
    plt.axis('off')
plt.tight_layout()
plt.show()

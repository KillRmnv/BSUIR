from PIL import Image, ImageFilter, ImageOps
import matplotlib.pyplot as plt

def apply_filters(image_path):
    # Открываем исходное изображение
    image = Image.open(image_path)

    # Применяем фильтры
    filters = {
        "Оригинал": image,
        "Размытие": image.filter(ImageFilter.BLUR),
        "Контур": image.filter(ImageFilter.CONTOUR),
        "Резкость": image.filter(ImageFilter.SHARPEN),
        "Оттенки серого": ImageOps.grayscale(image),
        "Усиление краёв": image.filter(ImageFilter.EDGE_ENHANCE)
    }

    # Сохраняем фильтрованные изображения
    for name, img in filters.items():
        filename = f"filtered_{name.replace(' ', '_').lower()}.jpg"
        img.save(filename)

    # Отображаем все фильтры через matplotlib
    plt.figure(figsize=(12, 8))
    for i, (name, img) in enumerate(filters.items(), 1):
        plt.subplot(2, 3, i)
        plt.imshow(img if img.mode == 'RGB' else img, cmap='gray')
        plt.title(name)
        plt.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    apply_filters("/home/kirillromanoff/University/OIIS/2/1.png")

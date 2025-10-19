from PIL import Image

# Укажите пути к файлам (замените на свои)
left_path = '/home/kirillromanoff/University/OIIS/5/l1.png'  # Путь к левому изображению
right_path = '/home/kirillromanoff/University/OIIS/5/l2.png'  # Путь к правому изображению

# Загрузка изображений
left = Image.open(left_path)
right = Image.open(right_path)

# Убедимся, что изображения одного размера (если нет, можно добавить ресайз)
if left.size != right.size:
    right = right.resize(left.size)

# Конвертация в RGB
left = left.convert('RGB')
right = right.convert('RGB')

# Разделение каналов
r_left, g_left, b_left = left.split()
r_right, g_right, b_right = right.split()

# Создание анаглифа: красный канал из левого, зеленый и синий из правого
anaglyph = Image.merge('RGB', (r_left, g_right, b_right))

# Отображение результата
anaglyph.show()

# Сохранение результата
anaglyph.save('anaglyph.jpg')
print("Стереоскопическое изображение сохранено как 'anaglyph.jpg'")
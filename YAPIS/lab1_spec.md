# Лабораторная работа 1 — примеры на синтаксисе SPEC.md (Вариант 19)

Три таргетированных примера на Go-стиле синтаксиса из `SPEC.md`:

| Пример | Что показывает |
|---|---|
| 1. Типы и классика | все 7 типов, неявные преобразования, все 14 операций, `if-else`, `switch-case`, `for`, `while`, `until`, `break`/`continue`, подпрограммы, области видимости |
| 2. Функции изображений | `load/save/width/height/sqrt`, методы `resize/rotate/crop/grayscale/invert/blur/map`, ручной обход через `img[x, y]`, лямбды |
| 3. Потоки | только потоковый оператор `->`: предикаты, мульти-ветвление `:`, финал `::`, терминалы, `blend`/`sobel`/`blur` — без лишнего шума |

---

## Пример 1. Типы, преобразования и классические конструкции

```go
// Глобальная область видимости
string appName = "ImgLang types demo"

// --- Подпрограммы объявляются в начале программы ---
// Параметры — по значению, возврат — через return, имена уникальны
func int maxOf(int a, int b) {
    if a > b {
        return a
    } else {
        return b
    }
}

func float brightnessOf(color c) {
    return (c.R + c.G + c.B) / 3
}

func void main() {
    // Инициализация всех 7 типов
    int w = 800
    float k = 1.5
    bool flag = true
    string initial = "A"
    string title = read()
    string label = "img_" + initial + "_" + title + "_" + w
    image src = load("photo.jpg")
    pixel p = {x: 10, y: 20}
    color white = 255              // неявное int -> color (серый)
    color bg = (10, 20, 30)        // кортеж
    color fg = {R: 255, G: 0, B: 0} // структура

    print("Start " + label + " (" + appName + ")")

    // Сложные выражения: все 14 операций
    color sample = src[p.x, p.y]   // [] и .
    float bright = brightnessOf(sample)
    float root = sqrt((bright * bright) + (w * w))
    color mix = ((sample * k) + white - 5) / 2 % 256
    int total = (w * 2) % 1000
    int rest = total - w
    bool ready = (w > 0) && (bright < 300) || !(total != 0) && flag

    if ready {
        print("ready")
    } else {
        print("not ready")
    }

    switch total {
    case 0: { print("пусто") }
    case 600: { print("стандарт") }
    default: { print("total=" + total) }
    }

    for int i = 0; i < 3; i = i + 1 {
        print("for " + i)
    }

    int j = 0
    while j < 2 {
        print("while " + j)
        j = j + 1
    }

    int n = 0
    until n == 2 {
        print("until " + n)
        n = n + 1
    }

    for int q = 0; q < 5; q = q + 1 {
        if q == 1 {
            continue
        }
        if q == 3 {
            break
        }
        print("q=" + q)
    }

    int m = maxOf(w, total)
    print("Done max=" + m + " root=" + root)
}
```

## Пример 2. Встроенные функции изображений и ручная обработка

```go
string appName = "ImgLang transforms demo"

func color dimPixel(color c, float k) {
    return c * k
}

func void main() {
    image src = load("photo.jpg")
    int w = width(src)
    int h = height(src)
    float k = 0.8
    string name = read()

    print("Transform " + name + " " + w + "x" + h + " (" + appName + ")")

    // Цепочка методов-трансформаций (возвращают image)
    image pre = src.resize(800, 600).rotate(90).crop(0, 0, 400, 300).grayscale()
    image soft = pre.blur(2)
    image neg = soft.invert()

    // Ручной обход пикселей: чтение, условие, запись
    for int x = 0; x < w; x = x + 1 {
        int y = 0
        while y < h {
            color px = src[x, y]
            float lum = (px.R + px.G + px.B) / 3
            if lum > 200 {
                src[x, y] = 255
            } else {
                src[x, y] = dimPixel(px, k)
            }
            y = y + 1
        }
    }

    // Лямбда через map
    image mapped = neg.map((color p) -> {
        return p * 1.2
    })

    save(mapped, "out_" + name + ".jpg")
    save(src, "manual_" + name + ".jpg")
    print("Done")
}
```

## Пример 3. Потоковая обработка (ключевая фишка языка)

Вся обработка — через оператор `->`. Ни одного ручного цикла по пикселям.

```go
// Пользовательский предикат: контекст собирается через color(R, G, B)
func bool isWarm(color c) {
    return c.R > 150 && c.G > 100 && c.G < 200
}

func void main() {
    image src = load("portrait.jpg")
    image logo = load("watermark.png")

    // Подсчёт пользовательской функцией-предикатом
    int warm = src -> (isWarm(color(R, G, B))) .count()
    print("Тёплых пикселей: " + warm)

    // Тёплые -> осветлить : иначе -> затемнить :: сохранить
    // print в середине цепочки: отладка с пробросом пикселя дальше
    src -> (isWarm(color(R, G, B))) .print("warm at " + x + "," + y) .brightness(1.3)
       : else .brightness(0.7)
       ::save("s1_warm.jpg")

    // Чейнинг: несколько модификаторов подряд для одной группы пикселей
    src -> (isRed()) .invert() .blur(2) .brightness(1.2)
       ::save("chain_reds.jpg")

    // Чейнинг в ветках: у каждой ветки своя цепочка модификаторов
    src -> (isBright()) .invert() .vignette()
       : else .grayscale() .blur(5) .brightness(0.8)
       ::save("chain_full.jpg")

    // Селективное размытие: блюр всего, кроме тёплых
    src -> (!(isWarm(color(R, G, B)))) .blur(3)
       ::save("s2_blur.jpg")

    // Карта краёв только для НЕ ярких участков
    src -> (!(isBright())) .sobel()
       ::save("s3_edges.jpg")

    // Цветовое кодирование по яркости за один проход
    src -> (isDark()) .color(0, 0, 255)
       : (isBright()) .color(255, 0, 0)
       : else .color(0, 255, 0)
       ::save("s4_coded.jpg")

    // Водяной знак лямбдой + общий финал-виньетка для всех пикселей
    src -> (isBright()) .blend(logo, (color s, color o) -> {
        return (s * 0.85) + (o * 0.15)
    })
       : else .brightness(0.9)
       ::vignette()
         .save("s5_final.jpg")

    // Поиск первого контура с остановкой всего обхода
    src -> (isContour()) .print("Contour at") .break()
       ::print("No contours")
}
```

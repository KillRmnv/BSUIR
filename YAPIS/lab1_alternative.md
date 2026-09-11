# Лабораторная работа 1 — примеры на альтернативном синтаксисе (Вариант 19)

Три таргетированных примера на человекочитаемом синтаксисе из `ALTERNATIVE.md`
(те же три сюжета, что в `lab1_spec.md`):

| Пример | Что показывает |
|---|---|
| 1. Типы и классика | все 7 типов (`Char` нет — символы в `String`), неявные преобразования, все 14 операций, `If-Otherwise`, `Switch-Case`, `For`, `While`, `Until`, подпрограммы, области видимости |
| 2. Функции изображений | `Load/Save/Width/Height/Sqrt`, трансформации `Resize/Rotate/Crop/Grayscale/Invert/Blur/Map`, ручной обход через `img[x, y]`, лямбды `Do On Each` |
| 3. Потоки | только блоки `Process`: предикаты, ветки, `Otherwise`/`Finally`, терминалы, чейнинг — без лишнего шума |

> **Примечание про скобки.** Круглые скобки вокруг условия в `If` **не требуются** —
> только для группировки внутри выражения. Правильно: `If ready:`, `If x > 10:`,
> `If R > 150 And G < 200:`. Скобки ниже стоят лишь там, где задают порядок вычислений
> (например, после префиксного `Not`).

---

## Пример 1. Типы, преобразования и классические конструкции

```
String appName = "ImgLang types demo"

Function Integer maxOf(Integer a, Integer b): {
    If a > b: {
        Return a
    } Otherwise: {
        Return b
    }
}

Function Float brightnessOf(Color c): {
    Return (c.R + c.G + c.B) / 3
}

Function Void main(): {
    Integer w = 800
    Float k = 1.5
    Boolean flag = True
    String initial = "A"
    String title = Read
    String label = "img_" + initial + "_" + title + "_" + w
    Image src = Load("photo.jpg")
    Pixel p = {x: 10, y: 20}
    Color white = 255
    Color bg = (10, 20, 30)
    Color fg = {R: 255, G: 0, B: 0}

    Print("Start " + label + " (" + appName + ")")

    Color sample = src[p.x, p.y]
    Float bright = brightnessOf(sample)
    Float root = Sqrt((bright * bright) + (w * w))
    Color mix = ((sample * k) + white - 5) / 2 % 256
    Integer total = (w * 2) % 1000
    Integer rest = total - w
    Boolean ready = (w > 0) And (bright < 300) Or Not (total Not == 0) And flag

    // Условие без скобок (скобки — только для группировки)
    If ready: {
        Print("ready")
    } Otherwise: {
        Print("not ready")
    }

    Switch total: {
        Case 0: { Print("пусто") }
        Case 600: { Print("стандарт") }
        Otherwise: { Print("total=" + total) }
    }

    For Integer i = 0; i < 3; i = i + 1: {
        Print("for " + i)
    }

    Integer j = 0
    While j < 2: {
        Print("while " + j)
        j = j + 1
    }

    Integer n = 0
    Until n == 2: {
        Print("until " + n)
        n = n + 1
    }

    For Integer q = 0; q < 5; q = q + 1: {
        If q == 1: {
            Continue
        }
        If q == 3: {
            Break
        }
        Print("q=" + q)
    }

    Integer m = maxOf(w, total)
    Print("Done max=" + m + " root=" + root)
}
```

## Пример 2. Встроенные функции изображений и ручная обработка

```
String appName = "ImgLang transforms demo"

Function Color dimPixel(Color c, Float k): {
    Return c * k
}

Function Void main(): {
    Image src = Load("photo.jpg")
    Integer w = Width(src)
    Integer h = Height(src)
    Float k = 0.8
    String name = Read

    Print("Transform " + name + " " + w + "x" + h + " (" + appName + ")")

    Image pre = Grayscale(Crop(Rotate(Resize(src, 800, 600), 90), 0, 0, 400, 300))
    Image soft = Blur(pre, 2)
    Image neg = Invert(soft)

    For Integer x = 0; x < w; x = x + 1: {
        Integer y = 0
        While y < h: {
            Color px = src[x, y]
            Float lum = (px.R + px.G + px.B) / 3
            If lum > 200: {
                src[x, y] = 255
            } Otherwise: {
                src[x, y] = dimPixel(px, k)
            }
            y = y + 1
        }
    }

    Image mapped = Map(neg, Do On Each: { Return p * 1.2 })

    Save(mapped, "out_" + name + ".jpg")
    Save(src, "manual_" + name + ".jpg")
    Print("Done")
}
```

## Пример 3. Потоковая обработка (ключевая фишка языка)

Вся обработка — через блоки `Process`. Ни одного ручного цикла по пикселям.

```
Function Boolean isWarm(Color c): {
    Return c.R > 150 And c.G > 100 And c.G < 200
}

Function Void main(): {
    Image src = Load("portrait.jpg")
    Image logo = Load("watermark.png")

    If isWarm(src[5, 5]): {
        Print("Проба тёплая")
    } Otherwise: {
        Print("Проба холодная")
    }

    Integer warm = Count(src, R > 150 And G > 100 And G < 200)
    Print("Тёплых пикселей: " + warm)

    Process src: {
        If R > 150 And G > 100 And G < 200: {
            Print("warm at " + x + "," + y)
            apply Brightness(1.3)
        }
        Otherwise: { apply Brightness(0.7) }
        Finally: { Save("s1_warm.jpg") }
    }

    // Чейнинг: несколько модификаторов через запятую
    Process src: {
        If pixel Is Red: { apply Invert, Blur(3), Brightness(1.2) }
        Finally: { Save("chain_reds.jpg") }
    }

    Process src: {
        If pixel Is Bright: { apply Invert, Vignette }
        Otherwise: { apply Grayscale, Blur(5) }
        Finally: { Save("chain_full.jpg") }
    }

    Process src: {
        If Not (R > 150 And G > 100 And G < 200): { apply Blur(3) }
        Finally: { Save("s2_blur.jpg") }
    }

    Process src: {
        If Not pixel Is Bright: { apply Sobel }
        Finally: { Save("s3_edges.jpg") }
    }

    Process src: {
        If pixel Is Dark: { apply Color(0, 0, 255) }
        If pixel Is Bright: { apply Color(255, 0, 0) }
        Otherwise: { apply Color(0, 255, 0) }
        Finally: { Save("s4_coded.jpg") }
    }

    Process src: {
        If pixel Is Bright: { apply Blend(logo, Do On Each: { Return (src * 0.85) + (over * 0.15) }) }
        Otherwise: { apply Brightness(0.9) }
        Finally: { apply Vignette, Save("s5_final.jpg") }
    }

    Process src: {
        If pixel Is Contour: {
            Print("Contour at")
            Stop
        }
        Finally: { Print("No contours") }
    }
}
```

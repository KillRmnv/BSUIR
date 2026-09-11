Вот компактный, короткий путь — без лишней архитектуры, ровно то, что нужно для лабы 5.

## Структура решения

```
ImgLang.sln
├── ImgLang.Runtime/     — библиотека на C#, обычная сборка
│   └── Runtime.dll
├── ImgLang.Compiler/    — ваш компилятор (ANTLR + Cecil)
│   └── ImgLang.exe
```

## Шаг 1. Runtime-библиотека (пишете как обычный C#)

Всё, что не входит в «скелет» программы (арифметика/ветвления/циклы пользователя), уходит сюда — обычные static-методы. Никакого IL руками.

```csharp
// ImgLang.Runtime/Color.cs
public struct Color {
    public int R, G, B;
    public Color(int r, int g, int b) { R = r; G = g; B = b; }
}

// ImgLang.Runtime/ImgOps.cs — статический класс встроенных функций
public static class ImgOps {
    public static Color Invert(Color p) => new Color(255 - p.R, 255 - p.G, 255 - p.B);
    public static Color Grayscale(Color p) {
        int g = (p.R + p.G + p.B) / 3;
        return new Color(g, g, g);
    }
    public static Color Brightness(Color p, float k) =>
        new Color(Clamp(p.R * k), Clamp(p.G * k), Clamp(p.B * k));

    public static bool IsRed(Color p) => p.R > p.G && p.R > p.B;
    public static bool IsBright(Color p) => (p.R + p.G + p.B) / 3 > 127;

    public static ImageBuf Load(string path) { /* через ImageSharp/System.Drawing */ }
    public static void Save(ImageBuf img, string path) { /* ... */ }
    public static ImageBuf Blur(ImageBuf img, int radius) { /* box blur */ }
    public static ImageBuf Sobel(ImageBuf img) { /* ... */ }

    static int Clamp(float v) => (int)Math.Clamp(v, 0, 255);
}

// ImgLang.Runtime/ImageBuf.cs — обёртка над буфером пикселей
public class ImageBuf {
    public int Width, Height;
    public Color[,] Pixels;
    public Color this[int x, int y] {
        get => Pixels[x, y];
        set => Pixels[x, y] = value;
    }
    public ImageBuf Clone() { /* для snapshot-семантики */ }
}
```

Собираете `dotnet build` → получаете `Runtime.dll`. Всё, руками CIL не трогаете.

## Шаг 2. Компилятор ссылается на Runtime.dll через Cecil

```csharp
using Mono.Cecil;
using Mono.Cecil.Cil;

var module = ModuleDefinition.CreateModule("ImgLangProgram", ModuleKind.Console);
var runtimeAsm = AssemblyDefinition.ReadAssembly("Runtime.dll");
var runtimeModule = runtimeAsm.MainModule;

// Импорт нужных методов один раз, кладём в словарь для codegen'а
var imgOpsType = runtimeModule.GetType("ImgLang.Runtime.ImgOps");
var invertRef  = module.ImportReference(imgOpsType.Methods.First(m => m.Name == "Invert"));
var loadRef    = module.ImportReference(imgOpsType.Methods.First(m => m.Name == "Load"));
var saveRef    = module.ImportReference(imgOpsType.Methods.First(m => m.Name == "Save"));
// ... и т.д. для всех билтинов — удобно сделать словарь string -> MethodReference
```

## Шаг 3. Генерация `main()` — эмиттер по AST

Один класс `IlEmitter`, который обходит AST/ANTLR-parse-tree и на каждый узел вызывает `il.Emit(...)`.

```csharp
var mainType = new TypeDefinition("ImgLang", "Program",
    TypeAttributes.Public | TypeAttributes.Class, module.TypeSystem.Object);
module.Types.Add(mainType);

var mainMethod = new MethodDefinition("Main",
    MethodAttributes.Public | MethodAttributes.Static, module.TypeSystem.Void);
mainType.Methods.Add(mainMethod);
module.EntryPoint = mainMethod;

var il = mainMethod.Body.GetILProcessor();

// Пример: генерация "image src = load(...)"
var srcVar = new VariableDefinition(module.ImportReference(runtimeModule.GetType("ImgLang.Runtime.ImageBuf")));
mainMethod.Body.Variables.Add(srcVar);

il.Emit(OpCodes.Ldstr, "photo.jpg");
il.Emit(OpCodes.Call, loadRef);
il.Emit(OpCodes.Stloc, srcVar);
```

**Соответствие конструкций ImgLang → CIL:**

| Конструкция ImgLang | Что эмитит компилятор |
|---|---|
| `int x = 10` | `ldc.i4` + `stloc` (переменная — `VariableDefinition`) |
| `a + b` | `ldloc a`, `ldloc b`, `add` |
| `if cond { } else { }` | вычислить cond → `brfalse` на `Instruction`-метку else-блока |
| `while cond { }` | метка начала → cond → `brfalse` на конец → тело → `br` на начало |
| `for init; cond; step { }` | init + `while`-паттерн выше со step в конце тела |
| вызов встроенной функции `invert(p)` | `ldloc p`, `call invertRef` |
| вызов пользовательской `func` | генерируете `MethodDefinition` для неё отдельно, вызываете `call` |
| `src -> (isRed()) .invert() .save(...)` | **разворачиваете в обычный вложенный `for` по x,y** прямо в момент кодогена (см. ниже) |

Переходы (`if`/`while`/`for`) в Cecil делаются не текстовыми метками, а прямыми ссылками на объекты `Instruction` — это единственная небольшая особенность API, которую стоит заранее понять:

```csharp
var condFalse = il.Create(OpCodes.Nop); // "метка" — просто будущая инструкция
// ... эмит условия ...
il.Emit(OpCodes.Brfalse, condFalse);
// ... тело if ...
il.Append(condFalse); // ставим метку в нужное место
```

## Шаг 4. Поток `->` — самая интересная часть, но не сложная

Компилятор **не** генерирует отдельный CIL-примитив для `->` — он просто **транслирует поток в обычный двойной `for`**, вызывая ваши уже готовые Runtime-методы:

```
// ImgLang:
src -> (isRed()) .invert()
   : else .grayscale()
   ::save("out.jpg")

// Эквивалент, который эмиттер строит как CIL (концептуально, в виде C#):
var result = src.Clone();          // snapshot
for (int y = 0; y < src.Height; y++)
    for (int x = 0; x < src.Width; x++) {
        var p = src[x, y];         // читаем из snapshot
        if (ImgOps.IsRed(p))
            result[x, y] = ImgOps.Invert(p);
        else
            result[x, y] = ImgOps.Grayscale(p);
    }
ImgOps.Save(result, "out.jpg");    // эпилог
```

То есть эмиттер для `Process`-узла AST просто генерирует два вложенных `for`-цикла (по уже отработанному вами паттерну `for`), внутри — цепочку `if/else if/else` по веткам, а в каждой ветке — последовательность `call` на методы модификаторов. Никакой отдельной "потоковой" IL-конструкции не нужно — весь потоковый оператор компилируется в комбинацию из того, что вы и так уже умеете генерировать (циклы, ветвления, вызовы).

## Шаг 5. Финализация

```csharp
module.AssemblyReferences.Add(runtimeAsm.Name); // ссылка на Runtime.dll
module.Assembly = AssemblyDefinition.CreateAssembly(
    new AssemblyNameDefinition("ImgLangProgram", new Version(1,0,0,0)), module.Name, module);
module.Write("out.exe");
```

Копируете `Runtime.dll` рядом с `out.exe` — готово, `dotnet out.exe` запускается.

## Итог — что писать в каком порядке

1. **Runtime.dll** — все встроенные функции/типы (`Color`, `ImageBuf`, `ImgOps`) как обычный C#. Собираете один раз.
2. **Импорт методов** через `ModuleDefinition.ImportReference` — один словарь `имя_билтина → MethodReference`.
3. **`IlEmitter`** — обход AST, по одному методу-обработчику на тип узла (`EmitVarDecl`, `EmitIf`, `EmitWhile`, `EmitFor`, `EmitCall`, `EmitProcess`), с использованием `ILProcessor` + `Instruction`-меток для переходов.
4. **`EmitProcess`** для потокового оператора — просто разворачивается в `EmitFor` + `EmitIf` + вызовы модификаторов, ничего принципиально нового не требует.
5. `module.Write(...)` в конце.

Это и есть самый короткий путь: 80% работы — обычный C# (Runtime.dll), 20% — Cecil-эмиттер, который per-конструкцию ImgLang генерирует 3-10 строк на `ILProcessor.Emit`.
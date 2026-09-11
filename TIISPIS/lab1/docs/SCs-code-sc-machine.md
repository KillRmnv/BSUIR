# SCs-code

> **Note**
> This is correct for only versions of sc-machine that >= 0.9.0.

---

## Common

SCs-code - is a text representation of SC-code. Whole text consist of sentences, that separated by `;;` symbols.

### Comments

You can use C-style comments in sc.s-text:

```scs
// one line comment
fruit -> apple;
/* Multiline
 * comment
 */
```

### Link to files

To make an `sc-link` into specified file you can use special type identifier:

```scs
"file://<file name>"
```

- `"file://<file name>"` - is a relative path to a file. According to a file, where it used;
- `"file:///<file_name>"` - is an absolute path to a file.

### Names

There are some tricks with sc-node names:

- `...` - is an unnamed sc-node;
- `_<node name>` - all sc-node names, that starts with symbol `_` represents a variable type of sc-nodes.

Objects identifier visibility. By default, all objects with name `x` are visible anywhere. After translating it into memory this object will have a **system identifier** equal to `x`. So if you use `x` in different *scs* files, then you designate the same object in them (would be the same element in a knowledge base).

Sometimes you need to designate the same objects in different files, but do not generate a **system identifier** in memory for it. In this case you should to prefix it name with a `.` symbol. For example: `.x`.

In case, when you need to make a named object just local for an *scs* file, then you should to use `..` prefix (example: `..x`).

So a rule to build identifier is:

```scs
[visibility][variable]<identifier>
```

For example identifier `.._x` locally visible variable identifier.

### Aliases

You can use alias for any sc-element by using `=` operator. There are some examples:

```scs
@file_alias = "file://...";;
@link_alias = [];;
@element_alias = element_idtf;;
@arc_alias = (c -> b);;
@alias_to_alias = @element_alias;;
```

> **Warning**
> Aliases visible just in a file scope.
> You should define alias before usage.

---

> **Note**
> SCs-code is split into levels. Each level allows to minimize number of string symbols to represent the same structures.

## SCs-code level 1

SCs-code level 1 is a simple representation of SC-code. It represents SC-texts with just simple triples. Each triple contains `subject`, `predicate`, `object` that are split by `|` symbol. Line `sc_node#subject_identifier | sc_membership_arc#predicate_identifier | sc_node#object_identifier;;` is a sentence.

Identifier of `subject`, `predicate`, `object` build with rule:

```scs
<type>#<identifier>
```

If object or subject is sc-link, then you should use the next one:

```scs
"file://<file name>"
```

Where `type` is an element type specification. It can be one of possible values:

- `sc_node` - equal to SCg-node;
- `sc_link` - equal to SCg-link;
- `sc_common_edge` - equal to SCg-node;
- `sc_common_arc` - equal to SCg-node;
- `sc_membership_arc` - equal to SCg-node;
- `sc_main_arc` - equal to SCg-node.

---

**Examples**

| SCg construction | Equal SCs-code level 1 text |
|---|---|
| *(SCg diagram)* | `sc_node#fruit` <br> `  \| sc_main_arc#..arc` <br> `  \| sc_node#apple;;` <br> `// append set of bananas into fruit set` <br> `sc_node#fruit` <br> `  \| sc_main_arc#..arc` <br> `  \| sc_node#banana;;` |
| *(SCg diagram)* | `sc_node#apple` <br> `  \| sc_common_arc#..common_arc` <br> `  \| "file://apple.png";;` <br> `/*append sc-arc from nrel_image relation into` <br> `  sc-arc between apple set and it's image*/` <br> `sc_node_non_role_relation#nrel_image` <br> `  \| sc_main_arc#..membership_arc` <br> `  \| sc_common_arc#..common_arc;;` |

SCs-code level 1 allows you to represent any kind of SC-code construction. It's a low-level representation and commonly used as a transport format, that is very simple for parsing.

## SCs-code level 2

This level of SCs-code add two new features:

- using of extended alphabet of sc-connectors;
- using of compound identifiers of sc-connectors.

On this level you can make sentences by rule:

```scs
<element> <connector> <element>;;
```

Where `<connector>` can be on of values:

| SCs-code | SCg-code |
|---|---|
| `?<=>` | Not specified |
| `?=> or <=?` | Not specified |
| `?.?> or <?.?` | Not specified |
| `<=>` | (const common edge) |
| `_<=>` | (var common edge) |
| `=> or <=` | (const common arc) |
| `_=><= or <=_` | (var common arc) |
| `??> or <??` | Not specified |
| `_?? or <??_` | Not specified |
| `?-?> or <?-?` | Not specified |
| `?..?> or <?..?` | Not specified |
| `?-?> or <?-?` | Not specified |
| `_-?> or <?-_` | Not specified |
| `..?> or <?..` | Not specified |
| `_..?> or <?.._` | Not specified |
| `?~?> or <?~?` | Not specified |
| `?%?> or <?%?` | Not specified |
| `~?> or <?~` | Not specified |
| `_~?> or <?~_` | Not specified |
| `%?> or <%?` | Not specified |
| `_%?> or <%_` | Not specified |
| `??> or <??` | Not specified |
| `??|> or <|??` | Not specified |
| `?/> or </?` | Not specified |
| `.> or <.` | Not specified |
| `_.> or <._` | Not specified |
| `?-> or <-?` | Not specified |
| `?..> or <..?` | Not specified |
| `?~> or <~?` | Not specified |
| `?%> or <%?` | Not specified |
| `-> or <-` | (const perm positive arc) |
| `..> or <..` | (const temp positive arc) |
| `~> or <~` | Not specified |
| `%> or <%` | Not specified |
| `_-> or <-_` | (var perm positive arc) |
| `_..> or <.._` | (var temp positive arc) |
| `_~> or <~_` | Not specified |
| `_%> or <%_` | Not specified |
| `?|> or <|?` | Not specified |
| `_?|> or <|?_` | Not specified |
| `?-|> or <|-?` | Not specified |
| `?..|> or <|..?` | Not specified |
| `?~|> or <|~?` | Not specified |
| `?%|> or <|%?` | Not specified |
| `-|> or <|-` | (const perm negative arc) |
| `..|> or <|..` | (const temp negative arc) |
| `~|> or <|~` | Not specified |
| `%|> or <|%` | Not specified |
| `_-|> or <|-_` | (var perm negative arc) |
| `_..|> or <|.._` | (var temp negative arc) |
| `_~|> or <|~_` | Not specified |
| `_%|> or <|%_` | Not specified |
| `/> or </` | (const fuzzy arc) |
| `_/> or </_` | (var fuzzy arc) |

---

| SCg construction | Equal SCs-code level 2 text |
|---|---|
| *(SCg diagram)* | `fruit -> apple;;` <br> `// backward direction` <br> `banana <- fruit;;` |

---

Compound identifier of a sc-connector builds as a sentence in SCs-code level 2, but without `;;` separator and inside brackets `()`: `(<element> <connector> <element>)`. So that allows to simplify usage of a sc-connector as a source or target of another one.

---

**Examples**

| SCg construction | Equal SCs-code level 2 text |
|---|---|
| *(SCg diagram)* | `nrel_image -> (fruit => "file://apple.png");;` |
| *(SCg diagram)* | `d -> (c -> (a -> b));;` |
| *(SCg diagram)* | `(a -> b) -> (c <- d);;` |

## SCs-code level 3

This level of SCs-code allows to minimize symbols to represent constructions like this one:

```scs
c -> (a -> b);;
```

To do that you should use sentence like this:

```scs
<object> <connector> <attribute>: <object>
```

For this example it would be like this:

```scs
a -> c: b;;
```

In case, when outgoing sc-arc from `c` is a variable, then use `::` splitter instead of `:`:

```scs
a -> c:: b;;
```

equal to:

```scs
c _-> (a -> b);;
```

> **Note**
> You can use `:`, `::` just to replace `->` or `_->` sc-arcs.

---

**Examples**

| SCg construction | Equal SCs-code level 3 text |
|---|---|
| *(SCg diagram)* | `apple => nrel_image: "file://apple.png";;` |
| *(SCg diagram)* | `a <=> c: d:: b;;` |

> **Note**: it is possible to use any number of `:`, `::` in one sentence.

## SCs-code level 4

This level of SCs-code allows to combine many sentences with one element into one. For that purposes used ';' symbol. So if we have some sentences like:

```scs
x -> y;;
x <- z;;
x => h: r;;
```

Then using SCs level 4 we can write them like this:

```scs
x
-> y;
<- z;
=> h: r;;
```

In other words, this level of SCs-code allows to use source element one time.

---

**Examples**

| SCg-code | Equal SCs-code level 4 text |
|---|---|
| *(SCg diagram)* | `fruit` <br> `-> apple;` <br> `-> banana;;` |
| *(SCg diagram)* | `a` <br> `-> c: d: b;` <br> `-> e;` <br> `-> g: f;;` |

## SCs-code level 5

Internal sentences added to SCs-code on this level. They are wrapped by `(* ... *)` brackets. This type of sentences allow to describe connections of an element inplace. You can place these internal sentences after `object` element in triple (`subject -> object (* ... *);;`), but before `;;` separator. You can use level `2-4` sentences inside this one. But there is a just one rule:

> You doesn't need to specify start element for each sentence. Because object (for which internal sentence builds) is going to be a subject for all internal sentences

Look at the examples, to understand how it works:

| SCs-code level 2-4 | SCs-code level 5 | Description |
|---|---|---|
| `set -> attr: item;;` <br> `item -> subitem;;` | `set` <br> `-> attr: item` <br> `(*` <br> `  -> subitem;;` <br> `*);;` | This is a simple example, that allow to make an sc.s-text more readable and useful. In this case text has a sublevels, that allows to read it faster. |
| `set -> attr: item;;` <br> `item -> subitem;;` <br> `item -> attr2: subitem2;;` | `set` <br> `-> attr: item` <br> `(*` <br> `  -> subitem;;` <br> `  -> attr2: subitem2;;` <br> `*);;` | You can use as much as you need sentences in `(* *)`, but all of them should be separated by `;;`. |
| `@en_idtf = [sc-element];;` <br> `@ru_idtf = [sc-элемент];;` <br> `@en_idtf <- lang_en;;` <br> `@ru_idtf <- lang_ru;;` <br> `sc_element` <br> `=> nrel_main_idtf:` <br> `  @en_idtf;` <br> `  @ru_idtf;;` | `sc_element` <br> `=> nrel_main_idtf:` <br> `  [sc-element]` <br> `  (* <- lang_en;; *);` <br> `=> nrel_main_idtf:` <br> `  [sc-элемент]` <br> `  (* <- lang_ru;; *);;` | This type of syntax is very useful, when you need to specify some meta information on `sc-link`'s. In this example we specify two main identifiers for a `sc_element`. One is an english (`lang_en`) identifier, another one is a russian (`lang_ru`). |

## SCs-code level 6

There are some new complex aliases, that adds by this level of SCs-code:

- `[...]` - this is a short representation of `sc-link` with a content. You can create `sc-link` with a specified content by using this feature. There are all possible cases:

| Type | Description | Example |
|---|---|---|
| `string` | You can write any string that you wish inside `[ ... ]` alias | `x -> [any string];;` <br> `x -> [this is a` <br> ` multiline text];;` |
| `number` | You can specify a number as a binary data. To do that, just use syntax: `[^"type: value"]`. Where `type` is a one of possible types: `int` - signed integer value (32 bit). You can also use such types for an integer: `int8`, `int16`, `int32`, `int64`; `uint` - unsigned integer value (32 bit). You can also use such type for an unsigned integer: `uint8`, `uint16`, `uint32`, `uint64`; `float` - 32-bit float value; `double` - 64-bit float value | `x -> [^"float: 435.2346"];;` <br> `x -> [^"int8: 7"];;` <br> `x -> [^"uint: 781236"];;` |

- `[* ... *]` this is a short representation of `sc-structure`. You can use just sc.s-text inside these brackets. So these brackets will designate an `sc-structure` (`sc-node` with a type `sc_node_structure`). All elements inside brackets will have incoming sc-arc (type `sc_main_arc`) from that `sc-node`.

| SCs-code level 2-5 | SCs-code level 6 |
|---|---|
| `@arc_alias = (set -> item);;` <br> `structure -> set; item; @arc_alias;;` | `@structure = [* set -> item;; *];;` |

> **That's important**
> Сс.s-text inside `[* ... *]` has the same rules and semantic, like it will be in a separated file

- `{ ... }` is a short representation of non-oriented set. This feature allow to make sets in very fast way. Syntax looks like:

```scs
@non_oriented_set = {
  element1;
  attr2: element2;
  ...
  last_element // no semicolon after last element
};;
```

- `< ... >` is a short representation of oriented set. This feature allow to make sets in very fast way. Syntax looks like:

```scs
@oriented_set = <
  element1;
  attr2: element2;
  ...
  last_element // no semicolon after last element
>;;
```

| SCs-code level 2-5 | SCs-code level 6 | Comments |
|---|---|---|
| `set` <br> `<- sc_node_tuple;` <br> `-> element1;` <br> `-> attr2: element2;` <br> `-> element3;;` | `@set = {` <br> `  element1;` <br> `  attr2: element2;` <br> `  element3 // no semicolon` <br> `};;` | Using set looks much cleaner. You can use even attributes on it. |
| `meta_set` <br> `<- sc_node_tuple;` <br> `-> set1;` <br> `-> set2;;` <br><br> `set1` <br> `<- sc_node_tuple;` <br> `-> element1;` <br> `-> attr2: element2;` <br> `-> element3;;` <br><br> `set2` <br> `<- sc_node_tuple;` <br> `-> element5;` <br> `-> element6;;` <br><br> `set3` <br> `<- sc_node_tuple;` <br> `-> element10;;` <br><br> `element` <br> `=> nrel_relation: set3;;` | `@meta_set = {` <br> `  {` <br> `    element1;` <br> `    attr2: element2;` <br> `    element3` <br> `  };` <br> `  {` <br> `    element5;` <br> `    element6` <br> `  }` <br> `};;` <br><br> `element` <br> `=> nrel_relation:` <br> `{` <br> `  element10` <br> `};;` | You can use set alias inside any other complex aliases and triples. |
| `set` <br> `<- sc_node_tuple;;` <br><br> `@first_arc = (set -> rrel_1: element1);;` <br> `@second_arc = (set -> element2);;` <br><br> `nrel_basic_sequence` <br> `-> (@first_arc => @second_arc);;` | `@set = <` <br> `  element1;` <br> `  element2 // no semicolon` <br> `>;;` | Using set looks much cleaner. You can use even attributes on it. |

## Keynodes

There are a list of element type keynodes, that can be used to specify type of sc-element:

| Keynode | Equal sc-type | Possible sc.g-elements |
|---|---|---|
| sc_node | ScType::Node | (const node, var node) |
| sc_link | ScType::ConstNodeLink | (const link, var link) |
| sc_common_edge | ScType::ConstCommonEdge | (common edge) |
| sc_common_arc | ScType::ConstCommonArc | (common arc) |
| sc_membership_arc | ScType::MembershipArc | (membership arc) |
| sc_main_arc | ScType::ConstPermPosArc | (const perm positive arc) |
| sc_node_tuple | ScType::NodeTuple | (const tuple, var tuple) |
| sc_node_structure | ScType::NodeStructure | (const structure, var structure) |
| sc_node_role_relation | ScType::NodeRole | (const role, var role) |
| sc_node_non_role_relation | ScType::NodeNonRole | (const non-role, var non-role) |
| sc_node_class | ScType::NodeClass | (const class, var class) |
| sc_node_superclass | ScType::NodeSuperclass | Not specified |
| sc_node_material | ScType::NodeMaterial | (const material, var material) |

There is an example of usage:

| SCs-code | Equal SCg-code |
|---|---|
| `a <- sc_node_class;;` <br> `a _-> _b;;` <br> `_b <- sc_node_material;;` | *(SCg diagram)* |
| `_x => nrel_y: t;;` <br> `nrel_y <- sc_node_non_role_relation;;` | *(SCg diagram)* |

## Frequently Asked Questions

- [What SCs-code level is recommended to use?](#what-scs-code-level-is-recommended-to-use)
- [Can I combine different levels in one SCs file?](#can-i-combine-different-levels-in-one-scs-file)
- [What is the difference between `set -> a; -> b; -> c;;` and `set -> a; b; c;;`?](#what-is-the-difference-between-set-a-b-c-and-set-a-b-c)

### What SCs-code level is recommended to use?

The first levels of SCs-code have minimal syntax, so it is simple to handle sc.s-text of these levels. But the last levels of SCs-code allow you to make sc.s-text more compact, but these levels of SCs-code have more complicated syntax.

### Can I combine different levels in one SCs file?

All levels of SCs-code can be combined. Usually it is useful to use 4-6 levels if you use 2-3 levels.

### What is the difference between `set -> a; -> b; -> c;;` and `set -> a; b; c;;`?

These sc.s-texts are identical. The second sc.s-text is just short version of the first sc.s-text, it allows to not duplicate sc.s-connectors between sc.s-elements.

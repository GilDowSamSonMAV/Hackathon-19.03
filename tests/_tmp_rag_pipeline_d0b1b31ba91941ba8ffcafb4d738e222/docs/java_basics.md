# Java Basics

## Variables and Data Types

Java is a statically typed language — every variable must be declared with a type before use. The type determines what values the variable can hold and what operations are allowed.

### Primitive Types

| Type | Size | Range | Example |
|---|---|---|---|
| `byte` | 8 bits | -128 to 127 | `byte b = 100;` |
| `short` | 16 bits | -32,768 to 32,767 | `short s = 1000;` |
| `int` | 32 bits | -2³¹ to 2³¹-1 | `int x = 42;` |
| `long` | 64 bits | -2⁶³ to 2⁶³-1 | `long l = 100000L;` |
| `float` | 32 bits | ~7 decimal digits | `float f = 3.14f;` |
| `double` | 64 bits | ~15 decimal digits | `double d = 3.14159;` |
| `char` | 16 bits | Unicode character | `char c = 'A';` |
| `boolean` | 1 bit | true or false | `boolean flag = true;` |

### Reference Types

Reference types include classes, interfaces, arrays, and strings. A reference variable stores a memory address pointing to the object, not the object itself. When you assign one reference to another, both point to the same object.

```java
String name = "Gil";          // String is a reference type
int[] numbers = {1, 2, 3};   // arrays are reference types
```

### Type Casting

**Widening (implicit):** smaller type to larger type. No data loss.
`int x = 10; double d = x;  // int → double automatically`

**Narrowing (explicit):** larger type to smaller type. Risk of data loss. Requires cast.
`double d = 9.78; int x = (int) d;  // x = 9, decimal part lost`

## Control Flow

### Conditional Statements

```java
// if-else
if (grade >= 90) {
    System.out.println("Excellent");
} else if (grade >= 70) {
    System.out.println("Good");
} else {
    System.out.println("Needs improvement");
}

// switch (Java 14+ enhanced)
switch (day) {
    case "Monday", "Tuesday" -> System.out.println("Weekday");
    case "Saturday", "Sunday" -> System.out.println("Weekend");
    default -> System.out.println("Unknown");
}
```

### Loops

```java
// for loop — when you know the number of iterations
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}

// while loop — when the condition is checked before each iteration
while (count > 0) {
    count--;
}

// do-while — executes at least once, checks condition after
do {
    input = scanner.nextLine();
} while (!input.equals("quit"));

// for-each — iterate over arrays or collections
for (String item : items) {
    System.out.println(item);
}
```

**break** exits the loop immediately. **continue** skips the rest of the current iteration and moves to the next one.

## Methods

A method is a block of code that performs a specific task and can be called by name. Methods promote code reuse and organization.

```java
// Method declaration
public static int add(int a, int b) {
    return a + b;
}

// Method call
int result = add(5, 3);  // result = 8
```

**Method signature** consists of the method name and parameter types. Java uses the signature to distinguish overloaded methods.

**Pass by value:** Java always passes arguments by value. For primitives, the value is copied. For objects, the reference (memory address) is copied — so the method can modify the object's state but cannot make the original reference point to a different object.

## Arrays

An array is a fixed-size, ordered collection of elements of the same type.

```java
// Declaration and initialization
int[] numbers = new int[5];          // array of 5 ints, initialized to 0
String[] names = {"Alice", "Bob"};   // array literal

// Access and modify
numbers[0] = 10;                     // set first element
int first = numbers[0];              // get first element
int length = numbers.length;         // array length (not a method — no parentheses)
```

**Common operations:**
- Iterate: `for (int i = 0; i < arr.length; i++)` or `for (int x : arr)`
- Sort: `Arrays.sort(arr)` — uses dual-pivot quicksort for primitives
- Search: `Arrays.binarySearch(arr, target)` — array must be sorted first
- Copy: `Arrays.copyOf(arr, newLength)` — creates a new array
- Print: `Arrays.toString(arr)` — returns string representation like `[1, 2, 3]`

**ArrayIndexOutOfBoundsException** is thrown when accessing an index outside `0` to `length-1`. This is the most common runtime error for beginners. Always check `arr.length` before accessing elements.

Arrays in Java are objects — they are allocated on the heap and accessed via references. When you pass an array to a method, the method receives a copy of the reference, so modifications to array elements inside the method are visible to the caller.

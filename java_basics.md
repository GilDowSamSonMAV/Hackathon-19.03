# Java Basics

Java is a statically-typed, object-oriented programming language. It runs on the Java Virtual Machine (JVM), which means Java programs are compiled to bytecode that can run on any platform with a JVM installed — this is the "write once, run anywhere" principle.

## Variables and Data Types

A **variable** is a named container that holds a value. In Java, every variable must be declared with a specific type before use.

**Primitive types** (stored directly in memory):
- `int` — 32-bit integer. Example: `int age = 25;`
- `long` — 64-bit integer. Example: `long population = 8000000000L;`
- `double` — 64-bit floating-point. Example: `double price = 19.99;`
- `float` — 32-bit floating-point. Example: `float ratio = 0.5f;`
- `boolean` — true or false. Example: `boolean isActive = true;`
- `char` — single character. Example: `char grade = 'A';`
- `byte` — 8-bit integer (-128 to 127). Example: `byte small = 42;`
- `short` — 16-bit integer. Example: `short medium = 1000;`

**Reference types** (stored as a reference to an object in memory):
- `String` — a sequence of characters. Example: `String name = "Lior";`
- Arrays, classes, interfaces — all reference types.

**Key difference**: Primitive types hold the actual value. Reference types hold a pointer to the object in heap memory. This matters for comparison — use `==` for primitives but `.equals()` for objects like String.

## Control Flow

**If-else statements:**
```java
if (grade >= 90) {
    System.out.println("Excellent");
} else if (grade >= 70) {
    System.out.println("Good");
} else {
    System.out.println("Needs improvement");
}
```

**Switch statement:**
```java
switch (day) {
    case "Monday":
        System.out.println("Start of the week");
        break;
    case "Friday":
        System.out.println("Almost weekend");
        break;
    default:
        System.out.println("Regular day");
}
```

**For loop:**
```java
for (int i = 0; i < 10; i++) {
    System.out.println(i);
}
```

**While loop:**
```java
int count = 0;
while (count < 5) {
    System.out.println(count);
    count++;
}
```

**For-each loop** (enhanced for loop, used with arrays and collections):
```java
int[] numbers = {1, 2, 3, 4, 5};
for (int num : numbers) {
    System.out.println(num);
}
```

## Methods

A **method** is a block of code that performs a specific task. Methods promote code reuse and organization.

```java
public static int add(int a, int b) {
    return a + b;
}
```

**Method signature components:**
- `public` — access modifier (who can call this method)
- `static` — belongs to the class, not an instance
- `int` — return type (use `void` if the method returns nothing)
- `add` — method name
- `(int a, int b)` — parameter list

**Method overloading**: Multiple methods with the same name but different parameter lists. Java determines which to call based on the arguments provided.

```java
public static int add(int a, int b) { return a + b; }
public static double add(double a, double b) { return a + b; }
```

## Arrays

An **array** in Java is a fixed-size, ordered collection of elements of the same type. Arrays are zero-indexed — the first element is at index 0.

**Declaration and initialization:**
```java
// Declare and allocate
int[] scores = new int[5];  // creates array of 5 integers, initialized to 0

// Declare and initialize with values
int[] scores = {85, 92, 78, 95, 88};

// Access an element
int first = scores[0];  // 85

// Modify an element
scores[2] = 80;  // changes 78 to 80

// Get array length
int size = scores.length;  // 5 (note: .length is a property, not a method)
```

**Iterating through an array:**
```java
// Traditional for loop
for (int i = 0; i < scores.length; i++) {
    System.out.println("Score " + i + ": " + scores[i]);
}

// Enhanced for-each loop
for (int score : scores) {
    System.out.println(score);
}
```

**2D arrays** (arrays of arrays):
```java
int[][] matrix = {
    {1, 2, 3},
    {4, 5, 6},
    {7, 8, 9}
};
int value = matrix[1][2];  // row 1, column 2 → 6
```

**Key array facts:**
- Arrays have a fixed size after creation — they cannot grow or shrink.
- Accessing an index outside the array bounds throws an `ArrayIndexOutOfBoundsException`.
- Arrays are objects in Java — they are passed by reference to methods.
- For dynamic-size collections, use `ArrayList` from `java.util`.

**Common array operations:**
- Sorting: `Arrays.sort(arr)` — uses dual-pivot quicksort for primitives.
- Searching: `Arrays.binarySearch(arr, key)` — array must be sorted first.
- Copying: `Arrays.copyOf(arr, newLength)` — creates a new array with specified length.
- Comparing: `Arrays.equals(arr1, arr2)` — checks if two arrays have the same elements.

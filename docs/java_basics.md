# Java Basics

Java is a high-level, class-based, object-oriented programming language that is designed to have as few implementation dependencies as possible. It is a general-purpose programming language intended to let programmers write once, run anywhere (WORA), meaning that compiled Java code can run on all platforms that support Java without the need to recompile.

Here are the fundamental building blocks of the Java language.

## 1. Variables and Data Types

In Java, every variable has a type, which determines the values it can hold and the operations that can be performed on it. Java is strongly typed.

### Primitive Types
Java has eight built-in primitive data types:
*   `byte`: 8-bit signed integer.
*   `short`: 16-bit signed integer.
*   `int`: 32-bit signed integer. (Default choice for integer values).
*   `long`: 64-bit signed integer.
*   `float`: 32-bit floating-point.
*   `double`: 64-bit floating-point. (Default choice for decimal values).
*   `boolean`: Represents `true` or `false`.
*   `char`: 16-bit Unicode character.

```java
int age = 25;
double salary = 50000.50;
boolean isEmployed = true;
char grade = 'A';
```

### Reference Types
Reference types hold references (memory addresses) to objects. The most common reference type is `String`.
```java
String name = "John Doe";
```

## 2. Operators

Java provides a rich set of operators:
*   **Arithmetic Operators:** `+` (addition), `-` (subtraction), `*` (multiplication), `/` (division), `%` (modulo - remainder).
*   **Assignment Operators:** `=`, `+=`, `-=`, `*=`, `/=`.
*   **Relational (Comparison) Operators:** `==` (equal to), `!=` (not equal), `>`, `<`, `>=`, `<=`.
*   **Logical Operators:** `&&` (logical AND), `||` (logical OR), `!` (logical NOT).

## 3. Control Flow

Control flow statements break up the flow of execution by employing decision making, looping, and branching, enabling your program to conditionally execute particular blocks of code.

### Conditional Statements
**if-else:**
```java
int score = 85;
if (score >= 90) {
    System.out.println("Grade A");
} else if (score >= 80) {
    System.out.println("Grade B");
} else {
    System.out.println("Grade C");
}
```

**switch:**
```java
int day = 3;
switch (day) {
    case 1:
        System.out.println("Monday");
        break;
    case 2:
        System.out.println("Tuesday");
        break;
    // ...
    default:
        System.out.println("Invalid day");
}
```

### Looping Statements
**for loop:** Used when you know exactly how many times you want to loop through a block of code.
```java
for (int i = 0; i < 5; i++) {
    System.out.println("Iteration: " + i);
}
```

**while loop:** Loops through a block of code as long as a specified condition is `true`.
```java
int count = 0;
while (count < 3) {
    System.out.println("Count: " + count);
    count++;
}
```

## 4. Methods

A method is a block of code which only runs when it is called. You can pass data, known as parameters, into a method. Methods are used to perform certain actions, and they are also known as functions.

Methods must be declared within a class.

```java
public class Calculator {
    // A method that takes two integers and returns their sum
    public static int add(int a, int b) {
        return a + b;
    }

    public static void main(String[] args) {
        int result = add(5, 10); // Calling the method
        System.out.println("Result: " + result);
    }
}
```
*   `public`: Access modifier (accessible from anywhere).
*   `static`: Means the method belongs to the Main class and not an object of the Main class.
*   `void`: The return type (means this method does not return a value). `int` means it returns an integer.

## 5. Arrays

Arrays are used to store multiple values in a single variable, instead of declaring separate variables for each value. In Java, arrays have a fixed size once created.

```java
// Declaring and initializing an array
String[] cars = {"Volvo", "BMW", "Ford", "Mazda"};

// Accessing an element (0-indexed)
System.out.println(cars[0]); // Outputs Volvo

// Changing an element
cars[0] = "Opel";

// Array length
System.out.println(cars.length); // Outputs 4

// Looping through an array
for (int i = 0; i < cars.length; i++) {
    System.out.println(cars[i]);
}
```
You can also declare an array and allocate memory for it later:
```java
int[] myNumbers = new int[5]; // Array of 5 integers, initialized to 0
myNumbers[0] = 10;
```

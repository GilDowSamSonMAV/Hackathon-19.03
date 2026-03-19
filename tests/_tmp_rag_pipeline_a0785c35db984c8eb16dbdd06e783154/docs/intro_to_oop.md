# Introduction to Object-Oriented Programming

## What is OOP?

Object-Oriented Programming (OOP) is a programming paradigm that organizes software design around data, or objects, rather than functions and logic. An object is a data field that has unique attributes and behavior. OOP focuses on the objects that developers want to manipulate rather than the logic required to manipulate them.

## Classes and Objects

A **class** is a blueprint or template for creating objects. It defines the properties (attributes) and behaviors (methods) that objects of that type will have. Think of a class as a cookie cutter — the class defines the shape, and each cookie is an object.

An **object** is a specific instance of a class. When you create an object from a class, you are "instantiating" it. Each object has its own copy of the instance variables defined by the class. For example, if `Dog` is a class, then `myDog` with name "Rex" and age 3 is an object (instance) of that class.

```java
class Dog {
    String name;
    int age;
    
    void bark() {
        System.out.println(name + " says: Woof!");
    }
}

Dog myDog = new Dog();  // myDog is an object of class Dog
myDog.name = "Rex";
myDog.age = 3;
```

## The Four Pillars of OOP

### 1. Encapsulation

Encapsulation is the bundling of data (attributes) and the methods that operate on that data into a single unit (class), and restricting direct access to some of the object's components. This is achieved using access modifiers:

- `private` — accessible only within the same class
- `protected` — accessible within the same class and subclasses
- `public` — accessible from anywhere

The principle behind encapsulation is **information hiding**. By making fields private and providing public getter and setter methods, you control how data is accessed and modified. This prevents external code from putting an object into an invalid state.

```java
class BankAccount {
    private double balance;  // hidden from outside
    
    public double getBalance() {
        return balance;
    }
    
    public void deposit(double amount) {
        if (amount > 0) {
            balance += amount;  // validation before modification
        }
    }
}
```

### 2. Inheritance

Inheritance allows a new class (subclass/child) to inherit properties and methods from an existing class (superclass/parent). This promotes code reuse and establishes a natural hierarchy.

In Java, inheritance is implemented using the `extends` keyword. A subclass inherits all non-private members of its parent class and can add new fields and methods or override existing ones.

```java
class Animal {
    String name;
    void eat() { System.out.println(name + " is eating"); }
}

class Cat extends Animal {
    void purr() { System.out.println(name + " is purring"); }
}
```

Java supports **single inheritance** only — a class can extend only one other class. However, a class can implement multiple interfaces. The inheritance chain can be multiple levels deep: `Animal → Cat → PersianCat`.

### 3. Polymorphism

Polymorphism means "many forms." It allows objects of different classes to be treated as objects of a common superclass. There are two types:

**Compile-time polymorphism (method overloading):** Multiple methods in the same class share the same name but have different parameter lists.

```java
class Calculator {
    int add(int a, int b) { return a + b; }
    double add(double a, double b) { return a + b; }
}
```

**Runtime polymorphism (method overriding):** A subclass provides a specific implementation of a method that is already defined in its superclass. The JVM determines which method to call at runtime based on the actual object type.

```java
Animal myAnimal = new Cat();  // polymorphic reference
myAnimal.eat();  // calls Cat's eat() if overridden, else Animal's
```

Polymorphism is powerful because it enables writing code that works with the superclass type but automatically adapts to the specific subclass behavior at runtime. This is the foundation of many design patterns.

### 4. Abstraction

Abstraction is the concept of hiding complex implementation details and showing only the necessary features of an object. In Java, abstraction is achieved through:

- **Abstract classes** — classes declared with `abstract` that cannot be instantiated and may contain abstract methods (methods without implementation)
- **Interfaces** — contracts that define what methods a class must implement, without specifying how

```java
abstract class Shape {
    abstract double area();  // no implementation — subclasses must provide it
    
    void describe() {
        System.out.println("This shape has area: " + area());
    }
}
```

Abstraction lets you define "what" an object does without specifying "how." The caller doesn't need to know the internal workings — they just use the public interface.

## Why OOP Matters

OOP provides modularity, making large programs easier to manage. It promotes code reuse through inheritance. It enables flexibility through polymorphism. And it protects data integrity through encapsulation. Most modern languages — Java, Python, C++, C# — are built around OOP principles. Understanding these four pillars is essential for writing maintainable, scalable software.

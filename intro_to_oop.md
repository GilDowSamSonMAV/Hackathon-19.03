# Introduction to Object-Oriented Programming

Object-Oriented Programming (OOP) is a programming paradigm that organizes software design around objects rather than functions and logic. An object is a data structure that contains both data (attributes) and code (methods) that operate on that data. OOP is the dominant paradigm in modern software engineering and is used in languages like Java, Python, C++, and C#.

## Classes and Objects

A **class** is a blueprint or template that defines the structure and behavior of objects. It specifies what attributes an object will have and what methods it can perform. An **object** is a specific instance of a class — it is created from the class blueprint and holds actual values for the attributes.

For example, a `Car` class might define attributes like `color`, `speed`, and `fuel_level`, and methods like `accelerate()`, `brake()`, and `refuel()`. When you create a specific car — say a red Toyota with speed 0 and full fuel — that is an object (an instance of the `Car` class).

A class can be thought of as a cookie cutter, and objects are the cookies. The cutter defines the shape, but each cookie is its own independent thing.

**Constructor**: A special method (often called `__init__` in Python or the class-name method in Java) that runs when a new object is created. It initializes the object's attributes with starting values.

## Encapsulation

**Encapsulation** is the principle of bundling data and the methods that operate on that data within a single unit (the class), and restricting direct access to some of the object's components. This is achieved through access modifiers:

- **Public**: Accessible from anywhere. In Java, declared with the `public` keyword.
- **Private**: Accessible only within the class itself. In Java, declared with `private`. In Python, conventionally indicated by a leading underscore `_attribute` or double underscore `__attribute` for name mangling.
- **Protected**: Accessible within the class and its subclasses. In Java, declared with `protected`.

The purpose of encapsulation is to protect the internal state of an object from unintended interference. Instead of accessing attributes directly, external code uses **getter** and **setter** methods. This allows the class to validate or transform data before it is stored.

For example, a `BankAccount` class might have a private `_balance` attribute. Instead of allowing direct modification, it provides a `deposit(amount)` method that checks if the amount is positive before adding it to the balance.

## Inheritance

**Inheritance** allows a new class (the **child** or **subclass**) to inherit attributes and methods from an existing class (the **parent** or **superclass**). The child class can then add new attributes or methods, or override existing ones.

This promotes code reuse. If you have a `Vehicle` class with attributes like `speed` and `fuel` and methods like `start()` and `stop()`, you can create `Car`, `Truck`, and `Motorcycle` subclasses that inherit all of those features and add their own specific behavior.

**Key terminology:**
- **Superclass / Parent class**: The class being inherited from.
- **Subclass / Child class**: The class that inherits.
- **Override**: When a subclass provides its own implementation of a method defined in the superclass.
- **`super()`**: A reference to the parent class, used to call the parent's constructor or methods from within the child class.

**Types of inheritance:**
- **Single inheritance**: A class inherits from one parent (supported in Java, Python).
- **Multiple inheritance**: A class inherits from multiple parents (supported in Python, NOT in Java — Java uses interfaces instead).
- **Multilevel inheritance**: A chain where class C inherits from B, which inherits from A.

## Polymorphism

**Polymorphism** means "many forms." In OOP, it allows objects of different classes to respond to the same method call in their own way. The caller does not need to know the specific type of the object — only that it supports the method being called.

There are two main types of polymorphism:

**Compile-time polymorphism (Method Overloading)**: Multiple methods in the same class have the same name but different parameter lists. The compiler determines which method to call based on the arguments provided. Example: a `Calculator` class might have `add(int a, int b)` and `add(double a, double b)`.

**Runtime polymorphism (Method Overriding)**: A subclass provides its own implementation of a method defined in its superclass. The method that gets called is determined at runtime based on the actual object type, not the reference type. This is the more powerful form and is the basis of many design patterns.

Example: A `Shape` superclass has a `draw()` method. `Circle`, `Square`, and `Triangle` each override `draw()` with their own implementation. A list of `Shape` objects can call `draw()` on each one, and each shape draws itself correctly — without the calling code knowing which specific shape it is.

## Abstraction

**Abstraction** is the principle of hiding complex implementation details and exposing only the essential features of an object. Abstract classes and interfaces are the primary mechanisms for achieving abstraction.

An **abstract class** cannot be instantiated directly. It serves as a base class that defines a contract — certain methods that subclasses must implement. In Java, this is declared with the `abstract` keyword.

An **interface** is a completely abstract type that defines only method signatures without any implementation (in traditional Java; modern Java allows default methods). A class can implement multiple interfaces, which is Java's workaround for lacking multiple inheritance.

Abstraction helps manage complexity in large systems. A developer using a `Database` interface doesn't need to know whether the underlying implementation uses MySQL, PostgreSQL, or MongoDB — they just call `connect()`, `query()`, and `close()`.

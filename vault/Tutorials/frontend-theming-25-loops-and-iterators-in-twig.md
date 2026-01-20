---
title: "Loops and Iterators in Twig"
url: "https://drupalize.me/tutorial/loops-and-iterators-twig?p=2464"
guide: "[[frontend-theming]]"
order: 25
---

# Loops and Iterators in Twig

## Content

Many of the variables that you have access to inside of a Twig template file are arrays. For example a list of values for a multi-value field, or a set of error messages generated when validating a form submission. In order to work with arrays in Twig you'll need to understand how `for` loops work. This is essential information for anyone creating Drupal themes.

In this tutorial we'll cover:

- Using the `for` tag to iterate over an array
- Using the `loop` variable inside of a `for` loop for additional context

## Goal

Understand what loops and interators are and what's inside the special context variable `loop`.

## Prerequisites

- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)
- [Arrays and Objects in Twig](https://drupalize.me/tutorial/arrays-and-objects-twig)

## Loops and iterators

In Twig, the `for` tag is used to loop over each item in a sequence. It might be used to display a list of tags from a multiple value taxonomy reference field. Whatever markup is inside of the `for` block will be rendered once for each item in the sequence.

The following example outputs an unordered list of items:

```
  <ul class='blog-post__tags field__items'>
    {% for item in items %}
      <li>{{ item.content }}</li>
    {% endfor %}
  </ul>
```

Note: A sequence can be either an array or an object implementing the [Traversable interface](https://www.php.net/manual/en/class.traversable.php).

In Drupal, this comes into play when dealing with things like multiple value fields where you might have one or more tags to print in a list. Or you might have a page template that displays a status message at the top of a page, and need to accommodate the display of zero, one, or more messages.

## The loop variable

Inside of a `for` loop block you also have access to the special `loop` variable which contains information about the current state, and context of the loop. These properties are documented below.

| Variable | Description |
| --- | --- |
| `loop.index` | The current iteration of the loop. (1 indexed) |
| `loop.index0` | The current iteration of the loop. (0 indexed) |
| `loop.revindex` | The number of iterations from the end of the loop (1 indexed) |
| `loop.revindex0` | The number of iterations from the end of the loop (0 indexed) |
| `loop.first` | True if first iteration |
| `loop.last` | True if last iteration |
| `loop.length` | The number of items in the sequence |
| `loop.parent` | The parent context |

## Iterating over key/value pairs

You can access both the keys and their corresponding values when looping over an array.

```
  <ul class='blog-post__tags field__items'>
    {% for delta, value in items %}
      <li>{{delta}}: {{ value.content }}</li>
    {% endfor %}
  </ul>
```

## Update templates that use `if` conditions in loops

[Drupal now uses Twig 3](https://www.drupal.org/node/3256890). Support for the `if` clause has been removed from `for` statements as of Twig 2.10. You can use a filter or an `if` condition inside the `for` body, (if your condition depends on an updated variable inside the loop and you are not using the `loop` variable).

You will need to update Twig templates that contain code blocks that use `if` in a `for` statement.

Before, you might have something like this:

```
  <ul class='blog-post__tags field__items'>
    {% for item in items if item.status %}
      <li>{{ value.content }}</li>
    {% endfor %}
  </ul>
```

You could update the above code block to separate the `if` and `for` statements (instead of combined as was previously supported).

```
  <ul class='blog-post__tags field__items'>
    {% for item in items %}
      {% if item.status %}
        <li>{{ value.content }}</li>
      {% endif %}
    {% endfor %}
  </ul>
```

See also this change record: [Twig updated from 2.x to 3.x](https://www.drupal.org/node/3256890).

### The `else` condition

The `else` condition provides a simple way to handle the scenario where a variable may be empty and you would like to display a special "empty" text instead of just nothing.

```
  <ul class='blog-post__tags field__items'>
    {% for item in items %}
      <li>{{ item.content }}</li>
    {% else %}
      <li>This list is empty</li>
    {% endfor %}
  </ul>
```

## Recap

In this tutorial, we familiarized ourselves with the `for` loop syntax and the special `loop` variable that's available inside a `for` loop.

## Further your understanding

- Find a template in Drupal core that uses a `for` loop as an example that you could copy/paste from in the future.
- Learn how to print values from a field in Drupal with a `for` loop in this tutorial: [Print Values from a Field with a For Loop](https://drupalize.me/tutorial/print-values-field-loop).

## Additional resources

- [Twig documentation on for loops](https://twig.symfony.com/doc/3.x/tags/for.html) (twig.symfony.com)
- Change record: [Twig updated from 2.x to 3.x](https://www.drupal.org/node/3256890) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Arrays and Objects in Twig](/tutorial/arrays-and-objects-twig?p=2464)

Next
[Print Values from a Field with a For Loop](/tutorial/print-values-field-loop?p=2464)

Clear History

Ask Drupalize.Me AI

close
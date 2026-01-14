---
title: "Arrays and Objects in Twig"
url: "https://drupalize.me/tutorial/arrays-and-objects-twig?p=2464"
guide: "[[frontend-theming]]"
order: 53
---

# Arrays and Objects in Twig

## Content

Twig has a special syntax for accessing array keys and objects, also known in Twig as *variable attributes*. In this tutorial, we'll cover the period or dot (`.`) operator to access a variable attribute, as well as subscript or square-bracket syntax, useful for when the key of the array contains special characters, like a dash (`-`) or pound sign (`#`). We'll also look at the logic Twig uses to find the matching attribute in an array or object.

## Goal

Know how to access array keys with and without special characters in a Drupal template file using Twig.

## Prerequisites

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [Inspect Variables Available in a Template](https://drupalize.me/tutorial/inspect-variables-available-template)
- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)

Sprout Video

## Variable attributes

In the context of a Twig template file, variables may have accessible attributes or elements that you can access. These *variable attributes* can be array keys, object properties, or object methods.

To make it more convenient for template designers, Twig uses the dot (".") to access attributes on variables, regardless of their data type. Twig goes through a series of logic checks to find a matching variable. Only if it can't find a match will it return `null`. Here's the order of checks that Twig performs:

On the PHP layer in Drupal, for `{{ foo.bar }}` in a *\*.html.twig* file, the following checks are performed:

1. Check if `foo` is an array and `bar` a valid element.
2. If not, and if `foo` is an object, check that `bar` is a valid property.
3. If not, and if `foo` is an object, check that `bar` is a valid method (even if `bar` is the constructor, use `__construct()` instead).
4. If not, and if `foo` is an object, check that `getBar` is a valid method.
5. If not, and if `foo` is an object, check that `isBar` is a valid method.
6. If the variable passed is a render array, check to see if it was pre-rendered by checking to see if its property `#printed` exists and is true and if so, output its `#markup` property value, otherwise, call `render()` on it.
7. If no checks return true, return a `null` value.

See also: [Twig documentation on variables](https://twig.symfony.com/doc/3.x/templates.html#variables).

Note: Step 6 is Drupal-specific. See `Drupal\Core\Template\TwigExtension::renderVar()` in *core/lib/Drupal/core/Template/TwigExtension.php*, starting with line 586 and `Drupal\Core\Template::doLeaveNode()` in *core/lib/Drupal/Core/Template/TwigNodeVisitor.php* which calls it.

## Array keys in Twig

Some variables passed to the template file are a PHP array data type. A common example is the `page` array in *page.html.twig*, which contains an array of page regions. To print out these regions in our page template file, we need to know how to access array elements in the `page`. variable.

To access an array key, use the period (`.`) operator. For example, to access the `sidebar_right` key of the `page` variable array: `page.sidebar_right`.

To print out `page.sidebar_right`, use the double-curly-brace syntax delimiter:

```
{{ page.sidebar_right }}
```

To use it within a control structure, such as with an `if` tag, follow this example, using curly-brace-percent delimiters:

```
{% if page.sidebar_right %}
  {{ page.sidebar_right }}
{% endif %}
```

## Numeric array keys

To access a numeric key outside of a `for` loop, you can still use the dot with a numeral:

```
{{ variable.1 }}
```

In fact, even though technically you can use square brackets to access a numerical key, for example, `variable[1]`, we recommend that you use the dot syntax.

(To print out multiple items in an array, Twig has a special syntax for printing out items inside a `for` loop. Learn how to use it in [Print Values from a Field with a For Loop](https://drupalize.me/tutorial/print-values-field-loop).)

## Square brackets and special characters

Square brackets, also known as "subscript syntax", are allowable as well, but only on arrays. You'll need to wrap the array key in single-quotes and square brackets if your variable name contains a function or special characters, such as a pound sign (`#`) for a hash key or a dash (`-`), which would otherwise get interpreted as a subtraction operator. In Drupal, hash keys are quite prevalent, [as they signify properties in render arrays](https://drupalize.me/tutorial/what-are-render-arrays).

Here are a few recommended examples of how square brackets can be used to reference array keys in Twig:

```
{{ variable['#key'] }}
{{ variable['hyphenated-key'] }}
{{ content.field_image.0['#item'].alt }}
{{ variable[random(4)] }}
```

These examples will technically work, but we recommend that you use the dot syntax instead.

```
{{ variable['key'] }} {# This is allowed, but use {{ variable.key }} instead! #}
{{ variable[0] }} {# This is allowed, but use {{ variable.0 instead! }} #}
```

In fact, we recommend that you only use square brackets to reference an array key when the name of the key includes a special character like a hyphen (`-`) or a pound sign (`#`) or if you're using a function as a variable.

## Attribute function

The attribute function can be used to replace a key containing special characters in square brackets. It takes two parameters, the variable (including any attributes) and the name of the key you want to find inside the first variable. For example:

```
{{ attribute(content.field_image.0, '#item').alt }}
```

However, as you can see, it doesn't enhance the readability of this code, especially in this example.

We recommend square brackets and not the attribute function for referencing array keys containing special characters, for example:

```
{{ content.field_image.0['#item'].alt }}
```

There are no examples of `attribute()` in Drupal core.

While we don't recommend using the `attribute()` function, we include it here for completeness, as it is part of the Twig documentation on referencing variable attributes. And who knows, you might find an edge use case for it.

## Multi-level and combining syntaxes

To access an array key multiple levels deep, keep using the period operator.

```
{{ variable.key.another }}
{{ variable.key.0.another }}
```

If you need to combine the period operator with square syntax, omit the preceding period before the square-bracketed key. And to access a level deeper than the square-bracketed key, follow the closing bracket with a period and then the next key. For example:

```
{{ variable.0['#hash'].key }}
```

Another example: let's say I have a custom block with an image field. Overriding the block's template file in my custom theme, using one of the file name suggestions, I can access the `alt`, `width`, and `height` values like so:

```
{{ content.field_image.0['#item'].alt }} {# Alt attribute #}
{{ content.field_image.0['#item'].width }} {# Width attribute #}
{{ content.field_image.0['#item'].height }} {# Height attribute #}
```

## The use of object operators in Twig

Note that you cannot use the PHP object operator (`->`) in a Twig template file. Twig will escape the greater-than sign that is part of the object operator and will return a PHP error on the page containing your template. To access elements inside an object, use the dot operator or the `attribute()` function, or failing that, make the variable available to your template via a [preprocess function](https://drupalize.me/tutorial/add-variables-template-file).

## Recap

In this tutorial, we learned how to access arrays and objects in a Twig template file using the period (`.`) syntax. We also learned how to access variable attributes containing special characters as well as how to access variable attributes multiple levels deep.

## Further your understanding

- [Put your local site instance into developer mode](https://drupalize.me/tutorial/configure-your-environment-theme-development), [create a custom theme](https://drupalize.me/tutorial/describe-your-theme-info-file), and [override a template file](https://drupalize.me/tutorial/override-template-file). (Maybe start with *page.html.twig*.) [Inspect variables in your template of choice](https://drupalize.me/tutorial/inspect-variables-available-template) and practice printing out variables that contain attributes, such as regions in a page template file.

## Additional resources

- [Twig documentation for template designers: Variables](https://twig.symfony.com/doc/3.x/templates.html#variables) (twig.symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Twig Syntax Delimiters](/tutorial/twig-syntax-delimiters?p=2464)

Next
[Loops and Iterators in Twig](/tutorial/loops-and-iterators-twig?p=2464)

Clear History

Ask Drupalize.Me AI

close
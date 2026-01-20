---
title: "Drupal Code Standards: Documentationfree"
url: "https://drupalize.me/tutorial/drupal-code-standards-documentation?p=2458"
guide: "[[develop-drupal-sites]]"
order: 8
---

# Drupal Code Standards: Documentationfree

## Content

Standardized documentation is crucial to a project, whether it is just you or an entire team working on it. In this tutorial we're going to look at:

- Standards for `@docblock` comments
- Standards for inline comments
- Why standards for documentation and comments are as important as standards for the rest of your code.

By the end of this tutorial you'll know how to add inline documentation for all the PHP code that you write for Drupal.

## Goal

Write comments and documentation that adhere to the coding standards guidelines.

## Prerequisites

- [What Are Coding Standards?](https://drupalize.me/tutorial/what-are-drupal-code-standards)

## Contents

- [Why is documentation important?](#why)
- [Doc blocks](#docblock)
  - [File doc blocks](#file)
  - [Function doc blocks](#function)
  - [Tags](#tags)
  - [Lists](#lists)
  - [Implements hook\_xyz()](#implements)
- [API module](#api-module)
- [Inline comments](#inline-comments)
- [Content style guide](#content-style-guide)

## Why is documentation important?

Documentation tells us what our code does: how it’s set up, what variables it uses, what it returns. It tells us what to expect from our code.

### But I know what my code does!

Sure you do—right now. You just wrote it. But how about 2 months or 10 projects from now? What about someone else? The key is to make your code maintainable by everyone. Of course, ideally, you’re writing code that’s easy to comprehend because you did everything in a perfectly logical and straightforward way--but comment it thoroughly, just in case. You might also do something clever to solve a tricky problem, but to the next person, it might look like a mistake. Documentation can clear this up.

### But my code is so good, it’s self-documenting!

Of course it is, but even to the best programmer, documentation is quicker and easier to read than code. Documentation is especially helpful for beginning programmers, say someone who’s just starting with Drupal and PHP is looking through your code to see if it does what they need. If you can spell it out for them, you’ll help them figure out what they need a lot faster. Thanks to Drupal’s [documentation standards](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards), we have a few ways to document code that are designed to be quick and easy for the developer writing the code, as well as the developers reading and modifying it. That said, try to avoid repetitive inline comments. You don't need to comment on every single line of code, especially if it's very clear what it's doing. Comment on functions, large blocks of code, tricky things, things that may change. Think about what might be unclear to the next person who looks at it.

## Doc blocks

One of the most important parts of documentation in Drupal is the doc block, a specially formatted block of information that goes either at the top of a PHP file or before each function, method, or class definition.

### File doc blocks

A file doc block goes at the top of a file to give you an overview of what the file contains. These go at the top of every PHP file, and there should be one blank line between the opening tag and the doc block. Here’s an example from the [Backup and Migrate](https://www.drupal.org/project/backup_migrate) module:

```
<?php

/**
 * @file
 * Create (manually or scheduled) and restore backups of your Drupal MySQL
 * database with an option to exclude table data (e.g. cache_*).
 */
```

It’s short and simple and explains what to expect in this module file. Each function will be documented separately, so this doesn’t need to be extensive. On the next line after the file tag, we have a description. The `@file` doc block may also commonly include `@author` and `@version`.

```
/**
 * @file
 * Provides hook implementations for the chromatic_blog module.
 *
 * @author Chris Free
 *
 * @version 1.0
 */
```

In something like a template file, you’ll see more detail in the `@file` doc block, because the rest of the file may not have as much documentation. The `@file` doc block may often spell out available variables.

Here’s an example from the [Bartik](https://www.drupal.org/project/bartik) theme's *comments.tpl.php* template:

**Note:** This example is from a Drupal 7 *\*.tpl.php* template file. For Twig files used in Drupal see [Drupal Code Standards: Twig](https://drupalize.me/tutorial/drupal-code-standards-twig).

```
/**
 * @file
 * Bartik's theme implementation to provide an HTML container for comments.
 *
 * Available variables:
 * - $content: The array of content-related elements for the node. Use
 *   render($content) to print them all, or
 *   print a subset such as render($content['comment_form']).
 * - $classes: String of classes that can be used to style contextually through
 *   CSS. It can be manipulated through the variable $classes_array from
 *   preprocess functions. The default value has the following:
 *   - comment-wrapper: The current template type, i.e., "theming hook".
 * - $title_prefix (array): An array containing additional output populated by
 *   modules, intended to be displayed in front of the main title tag that
 *   appears in the template.
 * - $title_suffix (array): An array containing additional output populated by
 *   modules, intended to be displayed after the main title tag that appears in
 *   the template.
 *
 * The following variables are provided for contextual information.
 * - $node: Node object the comments are attached to.
 * The constants below the variables show the possible values and should be
 * used for comparison.
 * - $display_mode
 *   - COMMENT_MODE_FLAT
 *   - COMMENT_MODE_THREADED
 *
 * Other variables:
 * - $classes_array: Array of html class attribute values. It is flattened
 *   into a string within the variable $classes.
 *
 * @see template_preprocess_comment_wrapper()
 */
```

### Function doc blocks

A function doc block goes just before every function in every PHP file. No exceptions. Even if it’s a one-line function, it gets a doc block. Now, the Coder module will let you get away with only putting the one-line summary of your function, as this is all that’s technically required. For some functions, this may be appropriate, but if your function has any parameters or return values, you should absolutely be documenting them. Yes, it’s more work upfront, but it’s vital work that saves time in the future.

Here we’ll look at a function from the [Backup and Migrate](https://www.drupal.org/project/backup_migrate) module.

This passes Coder's checks, as it has a one-line summary of the function:

```
/**
 * Restore from a file in the given destination.
 */
```

But this is better:

```
/**
 * Restore from a file in the given destination.
 *
 * @param string $destination_id
 *   The machine-readable path of the backup destination.
 * @param object|string $file
 *   The file object, or its name.
 * @param object|array $settings
 *   A settings object, or array to create a settings object.
 *
 * @return object|bool
 *   Returns the file, or FALSE if the restore had any errors.
 */
```

Now we know what is passed to the function, what each variable is, and what the function returns. Good documentation can also aid in debugging - if the documentation doesn’t match what’s happening in the code, you know something is wrong, and you’ve got a starting point for fixing it.

### Tags

There are a variety of tags you can use in your doc blocks to indicate what this documentation is about, and they’re expected to go [in a certain order](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#order), as follows:

- One-line summary, ending in a period, preferrably 80 characters or fewer
- Additional paragraph(s) of explanation wrapped at 80 charaters
- [@var](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#var): Document a variables data type
- [@param](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#param): Document paramaters for a function or method
- [@return](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#return): Document return values for a function or method
- [@throws](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#throws): Document exceptions thrown
- [@ingroup](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#defgroup): Indicate this code belongs to a `@defgroup` topic
- [@deprecated](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#deprecated): Indicate that this code has been deprecated
- [@see](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#see): Reference related code or topics
- [@todo](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#todo): List of known todo items related to a block of code
- [@Plugin](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#Plugin) and other [annotations](https://drupalize.me/tutorial/annotations)

Each type of tag should be separated by a blank line. The most-used tags in function doc blocks are probably `@param` and `@return`.

Here’s an example of how the [Countries](https://www.drupal.org/project/countries) module uses some of the other tags:

```
/**
 * Generate a country form.
 *
 * @ingroup forms
 *
 * @see countries_admin_form_validate()
 * @see countries_admin_form_submit()
 */
```

Groups and topics are tags that come from [Doxygen](https://www.doxygen.nl/index.html), on which these standards are based, and it helps to group generated documentation from the [API module](https://www.drupal.org/project/API). From [Drupal.org](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#defgroup):

> ### @defgroup, @addtogroup, @ingroup, @{, @}: Groups and topics
>
> The `@defgroup` tag is used to define a "group" (in Doxygen terms), which the API module displays as a Topic page. A `@defgroup` tag needs to be in its own docblock (not inside a file description docblock, function docblock, class docblock, etc.). A group defined by `@defgroup` has an identifier (starting with a letter, and composed of numbers, letters, underscores, periods, and hyphens), a title, a summary, and documentation. In addition, individual "items" (files, functions, classes, and other things that are documented with docblocks in the API module) can be designated as being "in" the group. The API module makes a page for each group/topic, and on the page, it lists all of the items that are part of the group.

Here’s an example of `@defgroup` from Drupal core - groups are used more often when you have a large amount of code, like core does. You’ll also see an example of `@code` and `@endcode` used here - this tells the API Module to format that text as code.

```
/**
 * @defgroup php_wrappers PHP wrapper functions
 * @{
 * Functions that are wrappers or custom implementations of PHP functions.
 *
 * Certain PHP functions should not be used in Drupal. Instead, Drupal's
 * replacement functions should be used.
 *
 * For example, for improved or more secure UTF8-handling, or RFC-compliant
 * handling of URLs in Drupal.
 *
 * For ease of use and memorizing, all these wrapper functions use the same name
 * as the original PHP function, but prefixed with "drupal_". Beware, however,
 * that not all wrapper functions support the same arguments as the original
 * functions.
 *
 * You should always use these wrapper functions in your code.
 *
 * Wrong:
 * @code
 *   $my_substring = substr($original_string, 0, 5);
 * @endcode
 *
 * Correct:
 * @code
 *   $my_substring = Unicode::substr($original_string, 0, 5);
 * @endcode
 *
 * @}
 */
```

And in another function block, we’ll see:

```
@ingroup php_wrappers
```

Which tells us that this function is part of the php\_wrappers group. It’s a handy way to organize your code once you get the hang of it!

As an example of this in the real world, check out the [PHP wrapper functions](https://api.drupal.org/api/drupal/core%21includes%21common.inc/group/php_wrappers) page on api.drupal.org. The doc block shown above is used for the main content of the page, and the list of functions in the table at the bottom is derived from the `@ingroup php_wrappers` tag.

The `@deprecated` tag is useful if you don’t want to delete a function – someone could have custom code that relies on it – but you want to let people know this is no longer the best practice way to do something and will be removed in a future version.

```
/**
 * Wrapper for country_load().
 *
 * @deprecated
 *   Use country_load($iso2) instead.
 */
```

### Lists

[You can create lists](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards#lists) in your doc blocks that will be interpreted by the API module as unordered lists. They can also make it easier to read. Start the line with a hyphen to indicate a list item. Here is an example from the [CKEditor](https://www.drupal.org/project/ckeditor) module:

```
/**
 * Implementation of hook_requirements().
 *
 * This hook will issue warnings if:
 * - The CKEditor source files are not found.
 * - The CKEditor source files are out of date.
 * - Quick upload and/or the built-in file browser are used and $cookie_domain is not set.
 */
```

### Implements hook\_xyz()

If you are implementing a hook - for example, `hook_menu`, all you have to put in the function doc block is:

```
/**
 * Implements hook_menu().
 */
```

In fact, if you put more than this, Coder will give you a warning such as:

```
 8 | WARNING | Format should be "* Implements hook_foo().", "* Implements
   |         | hook_foo_BAR_ID_bar() for xyz_bar().",, "* Implements
   |         | hook_foo_BAR_ID_bar() for xyz-bar.html.twig.", or "* Implements
   |         | hook_foo_BAR_ID_bar() for xyz-bar.tpl.php.".
```

You also do not need to duplicate the documentation for the function, such as the parameters. If you do, you’ll get a warning such as:

```
11 | WARNING | Hook implementations should not duplicate @param documentation
```

The thinking here is that there is no reason to duplicate documentation and that anyone wanting to know what the parameters or return values for this particular function are can read the documentation for the hook itself.

If it’s really important that you document something that has changed in your implementation, never skimp on documentation. However, you can always put the documentation inside the function if you want to keep Coder happy about the doc block.

## API module

Why are these doc blocks so important, and why do they have to be formatted so exactly? The [API Module](https://www.drupal.org/project/API) parses the information in doc blocks into the easier to read and navigate documentation available on [api.drupal.org](https://api.drupal.org/api/drupal), so it’s especially important to make sure the format is correct. Any documentation that strays from this format will be human-readable, but won’t be properly parsed.

## Inline comments

Inline comments are important, because this is what you’ll use to explain your code throughout your files. Drupal generally uses the C++-style `//` notation, though C-style comments (`/* */`) are allowed, but discouraged within functions. Inline comments shouldn’t follow a statement - this means they must get their own line. It’s usually understood that a comment precedes the line it’s commenting on, but you can always make this clearer by saying something like "The following line does XYZ."

Remember from our [Code Standards Formatting tutorial](https://drupalize.me/tutorial/drupal-code-standards-formatting) that inline comments must always end with a period and must never be longer than 80 characters. Here’s an example from a contributed module:

Wrong:

```
  'iso2' => array(
    '12', // Numerical
    '', // Empty
    '$s', // Special char
    'au', // Duplicate
    'd', // Single property
    'ddd', // Too long
  ),
```

Right:

```
  'iso3' => array(
    // Numerical.
    '123',
    // Special char.
    '$ss',
    // Duplicate.
    'aus',
    // Single char.
    'd',
    // Double char.
    'dc',
    // Too long.
    'xaaa',
  ),
```

Right, but discouraged:

```
'numcode' => array(
  '1001', /* Too big. */
  '-1', /* Too small. */
  '-12', /* Too small. */
  '-123', /* Too small. */
  '$23', /* Special char. */
  '23#', /* Special char. */
  '048', /* Duplicate. */
  '4', /* Duplicate. */
  '04', /* Duplicate. */
),
```

## Content style guide

Drupal.org has [a style guide for content](https://www.drupal.org/drupalorg/style-guide/content) on the site, and it’s encouraged to use this guide for anything you write inside of Drupal code. Much of it is the style of various industry-related terms, along with Drupal-specific terms. It’s worth reviewing at least once. The clearer our content, the better we can communicate with each other and with new Drupal users.

## Recap

In this tutorial we’ve covered why documentation is essential, how to write file and function doc blocks for the API module in your Drupal code, and inline comments. As detailed as this may seem, it’s still only an overview &em;the [Drupal.org page](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards) has even more detail&em; but this overview will get you started and give you a reference point. Now go forth and document!

## Further your understanding

- Check out [api.drupal.org](https://api.drupal.org/api/drupal). The content of this site is generated entirely from the documentation and comments in the Drupal core codebase.
- Can you find examples of different tags like `@ingroup`, and `@see`, and `@deprecated` in the Drupal core code? If you look up those functions or methods on <api.drupal.org>, how are these tags represented?

## Additional resources

- [API documentation and comment standards](https://www.drupal.org/docs/develop/coding-standards/api-documentation-and-comment-standards) (Drupal.org) - Drupal's official commenting and documentation standards.
- [API documentation samples](https://www.drupal.org/docs/develop/coding-standards/api-documentation-samples) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal Code Standards: Formatting](/tutorial/drupal-code-standards-formatting?p=2458)

Next
[Drupal Code Standards: Object-Oriented Programming](/tutorial/drupal-code-standards-object-oriented-programming?p=2458)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Drupal Training Resources by Alanna Burke of [Chromatic](https://chromatichq.com) are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://chromatichq.com/blog>.

Clear History

Ask Drupalize.Me AI

close
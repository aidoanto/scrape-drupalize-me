---
title: "Drupal Code Standards: Formattingfree"
url: "https://drupalize.me/tutorial/drupal-code-standards-formatting?p=2458"
guide: "[[develop-drupal-sites]]"
order: 7
---

# Drupal Code Standards: Formattingfree

## Content

Formatting standards cover things like the use of whitespace, how to format control structures, and other aspects that affect your code's appearance and format.

In this tutorial we’ll talk specifically about standards regarding formatting. This is by no means an exhaustive list of PHP syntax rules, but rather is focused on formatting standards for Drupal.

By the end of this tutorial you'll know about the most common Drupal code formatting standards as well as where to find more information when questions arise.

## Goal

Introduce the most commonly encountered standards regarding the formatting of Drupal code.

## Prerequisites

- [What Are Coding Standards?](https://drupalize.me/tutorial/what-are-drupal-code-standards)

## Contents

- [Indentation](#indentation)
- [Whitespace](#whitespace)
- [File endings](#file-endings)
- [Line length](#line-length)
- [Operators](#operators)
- [Function calls and declarations](#functions)
- [Constants](#constants)
- [Control structures](#control-structures)
- [Twig](#twig)
- [Casting](#casting)
- [Semicolons](#semicolons)
- [PHP Tags](#php-tags)

## Indentation

There is much debate over tabs versus spaces in the programming world, but here in the Drupal community, we use spaces—two spaces, to be exact.

In [How to Implement Code Standards](https://drupalize.me/tutorial/how-implement-drupal-code-standards), we talked about setting up your editor to help you out. You can set it to use 2 spaces for indentation.

## Whitespace

No trailing whitespace! There should never be a space at the end of a line. In [How to Implement Code Standards](https://drupalize.me/tutorial/how-implement-drupal-code-standards), we talked about how you can set up your text editor to remove this for you automatically. Try to avoid extra blank lines throughout your files and functions. Use blank lines sparingly to keep crowded code readable, if necessary.

## File endings

Use the Unix file ending, which is a single blank line at the end of each file. This is another thing most text editors can do for you! Just one line, no more, no less.

## Line length

Lines should be 80 characters long. However, keep in mind that this is primarily for readability. If forcing your code to be broken up over multiple lines makes it *less* readable, then you should reconsider. This is especially true for conditions, which should never be wrapped onto multiple lines. Comment and documentation text, however, should always be 80 characters or under. [Make sure that you have a ruler set up in your editor](https://drupalize.me/tutorial/how-implement-drupal-code-standards) to show you where you’re going over, and you’ll never have to guess.

If you have an array declaration that’s longer than 80 characters, split it into a multi-line array, like so:

```
  $items['advanced_forum_l'] = [
    'variables' => [
      'text' => NULL,
      'path' => NULL,
      'options' => [],
      'button_class' => NULL,
    ],
  ];
```

Here we see each item is on its own line, and each item is followed by a comma, even the last item. This is a Drupal best practice regarding arrays in PHP (other languages, such as JavaScript, may differ).

While we’re on the subject of arrays, if you have a super long array (hundreds of items, for example), you could break each item into its own line. That would be very long, but very readable. However, if the programmer who looks at this code next is unlikely to need this information at their fingertips (for example, a list of countries or zip codes that the programmer will not need to reference), consider [importing it from a CSV file](https://www.php.net/manual/en/function.str-getcsv.php) or similar, and keeping it out of your code.

## Operators

There should always be one space around operators (`=`, `-`, `+`, `*`, `=>`, `.`, etc). Whether you’re doing math, assignments, or concatenating strings - when in doubt, every piece of an expression probably needs to be separated by one space. Just one! You do not need spaces just inside of parentheses.

Here’s an example without spaces, to show how hard it is to read:

```
  if ($a='system'||$b=='system') {
    return $a=='system'?-1:1;
  }
```

And properly formatted:

```
  if ($a == 'system' || $b == 'system') {
    return $a == 'system' ? -1 : 1;
  }
```

## Function calls and declarations

When declaring a function, there should always be a single space after the argument list and before the opening curly brace. The function then begins on the next line, indented with 2 spaces. The closing brace goes on its own line.

A function call always has a set of parentheses, with no spaces on either side of them, whether or not there are parameters. If there are parameters, they should be separated by a comma, followed by a space. This update hook from the [Advanced Forum contributed module](https://www.drupal.org/project/advanced_forum) is a simple example of both a function declaration and function call:

```
function advanced_forum_update_7200() {
  if (variable_get('advanced_forum_forum_disabled') == NULL) {
    variable_set('advanced_forum_forum_disabled', FALSE);
  }
```

## Constants

Take a look at the code above. Notice the all capitals? `TRUE`, `FALSE`, and `NULL` are always capitalized in Drupal code. They are constants, which are always in all capitals in Drupal.

Custom constants must be prefixed with the module name. Here’s an example from the CKEditor module:

```
define('CKEDITOR_FORCE_SIMPLE_TOOLBAR_NAME', 'DrupalBasic');
define('CKEDITOR_ENTERMODE_P', 1);
define('CKEDITOR_ENTERMODE_BR', 2);
define('CKEDITOR_ENTERMODE_DIV', 3);
```

## Control structures

When using control structures like `if`, `else`, `elseif`, `case`, `switch`, `foreach`, `while`, `do`, etc., there should always be a space after the control structure term. Also, there should always be a space before the opening curly brace. The statement is indented on the next line, and the closing brace is on its own line, much like functions.

Inline control structures are not permitted in Drupal, although they are valid PHP. You should NOT use either of the following structures in Drupal:

```
if($foo) echo bar();
```

Or

```
if($foo)
  echo bar();
```

Control structures must always have braces, and the statement(s) must always be on the next line:

```
if ($foo) {
  echo bar();
}
```

Here’s an example using `if` and `foreach` from the [Advagg contributed module](https://www.drupal.org/project/advagg):

```
// Loop through all files.
 foreach ($files as $values) {
   // Insert files into the advagg_files table if it doesn't exist.
   // Update if needed.
   if (advagg_insert_update_files($values['files'], $type)) {
     $write_done = TRUE;
   }

   // Insert aggregate into the advagg_aggregates table if it doesn't exist.
   if (advagg_insert_aggregate($values['files'], $values['aggregate_filenames_hash'])) {
     $write_done = TRUE;
   }

   // Insert aggregate version information into advagg_aggregates_versions.
   if (advagg_insert_aggregate_version($values['aggregate_filenames_hash'], $values['aggregate_contents_hash'], $root)) {
     $write_done = TRUE;
   }
 }
 return $write_done;
```

Here’s another example with statements using `if`, `elseif`, and `else`. Note that in Drupal, the standard is to use `elseif` as one word, *not* `else if`. Both are valid PHP, but the Drupal standards specify it as one word.

```
if ($type === 'css') {
  list($contents) = advagg_get_css_aggregate_contents($file_aggregate, $aggregate_settings);
}
elseif ($type === 'js') {
  list($contents) = advagg_get_js_aggregate_contents($file_aggregate, $aggregate_settings);
}

if (!empty($contents)) {
  $compressed = gzencode($contents, 9, FORCE_GZIP);
  $files[$type][$filename] = strlen($compressed);
}
else {
 $files[$type][$filename] = 0;
}
```

Here’s an example from the [Advanced Forum contributed module](https://www.drupal.org/project/advanced_forum) showing how to format a `switch` statement. Every case-breaking statement must be followed by a blank line. A case-breaking statement is the last statement that is executed, generally a break or return. If you take a look at the last line of the following example, you’ll see that a closing brace counts as a blank line. This is also a good example of spacing between operators.

```
switch ($period) {
  case 'day':
    $period_arg = 60 * 60 * 24;
    break;

  case 'week':
    $period_arg = 60 * 60 * 24 * 7;
    break;

  case 'month':
    $period_arg = 60 * 60 * 24 * 30;
    break;

  case 'quarter':
    $period_arg = 60 * 60 * 24 * 91;
      break;

  case 'year':
    $period_arg = 60 * 60 * 24 * 365;
      break;
}
```

## Alternate control statement syntax for theme templates

For ease of coding and readability, there is an alternate structure to use for control structures inside theme templates in Drupal 7. Use `if ():` and `endif;` instead of braces. Statements must still be on their own line, as must the `endif` statement. Here’s an example from [the Zen subtheme](https://www.drupal.org/project/zen):

```
<?php if ($comments && $node->type != 'forum'): ?>
    <h2 class="comments__title title"><?php print t('Comments'); ?></h2>
<?php endif; ?>
```

## Twig

In Drupal, we use the Twig template engine. The [Drupal Twig standards](https://www.drupal.org/node/1823416) are based on the [Twig coding standards](https://twig.symfony.com/doc/3.x/coding_standards.html), and you can learn more about them in the [Twig Code Standards tutorial](https://drupalize.me/tutorial/drupal-code-standards-twig).

## Casting

For casting, always put a space between the type and the variable, like in this snippet from the [Big Menu contributed module](https://www.drupal.org/project/bigmenu):

```
$p_depth = 'p' . (string) ((int) $depth + 3);
```

Note that there is a space after `(string)` and after `(int)`.

## Semicolons

Every PHP statement ends with a semicolon. Always!

## PHP tags

All PHP files begin with an opening tag, `<?php`, but never, ever use a closing tag. There are many reasons for this, one of which is that whitespace after a closing tag can cause errors, so allowing PHP to close it on its own eliminates those errors.

Also, never use PHP short tags (`<?` `?>`).

## Recap

This is an overview of the major things that Drupal may do differently than other PHP frameworks or content management systems. If you want to dig into Drupal and PHP syntax, there’s a long rabbit hole waiting for you, but these basics will keep you from making major mistakes, and keep your code readable. You’ll also run into fewer hiccups when contributing to core code or modules on Drupal.org. Many of these examples were from Drupal 7. To find out more about Drupal and object-oriented programming, read the [Object-Oriented Code Standards tutorial](https://drupalize.me/tutorial/drupal-code-standards-object-oriented-programming).

## Further your understanding

- Do you currently use coding standards for formatting of your code? What are they?
- This is just an overview of the major points of Drupal's PHP coding standards. We recommend you review [the complete standards](https://www.drupal.org/docs/develop/standards/coding-standards) at least once, and then use it as a source for looking things up when you can't remember

## Additional resources

- [Coding Standards](https://www.drupal.org/docs/develop/standards/coding-standards) (Drupal.org) - Drupal's official PHP coding standards.
- [How to Implement Drupal Code Standards](https://drupalize.me/tutorial/how-implement-drupal-code-standards)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Drupal Code Standards?](/tutorial/what-are-drupal-code-standards?p=2458)

Next
[Drupal Code Standards: Documentation](/tutorial/drupal-code-standards-documentation?p=2458)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

Drupal Training Resources by Alanna Burke of [Chromatic](https://chromatichq.com) are licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://chromatichq.com/blog>.

Clear History

Ask Drupalize.Me AI

close
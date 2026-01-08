---
title: "Output Plain Text and Simple HTML Markup"
url: "https://drupalize.me/tutorial/output-plain-text-and-simple-html-markup?p=3252"
guide: "[[output-and-format-data-code]]"
---

# Output Plain Text and Simple HTML Markup

## Content

Strings of simple HTML and plain text can be defined in a render array using the `#markup` and `#plain_text` element types. In this tutorial we'll look at:

- Adding simple strings to a render array so they appear as HTML on the page
- When to use `#markup` and `#plain_text` in your code

By the end of this tutorial, you should be able to add simple strings of HTML and plain text to a render array.

## Goal

Use the `#plain_text` and `#markup` render element types to display strings of plain text and simple HTML respectively.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)

## Output plain text

Strings of plain text can be described using `#plain_text`. This specifies that the array provides text that needs to be escaped. This value takes precedence over `#markup` when present.

Example `#plain_text` element:

```
$build['simple_text'] = [
  '#plain_text' => '<em>This is escaped</em>',
];
```

This would result in the markup: `&lt;em&gt;This is escaped&lt;/em&gt;` after rendering.

### Output simple HTML

Using the `#markup` property, you can provide HTML markup directly. Unless the markup is very simple, such as an explanation in a paragraph tag, it is preferable to use `#theme` or `#type` instead, so that the markup can be customized by the theme layer.

Example `#markup` element:

```
// Example #markup element, the quickest way to output a string of simple
// HTML.
$build['simple_markup'] = [
  '#markup' => '<p>' . $this->t('Hello world.') . '</p>',
];
```

This would result in the markup: `<p>Hello world.</p>` after rendering.

When using `#markup` the HTML string is run through `Drupal\Component\Utility\Xss::filterAdmin()` in order to strip known XSS vectors. For example, `<script>` and `<style>` are not allowed. See `Drupal\Component\Utility\Xss::$adminTags` for the list of allowed tags. If your markup needs any tags not in this whitelist, you can use the `#allowed_tags` property to alter which tags are filtered.

```
$build['extra_tags'] = [
  '#markup' => '<marquee>' . $this->t('Hello world.') . '</marquee>',
  // An array of tags to allow in addition to those already in the list
  // of allowed tags. Drupal\Component\Utility\Xss::$adminTags
  '#allowed_tags' => ['marquee'],
];
```

This would result in the markup: `<marquee>Hello world.</marquee>` after rendering.

Example using additional common properties:

```
$build['simple_extras'] = [
  // Note the addition of '#type' => 'markup' in this example compared to
  // the one above. Because #markup is such a commonly used element type, you
  // can exclude the '#type' => 'markup' line and it will be assumed
  // automatically if the '#markup' property is present.
  '#type' => 'markup',
  '#markup' => '<p>' . $this->t('This one adds a prefix and suffix, wrapping the item in a blockquote tag.') . '</p>',
  '#prefix' => '<blockquote>',
  '#suffix' => '</blockquote>',
];
```

This would result in the markup: `<blockquote><p>This one adds a prefix and suffix, wrapping the item in a blockquote tag.</p></blockquote>` after rendering.

## Recap

In this tutorial, we looked at using `#markup` elements to output simple HTML strings, and `#plain_text` for strings of plain, escaped, text within a render array. As a module developer you'll use these when you need to display things like short descriptions, help text, or other content that is unlikely to require the ability for the theme layer to manipulate it via templates.

## Further your understanding

- Find some examples of `#markup` and `#plain_text` being used in Drupal core. What content is the code displaying?
- Remember, all elements in a render array can use any of the common `RenderElementBase` properties. [View the list](https://drupalize.me/tutorial/what-are-render-arrays).

## Additional resources

- [Render API overview](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/theme_render/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Use #prefix and #suffix Properties to Wrap an Element](/tutorial/use-prefix-and-suffix-properties-wrap-element?p=3252)

Clear History

Ask Drupalize.Me AI

close
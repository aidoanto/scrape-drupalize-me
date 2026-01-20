---
title: "Use #prefix and #suffix Properties to Wrap an Element"
url: "https://drupalize.me/tutorial/use-prefix-and-suffix-properties-wrap-element?p=3252"
guide: "[[output-and-format-data-code]]"
order: 9
---

# Use #prefix and #suffix Properties to Wrap an Element

## Content

`#prefix` and `#suffix` are two commonly used examples of standard properties. That is, they are available for use on any element in a render array regardless of the element `#type` or `#theme` property's value. They are a great way to add additional layout markup to an element in a theme-agnostic way.

In this tutorial we'll:

- Use the `#prefix` and `#suffix` Render API properties to wrap an element
- Look at some possible use cases for using `#prefix` and `#suffix` in your own code

By the end of this tutorial you should know how, and when, to use the `#prefix` and `#suffix` properties in a render array.

## Goal

Use the `#prefix` and `#suffix` properties common to all Render API elements to wrap the content of an element with an extra HTML tag.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)

## Tacking on extras with `#prefix` and `#suffix`

Wrapping existing content with additional markup is a common task for module and theme developers. You might, for example, want to add an additional structural `<div>` around one or more elements on the page. The best way to do this with render arrays is using the `#prefix` and `#suffix` properties.

Example:

```
$build['simple_extras'] = [
  '#markup' => '<p>' . $this->t('This one adds a prefix and suffix, which put a blockquote tag around the item.') . '</p>',
  '#prefix' => '<blockquote>',
  '#suffix' => '</blockquote>',
];
```

Example output:

```
<blockquote><p>This one adds a prefix and suffix, which put a blockquote tag around the item</p></blockquote>
```

One benefit of using `#prefix` and `#suffix` here is that you're keeping the presentation logic separate from the content. The `#markup` property can contain only the semantic HTML that's required to give the content proper meaning. And the `#prefix` and `#suffix` properties can easily be changed, removed, or added to, without changing the meaning of the content.

These properties can also be used independently. For example, you might be writing a module that places additional tooltips on the page for each form element. In order to do so you should add a `<div class="tooltips"></div>` element just after each form element. You could use `'#suffix'` for this.

It is worth noting that `#prefix` and `#suffix` wrap the entire HTML element rendered by the array. That is, the renderer will first calculate the HTML of the element, and then wrap the whole element. They are independent of the method used to create the main HTML. So for example, an element that uses `'#theme' => 'item_list'` will be rendered to HTML via an *item-list.twig.html* template. That template might be the one in core, or it might be an [override in the current theme](https://drupalize.me/tutorial/override-template-file). In either case, it doesn't require the theme developer to know about the markup in order to use `#prefix` and `#suffix` tags. Therefore, module developers can rely on it working regardless of what theme is being used.

## Recap

In this tutorial we showed that `#prefix` and `#suffix` are commonly used standard render array properties that can add additional structural markup to elements in a theme- and content-agnostic way.

## Further your understanding

- Can you find some examples of `#prefix` and `#suffix` being used in Drupal core? What markup do they contain? Why do you think the developer chose to add the markup in this way?
- Read about other standard render array properties in our [Render Arrays](https://drupalize.me/tutorial/what-are-render-arrays) tutorial.

## Additional resources

- [Render API overview](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/theme_render/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Output Plain Text and Simple HTML Markup](/tutorial/output-plain-text-and-simple-html-markup?p=3252)

Next
[Use Render Element Types in a Render Array](/tutorial/use-render-element-types-render-array?p=3252)

Clear History

Ask Drupalize.Me AI

close
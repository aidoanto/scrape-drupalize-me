---
title: "Output a List of Items"
url: "https://drupalize.me/tutorial/output-list-items?p=3252"
guide: "[[output-and-format-data-code]]"
---

# Output a List of Items

## Content

Drupal makes it easy to convert an array of strings to an ordered or unordered HTML list using `'#theme' => 'item_list'` elements in a render array. This is commonly done by module developers to display a list such as links to content, the values of settings in a module, or the names of everyone who has viewed a page. Displaying lists is a super common task for a content management system.

In this tutorial we'll look at:

- Outputting an array of items as an unordered `<ul>` list
- Properties specific to `'#theme' => 'item_list'` in a render array

By the end of this tutorial you should be able to output unordered lists.

## Goal

Use a `'#theme' => 'item_list'` render array element to define an unordered list.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)

## Output an HTML list

The best way to define either an unordered (`<ul>`) or ordered (`<ol>`) list in a render array is to use the `'#theme' => 'item_list'` element type.

Markup is rendered via an [*item-list.html.twig* template](https://api.drupal.org/api/drupal/core%21modules%21system%21templates%21item-list.html.twig/11.x).

## Element-specific properties

In addition to the following properties specific to `#item_list` elements you can also use any of [the common properties available for all render arrays](https://drupalize.me/tutorial/what-are-render-arrays).

**#items**: An array of items to be displayed in the list. Each item can be either a string or a render array. If `#type`, `#theme`, or `#markup` properties are not specified for child render arrays, they will be inherited from the parent list, allowing callers to specify larger nested lists without having to explicitly specify and repeat the render properties for all nested child lists.

**#title**: The title of the list.

**#list\_type**: The tag for list element, either "ul" or "ol".

**#wrapper\_attributes**: HTML attributes to be applied to the list wrapper. Note that not all themes implement a wrapper. Compare the *item-list.html.twig* files in [Olivero](https://api.drupal.org/api/drupal/core%21themes%21olivero%21templates%21dataset%21item-list.html.twig/11.x) and [Claro](https://api.drupal.org/api/drupal/core%21themes%21claro%21templates%21classy%21dataset%21item-list.html.twig/11.x).

**#empty**: A message to display when there are no items. Allowed value is a string or render array.

Simple example:

```
$build['list'] = [
  '#theme' => 'item_list',
  '#items' => [
    $this->t('This is some text that should be put in a list'),
    $this->t('This is some more text that we need in the list'),
  ],
];
```

More complex example:

```
$items = array();
// A simple string item.
$items[] = 'Simple string';

// A simple string item as render array.
$items[] = [
  '#markup' => 'Simple <span>#markup</span> string',
];

// Set custom attributes for a list item.
$items[] = [
  '#markup' => 'Custom item',
  '#wrapper_attributes' => array(
    'class' => array('custom-item-class'),
  ),
];

// An item with a nested list.
$items[] = [
  '#markup' => 'Parent item',
  'children' => [
    'Simple string child',
    [
      '#markup' => 'Second child item with custom attributes',
      '#wrapper_attributes' => [
        'class' => array('custom-child-item-class'),
      ],
    ],
  ],
];

$build['theme_element'] = [
  '#theme' => 'item_list',
  '#title' => $this->t('Example of using #theme item_list'),
  '#items' => $items,
];
```

Output:

```
<h3>Example of using #theme</h3>
<ul>
  <li>Simple string</li>
  <li>Simple <span>#markup</span> string</li>
  <li class="custom-item-class">Custom item</li>
  <li>Parent item
    <ul>
      <li>Simple string child</li>
      <li class="custom-child-item-class">Second child item with custom attributes</li>
    </ul>
  </li>
</ul>
```

## Recap

In this tutorial we looked at how you can use `'#theme' => 'item_list'` in a render array to define ordered and unordered lists.

## Further your understanding

- Can you find an example of a render array that uses '`#theme' => 'item_list'` in Drupal core?
- Did you know you can use [theme hook suggestions](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions) in a render array?

## Additional resources

- [`template_preprocess_item_list()`](https://api.drupal.org/api/drupal/core%21includes%21theme.inc/function/template_preprocess_item_list/) (Drupal.org)
- Change record: [theme\_item\_list()'s $items variable are either strings or render arrays now](https://www.drupal.org/node/1842756) - compares Drupal 7 and 8 `item_list` implementations (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Render Element Types in a Render Array](/tutorial/use-render-element-types-render-array?p=3252)

Next
[Output a Table](/tutorial/output-table?p=3252)

Clear History

Ask Drupalize.Me AI

close
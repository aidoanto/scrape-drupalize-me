---
title: "Output Content with a Template File"
url: "https://drupalize.me/tutorial/output-content-template-file?p=3252"
guide: "[[output-and-format-data-code]]"
order: 13
---

# Output Content with a Template File

## Content

In this tutorial we'll look at how you can use the `#theme` property of a [render array](https://drupalize.me/tutorial/what-are-render-arrays) to define custom HTML. With this information, module developers can use render arrays to define content, and theme developers can understand how elements in a render array are converted to HTML and which templates they can override to change the output for a specific element.

Learn how to:

- Use `hook_theme()` to define a new theme hook and define default values for variables
- Create a corresponding Twig template file that outputs the variables and any custom HTML markup
- Use a preprocess function to add additional variables for the Twig template file you created
- Use the new theme hook in conjunction with a `#theme` property in a render array to link your Twig template file to actual content

By the end of this tutorial you should know how to define new templates to output content as HTML. You should also have a better understanding of how Twig template files are linked to elements in a render array.

## Goal

Use the `#theme` property of a render array to output content using a Twig template.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)
- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)

Sprout Video

## Output content with a template file

When using the `#theme` property of a render array element you can either use an existing theme hook implemented by another module, or you can define a new one. In this tutorial we walk through the process of defining a new theme hook and related template file, and using it with `#theme`. Understanding how this relationship works should also help you understand how to make use of any existing theme hook from your own code.

## Define a new theme hook and use it with a render array

### Implement hook\_theme()

Tell Drupal that you've got a new template file that you would like to use by [implementing hook\_theme()](https://drupalize.me/tutorial/implement-any-hook) in your module or theme. This returns an array of theme hooks. In the case of template files, the key will be treated as the [base name for the theme hook](https://drupalize.me/tutorial/determine-base-name-template). This should contain information about the theme hook and its implementation.

When defining a value for use with `#theme` the 'variables' key of the sub-array is required. This key is itself an array of variables, where the array keys are the names of the variables, and the array values are the default values if they are not given in the render array. Template implementations receive each array key as a variable in the template file.

Here's an extract of the `hook_theme()` implementation from *render\_example.module*:

```
/**
 * Implements hook_theme().
 */
function render_example_theme() {
  return [
    'render_example_marquee' => [
      'variables' => [
        'content' => '',
        'attributes' => array(),
      ],
    ],
  ];
}
```

The absence of a `template` key in the array describing the `render_example_marquee` theme hook means that a default template name will be assumed based on the theme hook -- in this case, *render-example-marquee.html.twig*.

[Documentation for hook\_theme()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme).

#### Deprecating templates

As of Drupal 10.2, you can mark entire Twig templates as deprecated using a `deprecated` key in your `hook_theme()` implementation. This informs site builders and developers that a specific theme hook or template should no longer be used and provides guidance about replacements.

Example:

```
/**
 * Implements hook_theme().
 */
function mymodule_theme() {
  return [
    'mymodule_old_template' => [
      'variables' => [
        'content' => '',
      ],
      'deprecated' => 'The "mymodule_old_template" template is deprecated in drupal:10.2.0 and is removed from drupal:11.0.0. Use "mymodule_new_template" instead. See https://www.drupal.org/node/12345',
    ],
  ];
}
```

When a deprecated template is used, developers will see a deprecation warning, helping them update their code before the template is removed.

### Create a new template file

Add the new template file to your module in the default location of *MODULENAME/templates/render-example-marquee.html.twig*, or use the `path` option of `hook_theme()` to change the location. The variables available for use in the template file match those defined in the `variables` key in the previous step, plus any added via a preprocess function in the next step.

Example from *render-example-marquee.html.twig*:

```
{#
/**
 * @file
 * Default theme implementation for the marquee render element.
 *
 * Available variables:
 * - attributes: Attributes for the marquee tag.
 * - content: The text to display within the marquee tag.
 *
 * @ingroup themeable
 * @ingroup render_example
 */
#}
<marquee{{ attributes }}>{{ content }}</marquee>
```

It is considered best practice to provide a documentation block in your template file that outlines the available variables so that a themer can understand what is available in the template file without having to read the underlying PHP code.

### Implement a preprocess function

Every template file can have one or more corresponding preprocess functions that define variables for the template. These can exist in either a module or a theme. When adding a new template file to your custom module you can implement a special `template_preprocess_HOOK()` function that is guaranteed to be executed first, allowing you to add variables that other preprocess functions executed later on can access. For example, the node module uses a `template_preprocess_node()` function to provide a base set of variables for the node template file. All subsequent `HOOK_preprocess_node()` functions then have access to those variables and can use it when computing their own new variables.

`HOOK`, in this instance, is the theme hook from above, resulting in a function named `template_preprocess_render_example_marquee()`.

Example:

```
function template_preprocess_render_example_marquee(&$variables) {
  // The $variables array contains the same keys as in the hook_theme() implementation
  // by default. Any new values added will be new variables available in the
  // template file.
  $variables['direction'] = $variables['attributes']['direction'];
  // Convert attributes to a proper \Drupal\Core\Template\Attribute object.
  $variables['attributes'] = new Attribute($variables['attributes']);
}
```

For more on preprocess functions and naming conventions, see [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)

For an example, check out `template_preprocess_node()` in *node.module*, and the variables that it adds for *node.html.twig* templates.

### Use `#theme` in a render array

The final step is to make use of the new theme hook in a renderable array. You can do so by setting the value of the `#theme` property to the name of the theme hook defined in `hook_theme()`. The values of the additional variables defined in `hook_theme()` can also be set by render array properties. Simply add a `#` to the variable name.

Example:

```
$build['marquee'] = [
  '#theme' => 'render_example_marquee',
  '#content' => $this->t('Hello world!'),
  '#attributes' => [
    'class' => ['my-marquee-element'],
    'direction' => 'right',
  ],
];
```

## Recap

In this tutorial we looked at how the `#theme` property of a render array is used in conjunction with Twig template files to output content. We walked through the process of creating a new theme hook with `hook_theme()`, defining a corresponding template file and optional preprocess function, and finally using the new theme hook in a render array to display some content as HTML.

## Further your understanding

- Explore the existing `hook_theme()` implementations in Drupal core to see examples of how to define your own theme hooks for render arrays, as well as to get an idea of what values already exist that you can use with the `#theme` property of a render array.

## Additional resources

- Render Example module from the [Examples for Developers project](https://www.drupal.org/project/examples) (Drupal.org)
- [Output HTML lists with `'#theme' => 'item_list'`](https://drupalize.me/tutorial/output-list-items) (Drupalize.Me)
- [hook\_theme() documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Output a Table](/tutorial/output-table?p=3252)

Next
[Add Classes and HTML Attributes to Render Arrays](/tutorial/add-classes-and-html-attributes-render-arrays?p=3252)

Clear History

Ask Drupalize.Me AI

close
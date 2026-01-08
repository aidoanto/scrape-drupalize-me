---
title: "What Are Preprocess Functions?"
url: "https://drupalize.me/tutorial/what-are-preprocess-functions?p=2851"
guide: "[[frontend-theming]]"
---

# What Are Preprocess Functions?

## Content

Preprocess functions allow Drupal themes to manipulate the variables that are used in Twig template files by using PHP functions to *preprocess* data before it is exposed to each template. All of the dynamic content available to theme developers within a Twig template file is exposed through a preprocess function. Understanding how preprocess functions work, and the role they play, is important for both module developers and theme developers.

In this tutorial we'll learn:

- What preprocess functions are and how they work
- The use case for preprocess functions
- The order of execution for preprocess functions

By the end of this tutorial you should be able to explain what preprocess functions are and the role they play in a Drupal theme.

## Goal

Understand what a preprocess function is in Drupal and the purpose of the various preprocess hooks available.

## Prerequisites

- [Add Logic with THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme)

## Watch: What Are Preprocess Functions?

Sprout Video

## Overview: Preprocess functions in Drupal

Preprocess functions can be used to perform additional conditional logic and data processing of the variables present in a Twig template file. Preprocess functions are optional, and are defined in a theme's *[THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme)* file.

Preprocess functions are called once for each time a template is used. So if the page in question displays four nodes in a list, the *node.html.twig* file is used four times (once for each) and the corresponding preprocess function(s) are called four times.

Preprocess functions follow a specific naming convention:

`THEMENAME_preprocess_HOOK()`

Where `THEMENAME` is the machine readable name of your theme, and `HOOK` is roughly the name of the template file for which you want to preprocess data. Valid values for `HOOK` include the base hook for a template, and any theme hook suggestions. [Learn more about theme hook suggestions for template files](https://drupalize.me/tutorial/what-are-template-files).

For example, given a node of type `article` with the ID 42, the node template would have a base name of *node* and theme hook suggestions like *node\_\_42*, *node\_\_article*, etc. (Note: in the administrative UI, node types are referred to as *content types*). If you want to preprocess variables for the template *themes/icecream/templates/node--article.html.twig* you have several options: `THEMENAME_preprocess_node__42()`, `THEMENAME_preprocess_node__article()`, and `THEMENAME_preprocess_node()`.

1. `THEMENAME_preprocess_node__42()`: This is the most specific version and will only be called for a node with an ID of 42.
2. `THEMENAME_preprocess_node__article()`: This would be called for any article node, but not for other node types.
3. `THEMENAME_preprocess_node()`: This will be called for all nodes.

Only the most specific preprocess function and the one corresponding to the base hook will be called. So, in this example, if you implemented all three of the above functions:

- The 1st and 3rd would be called for the node with ID 42
- The 2nd, and 3rd would be called for all article nodes
- The 3rd would be called for all non-article nodes.

Each preprocess function receives a single argument, usually named `$variables`, that is an associative array. The array is [passed by reference](http://php.net/manual/en/language.references.pass.php) so that you can manipulate the data it contains. The keys of this array directly correspond with the names of the variables in the preprocess function's corresponding template file.

For example, your *THEMENAME.theme* file might include a preprocess function like the following which acts on variables for the *node.html.twig* template file:

```
function icecream_preprocess_node(&$variables) {
  // The array key 'title' maps to the variable {{ title }} in the node.html.twig
  // template file.
  $variables['title'] = array(
    '#markup' => \Drupal::t('My Custom Title'),
  );

  // Example of how nested arrays or object properties relate.
  // This variable in the preprocess function would be {{ node.title }} in the Twig
  // template file.
  $variables['node']->title = \Drupal::t('My Custom Title');
}
```

In addition to the template-specific preprocess functions, there is also a single `THEMENAME_preprocess()` function that is called for every template file. This function receives a second argument which is the *hook* or template name. This can be used for scenarios where you want to perform data processing for every single template file. Warning: this function is called frequently, possibly hundreds of times for a single page, so you should limit the complexity of processing done in this function whenever possible.

Modules can also implement preprocess functions, and frequently do so in order to define the default set of variables available in a template file. The complete list of preprocess functions called for a template file is below, listed in the order they are called (if they exist):

- `template_preprocess(&$variables, $hook)`: Creates a default set of variables for all theme hooks with template implementations. Provided by Drupal Core.
- `template_preprocess_HOOK(&$variables)`: Should be implemented by the module that registers the theme hook, to set up default variables.
- `MODULE_preprocess(&$variables, $hook)`: `hook_preprocess()` is invoked on all implementing modules.
- `MODULE_preprocess_HOOK(&$variables)`: `hook_preprocess_HOOK()` is invoked on all implementing modules, so that modules that didn't define the theme hook can alter the variables.
- `ENGINE_engine_preprocess(&$variables, $hook)`: Allows the theme engine to set necessary variables for all theme hooks with template implementations.
- `ENGINE_engine_preprocess_HOOK(&$variables)`: Allows the theme engine to set necessary variables for the particular theme hook.
- `THEME_preprocess(&$variables, $hook)`: Allows the theme to set necessary variables for all theme hooks with template implementations.
- `THEME_preprocess_HOOK(&$variables)`: Allows the theme to set necessary variables specific to the particular theme hook.

Taken from the Drupal [theme system overview](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/themeable/) documentation.

## Tips and tricks

When adding new elements to the `$variables` array that represent content which should be displayed as HTML it's best practice to define a [render array](https://drupalize.me/tutorial/render-api-overview) instead of hard-coding the markup. This follows the pattern of delaying rendering of data to HTML for as long as possible because arrays are easier to manipulate than HTML strings.

Example:

```
// Good: Use the #table render element type.
$variables['my_new_content'] = ['#type' => 'table', ...];

// Bad: Hard-coding the HTML for a table.
$variables['my_new_content'] = '<table><tr> ... </table>';

// Good: Use a #markup element for HTML
$variables['my_new_content'] = ['#markup' => '<p>Hello there</p>'];

// Bad: Returning hard-coded HTML with text.
$variables['my_new_content'] = '<p>Hello there</p>';

// Good: If the value is not intended to be used as HTML you don't need to use a render array.
$variables['is_new_content'] = $content->isNew() ? TRUE : FALSE;
```

Because the `$variables` argument of a preprocess function is always [passed by reference](https://www.php.net/manual/en/language.references.pass.php) you don't use the `return` keyword to return the `$variables` array.

When printing a variable in a template, e.g. `{{ my_new_content }}`, Twig will check to see if it's a render array and convert it to HTML automatically if needed. There is no need to call `theme()` or `drupal_render()` inside a preprocess function. This allows for more customization within the Twig template file, and is more performant because you don't end up rendering an array that is never displayed on the page.

For the same performance reason, it is a good idea to call filters and utility functions from Twig instead of in a preprocess function.

Example:

```
<p>
  {{ 'Go to the <a href="@link">about</a> page.'|t({'@link': url('about')}) }}
</p>
```

## Add a PHP callable as a `THEME_hook_preprocess()` callback

Starting with Drupal 9.4.x, you can add to the theme registry any PHP callable to used as a preprocess callback. (See the change record: [Allow PHP callables to be used as theme HOOK preprocess callbacks](https://www.drupal.org/node/3266641)). A theme or module can add preprocess callbacks by implementing `hook_theme_registry_alter()` and adding the theme preprocess callback to the theme registry. Here's an example from the change record:

```
function mymodule_theme_registry_alter(&$theme_registry) {
  if (!empty($theme_registry['node'])) {
     // Object that implements function __invoke().
     $theme_registry['node']['preprocess functions'][] = new Invokable();

     // Array with class instance and method name.
     $preprocess = new ThemePreprocess();
     $theme_registry['node']['preprocess functions'][] = [$preprocess, 'objectMethodName'];
  }
}
```

## Use case for preprocess functions

- [Add new variables](https://drupalize.me/tutorial/add-variables-template-file) to a template file
- [Modify existing variables](https://drupalize.me/tutorial/change-variables-preprocess-functions) before they are sent to a template file
- Changing the list of theme hook suggestions for a template file

## Recap

In this tutorial, we discussed the purpose of preprocess functions, as an opportunity to modify render array data passed to the theme before it is rendered in its final form.

## Further your understanding

- What is the naming convention for preprocess functions? What is a HOOK?
- Explain the relationship between preprocess functions and template files.
- Can you give two example use-cases where you could use preprocess functions in your own theme to help clean up a template file?

## Additional resources

- Learn how to [add variables to a template file](https://drupalize.me/tutorial/add-variables-template-file) using preprocess functions (Drupalize.Me)
- Learn how to [change the existing variables in a template file](https://drupalize.me/tutorial/change-variables-preprocess-functions) using preprocess functions (Drupalize.Me)
- [Define a THEMENAME.theme file](https://drupalize.me/tutorial/add-logic-themenametheme) for your preprocess functions (Drupalize.Me)
- Learn more about Drupal's [Render API](https://drupalize.me/tutorial/render-api-overview) (Drupalize.Me)
- [Twig best practices - preprocess functions and templates](https://www.drupal.org/node/1920746) (Drupal.org)
- [API docs for Drupal's Theme System](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/themeable/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Logic with THEMENAME.theme](/tutorial/add-logic-themenametheme?p=2851)

Next
[Change Variables with Preprocess Functions](/tutorial/change-variables-preprocess-functions?p=2851)

Clear History

Ask Drupalize.Me AI

close
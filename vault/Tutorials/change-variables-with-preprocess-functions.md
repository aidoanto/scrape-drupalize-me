---
title: "Change Variables with Preprocess Functions"
url: "https://drupalize.me/tutorial/change-variables-preprocess-functions?p=2851"
guide: "[[frontend-theming]]"
---

# Change Variables with Preprocess Functions

## Content

Preprocess functions are specially-named PHP functions that allow themes and modules to modify the variables passed to a Twig template file. They are commonly used by themes to alter existing variables before they are passed to the relevant template files. For example; Changing the makeup of render array so that it renders an `<ol>` list instead of a `<ul>` list. Or appending data to the label of a node depending on custom logic.

In this tutorial we'll:

- Define a new preprocess function in our theme's *.theme* file
- Use the preprocess functions to modify the content of an existing variable before it's used in Twig

By the end of this tutorial you should be able to define new preprocess functions in a theme (or module) that manipulate the variables for a specific Twig template file.

## Goal

Modify the `{{ label }}` variable used by the *node.html.twig* template file so that it contains data about the currently logged-in user using a preprocess function.

## Prerequisites

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [Add Logic with THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme)
- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)

## Changing existing variables

Sprout Video

Our goal is to preprocess variables for the *node.html.twig* file, and demonstrate how you could append the text " - you are the author" to the title of any node written by the currently logged-in user. This demonstrates the use of preprocess functions for manipulating existing variables. A similar technique can be used to add new variables. See [Add Variables to a Template File](https://drupalize.me/tutorial/add-variables-template-file)

### Create a .theme file

Start by creating a .theme file if one doesn't already exist. We'll call ours *icecream.theme*, and place it at *themes/icecream/icecream.theme*. If your theme already has a .theme file you can edit the existing file.

### Determine the hook name

Identify the hook, or base name, of the template you are going to add variables to. In our case the template is *node.html.twig*, but it could also be more specific like *node--flavor.html.twig*. In both cases, the base name is *node*. We'll use this information when defining a preprocess function.

Read more about [determining the base name of a template file](https://drupalize.me/tutorial/determine-base-name-template).

### Add a preprocess function

In your *icecream.theme* file, create the following new function if it doesn't already exist:

```
function icecream_preprocess_node(&$variables) {

}
```

This function name follows the pattern THEMENAME\_preprocess\_HOOK(). Learn more about [naming preprocess functions](https://drupalize.me/tutorial/what-are-preprocess-functions).

### Find the variable you want to change

The `$variables` argument passed to this new function is an associative array. Each key in the array represents a variable that will be present in the Twig template file.

For example:

`$variables['label']` in your preprocess function maps to `{{ label }}` in the Twig template.

To make changes to the content of any variable you can simply modify that entry in the `$variables` array within a preprocess function, since the argument is passed by reference. Learn more about [passing arguments by reference](https://www.php.net/manual/en/language.references.pass.php) in PHP.

### Modify the variable

Add some code that compares the currently logged-in user to the author of the node and then modifies the `{{ label }}` variable.

```
/**
 * Preprocess function for node.html.twig.
 */
function icecream_preprocess_node(&$variables) {
  // If the current user is logged in, and they are the owner of the node
  // being viewed, add a suffix to the label variable.
  if ($variables['logged_in'] == TRUE && $variables['node']->getOwnerId() == $variables['user']->id()) {
    $variables['label']['#suffix'] =' [you are the author]';
  }
}
```

The `$variables` array is special kind of array in Drupal called a *render array*, part of Drupal's Render API. A render array contains all the information that the system needs to display or render this data. In this example, a pre-existing variable named `label`, which contains the title of the content being viewed, is being modified to add a *property* called `#suffix`, which as you might guess, appends whatever you specify after the value of the parent array key.

Learn more about render arrays

Drupal's Render API is used by both module and theme developers. Get started with these tutorials:

- [Render API Overview](https://drupalize.me/tutorial/render-api-overview)
- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)

### Clear the cache

If you created the .theme file in this tutorial from scratch, or you added a new preprocess function instead of modifying an existing one, you'll need to clear the cache so that Drupal will locate your new preprocess function and execute its code.

Other examples of things you might do in a preprocess function:

- Make modifications to render arrays being sent to a template to change the way it ends up being rendered
- Perform logic on a set of numbers to calculate a percentage and display the outcome

## A note about Drupal 7

In Drupal 7 it was common to use preprocess functions to dynamically change the classes associated with an element. For example, you might do something like the following in order to add the class ‘node-unpublished’ to the wrapper for all nodes:

```
function icecream_preprocess_node(&$variables) {
  if (!$variables['status']) {
    $variables['classes_array'][] = 'node--unpublished';
  }
}
```

In Drupal, the preferred way to deal with altering/adding class names is via the Twig template file. In this example, you would add the following to the top of your node.html.twig template in order to accomplish the same thing as above:

```
{%
  set classes = [
    not node.isPublished() ? 'node--unpublished',
  ]
%}
```

## Recap

In this tutorial we learned how to modify the variables passed to a Twig template file using a preprocess function. We added a new `hook_preprocess_HOOK()` function to our theme's *.theme* file, and used it to alter the `{{ label }}` variable passed to the *node.html.twig* template file.

## Further your understanding

- Use a preprocess function to modify variables for the *node.html.twig* template. Can you change a [Render API](https://drupalize.me/tutorial/render-api-overview) array so that its content is printed out differently?
- If your theme is a subtheme of another theme, like Classy, does the theme system call both `mytheme_preprocess_node()` and `classy_preprocess_node()`? If so, in what order?
- Define a scenario in your own theme where you could use a preprocess function to change a variable, or set of variables, and simplify the content of a template file as the result.

## Additional resources

- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions) (Drupalize.Me)
- In addition to changing variables you can also [add variables with preprocess functions](https://drupalize.me/tutorial/add-variables-template-file) (Drupalize.Me)
- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files) (Drupalize.Me)
- [Documentation about preprocessing variables](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/themeable/) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Preprocess Functions?](/tutorial/what-are-preprocess-functions?p=2851)

Next
[Add Variables to a Template File](/tutorial/add-variables-template-file?p=2851)

Clear History

Ask Drupalize.Me AI

close
---
title: "Add Variables to a Template File"
url: "https://drupalize.me/tutorial/add-variables-template-file?p=2851"
guide: "[[frontend-theming]]"
---

# Add Variables to a Template File

## Content

Preprocess functions are specially-named functions that can be used to add new variables to a Twig template file. They are commonly used by themes to add new variables based on custom PHP logic and simplify accessing the data contained in complex entity structures. For example: adding a variable to all *node.html.twig* template files that contains the combined content a couple of specific fields under a meaningful name like `{{ call_to_action }}`. Modules use preprocess functions to expose the dynamic data they manage to Twig template files, or to alter data provided by another module based on custom logic.

In this tutorial we'll learn how to:

- Use PHP to perform some complex logic in our theme.
- Store the resulting calculation in a variable.
- Make that variable available to a Twig template file.

Example use cases for adding variables with preprocess functions include:

- Anytime calculating the value to output in a template requires logic more complex than an if/else statement.
- Anytime the desired value requires additional string manipulation beyond what can be easily accomplished using an existing Twig filter or function.

By the end of this tutorial you should be able to expose new variables to a Twig template file by defining a preprocess function in either a module or a theme.

## Goal

Add a new variable to the *node.html.twig* template file that contains a Boolean value indicating if the currently logged-in user is the author of the node being displayed.

## Prerequisites

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [Add Logic with THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme)
- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)

## Adding variables to a template file

Sprout Video

Let's add a new variable named `current_user_is_owner` to all *node.html.twig* templates in the Ice Cream theme. This variable serves as a flag we can use within the template file in order to alter the markup depending on whether or not the node being displayed was created by the user viewing it.

### Create a .theme file

Start by creating a .theme file if one doesn't already exist. We'll call ours *icecream.theme*, and place it at *themes/icecream/icecream.theme*. If there is already a .theme file, you can simply edit the existing file.

### Determine the hook name

Identify the hook, or base name, of the template you are going to add variables to. In our case the template is *node.html.twig*, but it could also be more specific like *node--flavor.html.twig*. In both cases the base name is *node*. We'll use this information when defining a preprocess function.

Read more about [determining the base name of a template file](https://drupalize.me/tutorial/determine-base-name-template).

### Add a preprocess function

In your *icecream.theme* file, create the following new function if it doesn't already exist:

```
function icecream_preprocess_node(&$variables) {

}
```

This function name follows the pattern `THEMENAME_preprocess_HOOK()`. Learn more about [naming preprocess functions](https://drupalize.me/tutorial/what-are-preprocess-functions).

### Add a variable

The `$variables` argument passed to this new function is an associative array. Each key in the array represents a variable that will be present in the Twig template file. Adding new keys to this array will also have the effect of adding new variables to the Twig template file in question. For example:

```
function icecream_preprocess_node(&$variables) {
  // If the current user is logged in, and they are the owner of the node
  // being viewed, add a new variable that can be used to identify this in
  // Twig templates.
  $variables['current_user_is_owner'] = FALSE;
  if ($variables['logged_in'] == TRUE && $variables['node']->getOwnerId() == $variables['user']->id()) {
    $variables['current_user_is_owner'] = TRUE;
  }
}
```

Because the `$variables` array is passed by reference, preprocess functions do not need to return anything. Any changes made to the referenced argument will be automatically reflected upstream. Read more about PHP's [pass by reference](https://www.php.net/manual/en/language.references.pass.php) arguments.

Image

![preprocess add variables](/sites/default/files/styles/max_800w/public/tutorials/images/task-preprocess_add_variables.png?itok=M7gcbuAL)

A note about naming: Because keys added to the `$variables` array are ultimately converted to Twig variables, it's important to use names that will result in a valid Twig variable name. For this reason, when adding variables via a preprocess function make sure you start with an alphabetical character, and replace any spaces with an underscore.

### Use your new variable

Any new variables added in a preproccess function will have a new corresponding Twig variable injected into the template file being preprocessed. In this example, our *node.html.twig* files in the Ice Cream theme will all have an additional `{{ current_user_is_owner }}` variable available.

Any new variables that add content should represent that content as a renderable array whenever possible. This is especially true of modules implementing preprocess functions.

## Recap

In this tutorial we learned how to add new variables to a Twig template file using a preprocess function in the *.theme* file of a theme. This is done by adding new key/value pairs to the `$variables` array passed to all preprocess functions. The content of that array is the values passed to the corresponding template files. The keys of the array become the names of individual variables in the template file. We also learned that modules can use this same technique.

## Further your understanding

Did you know that all the variables added to a template file are done so via preprocess functions? Drupal core, modules, and the theme engine can all implement preprocess functions for a template file. The results of all these preprocess functions are aggregated together, and create the final list of variables passed to a template. See [template\_preprocess\_node()](https://api.drupal.org/api/drupal/core!modules!node!node.module/function/template_preprocess_node/) where the core node module adds variables for *node.html.twig* as an example.

- When should you consider using a preprocess function instead of just handling the logic in your template file?
- Are preprocess functions called once per page request, or once for every time a template is used in a request? Why?
- Take a look at the `template_preprocess()` function in Drupal core. These variables are available in every single template file. Can you find other examples of modules using preprocess functions to add dynamic content to template files?

## Additional resources

- In addition to adding variables you can also [change variables with preprocess functions](https://drupalize.me/tutorial/change-variables-preprocess-functions) (Drupalize.Me)
- [Preprocessing and modifying attributes in a .theme file](https://www.drupal.org/docs/8/theming-drupal-8/modifying-attributes-in-a-theme-file) (Drupal.org)
- [Theme system overview](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/group/themeable/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Change Variables with Preprocess Functions](/tutorial/change-variables-preprocess-functions?p=2851)

Clear History

Ask Drupalize.Me AI

close
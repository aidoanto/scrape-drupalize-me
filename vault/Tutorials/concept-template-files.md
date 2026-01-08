---
title: "Concept: Template Files"
url: "https://drupalize.me/tutorial/concept-template-files?p=3239"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Template Files

## Content

Template files in Drupal modules provide the default HTML markup for the visual presentation of a module's data. Be aware that themes are likely to override the template with site-specific customizations. This template should contain only minimal markup to ensure functionality, and document the variables fed into the template.

In this tutorial, we'll:

- Explain the role of Twig template files in modules.
- Show how modules declare and use template files.
- Recognize how a render array can specify a template.

By the end of this tutorial, you should be able to articulate how and when a module should define a new template file.

## Goal

Understand the rationale and process for a module to offer a template file for rendering its custom data.

## Prerequisites

- [Concept: Themeable Output](https://drupalize.me/tutorial/concept-themeable-output)
- [Concept: Render API](https://drupalize.me/tutorial/concept-render-api)

## Template files in modules

In Drupal, files in a */templates* subdirectory ending with *.html.twig* are recognized as template files. Although often associated with themes, modules also use template files to ensure output is themeable. When a module's output requires structured HTML, like `<div>` wrapping elements or a `<nav>` tag for menus, it should use a template file. This approach offers flexibility and allows themes to customize the markup.

## Declaring template files in modules

Modules declare template files through `hook_theme()` implementations. This function specifies the theme hook, template name, and variables for the template.

Example of declaring a theme hook in a module:

```
function my_module_theme($existing, $type, $theme, $path) {
  return [
    'my_module_template' => [
      // These are the variables that will be passed to the template file.
      'variables' => ['title' => NULL, 'content' => NULL],
      'template' => 'my-module-template',
    ],
  ];
}
```

This code snippet tells Drupal that `my_module_template` is a theme hook linked to a template file named *my-module-template.html.twig*, in the *templates/* subdirectory of the module. It also declares that the variables `title` and `content` will be fed into the template.

## Using template files for rendering

Modules use render arrays to designate the template file for rendering specific data. The `#theme` property in a render array connects the data with its template via the theme hook.

Example of using `#theme` in a render array:

```
$build['example'] = [
  '#theme' => 'my_module_template',
  // These property names match the 'variables' defined in the hook_theme()
  // implementation.
  '#title' => 'Example Title',
  '#content' => 'This is some example content.',
];
```

This render array will be processed with the *my-module-template.html.twig* file, passing `title` and `content` to the template. Since we are using these variables in a render array, we need to prefix the variable names defined here with a `#`.

## Templates are authored using Twig

Twig is the default template engine for Drupal. It uses an easy-to-read syntax to allow mixing HTML with basic logic, and placeholders for dynamic content. Module developers should familiarize themselves with the basic Twig syntax. Learn more in [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal).

## Use preprocess functions for additional logic

Modules and themes can employ preprocess functions to modify variables before passing them to the template, adding dynamic content manipulation and flexibility. Learn more in [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions).

## Template overrides

Themes have the capability to override module-provided template files, allowing customization of the default HTML output. When rendering a node, Drupal looks for template derivatives of *node.html.twig* in the theme, base theme (if applicable), and finally in Drupal core or contributed modules, using the first found instance or defaulting to the base template if no override exists. Learn more in [Override a Template File](https://drupalize.me/tutorial/override-template-file).

## Recap

This tutorial covered the integration of Twig template files within Drupal modules. By implementing `hook_theme()`, modules can define a new theme hook and associate it with a template file. This theme hook is then linked to data in a render array via the `#theme` property, ensuring content is themeable.

## Further your understanding

- Reflect on how template files enhance Drupal's theming flexibility. Why might a module opt to provide a template file for its output?
- What is the role of preprocess functions in theming?

## Additional resources

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files) (Drupalize.Me)
- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal)
- [Override a Template File](https://drupalize.me/tutorial/override-template-file) (Drupalize.Me)
- [What Are Preprocess Functions](https://drupalize.me/tutorial/what-are-preprocess-functions) (Drupalize.Me)
- [Output Content with a Template File](https://drupalize.me/tutorial/output-content-template-file) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Output Content Using Render API](/tutorial/output-content-using-render-api?p=3239)

Next
[Add a Template File](/tutorial/add-template-file?p=3239)

Clear History

Ask Drupalize.Me AI

close
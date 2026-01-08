---
title: "Add Logic with THEMENAME.theme"
url: "https://drupalize.me/tutorial/add-logic-themenametheme?p=2851"
guide: "[[frontend-theming]]"
---

# Add Logic with THEMENAME.theme

## Content

Every theme can contain an optional *THEMENAME.theme* file. This file contains additional business logic written in PHP and is primarily used for manipulation of the variables available for a template file, and suggesting alternative candidate template file names. Themes can also use this file to implement some, but not all, of the hooks invoked by Drupal modules.

In this tutorial we'll learn:

- The use case for *THEMENAME.theme* files, and where to find them
- The different types of functions and hooks you can implement in a *THEMENAME.theme* file

By the end of this tutorial you should be able to know how to start adding PHP logic to your custom theme.

## Goal

Know where to locate your theme's *.theme* file and what you can expect a *.theme* file to contain.

## Prerequisites

- [Structure of a Theme](https://drupalize.me/tutorial/structure-theme)
- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)

## The .theme file

The *THEMENAME.theme* file is a PHP file, with a *.theme* extension. It is used for complex conditional logic and data processing in the theme layer. The use of *THEMENAME* in this case is just a placeholder for the actual machine readable name of your theme, which is derived from the name given to the theme's *.info.yml* file.

The file is not required, and can be safely ignored if it is not needed. Thus, you will find some themes which do not have a *THEMENAME.theme* file. If you encounter a scenario that requires a *THEMENAME.theme* file and the theme you're working on doesn't have one yet, you can create it at any time.

*THEMENAME.theme* files are always located in the root directory of your theme.

Example:

```
themes/icecream/
  - icecream.info.yml
  - icecream.theme
```

Most documentation will refer to this as either a *THEMENAME.theme* file, or just a *.theme* file.

This file is the primary location for any PHP code within a theme. This keeps business logic out of your template files and cleanly separated from the markup. If you ever find yourself starting to write complex logic in a template file, consider whether it can be relocated into a *.theme* file.

If you are upgrading a Drupal 7 theme, then you will put the preprocess hooks and other functions from *template.php* into *THEMENAME.theme*. (Other modifications in your PHP code may be required; see <https://api.drupal.org/> and <https://www.drupal.org/list-changes> for API updates.)

## Use cases for THEMENAME.theme files

What are some use cases for needing a *.theme* file in a Drupal theme?

### Preprocess functions

A *THEMENAME.theme* file can contain preprocess functions. These are specially-named PHP functions that are executed just before rendering a related Twig template file. Preprocess functions are used to alter, and add to, the variables available in a template file. See:

- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)
- [Add Variables to a Template File](https://drupalize.me/tutorial/add-variables-template-file)
- [Change Variables with Preprocess Functions](https://drupalize.me/tutorial/change-variables-preprocess-functions)

### Theme hook suggestions

A *THEMENAME.theme* file can also contain implementations of `hook_theme_suggestions_alter()` and `hook_theme_suggestions_HOOK_alter()`. These allow you to add to, or alter, the list of candidate template file names used when locating the template to use for rendering a specified element.

Learn more about [theme hook suggestions](https://drupalize.me/tutorial/what-are-template-files).

### Implement alter hooks

A theme can implement some, but not all, [Drupal hooks](https://drupalize.me/tutorial/what-are-hooks) via the *.theme* file. It's limited to a specific set of alter hooks which allow theme developers access to UX related business logic. The list of hooks that a theme can implement is:

- `hook_css_alter()`
- `hook_js_alter()`
- `hook_library_info_alter()`
- `hook_form_alter()` and `hook_form_FORM_ID_alter()`
- `hook_plugin_filter_TYPE_alter()` and `hook_plugin_filter_TYPE__CONSUMER_alter()`
- `hook_element_info_alter()`
- `hook_page_attachments_alter()`
- `hook_theme_suggestions()` and `hook_theme_suggestions_HOOK()`
- `hook_theme_suggestions_alter()` and `hook_theme_suggestions_HOOK_alter()`
- `hook_views_ui_display_tab_alter()`
- `hook_views_ui_display_top_alter()`

Hooks in a *.theme* file are invoked via `\Drupal\Core\Theme\ThemeManagerInterface::alter`. The most reliable way to figure out what hooks are available in a theme for your specific codebase is by searching for usages of this method.

## Recap

Every theme may contain one *.theme* file. A *.theme* file is optional, and not a required file in a Drupal theme. This file contains PHP logic for the theme and are composed of preprocess functions which can:

- Add variables to a template file.
- Alter the variables for a template file.
- Modify the list of *theme hook suggestions* based on custom logic.

## Further your understanding

- Where, in the file structure of your theme, does the *.theme* file live?
- Does your theme, or a base theme that you're using, have a *THEMENAME.theme* file? What's in it?
- If you are just starting a new theme, do you think you'll have a use-case for a *.theme* file in your theme? Be specific.

## Additional resources

- [Preprocessing and modifying attributes in a .theme file](https://www.drupal.org/docs/8/theming-drupal-8/modifying-attributes-in-a-theme-file) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[What Are Preprocess Functions?](/tutorial/what-are-preprocess-functions?p=2851)

Clear History

Ask Drupalize.Me AI

close
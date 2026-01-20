---
title: "Attach an Asset Library"
url: "https://drupalize.me/tutorial/attach-asset-library?p=2860"
guide: "[[integrate-javascript-drupal]]"
order: 13
---

# Attach an Asset Library

## Content

Once you've defined an asset library you'll need to tell Drupal when you want to add the CSS and JavaScript that it includes to the page. Ideally you'll do so in a way that allows Drupal to only add the corresponding assets on pages where they are needed.

You can attach a library to all pages, a subset of pages, or to elements in a render array. This allows you to have some assets that are global, and others that get loaded on an as-needed basis. To attach a library you'll need to know both its name and prefix, and then use one of the techniques outlined below to let Drupal know when to include it.

In this tutorial, we'll look at attaching asset libraries:

- Globally, via your *THEMENAME.info.yml* file
- Conditionally, via a preprocess function using the `#attached` render array property
- Inside of a Twig template file

By the end of this tutorial you should be able to attach asset libraries in various different ways depending on your use case.

## Goal

Attach an asset library so that the associated CSS and JavaScript are loaded on specific pages, or as part of specific render elements.

## Prerequisites

- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries)
- We're going to pick up where we left off in [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library) with the Retro library, so you may want to refer to that tutorial before continuing.

**Note:** While the example below covers how to attach a library in a theme, the same steps work for modules. In the case of modules you'll most likely want to use `#attached` as part of a [Render Array](https://drupalize.me/tutorial/what-are-render-arrays).

Skip to:

- [Attach an asset library globally](#attach-an-asset-library-globally)
- [Attach an asset library to a specific page](#attach-an-asset-library-to-a-specific-page)
- [Add an asset library with a preprocess function](#add-an-asset-library-with-a-preprocess-function)
- [Attach an asset library in a Twig template](#attach-an-asset-library-in-a-twig-template)

Here is the finished product of placing our asset library *retro* on the homepage:

Image

![Retro library in action](../assets/images/retro-olivero.gif)

## Watch a video of attaching an asset library

Sprout Video

## Asset library naming conventions

When attaching an asset library, you'll refer to it by the theme name and the library key name: `theme/library`. Since theme names must be unique within your Drupal site system, referring to a library by both the theme name and the library name will ensure its uniqueness.

For example, if the theme `bartik` defined an asset library called `global-styling`, then when attaching the library, you would refer to it as `bartik/global-styling`. This also means that multiple themes in your system could define a library called `global-styling` and remain distinct because of the different theme names, i.e. `bartik/global-styling`, `retro/global-styling`, `myawesometheme/global-styling`.

Image

![Asset library name in THEME.libraries.yml](../assets/images/asset-library-naming.png)

## Attach an asset library globally

**Note:** This approach will only work for a theme. Modules should use `hook_page_attachments_alter()` or similar.

In order to attach a library globally, or to every page on your site, you can specify the library in your *THEMENAME.info.yml* file. Since our site is using a custom theme (called *Retro*), we'll open up */themes/custom/retro/retro.info.yml*

```
name: retro
type: theme
description: An amazing Retro theme
package: Other
core_version_requirement: ^9 || ^10
base theme: olivero

libraries:
  - retro/global-styling
  - retro/rainbow
  - retro/retro
```

Any asset libraries specified here in the *THEMENAME.info.yml* file will be made available on every page. Because of this you'll want to take extra care with this approach. With an asset library that provides something like an analytics tracking code this global approach might be a good idea. Often, however, you don't actually need an asset library on every single page.

## Attach an asset library to a specific page

In most cases it's best to restrict the conditions in which your library is attached to a page. So let's remove our library from *retro.info.yml* and figure out how to add it on only the front page.

One method of conditionally restricting when your library is attached is to use the [hook\_page\_attachments\_alter](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Render!theme.api.php/function/hook_page_attachments_alter/) function in our *retro.theme* file or in a module's *MODULE.module* file.

```
/**
* Implements hook_page_attachments_alter
*/
function retro_page_attachments_alter(array &$page) {
  // Get the current path.
  $path = $current_path = \Drupal::service('path.current')->getPath();
  // If we're on the node listing page, add our retro library.
  if ($path == '/node') {
    $page['#attached']['library'][] = 'retro/retro';
  }
}
```

By implementing `hook_page_attachments_alter()` we're able to add conditional logic that determines whether or not our asset library will be included on the page. In the example here we're only adding the retro library to the node listing page (the default front page).

For more about implementing hooks see [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook).

## Add an asset library with a preprocess function

Another useful way to **conditionally add an asset library** is by using a [preprocess function](https://drupalize.me/tutorial/what-are-preprocess-functions) like `hook_preprocess_page()`. Here's another example of restricting our retro asset library to the front page.

```
/**
* Implements hook_preprocess_page() for PAGE document templates.
*/
function retro_preprocess_page(&$variables) {
  if ($variables['is_front'] == TRUE) {
    $variables['#attached']['library'][] = 'retro/retro';
  }
}
```

This method of attaching an asset library works in preprocess functions, in manipulating form elements, or render arrays.

## Attach an asset library in a Twig template

Asset libraries can also be attached from within a Twig template using the `attach_library` filter. Anytime that template is used the corresponding library will be attached in accordance with any template-specific conditions.

In order to see this in action, we need to create a template in our Retro theme. Since we're using Bartik as our base theme, we can copy the *node.html.twig* from Bartik into our theme directory. After rebuilding the cache, we can see this new template in action. Let's add a bit of code so that our `retro` library is only added to the page if we're viewing a node of the type, `article`.

```
{# Only attach our retro library if this is an 'article' node. #}
{% if node.bundle == 'article' %}
  {{ attach_library('retro/retro') }}
{% endif %}
```

With this code in place, when a user views an `article` node, our Retro theme's `retro` library will get included in the page (`retro/retro`), and the user will see that library's CSS styles and JavaScript behaviors applied to the article content. If a page being viewed does not include any articles, then our `retro/retro` library and its listed dependencies will not be attached to the page.

## Recap

In this tutorial we learned how to determine the full name of an asset library by combining the theme's name and the library name from the *.libraries.yml* file. Then, we looked at 4 different ways that we can tell Drupal when to include an asset library, including:

1. Globally via the *.info.yml* file
2. Per-page via `hook_page_attachments_alter()`
3. To a render element via a preprocess function
4. Via a Twig template file.

## Further your understanding

- What is the benefit of conditionally attaching libraries versus adding them globally?
- Can you use `#attached` to add a library to the search form displayed by the search block?
- Learn about using `#attached` in combination with JavaScript settings in [Use Server-Side Settings with drupalSettings](https://drupalize.me/tutorial/use-server-side-settings-drupalsettings)
- Learn how to [extend or override an existing asset library](https://drupalize.me/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries).

## Additional resources

- [Custom Retro theme](https://drupalize.me/sites/default/files/tutorials/retro-drupal-10.zip) (.zip) (Drupalize.Me)
- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries) (Drupalize.Me)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library) (Drupalize.Me)
- [Extend or Alter Existing CSS and JavaScript Asset Libraries](https://drupalize.me/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define an Asset Library](/tutorial/define-asset-library?p=2860)

Next
[Extend or Alter Existing CSS and JavaScript Asset Libraries](/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries?p=2860)

Clear History

Ask Drupalize.Me AI

close
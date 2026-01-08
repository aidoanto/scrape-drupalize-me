---
title: "Extend or Alter Existing CSS and JavaScript Asset Libraries"
url: "https://drupalize.me/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries?p=2860"
guide: "[[integrate-javascript-drupal]]"
---

# Extend or Alter Existing CSS and JavaScript Asset Libraries

## Content

As a theme developer you can extend an existing asset library to include custom CSS and/or JavaScript from your theme. This is useful when you want to add styles or behaviors to components provided by Drupal core or another module.

Sometimes there are CSS or JavaScript asset libraries attached to the page by Drupal core, a contributed module, or another theme, that do something you don't like, and you want to change it or even exclude it all together. There are a couple of different ways that themes can override, alter, or extend, an existing asset library in order to modify the CSS and JavaScript that get attached the page by other code belonging to another theme or module.

In this tutorial we'll learn how to:

- Extend an existing asset library using `libraries-extend`, so that our custom CSS and JavaScript is included whenever that library is used.
- Override an existing asset library using `libraries-override`, to alter the definition of the library, and replace or exclude individual assets (or the entire library).

By the end of this tutorial you should be able to use your custom theme to override, extend, or alter any of the asset libraries added to the page by another theme or module.

## Goal

Demonstrate how you can add custom CSS and JavaScript assets to existing UI elements like the core dropbutton component.

## Prerequisites

This tutorial assumes you're already familiar with:

- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library)
- [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library)

In Drupal core, there's a `'#type' => 'dropbutton'` [render element type](https://drupalize.me/tutorial/what-are-render-elements). Whenever a dropbutton is displayed on the page the `core/drupal.dropbutton` asset library is also included. That asset library, defined in *core.libraries.yml*, looks like this:

```
drupal.dropbutton:
  version: VERSION
  js:
    misc/dropbutton/dropbutton.js: {}
  css:
    component:
      misc/dropbutton/dropbutton.css: {}
  dependencies:
    - core/jquery
    - core/drupal
    - core/drupalSettings
    - core/once
    - core/jquery.once.bc
```

Let's say our custom theme calls for some changes to the styling of the dropbutton element. Rather than globally including our CSS on every page (to ensure its presence in case a dropbutton is displayed), we can extend--or override--the existing library definition so that whenever the `core/drupal.dropbutton` library is used, our modifications are included.

These changes are all made in your theme's *\*.info.yml* file. **Note**: We're editing the **.info.yml** file *not* the **.libraries.yml** file where asset libraries are defined.

## Extend an existing asset library

Create a CSS file with your styling rules, and [define an asset library](https://drupalize.me/tutorial/define-asset-library) that includes the new CSS (and JavaScript if required). We'll call ours `icecream/dropbutton`.

You can ensure that it is added to the page anytime the `core/drupal.dropbutton` library is used by using the `libraries-extend` key in your theme's *.info.yml* file.

Here's what we'd add to our *icecream.info.yml*:

```
libraries-extend:
  # Name of the library you want to extend.
  core/drupal.dropbutton:
    # A list of one or more libraries you want included each time the parent is
    # used.
    - icecream/dropbutton
```

Using `libraries-extend` to add our custom CSS whenever *{thing}* is on a page, is something we commonly do when creating custom themes. In this case, `libraries-extend` is appropriate and works well. But, we recommend that if *{thing}* is represented by a [template file](https://drupalize.me/tutorial/what-are-template-files) it makes sense to [define your new asset library](https://drupalize.me/tutorial/define-asset-library) and then use Twig's `{{ attach_library('icecream/dropbutton') }}` function to [attach the asset library to the template file](https://drupalize.me/tutorial/attach-asset-library). This also improves the theme developer experience, because anyone can open the template file and readily see which asset library is attached to it.

## Overriding an existing asset library

The next 2 examples are less common in practice but still useful. They demonstrate how you can override and alter the definition of an asset library provided by another module or theme.

### Replace one or more assets from an existing library

In the previous example, we **added** new CSS and JavaScript assets to the ones included by the `core/drupal.dropbutton` library. But what if you want to **replace** one of the files included by the library with your own CSS or JavaScript file? Maybe in order to implement your style changes, you find yourself overriding and resetting CSS rules from the core's *dropbutton.css* file. In this case, it would be easier if core's *dropbutton.css* files wasn't loaded in the first place. You can replace a library's asset with the `libraries-override` key in your theme's *\*.info.yml* file.

Example from *icecream.info.yml*:

```
libraries-override:
  core/drupal.dropbutton:
    css:
      component:
        misc/dropbutton/dropbutton.css: css/my-dropbutton.css
```

Notice the line, `misc/dropbutton/dropbutton.css: css/my-dropbutton.css`. This tells Drupal that instead of including *misc/dropbutton/dropbutton.css* it should discard it and use *css/my-dropbutton.css* from your theme instead.

The `css > component > misc/dropbutton/dropbutton.css` hierarchy needs to match what's defined in the asset library you are overriding. Our recommendation is copy and paste the relevant section of the existing library and then edit it. And, this works for any files defined under the `js:` key as well.

### Exclude a file (instead of replacing it)

If instead, you want to exclude the core library's CSS file, and not replace it, set the value of the filename key to `false`. For example:

```
libraries-override:
  core/drupal.dropbutton:
    css:
      component:
        misc/dropbutton/dropbutton.css: false
```

### Exclude the library

If you want to exclude the entire library, set the value of the asset library key to `false`.

Example from *icecream.info.yml*:

```
libraries-override:
  core/drupal.dropbutton: false
```

## Recap

In this tutorial we learned how themes can extend or alter an existing asset library in order to customize the styling or behavior of a component provided by core or another theme or module. Using `libraries-extend` or `libraries-override` in a theme's info file allows you to create unique CSS styles, make modifications, or exclude assets whenever the associated asset library is loaded.

Remember that the code for doing so goes in your theme's *\*.info.yml* file and not the *{THEME}.libraries.yml* file (which is where a [theme's asset libraries are defined](https://drupalize.me/tutorial/define-asset-library)).

## Further your understanding

- Can you create a new asset library and attach to the page whenever a user profile page is viewed?
- Describe a use case for extending an existing asset library.

## Additional resources

- [Adding assets (CSS, JS) to a Drupal theme via \*.libraries.yml](https://www.drupal.org/docs/develop/theming-drupal/adding-assets-css-js-to-a-drupal-theme-via-librariesyml) (Drupal.org)
- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries) (Drupalize.Me)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library) (Drupalize.Me)
- [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Attach an Asset Library](/tutorial/attach-asset-library?p=2860)

Clear History

Ask Drupalize.Me AI

close
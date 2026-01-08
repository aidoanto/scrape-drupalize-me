---
title: "override the template"
url: "https://drupalize.me/tutorial/override-template-file"
guide: "[[theming-cheat-sheet]]"
---

# override the template

## Content

This tutorial demonstrates how to locate the template file that is currently being used to render an element and override it in your own theme. This is an important skill for anyone who wants to make changes to Drupal's default HTML markup.

In this tutorial we'll:

- Override the *node.html.twig* template in our theme
- Make changes to the markup
- Create a content-type-specific template override like *node--CONTENT\_TYPE.html.twig*

By the end of this tutorial you should be able to modify the HTML markup used to display a node, or any other element of the page generated using a template file.

## Goal

Modify the markup of *Page* nodes by overriding the *node.html.twig* template file in a custom theme.

## Prerequisites

- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)
- [What are Template Files?](https://drupalize.me/tutorial/what-are-template-files)

## Get the most out of this tutorial

This tutorial contains both a written and video tutorial. You can choose to use one or the other, or both! If you're new to Drupal theming, we suggest watching the video, then reading the written tutorial, in order to solidify your understanding. You can use the written tutorial as a reference or refresher later on, too, if you like.

Sprout Video

## How to override a template file

### Locate the template you wish to override

With [debugging enabled](https://drupalize.me/tutorial/configure-your-environment-theme-development), when you view the source of a page that contains the element you want to theme you should see output that looks something like the following (assuming we're talking about overriding the template used to display nodes):

```
<!-- THEME DEBUG -->
<!-- THEME HOOK: 'node' -->
<!-- FILE NAME SUGGESTIONS:
   * node--view--frontpage--page-1.html.twig
   * node--view--frontpage.html.twig
   * node--2--teaser.html.twig
   * node--2.html.twig
   * node--page--teaser.html.twig
   * node--page.html.twig
   * node--teaser.html.twig
   x node.html.twig
-->
<!-- BEGIN OUTPUT from 'core/themes/bartik/templates/node.html.twig' -->
<article class="contextual-region node node--type-page ... " about="/node/2">
```

The "FILE NAME SUGGESTIONS" section is a list of possible template names we can use, starting with the most specific. The one with an "x" next to the file name indicates that that is the theme hook suggestion currently being used.

The "BEGIN OUTPUT" section shows specifically which template file is currently being used.

### Copy the file

Once you've located the template file that is being used, copy that file to your theme.

Copy *core/themes/bartik/templates/node.html.twig* to *themes/icecream/templates/node.html.twig*

Note: It is important that you **COPY** and **not MOVE** the template file. If you don't leave the default in place, Drupal will have nothing to fall back on, which can ultimately break your application.

### Change the file name

Optionally, change the template name in order to be more, or less, specific using one of the suggestions from the "FILE NAME SUGGESTIONS" list in the debugging output.

Example: *themes/icecream/templates/node--page.html.twig* to theme just nodes of the type "page".

### Clear the cache

Clear the cache (or enable debugging mode), so that the next time the page is loaded Drupal goes through the process of locating the template files it needs and finds the one in your theme.

### Modify the template

Make your desired changes to the template file in your theme. Refresh the appropriate page in the browser to see your changes.

## Recap

In this tutorial we learned how to override a template file in order to modify the markup of *Page* nodes. First, we found the template file that is currently being used to generate the markup seen on the page. Then we copied that file into our custom theme, renaming it match the theme hook suggestion that targets only *Page* nodes and cleared the cache. Finally, we modified the new template file. In our browser, we can now reload a page on our site that uses this content type and see the changes we made in the template file.

## Further your understanding

- What is a *theme hook suggestion*?
- How can you figure out which template file is currently being used to output the HTML you want to override?
- On your site, right now, what possible names could you give to the *node.html.twig* file in your theme and have Drupal still find and use the file?

## Additional resources

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files) (Drupalize.Me)
- [Configure Your Environment For Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)
- [Working with Twig Templates](https://www.drupal.org/node/2186401) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close
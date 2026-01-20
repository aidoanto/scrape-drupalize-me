---
title: "fast by default"
url: "https://drupalize.me/tutorial/fast-default"
guide: "[[theming-cheat-sheet]]"
order: 2
---

# fast by default

## Content

Drupal comes with all of its caching features enabled by default. This improves response time, but can be frustrating for themers as it makes it harder to preview the changes you make to template files.

In this tutorial we'll look at:

- Why these features are enabled by default
- How the theme layer leverages Drupal's caches
- Why you should learn to disable them when doing development

## Goal

Understand which performance-related features in Drupal are turned on by default and how this can impact theme and front-end developers.

## Prerequisites

- None

## What is fast by default?

Note: If you just want to turn off caching and preview your changes in real time read about [configuring your environment for theme development](https://drupalize.me/tutorial/configure-your-environment-theme-development).

If you want to learn more about Drupal's front-end performance—read on!

In [this article](http://wimleers.com/article/performance-calendar-2013-making-the-entire-web-fast) Wim Leers makes the case for creating faster websites, and argues that tools like Drupal should be as fast as possible by default. They should not require users to locate and enable some buried settings, because many simply will not. In other words, if you want people to use best-practices, then make best-practice settings the default mode.

In the context of Drupal, "fast by default" implies things like page caching and CSS aggregation being enabled out of the box. Historically, these features were turned off on a new Drupal installation, and required an administrator to enable them. Which in turn required an administrator to *know* about them. In many cases they were never enabled—because people simply didn't know the option existed. So with Drupal, these performance-enhancing features are enabled by default, which encourages best practices, and helps to ensure that more Drupal sites take advantage of them.

Today's Drupal is fast by default, by having default settings that improve speed: [CSS and JS aggregation are enabled](https://www.drupal.org/node/2259531), [JavaScript assets are loaded from the bottom of the page](https://www.drupal.org/node/2412769) whenever possible, block caching is enabled by default, and so on.

Note: for various technical reasons, enabling page caching out of the box for Drupal 7 doesn't make a lot of sense.

## Impact on theme developers

This affects theme developers because now there are various different levels of caching, all enabled, and each of which can affect your ability to preview the changes you're making in different ways. Generally, we advise that you do your theming on a development version of the site and just [disable all the caching mechanisms](https://drupalize.me/tutorial/configure-your-environment-theme-development) while working, yet leaving them enabled on the production site.

Several different caches affect theme developers, as follows:

### Twig cache

Twig templates will be compiled and stored in the file system to increase performance. With caching enabled, changes to a Twig template will not be used until the cache is cleared and templates are re-compiled. Disabling the Twig cache will recompile the templates from source each time they are used and changes will be apparent immediately. Read more about [Twig's compilation cache](https://twig.symfony.com/doc/3.x/api.html#compilation-cache).

### Render API cache

Drupal caches any rendering it performs for Render API elements in order to speed up subsequent page loads. Since Twig template files are used to generate the HTML during the Render process, and that generated HTML is cached, changes to Twig templates for any Render API element will not take effect immediately when caching is enabled.

### CSS and JavaScript aggregation

It's not uncommon for a standard Drupal HTML page to include dozens of JavaScript files and even more CSS files. Aggregating the contents of these files into a smaller number of files means your browser makes fewer HTTP requests. This generally improves page performance. Since the files are aggregated once, and then cached on disk, subsequent changes to the source JavaScript or CSS files will not be detected by the browser until the cache has been cleared and the on-disk aggregate files have been recreated.

## Recap

In this tutorial we learned that Drupal has a number of cache and performance-related features "on" by default, making Drupal "fast by default." In the context of Drupal, "fast by default" implies things like page caching and CSS aggregation being enabled out of the box.

## Further your understanding

- Are you a front-end developer working on the theme? Learn to disable caching and [configure your localhost for theme development](https://drupalize.me/tutorial/configure-your-environment-theme-development).

## Additional resources

- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)
- [Change all default settings and config to fast/safe production values](https://www.drupal.org/node/2259531) (Drupal.org)
- [Debugging Twig templates](https://www.drupal.org/node/1906392) (Drupal.org)
- [Wim Leers on Drupal 8 caching](http://wimleers.com/blog/drupal-8-page-caching-enabled-by-default) (wimleers.com)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close
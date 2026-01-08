---
title: "Breakpoints and Media Queries"
url: "https://drupalize.me/tutorial/breakpoints-and-media-queries?p=3275"
guide: "[[media-and-responsive-images]]"
---

# Breakpoints and Media Queries

## Content

You've got a slick responsive theme for your Drupal site that's been implemented in CSS using media queries. But the content and images on your site will regularly be updated and you want to use the Responsive Images module to create responsive image style field formatters that you can apply to image field display settings.

In this lesson, we'll review the concepts of breakpoints and media queries so that you can better understand what's going on when you encounter them in non-CSS file contexts like configuration forms for responsive image styles or breakpoint YAML files.

By the end of this tutorial, you should have an understanding of what breakpoints are, how they are expressed in media queries, and how they are relevant in the context of Drupal.

## Goal

Know what breakpoints and media queries are and how Drupal uses these concepts outside of CSS files.

## Why this tutorial?

This tutorial primarily exists to help you understand the concepts at work in the Breakpoints and Responsive Images modules -- namely, breakpoints and media queries.

Media queries are implemented in CSS. In order for your site to have a "squishy" layout and have your site be responsive to various viewport widths, your theme will employ media queries to conditionally apply certain styles when certain environmental conditions are met.

Drupal now has a Breakpoints API that enables you to expose the media queries you've implemented using CSS to other modules or themes by implementing a [breakpoint configuration YAML file](https://drupalize.me/tutorial/what-breakpoint-yaml-file). This YAML file can contain an array of your site's breakpoints and media query information for the purpose of making this breakpoint information available to other modules or themes.

Why would a module need breakpoint information? Perhaps the module provides a page layout builder and enables you to select layouts suitable for specific breakpoints in your theme. Or, to cite an example in Drupal core, the Responsive Images module enables you to create responsive image styles, which essentially maps image styles to breakpoints. In order to use Responsive Images module, you either need to use the Responsive Images module's breakpoints YAML file, use another theme or module's breakpoints YAML file, or create your own custom breakpoint YAML file for your theme or module.

Please note that this tutorial is only meant to provide you with an overview and basic reference for these concepts, but not go into how to implement them in CSS. There are a lot of really great resources out there on responsive web design and responsive images in particular. These external resources can help you to understand the use cases for responsive images and are especially helpful if you want to go beyond a basic viewport-sizing solution for responsive images. A few that we've found helpful include:

- [Responsive Images 101 series](https://cloudfour.com/thinks/responsive-images-101-definitions/) by Jason Grigsby (Cloud Four)
- [Use Cases and Requirements for Standardizing Responsive Images](http://usecases.responsiveimages.org/) (Responsive Image Community Group, W3C)

## What are breakpoints and media queries?

A *breakpoint* consists of a label, an associated media query, and any other pertinent meta information. It is easier to refer to a breakpoint by its label than spouting off all of its properties every time you want to discuss it.

*Media queries* allow you to conditionally apply styles when certain environmental conditions are met. If you've been a web designer for a while, you've probably made a "print" style sheet. To call that style sheet, a media query would check for the *media type* "print" ("screen" being another media type). Now we can also check for *media features* like pixel-density, orientation, and max-width (among many others).

Breakpoint labels are often employed in communication about the design of the site, instead of always referring to them by their technically verbose media queries. For example, let's say your site has several layout styles that will be applied at various viewport-widths:

- **Mobile**: all content components are stacked in one-column, with a vertical menu hidden but activated by the touch of an icon
- **Tablet**: single and limited multi-column components accommodated, with a vertical menu in a sidebar
- **Desktop**: multi-column layout with a vertical or horizontal menu (or both!), perhaps even accommodating the all-popular multicolumn “mega-menu”

The team is likely to refer to each breakpoint by its descriptive label even before the specifics of the media query are determined. For example, “at the *tablet breakpoint*, the hero image background image should change to the cropped version”. Or, “the *tablet breakpoint* is 900 pixels, so let’s try a max-width media query of 899px and test it out.”

So a breakpoint, in practice, is a collection of information about a logical condition that evaluates to true when certain user-device environmental conditions are met. In Drupal, this collection of information about breakpoints is defined as identifier, label, media query, pixel-density multiplier, and (optional) breakpoint group.

## Media queries

As a Drupal developer, if you want to create a breakpoints configuration file, you will need to know how to identify and find the media queries in your site's CSS.

Media queries can be found in the `media` attribute of the `<link>` tag contained in the head of an HTML document or called inside a stylesheet using the `@media` syntax.

A media query is a logical expression that is either true or false. Media queries resemble property declarations, due to their format of "label: value" but they should be read and understood as expressions to be evaluated as true or false.

For example, the media query `screen and (min-width: 400px)` should be read as: "If the user device involves a screen and the viewport is greater than or equal to 400px wide, then load the following styles."

If you’re curious to learn exactly how media queries evaluate each media feature, read the [section of the W3C Media Queries specification on Media Features](https://www.w3.org/TR/css3-mediaqueries/#media1), which includes examples.

## Media query example in Drupal core

Drupal's Bartik theme uses media queries to make the sidebar component responsive in *core/themes/bartik/css/components/sidebar.css*

The media queries in this file are:

### Narrow breakpoint

```
@media all and (min-width: 560px) {}
```

### Wide breakpoint

```
@media all and (min-width: 851px) {}
```

The styles that are applied when the media query evaluates to “true” are nested within the media (as denoted by curly braces).

```
@media all and (min-width: 560px) {
  .sidebar {
    float: left; /* LTR */
    position: relative;
    width: 50%;
  }
  [dir="rtl"] .sidebar {
    float: right;
  }
  .layout-one-sidebar .sidebar {
    width: 100%;
  }
}
@media all and (min-width: 851px) {
  .layout-one-sidebar .sidebar {
    width: 25%;
  }
  #sidebar-first {
    width: 25%;
    margin-left: -100%; /* LTR */
  }
  [dir="rtl"] #sidebar-first {
    margin-right: -100%;
    margin-left: 0;
  }
  #sidebar-second {
    width: 25%;
    margin-left: -25%; /* LTR */
    clear: none;
  }
  [dir="rtl"] #sidebar-second {
    margin-right: -25%;
    margin-left: 0;
  }
}
```

## Breakpoints in Drupal

In Drupal, a site’s breakpoints can be exposed to other modules and themes in YAML format inside a [breakpoints configuration file](https://drupalize.me/tutorial/what-breakpoint-yaml-file). For example, the Bartik theme exposes the media queries in the above *sidebar.css* file as an array of breakpoints contained in a YAML file called *bartik.breakpoints.yml*.

For example, the media queries extracted from Bartik's CSS files and compiled as a collection of information about Bartik's breakpoints in the following file (*core/themes/bartik/bartik.breakpoints.yml*):

```
bartik.mobile:
  label: mobile
  mediaQuery: ''
  weight: 0
  multipliers:
    - 1x
bartik.narrow:
  label: narrow
  mediaQuery: 'all and (min-width: 560px) and (max-width: 850px)'
  weight: 1
  multipliers:
    - 1x
bartik.wide:
  label: wide
  mediaQuery: 'all and (min-width: 851px)'
  weight: 2
  multipliers:
    - 1x
```

By exposing your site's breakpoints in this way, other modules (such as Responsive Images module) can create features that make use of breakpoints.

- Learn more about [Breakpoint module and breakpoint configuration files](https://drupalize.me/tutorial/what-breakpoint-yaml-file)
- Learn more about [Responsive Image module](https://drupalize.me/tutorial/responsive-image-module-overview)

## Recap

In this tutorial, you learned about breakpoints and media queries, why you would want to use them, how they are constructed, and a little bit about how Drupal uses them. Learn more about [breakpoint configuration files in Drupal in the next tutorial](https://drupalize.me/tutorial/what-breakpoint-yaml-file).

## Further your understanding

- Are you new to media queries or need a refresher? The [W3C Media Query specification](https://www.w3.org/TR/css3-mediaqueries/) has a lot of great information and code examples. Read through it to learn about the myriad ways media queries can be constructed.
- Perform a search of all the media queries (search for the `@media` string) in your theme or a Drupal core theme. What are the common elements? Can you create a list of the breakpoints used in a particular theme? Give them descriptive labels and note the media query associated with each one.

## Additional resources

- [W3C Media Query specification](https://www.w3.org/TR/css3-mediaqueries/) (w3.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[What Is a Breakpoint YAML File?](/tutorial/what-breakpoint-yaml-file?p=3275)

Clear History

Ask Drupalize.Me AI

close
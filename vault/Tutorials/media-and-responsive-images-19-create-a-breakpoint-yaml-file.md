---
title: "Create a Breakpoint YAML File"
url: "https://drupalize.me/tutorial/create-breakpoint-yaml-file?p=3275"
guide: "[[media-and-responsive-images]]"
order: 19
---

# Create a Breakpoint YAML File

## Content

As we learned in the [What Is a Breakpoints YAML file?](https://drupalize.me/tutorial/what-breakpoint-yaml-file) tutorial, modules and themes can expose their site's CSS breakpoints and media queries to other Drupal modules and themes by implementing a breakpoints YAML file. In that tutorial, you also learned about the structure of a breakpoints configuration file and why you'd want to create one. In this tutorial, we’ll walk through the process of creating an example breakpoints file step-by-step.

By the end of this lesson, you should be able to create a working breakpoints YAML file in a theme or module. We'll test it out by enabling Drupal's Responsive Image module, where we'll be able to see it listed in the configuration form for creating a new responsive image style.

## Goal

Create a breakpoints configuration file in YAML with information about your site's key breakpoints and media queries and successfully test it using Drupal's Responsive Image module.

## Prerequisites

- [Introduction to YAML](https://drupalize.me/videos/introduction-yaml)
- [Breakpoints and Media Queries](https://drupalize.me/tutorial/breakpoints-and-media-queries)
- [What Is a Breakpoint YAML File?](https://drupalize.me/tutorial/what-breakpoint-yaml-file)

## Terminology review

- A [breakpoint](http://usecases.responsiveimages.org/#design-breakpoints) is one of a series of [CSS media queries](https://www.w3.org/TR/css3-mediaqueries/) which can update the styles of a page based on a matching of environmental conditions or [media features](http://usecases.responsiveimages.org/#dfn-media-features). (Responsive Image Community Group, W3C)
- If you need a refresher on breakpoints and media queries, check out this related tutorial: [Breakpoints and Media Queries](https://drupalize.me/tutorial/breakpoints-and-media-queries).
- In the context of a Drupal breakpoint YAML file, a breakpoint consists of an identifier, label, media query, weight, pixel-resolution multiplier, and optional group name.
- A breakpoint YAML file exposes your site's breakpoints and media queries to other Drupal modules and themes. Learn more in [What Is a Breakpoint YAML File?](https://drupalize.me/tutorial/what-breakpoint-yaml-file)

## Create a breakpoint configuration file

You can expose your site's breakpoints to other Drupal modules or themes, enabling them to be utilized in configuration forms or other features that a module or theme might provide. You do this by creating a breakpoint configuration file.

### Create the breakpoints YAML file

In the root of your theme or module's directory, create a new file called *EXTENSION.breakpoints.yml*, where *EXTENSION* is the short name of your theme or module. For example, Bartik's breakpoints YAML file is named *bartik.breakpoints.yml*.

Next, we need to gather the media query information we want to put in our breakpoints file. If you already know what media queries you want to put in this file, feel free to skip ahead.

### Find the media queries in your module or theme

- Search your theme or module's CSS directory for `@media`.

Image

![Search for media queries](../assets/images/breakpts_find_in_css.png)

### Make a list of all the media query search results

If you have a lot of results, it can be helpful to copy the results to a text file so that you can better organize them.

If you're using PhpStorm, you can export search results to a text file (see screenshot below):

Image

![Export search results to text in PhpStorm](../assets/images/phpstorm-export-search-results-txt.png)

For example, if you perform a search for the string `@media` in the Bartik theme's CSS directory (*core/themes/bartik/css*), you will get the following results:

(Note: the number in front of `@media` is the line number.)

```
Targets
    Occurrences of '@media' in Directory /Library/WebServer/Documents/demo-responsive-theming/docroot/core/themes/bartik/css
Found Occurrences  (27 usages found)
    demo-responsive-theming  (27 usages found)
        docroot/core/themes/bartik/css  (3 usages found)
            layout.css  (1 usage found)
                15@media all and (min-width: 851px) {
            maintenance-page.css  (2 usages found)
                56@media all and (min-width: 800px) {
                65@media all and (min-width: 600px) { 
        docroot/core/themes/bartik/css/components  (24 usages found)
            featured-bottom.css  (2 usages found)
                13@media all and (min-width: 560px) {
                25@media all and (min-width: 851px) {
            field.css  (1 usage found)
                45@media all and (min-width: 560px) {
            form.css  (2 usages found)
                94@media screen and (max-width: 60em) { /* 920px */
                307@media all and (max-width: 600px) {
            header.css  (3 usages found)
                14@media all and (min-width: 461px) {
                30@media screen and (max-width: 460px) {
                41@media all and (min-width: 901px) {
            main-content.css  (1 usage found)
                15@media all and (min-width: 851px) {
            primary-menu.css  (3 usages found)
                114@media all and (min-width: 461px) and (max-width: 900px) {
                163@media all and (min-width: 901px) {
                208@media all and (min-width: 461px) {
            sidebar.css  (2 usages found)
                3@media all and (min-width: 560px) {
                16@media all and (min-width: 851px) {
            site-branding.css  (3 usages found)
                19@media all and (min-width: 461px) {
                24@media all and (min-width: 901px) {
                34@media all and (min-width: 901px) {
            site-footer.css  (3 usages found)
                13@media all and (min-width: 560px) {
                23@media all and (min-width: 560px) and (max-width: 850px) {
                45@media all and (min-width: 851px) {
            table.css  (2 usages found)
                63@media screen and (max-width: 37.5em) { /* 600px */
                71@media screen and (max-width: 60em) { /* 920px */
            tabs.css  (2 usages found)
                27@media screen and (max-width: 37.5em) { /* 600px */
                42@media screen and (min-width: 37.5em) { /* 600px */
```

### Narrow down the list of media queries

As you can see from the search results for `@media` in the Bartik theme, there are many results. You don't necessarily have to represent every single media query in your breakpoints file. In fact, Bartik's breakpoints file only contains 3 breakpoints: mobile, narrow, and wide, representing the layout breakpoints that affect the main content area (and ignoring the media queries for header components, primary menu, tabs, tables, and forms).

Remember that the purpose of the breakpoints file is to expose your theme's breakpoints to another module in the Drupal system. Assuming that we're creating a breakpoints file to use with the Responsive Image module, let's just pull out the media queries that affect regions inside the main content area, where it's mostly likely that new content containing images would be displayed. Basically, anything between the header and the footer, but ignoring components such as menus, tabs, tables, and forms. Looking at our search results for Bartik, these would be the ones in:

- *layout.css*
- *featured-bottom.css*
- *field.css*
- *main-content.css*
- *sidebar.css*

In these files, we have some common media queries, namely:

- `@media all and (min-width: 851px)`
- `@media all and (min-width: 560px)`

### Order the breakpoints by min- or max-width

Let's put these in order, from the lowest minimum-width to the highest:

- `@media all and (min-width: 560px)`
- `@media all and (min-width: 851px)`

### Name the breakpoints

Given that the first layout style change is activated at a minimum-width of 560px, we can assume a "mobile-first" design. A mobile-first design usually implies that the default styles are meant to be applied to mobile-friendly viewport sizes, which in this case was determined to be less than 560px wide. Because of this assumption, we can name our first breakpoint "mobile", with an empty media query, followed by "narrow", triggered at a minimum-width of 560px, and "wide", triggered at a minimum-width of 851px. For each breakpoint label, note the associated media query. For example:

#### Mobile

Media query: (empty, default styles (no media query))

#### Narrow

Media query: `@media all and (min-width: 560px)`

#### Wide

Media query: `@media all and (min-width: 851px)`

### Add pixel-resolution multipliers

The Breakpoint module supports pixel-resolution multipliers of 1x, 1.5x, and 2x. Multipliers represent the ratio between the physical pixel size of the active device and the device-independent pixel size. For example "Retina" displays have a multiplier of 2x. If you're not sure what to put here, enter 1x for a multiplier. Even with a 1x multiplier in this file, we can still configure usage of 1.5x or 2x images using the sizes attribute when we configure a responsive image style.

#### Mobile

Media query: (empty, default styles (no media query))
Multipliers: 1x

#### Narrow

Media query: `@media all and (min-width: 560px)`
Multipliers: 1x

#### Wide

Media query: `@media all and (min-width: 851px)`
Multipliers: 1x

### Format breakpoint list as YAML

Now we're ready to take our list of breakpoints and put it into our *EXTENSION.breakpoints.yml* file.

For each label, we'll need to convert that to a machine-name identifier, and then under that fill in values for the keys:

- `label`
- `mediaQuery`
- `weight`
- `multipliers`

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

The identifiers should start with the theme or module name, then a dot, followed by a short label for the breakpoint, i.e. `bartik.mobile`.

For more information about each key, see [What Is a Breakpoint YAML File?](https://drupalize.me/tutorial/what-breakpoint-yaml-file)

### Enable Responsive Image module

You can test to see if your breakpoints YAML file is being recognized by Drupal by enabling the core Responsive Image module and navigating to the **Add responsive image styles** form and checking the **Breakpoint Group** form field for your theme or module name. If you don't specify an optional breakpoint group, this will be the name of your theme or module. Learn more about breakpoint groups in [What Is a Breakpoint YAML File?](https://drupalize.me/tutorial/what-breakpoint-yaml-file)

Install/Enable the core Responsive Image module:

- Navigate to *Extend*
- In the core group of modules, check **Responsive Image**
- Click **Install** button (bottom of page)

### View the "Add new responsive image style" form

- Using the *Manage* administrative menu, navigate to *Configuration* > *Media* > *Responsive image styles*
- Click **Add responsive image style** button

### Check the breakpoint groups field

- Select the dropdown list of breakpoint groups and check for your theme or module name. Or, if you've specified a breakpoint group, look for that name.

Image

![Check breakpoint group field](../assets/images/check-breakpoint-group.png)

If you don't see your theme, module, or breakpoint group name listed, make sure you've named your breakpoint file correctly (see step 1). Also make sure that your theme or module is enabled.

You now should have a Drupal-recognized breakpoints YAML file for your theme or module. Next, make use of it and [learn about responsive image styles provided by the Responsive Image module](https://drupalize.me/tutorial/responsive-image-module-overview).

## Recap

In this tutorial, we learned how to find the media queries in CSS files, pick out the relevant ones, label them as breakpoints, and put all that information into YAML inside a *EXTENSION.breakpoints.yml* file. We then tested it out by viewing the responsive image styles configuration form to make sure it was being recognized by the system.

## Further your understanding

- Check out the tutorials on [Responsive Image module](https://drupalize.me/tutorial/responsive-image-module-overview) to see how the breakpoint file is used by a module to customize a configuration form.
- [Learn more about the use cases for responsive images](http://usecases.responsiveimages.org) (Responsive Images Community Group, W3C)

## Additional resources

- [Breakpoints and Media Queries](https://drupalize.me/tutorial/breakpoints-and-media-queries) (Drupalize.Me)
- [What Is a Breakpoint YAML File?](https://drupalize.me/tutorial/what-breakpoint-yaml-file) (Drupalize.Me)
- [Working with breakpoints in Drupal](https://www.drupal.org/docs/8/theming-drupal-8/working-with-breakpoints-in-drupal-8) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Is a Breakpoint YAML File?](/tutorial/what-breakpoint-yaml-file?p=3275)

Clear History

Ask Drupalize.Me AI

close
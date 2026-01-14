---
title: "Exercise: Override the Main Page Template"
url: "https://drupalize.me/tutorial/exercise-override-main-page-template?p=3269"
guide: "[[frontend-theming]]"
---

# Exercise: Override the Main Page Template

## Content

In order to change Drupal's default markup you need to override template files. The *page template* controls the overall layout of your theme, including the placement of regions. You should practice the exercise following the written instructions below. Use the video walk-through to help if you get stuck.

In this exercise, we'll:

- Override the currently used *page.html.twig* template file.
- Modify the content of the file to include the regions defined in the theme's *.info.yml* file.
- Wrap the regions in the page template file with HTML markup using CSS classes from Bootstrap to achieve the example layout.

By the end of this tutorial, you'll gain practice creating a custom layout in a page template file.

## Goal

Edit the HTML markup in the *page.html.twig* file in your theme's *templates* directory to use CSS grid classes provided by the Bootstrap framework, creating a layout like the example below.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial you'll be applying your knowledge of template files (and a little bit of Twig). We assume that you're already familiar with the information in these tutorials:

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [Override a Template File](https://drupalize.me/tutorial/override-template-file)
- [Determine the Base Name of a Template File](https://drupalize.me/tutorial/determine-base-name-template)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)

## Exercise

In the following steps, we'll override a page template file and add regions to create a layout like this:

Image

![Illustration of layout with header, menu, breadcrumb, and highlighted regions all full width, content and both sidebars as 3 columns, and one column for each of the two footer regions.](../assets/images/multi-column-layout-example.png)

### Review the layout and goal

The page template controls the overall layout of a theme. We'll make use of the grid layout classes provided by Bootstrap. In order to do this you need to override or edit the current *page.html.twig* file and modify it to add classes and in some cases wrapping `<div>` elements.

### Determine which *page.html.twig* file is being used

Depending on how your theme is set up, you will either need to copy a *page.html.twig* template file into your theme's *templates* directory, or edit the one that is already there. View source of a content page in your browser and search for the Twig debug output for `THEME HOOK: 'page'`.

- If the *page.html.twig* file **is not** already in your theme (e.g. in a base theme), you will need to **[override](https://drupalize.me/tutorial/override-template-file)** it, (e.g. copy that file into your theme's *templates* directory). Then [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache), and verify in the HTML source code that the page template file in your theme is now being used.
- If the \_page.html.twig file **is** already somewhere in your theme's *templates* directory, you will **edit** it.

### Add missing regions

Open your theme's *page.html.twig* file in a code editor. Use the Twig syntax `{{ page.REGION_NAME }}` to add any missing regions to the *page.html.twig* template file. These should match the list of regions you defined in the theme's *.info.yml* file.

### Use the classes from the Bootstrap framework

In order to achieve the desired layout, we can modify the existing HTML markup of Drupal to use the utility classes provided by the Bootstrap framework.

Use the grid layout classes documented at [http://getbootstrap.com/css/#grid-example-basic](https://getbootstrap.com/css/#grid-example-basic) to create a layout like the illustration above.

You’ll need to use `container` , `row` ,and `grid` classes. As well as adding wrapping `<div>` elements in a few places to make this work. Add `pb-2 mt-4 mb-2 border-bottom` classes to the `{{ page.header }}` container and `jumbotron` to the `{{ page.highlighted }}` container.

### Verify your changes to the layout

View one of the generated content pages in a browser and refresh the page as you make changes to the template markup. You may need to add blocks to regions in *Structure* > *Block layout* to fully test the new layout.

## Recap

After completing this exercise when you view any page on your site that uses your theme it should render using a multi-column layout. Try placing blocks into each available region of the theme and ensure they appear in the correct location on the page.

Sprout Video

**Note:** This video demonstrates overriding a page template file from Classy base theme. [Classy has since been removed as a base theme from Drupal](https://www.drupal.org/node/3305674).

## Further your understanding

- Familiarize yourself with Bootstrap's documentation. For example, read about the classes used in this exercise: [jumbotron](https://getbootstrap.com/docs/4.5/components/jumbotron/), [spacing](https://getbootstrap.com/docs/4.5/utilities/spacing/), and [borders](https://getbootstrap.com/docs/4.5/utilities/borders/).

## Additional resources

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files) (Drupalize.Me)
- [Override a Template File](https://drupalize.me/tutorial/override-template-file) (Drupalize.Me)
- [Determine the Base Name of a Template File](https://drupalize.me/tutorial/determine-base-name-template) (Drupalize.Me)
- [Twig in Drupal](https://drupalize.me/tutorial/twig-drupal) (Drupalize.Me)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters) (Drupalize.Me)
- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)
- [Change record: Classy removed and replaced with Starterkit theme generator](https://www.drupal.org/node/3305674) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Configure Your Environment for Theme Development](/tutorial/exercise-configure-your-environment-theme-development?p=3269)

Next
[Exercise: Override the Node Template](/tutorial/exercise-override-node-template?p=3269)

Clear History

Ask Drupalize.Me AI

close
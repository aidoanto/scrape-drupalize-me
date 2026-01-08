---
title: "Exercise: Override the Node Template"
url: "https://drupalize.me/tutorial/exercise-override-node-template?p=3269"
guide: "[[frontend-theming]]"
---

# Exercise: Override the Node Template

## Content

The available dynamic tokens or *variables* vary from template to template. Each page is built from a set of templates.

In this exercise, we'll:

- Override and name the *node template* file so that it will only affect *Article* nodes on our Drupal site.
- Inspect the available variables.
- Customize the markup.
- Use the Twig filter `without`.

We recommend that you try to work through the exercise yourself, and refer to the video if you need help.

## Goal

Override the node template file affecting *Article* nodes only and use the `without` filter to put the image field output in a `<div>` separate from the rest of the content.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial you'll be applying your knowledge of overriding template files and Twig! We assume that you're already familiar with the information in these tutorials:

- [Determine the Base Name of a Template File](https://drupalize.me/tutorial/determine-base-name-template)
- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)
- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions)
- [Clear Drupal's Cache](https://drupalize.me/tutorial/clear-drupals-cache)

## Exercise

In the following steps, we'll:

- Override the *node.html.twig* template file and target only *Article* nodes.
- Modify the template so that the content of the image field of a node is output wrapped in a `<div>` independent of the rest of the node's content.

Example:

Image

![Screenshot showing image field of an article node displayed above the body content with a red border around it to indicate that it is in its own container.](/sites/default/files/styles/max_800w/public/tutorials/images/article-node-image-example.png?itok=eZK42iIo)

### Override the node template

Override the *node.html.twig* file. Find the one that is currently being used and copy it into your theme’s */themes/THEMENAME/templates* directory. If you already have a *node.html.twig* file in your theme, duplicate the file (we'll rename it in the next step).

### Use the appropriate file name suggestion

Rename the *node.html.twig* file you just created so that will apply *only* to nodes of the type *article*. [Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).

### Inspect available variables

Use the Twig statement `{{ dump(content|keys) }}` to inspect the contents of the content variable, or `{{ dump(_context|keys) }}` to inspect the content of all variables in the template.

Find the name of the image field property within the `content` variable.

### Modify the markup

Modify the template so that if `{{ content }}` contains a value for the attached image field (`field_image`), the content will be split across two columns: one for the image and another for everything else in `{{ content }}`. Otherwise, display the content in a single column.

**Hint:** use Twig’s `without` filter.

## Recap

After completing this exercise when you view an *Article* node with an image attached the body of the node should be split into two columns. One for the image, and another for everything else. If there is no image attached to the *Article* node it should display as a single column. All node types other than *Article* should remain unaffected.

Sprout Video

## Further your understanding

- See [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) for more information about alternatives to Twig `dump()`.
- Get more practice: [Exercise: Override the Main Menu Template](https://drupalize.me/tutorial/exercise-override-main-menu-template)

## Additional resources

- [Override a Template File](https://drupalize.me/tutorial/override-template-file)
- [Determine the Base Name of a Template File](https://drupalize.me/tutorial/determine-base-name-template)
- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions) (Drupalize.Me)
- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Override the Main Page Template](/tutorial/exercise-override-main-page-template?p=3269)

Next
[Exercise: Override the Main Menu Template](/tutorial/exercise-override-main-menu-template?p=3269)

Clear History

Ask Drupalize.Me AI

close
---
title: "Exercise: Override the Main Menu Template"
url: "https://drupalize.me/tutorial/exercise-override-main-menu-template?p=3269"
guide: "[[frontend-theming]]"
order: 17
---

# Exercise: Override the Main Menu Template

## Content

In this exercise, we'll practice theming by overriding the *main menu template*. We'll:

- Override and rename the main menu template so that it will only affect the main menu component of our Drupal site.
- Add Bootstrap classes from the *base nav* component into our overridden main menu template file.
- Add CSS classes to HTML selectors using `attributes.addClass()` and `set` methods.

We recommend that you work on the exercise steps below first. You can refer to the video if you need some help.

## Goal

Override the menu template file and add classes to match the *base nav* Boostrap component markup.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial, you'll apply your knowledge of overriding template files and Twig. We assume that you're already familiar with the information in these tutorials:

- [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates)
- [Clear Drupal's Cache](https://drupalize.me/tutorial/clear-drupals-cache)

## Exercise

In the following steps we'll:

- Override the *menu.html.twig* template file, using a file name suggestion to target only the *main menu*.
- Add CSS classes from the [base nav component in Bootstrap](https://getbootstrap.com/docs/4.2/components/navs/).

### Override the menu template

Override the *menu.html.twig* file. Find the one that is currently being used and copy it into your theme's */themes/THEMENAME/templates* directory.

### Use a theme hook suggestion

Rename the *menu.html.twig* file you just created so that it uses theme hook (file name) suggestions in order to only apply to only the *main menu* and clear the cache.

### Read the comment block

Read the description for the `items` variable in the comment block at the top of the overridden menu template file.

### Modify the markup

Modify the template and add classes so that the unordered list, list items, and anchor tags use the classes in the [base nav component in Bootstrap](https://getbootstrap.com/docs/4.2/components/navs/). Also, change the name of the `item.in_active_trail` variable to `active` instead of `is-active`. Finally, add a class that will right-align the menu component.

Hints:

- Consult the [Bootstrap docs](https://getbootstrap.com/docs/4.2/components/navs/) to find the appropriate classes.
- You will need to use a variety of methods to add the classes. Use the existing template markup as a guide and try to figure out which method to use or modify to add the necessary CSS classes.
- Apply classes for the menu `<ul>` inside the `if menu_level == 0` conditional statement.

Sprout Video

## Recap

After completing this exercise, the main menu items should be displayed horizontally and aligned to the right.

## Further your understanding

- Get more practice: [Exercise: Override the Image Field Template](https://drupalize.me/tutorial/exercise-override-image-field-template)

## Additional resources

- [Override a Template File](https://drupalize.me/tutorial/override-template-file)
- [Determine the Base Name of a Template File](https://drupalize.me/tutorial/determine-base-name-template)
- [Loops and Iterators in Twig](https://drupalize.me/tutorial/loops-and-iterators-twig) (Drupalize.Me)
- [Print Values from a Field with a For Loop](https://drupalize.me/tutorial/print-values-field-loop) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Override the Node Template](/tutorial/exercise-override-node-template?p=3269)

Next
[Exercise: Override the Image Field Template](/tutorial/exercise-override-image-field-template?p=3269)

Clear History

Ask Drupalize.Me AI

close
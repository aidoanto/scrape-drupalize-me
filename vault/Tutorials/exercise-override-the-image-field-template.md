---
title: "Exercise: Override the Image Field Template"
url: "https://drupalize.me/tutorial/exercise-override-image-field-template?p=3269"
guide: "[[frontend-theming]]"
order: 49
---

# Exercise: Override the Image Field Template

## Content

In this exercise, we'll continue our template overriding practice by overriding the *image field template*. We'll consult the Bootstrap documentation and add a responsive image class that will apply to any images uploaded by a user to the `field_image` field. Once again, we'll add this class to the `classes` array in the `set` Twig tag. You should work on the exercise steps below first, and you can refer to the video if you need some help.

## Goal

Override the image field template and add a responsive class to the `classes` array in the `set` Twig tag.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial you'll be applying your knowledge of overriding template files and Twig! We assume that you're already familiar with the information in these tutorials:

- [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates)
- [Clear Drupal's Cache](https://drupalize.me/tutorial/clear-drupals-cache)

## Exercise

In the following steps we'll:

- Override the image field template file.
- Add values to the `classes` array with `set`.

### Override the image field template

Override the *image.html.twig* template. Identify the one being used and copy it to your theme's */themes/THEMENAME/templates* directory and clear the cache.

Hint: Navigate to a generated Article node that has an image attached to it and view source.

### Modify the markup

Modify the template in order to dynamically add the `img-fluid` class to the other classes being applied to ![](). Check the [Bootstrap documentation for Responsive images](https://getbootstrap.com/docs/4.3/content/images/#responsive-images) to verify the class name.

Sprout Video

## Recap

After completing this exercise when you view an *Article* node with an image attached, you should see the `img_fluid` class added to the image's `<img>` tag.

## Further your understanding

- Get more practice: [Exercise: Use the t Filter in a Template](https://drupalize.me/tutorial/exercise-use-t-filter-template)

## Additional resources

- [Override a Template File](https://drupalize.me/tutorial/override-template-file)
- [Classes and Attributes in Twig Templates](https://drupalize.me/tutorial/classes-and-attributes-twig-templates) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Override the Main Menu Template](/tutorial/exercise-override-main-menu-template?p=3269)

Next
[Exercise: Use the t Filter in a Template](/tutorial/exercise-use-t-filter-template?p=3269)

Clear History

Ask Drupalize.Me AI

close
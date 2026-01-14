---
title: "Exercise: Use the t Filter in a Template"
url: "https://drupalize.me/tutorial/exercise-use-t-filter-template?p=3269"
guide: "[[frontend-theming]]"
order: 19
---

# Exercise: Use the t Filter in a Template

## Content

In this exercise, we'll practice using the `t` filter in a Twig template. As a best practice, all hard-coded text in a template should be translatable. Simple text (containing no dynamic tokens) can be passed through the `t` filter to achieve this objective. Along the way, we'll also use a basic conditional `if` statement with Twig. We recommend that you try following the exercise's steps first, and refer to the video if you need help.

## Goal

Use the `t` filter to make hard-coded text in a template translatable.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial you'll be applying your knowledge of filters in a Twig template. We assume that you're already familiar with the information in these tutorials:

- [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters)
- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions)
- [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable)

## Exercise

In the steps below we'll:

- Add a `<div class="label label-warning">` element to the article node template file that contains the string `"This node is not published"`.
- Use the `t` filter to make the hard-coded text translatable.
- Use basic logic statements with Twig to check if the node is published or not.

### Open *node--article.html.twig* for editing

We created this file in a [previous exercise](https://drupalize.me/tutorial/exercise-override-node-template).

### Add custom text and markup

Add a label to the page if the node being viewed is unpublished using the `<div class="label label-warning">` Bootstrap component. (Hint: read the comment block at the top of the template file to find a function that checks the node's published status.)

Use the string, `"This node is not published"` in your template in a way that allows it to be translated.

### Test it out

Test it out by unpublishing an article node and seeing if your message appears. Inspect the message to ensure the right classes were applied.

Sprout Video

## Recap

After completing this exercise when you view an unpublished *Article* node, you should see a message that says "This node is not published."

## Further your understanding

- Learn more about [Internationalization (i18n) in Drupal](https://drupalize.me/course/internationalization-i18n-drupal).

## Additional resources

- [Twig Filters and Functions](https://drupalize.me/tutorial/twig-filters-and-functions) (Drupalize.Me)
- [Make Your Theme Translatable](https://drupalize.me/tutorial/make-your-theme-translatable) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Override the Image Field Template](/tutorial/exercise-override-image-field-template?p=3269)

Next
[Exercise: Preprocess Functions](/tutorial/exercise-preprocess-functions?p=3269)

Clear History

Ask Drupalize.Me AI

close
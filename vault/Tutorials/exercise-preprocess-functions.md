---
title: "Exercise: Preprocess Functions"
url: "https://drupalize.me/tutorial/exercise-preprocess-functions?p=3269"
guide: "[[frontend-theming]]"
order: 20
---

# Exercise: Preprocess Functions

## Content

Preprocess functions allow you to change existing variables, or add new variables, for a template file using PHP code. In this exercise, you'll:

- Define a PHP function that implements a preprocess hook
- Create a new variable named `{{ today }}` that contains the current date and gets passed to the *page.html.twig* template file.

We recommend that you try the exercise's steps first, and refer to the video if you need help.

## Goal

Add a new variable named `today` that contains the current date and time to the *page* template file via a preprocess function.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial you'll be applying your knowledge of using a preprocess function to add a variable for use in a template file. We assume that you're already familiar with the information in these tutorials:

- [Add Logic with THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme)
- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)
- [Add Variables to a Template File](https://drupalize.me/tutorial/add-variables-template-file)

## Exercise

In the steps below we'll:

- Create a *THEMENAME.theme* file.
- Write a preprocess PHP function that adds variables to a page template file.

### Create a *.theme* file

If the file doesn’t already exist create a new *THEMENAME.theme* file in your theme’s root directory.

### Define a preprocess function

Define a new function that implements a preprocess hook for the *page.html.twig* template. Reminder, the function naming convention is `THEMENAME_preprocess_HOOK(array &$variables)`.

### Define a new variable

Create a new variable named `today` that contains the current date and time. The following PHP gives the value: `date('H:i, m-d-Y’)`

### Use the variable in a template file

Edit your *page.html.twig* template and print the new variable in the footer of the page template.

Sprout Video

## Recap

After completing this exercise when you view any page using your theme you should be able to see the current date and time displayed in the footer of the page.

## Further your understanding

- Check out our guide, [Frontend Theming](https://drupalize.me/guide/frontend-theming).

## Additional resources

- [Add Logic with THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme) (Drupalize.Me)
- [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions) (Drupalize.Me)
- [Change Variables with Preprocess Functions](https://drupalize.me/tutorial/change-variables-preprocess-functions) (Drupalize.Me)
- [Add Variables to a Template File](https://drupalize.me/tutorial/add-variables-template-file) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Use the t Filter in a Template](/tutorial/exercise-use-t-filter-template?p=3269)

Clear History

Ask Drupalize.Me AI

close
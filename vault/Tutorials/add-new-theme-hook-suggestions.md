---
title: "Add New Theme Hook Suggestions"
url: "https://drupalize.me/tutorial/add-new-theme-hook-suggestions?p=3268"
guide: "[[frontend-theming]]"
order: 54
---

# Add New Theme Hook Suggestions

## Content

Themes and modules can alter the list of theme hook suggestions in order to add new ones, remove existing ones, or reorder the list. This powerful feature allows for the definition of custom logic in your application that can tell Drupal to use different templates based on your own unique needs. You might for example; use a different page template for authenticated users, or a custom block template for someone's birthday.

In this tutorial we'll cover:

- Adding new theme hook suggestions from a theme using `hook_theme_suggestions_HOOK_alter()`
- Altering the list of theme hook suggestions
- Removing theme hook suggestions
- Reordering the list of theme hook suggestions

## Goal

Understand how to add, alter, remove, or reorder the list of theme hook suggestions for a template file.

## Prerequisites

- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)
- [Discover Existing Theme Hook Suggestions](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions)
- [Add Logic with THEMENAME.theme](https://drupalize.me/tutorial/add-logic-themenametheme)
- [Determine the Base Name of a Template](https://drupalize.me/tutorial/determine-base-name-template)
- [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks)

## Add your own theme hook suggestions

[Theme hook suggestions](https://drupalize.me/tutorial/what-are-template-files) are provided by one of three hooks, or by using special syntax when creating a Render API array. Both modules and themes can add or remove suggestions from the list. The most common scenario is likely to be altering the existing list in order to add a new suggestion, but you may also want to remove an existing suggestion or reorder the list so that Drupal looks for templates in a different order.

When you add a new theme hook suggestion you're telling Drupal that you would like it to also consider your additional suggestions when it's searching for template files. As a theme developer, this should correspond with also adding that template variant as a file to your theme. There's really no reason to add suggestions if you're not going to use them in your own theme.

There are all kinds of scenarios where adding a theme hook suggestion is a useful thing to know how to do. Here are some that I've used recently:

- Use a different page template for logged-in users
- Use a different template for the teaser version of a node versus the full page view
- Specify that certain pages on your site are part of a payment funnel and remove all side bars from those pages

[This article by Casey Wight](https://www.chapterthree.com/blog/how-to-create-custom-theme-suggestions-drupal-8) demonstrates accessing the request object to generate a theme hook suggestion. It's a great example of what you can accomplish with a bit of logic in your *THEMENAME.theme* file.

If you want to add to the list in your theme, the recommended method is to implement `hook_theme_suggestions_HOOK_alter()` in your *THEMENAME.theme* file. Don't be confused by the use of the word "hook" two times in naming this function. The first "hook" should be replaced with the name of your theme or module. The latter "HOOK" should be replaced with the base name of the template file for which you're suggesting alternatives. Learn more about [finding the base name of a template file](https://drupalize.me/tutorial/determine-base-name-template).

Let's add a new suggestion for a template file that will be used to theme nodes for any logged-in users. The base name of the node template is *node*. So we can add the following to your theme's *THEMENAME.theme* file.

```
/**
 * Implements hook_theme_suggestions_HOOK_alter().
 */
function MYTHEME_theme_suggestions_node_alter(array &$suggestions, array $variables) {
  $logged_in = \Drupal::currentUser()->isAuthenticated();
  if ($logged_in) {
    $suggestions[] = 'node__' . 'authenticated';
  }
}
```

Note that when adding to the array of suggestions we use underscores (`_`) instead of hyphens (`-`). The theme system will convert them to hyphens when looking for a matching template.

The above code would add a suggestion to use a template named *node--authenticated.html.twig* for any user who is currently logged in, but leave the suggestion off for anonymous users. And that's it. It's as easy as adding a new entry to the array of suggestions and then creating the newly suggested template file.

## Alter theme hook suggestions

Modules and themes can alter the list of theme hook suggestions using one of these two hooks. They both function the same but vary in specificity:

- [`hook_theme_suggestions_alter(array &$suggestions, array $variables, $hook)`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme_suggestions_alter/)
- [`hook_theme_suggestions_HOOK_alter(array &$suggestions, array $variables)`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme_suggestions_HOOK_alter/)

For a more in-depth look at how the default list of available theme hook suggestions is added see this related tutorial, [Discovering Theme Hook Suggestions](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions).

## Remove or reorder theme hook suggestions

Using `hook_theme_suggestions_HOOK_alter()`, a module or theme can also remove a suggestion from the list or reorder the list completely. You simply need to make modifications to the `$suggestions` array passed to the function. Suggestions are used in the order they appear in the array, so if you want to change priority simply shuffle the array. Both cases are rare, but good to know about.

## Recap

In this tutorial, you learned how to implement the hook `hook_theme_suggestions_HOOK_alter`, within which you can add, edit, remove, or reorder the list of theme hook suggestions for a template file.

## Further your understanding

- What are the default set of theme hook suggestions for the *page.html.twig* template?
- Can you add a theme hook suggestion that will allow you to use a different template for nodes on Wednesdays?
- Are there cases in your current project where the logic in a template file can be simplified by using theme hook suggestions? Hint: node templates are often a good candidate for this.

## Additional resources

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files) (Drupalize.Me)
- [Discover Existing Theme Hook Suggestions](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions) (Drupalize.Me)
- [Drupal 8 Theming Tutorial: How to Craft Custom Theme Hook Suggestions and Templates](http://dannyenglander.com/blog/drupal-8-theming-tutorial-how-craft-custom-theme-hook-suggestions-and-templates) (dannyenglander.com) - Contains a great example of a real world use-case for adding new theme hooks.
- [Working with Twig Templates](https://www.drupal.org/node/2186401) (Drupal.org)
- [Template Naming Conventions](https://www.drupal.org/node/2354645) (Drupal.org)
- [Information about theme hook suggestions in the API documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/themeable/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Discover Existing Theme Hook Suggestions](/tutorial/discover-existing-theme-hook-suggestions?p=3268)

Clear History

Ask Drupalize.Me AI

close
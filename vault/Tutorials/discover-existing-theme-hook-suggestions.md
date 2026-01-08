---
title: "Discover Existing Theme Hook Suggestions"
url: "https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions?p=3268"
guide: "[[frontend-theming]]"
---

# Discover Existing Theme Hook Suggestions

## Content

When determining which template file to use to theme an element, Drupal uses the list of [theme hook suggestions](https://drupalize.me/tutorial/what-are-template-files) to look for the best match. This allows for fine-grained control over how things appear based on dynamic state and contextual information in your application. The list of theme hook suggestions varies for each base template, so we need a way to figure out our options.

In this tutorial we'll look at:

- How to determine the list of valid theme hook suggestions for any template file
- How theme hook suggestions are added by modules and themes

By the end of this tutorial you should be able to explain how theme hook suggestions are added, and determine the valid suggestions for any template file.

## Goal

Learn how to find the list of valid theme hook suggestions for any template file.

## Prerequisites

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)

## Discover existing suggestions with debug mode

The quickest way to discover available theme hook suggestions is to [enable Twig debugging mode](https://drupalize.me/tutorial/configure-your-environment-theme-development) and view the source of any page that contains a copy of the element you want to theme.

Example output with `twig.debug` enabled:

```
<!-- THEME DEBUG -->
<!-- THEME HOOK: 'node' -->
<!-- FILE NAME SUGGESTIONS:
* node--2430--full.html.twig
* node--2430.html.twig
* node--blog-post--full.html.twig
* node--blog-post.html.twig
* node--full.html.twig
x node.html.twig
-->
<!-- BEGIN OUTPUT from 'core/themes/classy/templates/content/node.html.twig' -->

<article data-history-node-id="2430" data-quickedit-entity-id="node/2430" role="article" class="contextual-region node node--type-blog-post node--view-mode-full" about="/node/2430">
// Node content here ...
</article>
```

In this example, the list under `FILE NAME SUGGESTIONS` contains a list of all known possible template names that Drupal would use for this specific node. The most specific name appears at the top and the least specific is at the bottom. If any new template files are added using one of these names, Drupal will use the most specific one it finds. The template name that Drupal is currently using is preceded by an `x` instead of an `*`.

Here's another example: this one is taken from the block that displays the system menu, with the Bartik theme enabled:

```
<!-- THEME DEBUG -->
<!-- CALL: theme('block') -->
<!-- FILE NAME SUGGESTIONS:
* block--system.html.twig
* block--system-menu-block.html.twig
* block--system-menu-block--tools.html.twig
* block--bartik-tools.html.twig
x block.html.twig
-->
<!-- BEGIN OUTPUT from 'core/modules/block/templates/block.html.twig' -->
<div class="block block-system contextual-region block-menu" id="block-bartik-tools" role="navigation">

... HTML stuff was here ...

</div>
<!-- END OUTPUT from 'core/modules/block/templates/block.html.twig' -->
```

Did you notice that the suggestions vary depending on the type of element being themed? Both modules and themes can add theme hook suggestions. The list will vary depending on which modules you have enabled and your individual site configuration.

## How to add theme hook suggestions

There are a couple of different ways that a module or theme can add a theme hook suggestion to the list. Generally, what you'll see is a list of suggestions added by the module that provides the base template or [Render API](https://drupalize.me/tutorial/render-api-overview) output. Occasionally you'll see additional suggestions added by a base theme, if you're using one. Because theme hook suggestions can be added in a couple of different ways, and they are application-specific, there is no single place in code that contains a complete list. But, this should give you some ideas about where to start looking if you're curious.

When a render array uses the `#theme` property to specify the name of a template, it can optionally use an array instead of a single string value. For further reference, this is implemented in `Drupal\Core\Theme\ThemeManager::render`.

Example:

```
$element = array(
  '#theme' => array(
    'node__custom_suggestion', // node--custom-suggestion.html.twig
    'node__teaser' // node--teaser.html.twig
    'node' // node.html.twig
  ),
);
```

In a render array, the `#theme` property can be set to the name of a hook with a *`__SUGGESTION`* suffix. Search results are a good example:

```
$element = array(
  '#theme' => 'item_list__search_results',
);
```

In this case *item-list--search-results.html.twig* will be used if it exists, and the base *item-list.html.twig* template will be used as a fallback. This type of suggestion can also be combined with providing an array of theme hook names.

Modules that provide new templates can implement [hook\_theme\_suggestions\_HOOK()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme_suggestions_HOOK/) and return an array of possible theme hook suggestions for any template provided by the module.

Any module or theme can implement [hook\_theme\_suggestions\_HOOK\_alter()](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme_suggestions_HOOK_alter/) to modify or extend the list of theme hook suggestions for a given template.

Modules and themes can use one of these three hooks to add new theme hook suggestions:

- [hook\_theme\_suggestions\_HOOK(array $variables)](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme_suggestions_HOOK/)
- [hook\_theme\_suggestions\_alter(array &$suggestions, array $variables, $hook)](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme_suggestions_alter/)
- [hook\_theme\_suggestions\_HOOK\_alter(array &$suggestions, array $variables)](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/function/hook_theme_suggestions_HOOK_alter/)

**Note:** Don't be confused by the use of the word hook two times in naming these functions. The first `hook` should be replaced with the name of your theme or module. The latter `HOOK` should be replaced with the base name of the template that you're suggesting alternatives for. Learn more about [finding the base name of a template file](https://drupalize.me/tutorial/determine-base-name-template).

## Recap

In this tutorial, you learned how to find all possible names for a template file by discovering the list of a template file's theme hook suggestions. We also learned how modules and themes can add theme hook suggestions to the list. Knowing this can help discover valid options if Twig debugging output isn't available.

## Further your understanding

- Every template has a different set of suggestions. Enable debugging and scour the source code to get some ideas about how you might use theme hook suggestions to organize your theme and reduce the amount of if/else logic used in your templates
- If a Render API array has an element with the property `'#theme' => 'item_list__menu_item'`, what template files will it use to theme the item and in what order?

## Additional resources

- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files) (Drupalize.Me)
- [Add Additional Theme Hook Suggestions](https://drupalize.me/tutorial/add-new-theme-hook-suggestions) (Drupalize.Me)
- [Working with Twig Templates](https://www.drupal.org/node/2186401) (Drupal.org)
- [Template Naming Conventions](https://www.drupal.org/node/2354645) (Drupal.org)
- [Information about theme hook suggestions in the API documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Render%21theme.api.php/group/themeable/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Add New Theme Hook Suggestions](/tutorial/add-new-theme-hook-suggestions?p=3268)

Clear History

Ask Drupalize.Me AI

close
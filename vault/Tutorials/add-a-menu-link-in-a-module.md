---
title: "Add a Menu Link in a Module"
url: "https://drupalize.me/tutorial/add-menu-link-module?p=2758"
guide: "[[develop-custom-pages]]"
---

# Add a Menu Link in a Module

## Content

In this tutorial we will learn how to add menu links using a custom Drupal module. We will also look at the options available for configuring our new menu link. Lastly, we'll learn about using `hook_menu_links_discovered_alter()` that can be used to add new menu links, or alter the behavior of existing ones.

## Goal

Understand how to provide a new menu link, alter existing menu links, or add a dynamic menu link in code, inside a Drupal module.

## Prerequisites

- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)
- [Overview: Menu Links in a Module](https://drupalize.me/tutorial/overview-menu-links-module)

## Defining menu links

In this tutorial we'll be looking at the code provided by the [Examples module](https://www.drupal.org/project/examples) and in particular the [Page example](https://git.drupalcode.org/project/examples/-/tree/3.x/modules/page_example) sub-module. This module provides 2 menu links.

Modules can provide menu links by including a special YAML file in the root directory of the module. This YAML file should include the name of the module and end with the pattern *.links.menu.yml*. Let's take a look at the contents of the *page\_example.links.menu.yml* file:

```
page_example.description:
  title: Page Example
  route_name: page_example_description
  expanded: TRUE

page_example.simple:
  title: Simple - no arguments
  route_name: page_example_simple
  parent: page_example.description

# We can't define a menu link for the page_example_arguments route, because it
# requires path arguments.
```

This module provides 2 menu links. The keys in this YAML file are unique machine names for each of the menu links they define. The only value that's absolutely required is the `title` although you'll rarely find menu links that don't also include at least a `route_name` or a `url`. If the menu links to an internal route, the `route_name` value specifies the Drupal route for the link. An external resource can be included in a menu by specifying a `url` value instead of this `route_name`.

- **title**: The text of the menu link when it is rendered
- **description**: Text rendered either as a tooltip or in the admin UI to provide additional information about the link
- **parent**: The machine name of another menu link used to created nested menus
- **menu\_name**: The machine name of a menu to put the link in, if not the default Tools menu
- **route\_name** (or url): Where this menu link should point to
- **weight**: Allow menu links to be placed in a particular order

The [menu system documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu/) covers the additional values that we can provide in this YAML file.

Where do new menu links show up in the UI? That depends on the menu link definintion. If you specify either a `parent` or a `menu_name` that will dictate where in the existing menu structure the new menu links appear. In all other cases the new menu links will appear in the Tools menu in the UI and you can relocate them to a new place in the hierarchy by navigating to *Structure* > *Menus* and choosing the *Edit menu* operation for the Tools menu, locating the new link there, and then editing it to move it to a new location.

By specifying these menu links in a *MODULENAME.links.menu.yml* file they will then be rendered on our site. Here they are in action:

Image

![Page example module menu links](/sites/default/files/styles/max_800w/public/tutorials/images/menu-link.png?itok=OygfWhJZ)

## Altering existing menu links

Occasionally you may need to alter an existing menu link provided by another module. To do this, we can use the [hook\_menu\_links\_discovered\_alter](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/function/hook_menu_links_discovered_alter/) hook. This hook receives an associative array with all the static menu links built up from traversing the *MODULENAME.links.menu.yml* files that define menu links. The data structure of this array is similar to the structure of the YAML we've seen above. Here is an example of an implementation of the hook, used to change the weight and title of the user logout link.

```
function hook_menu_links_discovered_alter(&$links) {
  // Change the weight and title of the user.logout link.
  $links['user.logout']['weight'] = -10;
  $links['user.logout']['title'] = new \Drupal\Core\StringTranslation\TranslatableMarkup('Logout');
  }
}
```

## Creating dynamic menu links

To create dynamic menu links, you'll use [plugin derivatives](https://drupalize.me/tutorial/plugin-derivatives). Learn how in this tutorial: [Create Dynamic Menu Links](https://drupalize.me/tutorial/create-dynamic-menu-links).

## Recap

In this tutorial, we looked at how to specify menu links in the *MODULENAME.links.menu.yml* file of a custom module. We also looked at the configuration options available in this YAML file to provide additional information, nesting or ordering of our menu links. We've also seen how to use the `hook_menu_links_discovered_alter` function to alter existing menu links or add our own based on dynamic criteria.

## Further your understanding

- Look at the menus on your site. Can you find the implementation of some of these menu links?
- Try to add a few menu links in your custom module. Make sure to try both internal and external links.

## Additional resources

- [Menu system documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu/) (api.drupal.org)
- [Providing module defined menu links](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-menu-links) (Drupal.org)
- [hook\_menu\_links\_discovered\_alter documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/function/hook_menu_links_discovered_alter/) (Drupal.org)
- [Routing system overview](https://www.drupal.org/docs/drupal-apis/routing-system/routing-system-overview) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Menu Links in a Module](/tutorial/overview-menu-links-module?p=2758)

Next
[Add an Action Link in a Module](/tutorial/add-action-link-module?p=2758)

Clear History

Ask Drupalize.Me AI

close
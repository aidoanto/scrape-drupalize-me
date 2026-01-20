---
title: "Define a Menu Item"
url: "https://drupalize.me/tutorial/define-menu-item?p=3236"
guide: "[[drupal-module-developer-guide]]"
order: 20
---

# Define a Menu Item

## Content

Drupal's [Menu system](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu/) allows module developers to define navigational links, offering flexibility to site builders for configuration and arrangement. By linking to routes rather than URLs, these links remain functional, even when route definitions change.

In this tutorial, we'll:

- Create a *MODULE\_NAME.links.menu.yml* file.
- Define a new menu item link for the */weather* page in our *anytown* module.
- Configure Drupal to display the link in the primary navigation.

By the end of this tutorial, you'll be able to define new menu item links and integrate them into your site's configuration.

## Goal

Add a link to the */weather* page to the site's main navigation.

## Prerequisites

- [Concept: Menu Items and Links](https://drupalize.me/tutorial/concept-menu-items-and-links)
- [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page)

## Video tutorial

Sprout Video

## Add a link to the weather page

Now that we've created a custom page, we can add a link to it in the site's navigation. To do this, we'll need to provide a link definition in our module, then add it to a menu using the administrative UI.

### Create a menu links definition file

Create the file, *anytown.links.menu.yml*, in the root of your module. This YAML file can include multiple link definitions.

### Define the link

Insert the following YAML code into the *anytown.links.menu.yml* file:

```
# Each link needs a unique name. We recommend prefixing links with the name of
# your module. A links.menu.yml file can contain any number of link definitions.
anytown.weather:
  title: Weather
  description: Check this week's weather.
  menu_name: main
  # From anytown.routing.yml.
  route_name: anytown.weather_page
```

This code defines a link for the *Weather* page with a unique internal name `anytown.weather`, a human-readable title and description, the default menu, and the associated route name.

### Clear the cache

Link definitions are cached, so you'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) before Drupal will find your new link or any changes to existing links.

### Verify the new link

Assuming your site has the main menu displayed somewhere on the page, after clearing the cache, the link to the weather page should appear in the menu.

You can also find and manage the newly-added link in Drupal's administrative UI. In the *Manage* administration menu navigate to *Manage* > *Structure* > *Menus* (*admin/structure/menu*), then press the *Edit menu* button for the menu named *Main navigation*. From here you can re-order the links, including the new **Weather** link, in the menu or move a link to another menu.

## Recap

In this tutorial, we defined a new menu link for our */weather* page using a YAML file. This approach allows site builders to manage the link's placement and ensures consistency even if the route changes.

## Further your understanding

- What occurs if a default menu isn't specified in the link definition?
- Can you modify the link name through the Drupal administrative UI?

## Additional resources

- [Add a Menu Link in a Module](https://drupalize.me/tutorial/add-menu-link-module) (Drupalize.Me)
- [Drupal Menu System](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu) (api.drupal.org)
- Examples for Developers project: [menu\_example.links.yml](https://git.drupalcode.org/project/examples/-/blob/4.0.x/modules/menu_example/menu_example.links.menu.yml?ref_type=heads) (git.drupalcode.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Menu Items and Links](/tutorial/concept-menu-items-and-links?p=3236)

Next
[Concept: Permissions](/tutorial/concept-permissions?p=3236)

Clear History

Ask Drupalize.Me AI

close
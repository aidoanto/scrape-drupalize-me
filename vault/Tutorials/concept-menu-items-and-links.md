---
title: "Concept: Menu Items and Links"
url: "https://drupalize.me/tutorial/concept-menu-items-and-links?p=3236"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Menu Items and Links

## Content

Drupal offers module developers several methods for creating different types of links, all defined by module configuration. This tutorial explores these types of links, how they relate to each other, and when to use them.

In this tutorial, we'll learn:

- The nature of menu items, action links, and local task links.
- Examples of each link type in Drupal's UI and their application in our scenario.
- Criteria for selecting the appropriate link type for adding the weather page to site navigation.

By the end of this tutorial, you'll understand the different types of links in Drupal and how they apply to adding navigational elements for custom module pages.

## Goal

Understand different types of links modules can provide and when to use each.

## Prerequisites

- [5.5. Concept: Menu](https://drupalize.me/tutorial/user-guide/menu-concept)
- [Concept: Routes](https://drupalize.me/tutorial/concept-routes)

## Link types in Drupal

When adding a navigation element in Drupal as a module developer, consider Drupal's UI flexibility. We aim to enable site builders to toggle elements and customize their layout. Depending on the intent, a module can create new menu items, action links, or local tasks linked to routes.

Module-provided navigation elements should point to a route, not directly to a URL. This allows module developers to update the route definition without breaking user-configured menu links. For example, you could change the route's path and all links to that route will reflect the change without having to go update the path for each link. This also ensures that core subsystems and other modules can alter the final URL if needed. For example, the translation system might offer different paths like */en/weather* and */de/weather* for the same route, depending on the user's chosen language.

Image

![Screenshot of the Claro administrative theme with arrows pointing out menu items in the sidebar, a local action button, and local tasks rendered as tabs.](../assets/images/routes--overview-menu-items-and-links-diagram.png)

### Menu items

Menu items are individual entries in a menu, typically used for site navigation. For example, **Home**, **About Us**, and **Contact** links in the main navigation menu are typical menu items. Module-added menu items are associated with routes, while site administrators can add custom menu items pointing to hard-coded URLs.

Menu items are defined in a module's *MODULE\_NAME.links.menu.yml* file.

### Action links

Action links are for primary actions on a page, such as **Add content** on the *Content* overview page. These links usually lead to forms or operations specific to the current context, often displayed prominently, often as buttons.

Action links are defined in a module's *MODULE\_NAME.links.action.yml* file.

### Local task links (tabs)

Local task links, often seen as tabs, provide access to related tasks on a page. For example, on a node page, **View**, **Edit**, and **Delete** might appear as local task links for quick access to common operations for that content.

Local tasks (tabs) are defined in a module's *MODULE\_NAME.links.task.yml* file.

## Choosing the right link type

It makes sense to add a menu item that links to our new weather page. A menu item added by the *anytown* module will appear in the main navigation by default, and allows site administrators to reorder link within the menu.

## Recap

This tutorial explained the different types of links in Drupal and their specific uses. Menu items are individual entries in a menu, typically used for site navigation. Action links define primary actions in a certain context. Local tasks are identified by their "tab" appearance, and used for links such as the "View", "Edit", and "Delete" links on a content page as viewed by an administrator.

## Further your understanding

- Explore your Drupal site to identify some menu, action, and local task link types. Can you find their implementation in your codebase?
- Why add the weather page to the main navigation using a menu item? When might you choose a local task instead?

## Additional resources

- [Overview: Menu Links in a Module](https://drupalize.me/tutorial/overview-menu-links-module?p=2766) (Drupalize.Me)
- [Drupal Menu System](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu) (api.drupal.org)
- [5.5. Concept: Menu](https://drupalize.me/tutorial/user-guide/menu-concept) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Parameter to a Route](/tutorial/add-parameter-route?p=3236)

Next
[Define a Menu Item](/tutorial/define-menu-item?p=3236)

Clear History

Ask Drupalize.Me AI

close
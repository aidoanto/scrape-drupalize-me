---
title: "Add an Action Link in a Module"
url: "https://drupalize.me/tutorial/add-action-link-module?p=2758"
guide: "[[develop-custom-pages]]"
---

# Add an Action Link in a Module

## Content

Modules can provide action links to make common operations more readily available within a particular context. For example, a site administrator visiting the content management page may be interested in adding content. If you've ever noticed the *Add content* button on this page, that's an example of an action link. In this tutorial we'll take a look at how custom modules can provide these action links to make it easier for users to interact with our site.

## Goal

Learn what action links and local actions are and how they are added to custom modules.

## Prerequisites

- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)
- [Overview: Menu Links in a Module](https://drupalize.me/tutorial/overview-menu-links-module)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)

## Action links

Action links are a type of link that provide users with quick access to particular operations in contextually relevant places. The *Add content* button on the content administration page is an example of one of these action links.

Image

![Content administration add content action link](../assets/images/action-link.png)

Local action links, such as this one, are typically rendered as buttons. This is one of the easiest ways to distinguish between a local action and a [local task](https://drupalize.me/tutorial/add-local-task-link-module).

### Defining an action link

Like most of the other types of menu links, in order to define an action link you need to create a specially named YAML file, *MODULENAME.links.action.yml*. Core's Node module provides a couple of action links in the */core/modules/node/node.links.action.yml* file:

```
node.type_add:
  route_name: node.type_add
  title: 'Add content type'
  appears_on:
    - entity.node_type.collection
node.add_page:
  route_name: node.add_page
  title: 'Add content'
  appears_on:
    - system.admin_content
```

The *MODULENAME.links.action.yml* file uses a machine name for the link as the keys, and has several different values that provide additional configuration information.

- **route\_name**: Typically you'll notice that the link's machine name will match the `route_name` value. This isn't a hard requirement, but the convention makes it easier to locate the action links if another developer needs to alter the link later on.
- **title**: The `title` value provides the text that will be rendered on this action button.
- **appears\_on**: The YAML list `appears_on` lists the route(s) where the local action should appear.

In order to create an action link you will need to find the machine name of at least 2 routes: a route for the link's destination, and another for the route where the action button will appear.

If you find yourself needing to alter the local actions from another module you can do so by [implementing the hook](https://drupalize.me/tutorial/implement-any-hook): [hook\_menu\_local\_actions\_alter](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Menu!menu.api.php/function/hook_menu_local_actions_alter/).

## Recap

In this tutorial we learned what action links are and how they're different from local tasks. We looked at the implementation of action links provided by the Node module and saw the different pieces that make up the *MODULENAME.links.action.yml* file required to create action links.

## Further your understanding

- Find other instances of action links as you browse your site. Can you find the implementation?
- Try [implementing](https://drupalize.me/tutorial/implement-any-hook) `hook_menu_local_actions_alter` to change the title of one of the core action links.

## Additional resources

- [Menu system documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu/) (Drupal.org)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Menu Link in a Module](/tutorial/add-menu-link-module?p=2758)

Next
[Add a Contextual Link in a Module](/tutorial/add-contextual-link-module?p=2758)

Clear History

Ask Drupalize.Me AI

close
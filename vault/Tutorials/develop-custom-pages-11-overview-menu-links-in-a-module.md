---
title: "Overview: Menu Links in a Modulefree"
url: "https://drupalize.me/tutorial/overview-menu-links-module?p=2758"
guide: "[[develop-custom-pages]]"
order: 11
---

# Overview: Menu Links in a Modulefree

## Content

Drupal provides module developers several different methods for creating the different types of links we see on a typical page. In this tutorial we'll see how these different types of links relate to each other, and when you might want to make use of them.

Image

![Link types illustrated](../assets/images/content_entity_example_links.png)

In this tutorial we'll provide an overview of the following concepts:

- Menu links
- Action links
- Local tasks
- Contextual links

## Goal

Learn the differences between the various types of links available to module developers and understand when to use each type of link.

## Prerequisites

- [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules)

## Menu links

If a module wants to add a link to a menu in Drupal, it can do so by providing a menu link. From a high level these links are provided by custom modules by including a YAML file. Browsing Drupal core you will see that several modules include menu links. You can identify them by looking for files that end with the extension *.links.menu.yml*. For example, the Node module defines 2 menu links in the file *core/modules/node/node.links.menu.yml*.

```
entity.node_type.collection:
  title: 'Content types'
  parent: system.admin_structure
  description: 'Create and manage fields, forms, and display settings for your content.'
  route_name: entity.node_type.collection
node.add_page:
  title: 'Add content'
  route_name: node.add_page
```

Learn more about the various options for menu links in [Add a Menu Link in a Module](https://drupalize.me/tutorial/add-menu-link-module).

## Action links

While logged in as a site administrator, if you come across a link to *Add* something, chances are you're looking at an action link. Action links allow module developers to provide particular actions for working with their data structures. An example of this can be seen on the content type administration screen (*/admin/structure/types*) with the **Add content type** button. Actions are specified in yet another YAML file with a particular naming convention *MODULENAME.links.action.yml*. Again using the Node module as an example, here is the contents of the */core/modules/node/node.links.action.yml* file:

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

Learn more about action link options in [Add an Action Link in a Module](https://drupalize.me/tutorial/add-action-link-module).

## Local task links

Local tasks are by default rendered as tabs available to authenticated users. If you've ever visited a node page and clicked on the edit link you've clicked a local task link to reach the edit form. These links are also defined within a particularly named YAML file with the extension *.links.task.yml*. The Node module provides several local tasks. We can see that by looking at *core/modules/node/node.links.task.yml*.

```
entity.node.canonical:
  route_name: entity.node.canonical
  base_route: entity.node.canonical
  title: 'View'
entity.node.edit_form:
  route_name: entity.node.edit_form
  base_route: entity.node.canonical
  title: Edit
entity.node.delete_form:
  route_name: entity.node.delete_form
  base_route: entity.node.canonical
  title: Delete
  weight: 10
entity.node.version_history:
  route_name: entity.node.version_history
  base_route: entity.node.canonical
  title: 'Revisions'
  weight: 20
entity.node_type.edit_form:
  title: 'Edit'
  route_name: entity.node_type.edit_form
  base_route: entity.node_type.edit_form
entity.node_type.collection:
  title: List
  route_name: entity.node_type.collection
  base_route: entity.node_type.collection
```

Learn more about local task links in [Add a Local Task Link in a Module](https://drupalize.me/tutorial/add-local-task-link-module).

## Contextual links

Contextual links provide shortcuts to common administrator tasks. For example, when viewing a node, common actions may include editing or deleting the content. Contextual links provided by the Node module make that easier.

Image

![Contextual links on a node](../assets/images/contextual-links.png)

Contextual links, unlike the links we've looked at so far, are not only specified via a YAML file. Contextual links should identify the particular route (named URL path) that will be used as contextual links. These routes are listed in a YAML file with the *.links.contextual.yml* extension. In addition to the YAML file a contextual link needs to add a `#contextual_links` element to the render array where the link needs to appear. Returning to the Node module for an example we can find the */core/modules/node/node.links.contextual.yml* file:

```
entity.node.edit_form:
  route_name: entity.node.edit_form
  group: node
  title: Edit

entity.node.delete_form:
  route_name: entity.node.delete_form
  group: node
  title: Delete
  weight: 10
```

Learn more about contextual links in [Add a Contextual Link in a Module](https://drupalize.me/tutorial/add-contextual-link-module).

## Recap

In this tutorial, we looked at the four major types of links we can provide from a custom module. We looked at the hopefully familiar implementation of each of them from core's Node module. Menu links provide module developers a way to add any particular link to Drupal's menu system. Action links allow developers to add buttons for particular behaviors like adding additional entities. Local tasks can help group commonly needed tasks around working with a particular entity. Contextual links provide another avenue to provide these types of links with a less obtrusive UI pattern.

## Further your understanding

- Navigate around your Drupal site and try to identify some menu, action, local task and contextual link types. Can you find their implementation in your code base?
- When would you choose to use a local task link? When might a contextual link be more appropriate?
- Can you find where the `#contextual_links` render element is added within the Node module? New to render elements? Start with a [Render API Overview](https://drupalize.me/tutorial/render-api-overview).
- Each of these types of links are different plugins. While you probably don't need to know the details of the plugin system to understand how to create links, our [What Are Plugins](https://drupalize.me/tutorial/what-are-plugins) tutorial provides a good starting point if you're curious.

## Additional resources

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins) (Drupalize.Me)
- [Render API Overview](https://drupalize.me/tutorial/render-api-overview) (Drupalize.Me)
- [Drupal core menu documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Menu%21menu.api.php/group/menu/) (Drupal.org)
- [Providing module-defined menu links](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-menu-links) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Add a Menu Link in a Module](/tutorial/add-menu-link-module?p=2758)

Clear History

Ask Drupalize.Me AI

close
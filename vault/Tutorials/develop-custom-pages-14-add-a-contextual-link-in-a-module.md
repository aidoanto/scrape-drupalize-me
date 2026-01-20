---
title: "Add a Contextual Link in a Module"
url: "https://drupalize.me/tutorial/add-contextual-link-module?p=2758"
guide: "[[develop-custom-pages]]"
order: 14
---

# Add a Contextual Link in a Module

## Content

Contextual links provide yet another method for Drupal module developers to add helpful links for site administrators to quickly navigate to commonly used tasks. In this tutorial we'll learn how to implement and render contextual links from a custom module. We will also look at a pair of alter hooks that can be used to tweak existing contextual links.

## Goal

Learn how to provide or alter contextual links and understand how they are rendered.

## Prerequisites

- [Creating an info file for a module](https://drupalize.me/tutorial/create-info-file-module?p=2766)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)
- [Menu Links Overview](https://drupalize.me/tutorial/overview-menu-links-module)
- [Render API Overview](https://drupalize.me/tutorial/render-api-overview)

## Defining contextual links

Modules that define contextual links must provide a *MODULENAME.links.contextual.yml* file in the top level directory of their code. This file, like all of the other types of links, contains a YAML representation of the links. Here is the code from the Node module's contextual link implementation in */core/modules/node/node.links.contextual.yml*

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

The keys in this YAML file represent the machine name for the contextual link. There are three key values that define a contextual link.

- **title**: The `title` is what is rendered in the UI for the link as the link title
- **route\_name**: The `route_name` is the machine name of the route which ultimately provides the path the user will be taken to upon clicking the link.
- **group**: The `group` value is perhaps the most important, and unique to contextual links. This value defines the context group in which these links will be rendered. It corresponds to the key defined by a module within a `#contextual_links` render array element.

Image

![Contextual links for nodes](../assets/images/contextual-links.png)

### The context group

When an entity enters the rendering cycle, if there is a `#contextual_links` element in the render array the appropriate contextual link group is gathered. For a block, the relevant portion of the render array might look like this:

```
array(
  '#contextual_links' => array(
    'block' => array(
      'route_parameters' => array('block' => $entity->id()),
    ),
  ),
```

The `block` array key in the `#contextual_links` array defines the *group* for the contextual links that need to be loaded. The links for this group are then output via the rendering pipeline.

## Altering existing contextual links

Contextual links from other modules can be altered via the [hook\_contextual\_links\_alter](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Menu!menu.api.php/function/hook_contextual_links_alter/) function. This hook receives as associative array containing all the contextual links for a given group (the second parameter) as well as any route parameters that have been passed to this collection of links. Here is an example implementation that dynamically alters the title of the menu edit link:

```
function hook_contextual_links_alter(array &$links, $group, array $route_parameters) {
  if ($group == 'menu') {
    // Dynamically use the menu name for the title of the menu_edit contextual
    // link.
    $menu = \Drupal::entityManager()->getStorage('menu')->load($route_parameters['menu']);
    $links['menu_edit']['title'] = t('Edit menu: @label', array('@label' => $menu->label()));
  }
}
```

There is another hook that can be used to alter the render array of a contextual link: [hook\_contextual\_links\_view\_alter](https://api.drupal.org/api/drupal/core%21modules%21contextual%21contextual.api.php/function/hook_contextual_links_view_alter/). This alter hook receives the render array for the contextual links element, and can be used to do things like add classes to the link item, as in this example:

```
function hook_contextual_links_view_alter(&$element, $items) {
  // Add another class to all contextual link lists to facilitate custom
  // styling.
  $element['#attributes']['class'][] = 'custom-class';
}
```

## Recap

In this tutorial we learned how to create the *MODULENAME.links.contextual.yml* files required to add contextual links in a module. We also looked at how contextual links are rendered with the `#contextual_links` render array element. Lastly, we looked at 2 examples of alter hooks that can be used to manipulate the contextual links provided by other modules.

## Further your understanding

- Can you find the implementation code (including render elements) for some of the contextual links on your site?
- Examine the contextual links provided by the block system. Especially note how it makes use of grouping to organize links.

## Additional resources

- [Providing module-defined contextual links](https://www.drupal.org/docs/drupal-apis/menu-api/providing-module-defined-contextual-links) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add an Action Link in a Module](/tutorial/add-action-link-module?p=2758)

Next
[Add a Local Task Link in a Module](/tutorial/add-local-task-link-module?p=2758)

Clear History

Ask Drupalize.Me AI

close
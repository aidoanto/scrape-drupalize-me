---
title: "Create Dynamic Menu Links"
url: "https://drupalize.me/tutorial/create-dynamic-menu-links?p=2758"
guide: "[[develop-custom-pages]]"
order: 16
---

# Create Dynamic Menu Links

## Content

Learn how to generate menu links dynamically with plugin derivatives in a custom module. This tutorial walks through creating a single base menu link plugin definition and a deriver class that expands that definition into one menu link per content entity. The code will automatically generate links for all published basic pages, placing dynamic menu links in the main menu.

By the end of this tutorial, you should be able to:

- Understand which files you need in order to define menu link plugin derivatives, also known as dynamic menu links
- Create the necessary code to define menu link plugin derivatives for an example use case

## Goal

Automatically add a menu link to the Main navigation for every published Basic page using plugin derivatives.

## Prerequisites

- [Overview: Menu Links in a Module](https://drupalize.me/tutorial/overview-menu-links-module)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [Plugin Derivatives](https://drupalize.me/tutorial/plugin-derivatives)

## Overview

Menu links are plugins. With plugin derivatives, one plugin definition can generate many menu links at runtime. In this example, you will create a dynamic link for every published basic page content item (content type `page`) and place the links in a menu of your choice.

## Set up

This example assumes your site has the "Basic page" content type with published content and the Main navigation menu (machine name: `main`).

Create a custom module called `dynamic_page_links`. (Tip: Use `drush generate module` to quickly create the module scaffolding.)

### Add a base menu link definition

Create the file, *modules/custom/dynamic\_page\_links/dynamic\_page\_links.links.menu.yml*, with the following contents:

```
dynamic_page_links.page:
  class: Drupal\dynamic_page_links\Plugin\Menu\PageMenuLink
  deriver: Drupal\dynamic_page_links\Plugin\Derivative\PageMenuLinkDeriver
  menu_name: main
  weight: 0
```

This defines a dynamic menu link plugin. In [Add a Menu Link in a Module](https://drupalize.me/tutorial/add-menu-link-module), we learned how to add a menu link plugin by hard-coding the link's `title` and `route`. Here we're saying that we want to use a special `deriver` class that will dynamically calculate a list of menu links and provide them as an instance of the named `class`. You should think of this as saying: instead of hard-coding the YAML definition of the links, I want Drupal to invoke my `deriver` which will tell it what YAML to include.

The result:

- Multiple menu links (one for each published page on our site)
- Automatically added to the `main` menu
- Without the need to manually add or remove menu items when the list of published pages changes

### Create the default plugin class

We need a default plugin class that extends `MenuLinkDefault`.

Inside to your module's directory, create the file, *src/Plugin/Menu/PageMenuLink.php*:

```
<?php

namespace Drupal\dynamic_page_links\Plugin\Menu;

use Drupal\Core\Menu\MenuLinkDefault;

/**
 * Base plugin for dynamic Page menu links.
 */
class PageMenuLink extends MenuLinkDefault {}
```

### Create the deriver class

Inside to your module's directory, create the file, *src/Plugin/Derivative/PageMenuLinkDeriver.php*:

```
<?php

namespace Drupal\dynamic_page_links\Plugin\Derivative;

use Drupal\Component\Plugin\Derivative\DeriverBase;
use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Plugin\Discovery\ContainerDeriverInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Generates a menu link for each published Page node.
 */
class PageMenuLinkDeriver extends DeriverBase implements ContainerDeriverInterface {

  /**
   * The entity type manager service.
   */
  protected EntityTypeManagerInterface $entityTypeManager;

  /**
   * Constructs the deriver.
   */
  public function __construct($base_plugin_id, EntityTypeManagerInterface $entity_type_manager) {
    $this->entityTypeManager = $entity_type_manager;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container, $base_plugin_id) {
    return new static(
      $base_plugin_id,
      $container->get('entity_type.manager')
    );
  }

  /**
   * {@inheritdoc}
   */
  public function getDerivativeDefinitions($base_plugin_definition) {
    $links = [];

    $storage = $this->entityTypeManager->getStorage('node');
    $pages = $storage->loadByProperties([
      'type' => 'page',
      'status' => 1,
    ]);

    foreach ($pages as $node) {
      $id = $node->id();

      $links[$id] = [
        'title' => $node->label(),
        'route_name' => 'entity.node.canonical',
        'route_parameters' => ['node' => $id],
        'weight' => 0,
      ] + $base_plugin_definition;
    }

    return $links;
  }

}
```

### Rebuild caches

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) and view your site in a browser.

## Recap

In this tutorial, you learned how to use plugin derivatives to create dynamic menu links based on your site's content. You added a base menu link definition, created a simple plugin class, and wrote a deriver that loads published basic page content and generates one menu link per content item. After rebuilding caches, Drupal automatically discovered and added these links to the Main navigation menu. This pattern allows your menu structure to stay in sync with your content without manually creating links.

## Further your understanding

- Try generating links for a different content type or only for content that meets certain conditions.
- Add a parent value to nest the generated links under another link in the Main menu.

## Additional resources

- [Dynamic menu links in Drupal 8 with plugin derivatives](https://www.webomelette.com/dynamic-menu-links-drupal-8-plugin-derivatives) (webomelette.com)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins) (Drupalize.Me)
- [Plugin Derivatives](https://drupalize.me/tutorial/plugin-derivatives) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add a Local Task Link in a Module](/tutorial/add-local-task-link-module?p=2758)

Clear History

Ask Drupalize.Me AI

close
---
title: "Implement a Block Plugin"
url: "https://drupalize.me/tutorial/implement-block-plugin?p=3241"
guide: "[[drupal-module-developer-guide]]"
---

# Implement a Block Plugin

## Content

Implementing plugins is a common task for Drupal developers. Often, you'll need to add custom functionality using an existing plugin type--most likely an attribute-based plugin. This tutorial offers a structured approach to understanding and creating Drupal plugins, with a focus on attribute-based plugins.

In this tutorial, we'll:

- Examine the custom block code we previously wrote, this time from the perspective of the Plugin API.
- Introduce a method for creating PHP attribute-based Drupal plugins.
- Demonstrate how to find the necessary information for new plugin creation from existing plugins.

By the end of this tutorial, you will know how to examine the structure of existing plugin classes, so that you know how to implement a plugin of that type.

## Goal

Deepen your understanding of plugin implementations by revisiting the "Hello, World!" block created earlier in the guide.

## Prerequisites

- [Create a Custom "Hello, World!" Block](https://drupalize.me/tutorial/create-custom-hello-world-block)
- [Concept: What Are Plugins?](https://drupalize.me/tutorial/concept-what-are-plugins)

A solid grasp of Drupal's Plugin API, PHP design patterns, and other Drupal APIs is beneficial for effectively implementing plugins.

- Familiarity with PHP [class inheritance](https://drupalize.me/tutorial/introduction-inheritance-php) and [interfaces](https://drupalize.me/tutorial/introduction-interfaces).
- Knowledge of [the PSR-4 standard](https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4) within Drupal.
- Understanding of [PHP attributes](https://drupalize.me/tutorial/php-attributes) for most plugin types, and [annotations](https://drupalize.me/tutorial/annotations) for annotation-based plugins.
- Experience with [dependency injection](https://drupalize.me/tutorial/concept-dependency-injection) and [services](https://drupalize.me/tutorial/concept-services-and-container) usage within plugins, which we'll practice using in [Use a Service in a Plugin](https://drupalize.me/tutorial/use-service-plugin).

## Video tutorial

Sprout Video

## Blocks as plugins

The "Hello, World!" block we created in the *anytown* module serves as an introductory example to the Plugin API. Let's revisit its code with our new understanding of plugins.

Attribute-based plugins are common within Drupal. To implement one, you need to know:

- The plugin type to implement.
- The required PHP attribute.
- The correct PSR-4 subdirectory.
- The interface to implement and whether a base class exists for extension.

How do you find these details for implementing a plugin of any type? Find an implementation of the plugin, then use identifying details to search for the code that implements it.

For example: Find a page that displays the ["Hello, World" block on your demo site that we created in a previous tutorial](https://drupalize.me/tutorial/create-custom-hello-world-block). (Pretend that a colleague created it, and you need to find the code that implements it.) In your IDE, search for the rendered text, `Hello, World!`.

Image

![Screenshot of the front page of Anytown Farmer's Market site with the Hello World block placed in the sidebar region.](/sites/default/files/styles/max_800w/public/tutorials/images/hello--block_sidebar.png?itok=tgU_YGis)

In your IDE's search results, you should find the code in *src/Plugin/Block/HelloWorldBlock.php*. Let's take a look:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Plugin\Block;

use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\StringTranslation\TranslatableMarkup;

/**
 * Provides a hello world block.
 */
#[Block(
  id: 'anytown_hello_world',
  admin_label: new TranslatableMarkup('Hello World'),
  category: new TranslatableMarkup('Custom')
)]
class HelloWorldBlock extends BlockBase {

  /**
   * {@inheritdoc}
   */
  public function build(): array {
    $build['content'] = [
      '#markup' => $this->t('Hello, World!'),
    ];
    return $build;
  }

}
```

This code snippet tells us everything we need to know about how to implement a block plugin.

From the `#[Block()]` attribute for the `HelloWorldBlock` class, we know the **plugin type** is *Block*, and the **attribute class** is `\Drupal\Core\Block\Attribute\Block`. The arguments to the constructor on that class tell us what we can enter into our block plugin's **attribute**. Start by copy/pasting the example you found.

The **namespace** is `namespace Drupal\anytown\Plugin\Block;`. If you remove `Drupal\MODULE_NAME`, for example, `Drupal\anytown`, you get the PSR-4 **subdirectory**, `Plugin\Block`. Which means your custom code should live in a *src/Plugin/Block/{CLASS\_NAME}.php* file. You can copy/paste this namespace and replace *anytown* with the machine name of your module.

There's a **base class** we can extend, `Drupal\Core\Block\BlockBase`. That base class implements `\Drupal\Core\Block\BlockPluginInterface`. This is the **interface** for the plugin type that we need to adhere to. All plugin types will implement an interface, and you can look at the interface as a guide for what the plugin *should* do. Most plugin types will have a base class that implements features common to most plugins of that type. When they exist, these base classes can help reduce a lot of boilerplate code. **We recommend that you extend the base class**.

To summarize, the plugin type is *Block*, with a `#[Block()]` attribute, residing in the *src/Plugin/Block/* directory, implementing `\Drupal\Core\Block\BlockPluginInterface`, and extending `Drupal\Core\Block\BlockBase`.

## Recap

This tutorial examined a custom block to find all the information we need to implement another plugin of this type. By analyzing the components of an existing plugin, developers can confidently create their own.

## Further your understanding

- Could you create a new block plugin from scratch based on the block plugin definition?
- Explore a *FieldFormatter* plugin in Drupal core to identify its attribute class, interface, namespace, and base class.

## Additional resources

- [Discover Existing Plugin Types](https://drupalize.me/tutorial/discover-existing-plugin-types) (Drupalize.Me)
- [Implement a Plugin of Any Type](https://drupalize.me/tutorial/implement-plugin-any-type) (Drupalize.Me)
- [PHP Attributes](https://drupalize.me/tutorial/php-attributes) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: What Are Plugins?](/tutorial/concept-what-are-plugins?p=3241)

Next
[Use a Service in a Plugin](/tutorial/use-service-plugin?p=3241)

Clear History

Ask Drupalize.Me AI

close
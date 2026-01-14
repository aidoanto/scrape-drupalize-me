---
title: "Create a Custom \"Hello, World!\" Blockfree"
url: "https://drupalize.me/tutorial/create-custom-hello-world-block?p=3235"
guide: "[[drupal-module-developer-guide]]"
---

# Create a Custom "Hello, World!" Blockfree

## Content

Every introduction to coding starts with a "Hello, World!" example, right? With Drupal, it's a bit more complex than just `echo "Hello, World!"`. To follow Drupal best practices, we should provide content from our custom code in a way that allows a site administrator to choose where and when it's shown, instead of hard-coding those decisions. This keeps our Drupal application flexible and customizable.

In this tutorial, we'll:

- Author a custom block plugin that outputs the string "Hello, World!".
- Place the block on the home page of our site.

By the end of this tutorial, you should have written the code for a custom block that can display the string "Hello, World!".

## Goal

Write some Drupal-specific code and display the text "Hello, World!" on the page with a custom block plugin.

## Prerequisites

- We'll add the "Hello, World!" block to the custom module named *anytown* that we started in [Create an Info File for a Module](https://drupalize.me/tutorial/create-info-file-module-mdg).

## Video tutorial

Sprout Video

As with any "Hello, World!" example, we won't get too much into specifics yet. Instead, we'll focus on achieving an early win and then revisit this example throughout the guide to explain the details and the choices we make.

## Create a custom block plugin

Blocks defined by modules are *plugins*. (More on this later in [Concept: What Are Plugins?](https://drupalize.me/tutorial/concept-what-are-plugins)). That blocks are *plugins* determines the PSR-4 namespace, and the location of our block plugin code.

Block plugins use the `Drupal\MODULE_NAME\Plugin\Block` namespace.

**Tip:** You can generate the scaffolding for a new custom block plugin with `drush generate block`. This will result in a file like the one described below.

### Create the file for custom block code

Let's create a custom "Hello, World!" block, defined by a class named `HelloWorldBlock`.

Create the file *MODULE\_NAME/src/Plugin/Block/HelloWorldBlock.php* in your IDE.

### Write the code

Add the following code to the file *src/Plugin/Block/HelloWorldBlock.php*:

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

Note the following in this code:

- The class name `HelloWorldBlock` matches the file name *HelloWorldBlock.php*, following the PSR-4 standard.
- The class has an `Block` attribute, telling Drupal this code defines a block.
- The custom block code returns its content as a structured *renderable array* instead of a string of HTML.

### Clear the cache and place the block

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache), so Drupal can find our new code.

```
drush cr
```

Place the block in a region to view its output.

1. In the *Manage* administration menu, navigate to *Structure* > *Block layout* (*admin/structure/block*).
2. Select the *Place block* button for the *Sidebar first* region.
3. Find the *Hello World* block, and select *Place block*.
4. Back on the Block layout page, use the cross-hairs to reorder the *Hello World* block to appear first within the *Sidebar first* region.
5. Select the **Save blocks** button at the bottom of the page.

Learn more about placing blocks in [8.3. Placing a Block in a Region](https://drupalize.me/tutorial/user-guide/block-place).

### Verify it worked

After placing the block, return to the home page, and the "Hello World" block should appear in the sidebar.

Image

![Screenshot of the front page of Anytown Farmer's Market site with the Hello World block placed in the sidebar region.](../assets/images/hello--block_sidebar.png)

## Recap

In this tutorial, we created a custom block plugin that outputs "Hello, World!" when placed in a region. This gave you an early "win" in module development and demonstrated how to implement a common Drupal-define pattern and best practice. We'll be revisiting our block plugin throughout the guide, so let's keep going!

## Further your understanding

- Can you modify the block's content to include the current time or additional lines of text?
- Why should you write a custom block plugin instead of just hard-coding "Hello, World!" into the page's content?

## Additional resources

- [Drupal User Guide Chapter 8. Blocks](https://drupalize.me/series/user-guide/blocks-chapter) (Drupalize.Me)
- [Concept: What Are Plugins?](https://drupalize.me/tutorial/concept-what-are-plugins) (Drupalize.Me)
- See also the [block\_example in the Examples for Developers project](https://git.drupalcode.org/project/examples/-/tree/4.0.x/modules/block_example?ref_type=heads) (git.drupalcode.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create an Info File for a Module](/tutorial/create-info-file-module-mdg?p=3235)

Clear History

Ask Drupalize.Me AI

close
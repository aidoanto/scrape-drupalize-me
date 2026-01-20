---
title: "Using Entity Bundle Classes for Site-Specific Features"
url: "https://drupalize.me/tutorial/using-entity-bundle-classes-site-specific-features?p=2607"
guide: "[[work-data-modules]]"
order: 10
---

# Using Entity Bundle Classes for Site-Specific Features

## Content

Bundle classes are a feature of the [Drupal Entity API](https://drupalize.me/tutorial/entity-api-overview) that let you attach PHP classes to individual bundles (for example, content types) so you can keep site-specific business logic close to the data it acts on. Bundle classes are a powerful way to encapsulate site-specific business logic and bridge user-configured fields and PHP logic based on those fields. In this tutorial, you will build a reusable bundle base class that adds a generic share behavior for all node types on a site and then extend it for a specific node type.

In this tutorial, we will:

- Explore a real-world problem that bundle classes can help you solve.
- Create a bundle base class for common share features shared across multiple node types.
- Implement a node-type-specific class that extends the base class with behavior tailored to the underlying content type.

By the end of this tutorial, you'll be able to use bundle classes to encapsulate per-bundle logic, assume the presence of UI-configured fields when appropriate, and register those classes so Drupal uses them at runtime.

## Goal

Build a reusable `ShareableNodeBase` bundle class that encapsulates social share behavior for multiple node types, plus an `ArticleNode` class that extends it. Register both via bundle class hooks so Drupal automatically uses the correct class per node type.

## Prerequisites

- [Entity API overview](https://drupalize.me/tutorial/entity-api-overview)

To follow along with the example use case in this tutorial, your site needs at least an *Article* content type with the following fields configured via the UI:

- *field\_share\_image* (Media—Image) on any bundle that should support sharing.
- *field\_share\_summary* (Text—plain) (optional).

## Entity classes

In [Create a custom content entity](https://drupalize.me/tutorial/create-custom-content-entity), you learned that entity types are declared via custom classes with a `#[ContentEntityType]` attribute. When you work with any single entity, the API initializes and returns an instance of that entity type’s specific class.

For example:

```
$node = \Drupal::entityTypeManager()->getStorage('node')->load(1);
$user = \Drupal::entityTypeManager()->getStorage('user')->load(1);

// get_class($node) === 'Drupal\node\Entity\Node'
// get_class($user) === 'Drupal\user\Entity\User'
```

All nodes, regardless of their bundle (for example, *article*, *page*, *blog*), are instances of the same `\Drupal\node\Entity\Node` class by default. Bundle classes allow you to associate custom classes on a per-bundle basis that extend the core `Node` class with additional functionality.

For example:

```
// Load a generic node.
$node = \Drupal::entityTypeManager()->getStorage('node')->load(1);

// Suppose node 1 is an Article. Because of bundle class registration,
// this will return an instance of our ArticleNode class.
get_class($node); // "Drupal\mymodule\Entity\Node\ArticleNode"

// You can now call bundle-specific methods:
$node->getShareTitle();  // Provided by ShareableNodeBase or ArticleNode.
$node->buildShareMeta(); // Generates meta tags for this bundle.
```

Without bundle classes, every loaded node would simply be an instance of `Drupal\node\Entity\Node`. You would have to use conditionals to handle bundle-specific logic manually.

Next, you will look at how this feature solves a realistic problem.

## The problem: scattered share logic across content types

Imagine you need to provide consistent social sharing (Open Graph tags, share URLs, share images) for several content types—*Article*, *Event*, and *News*. The output needs to adhere to the same structure (for example, JSON-LD) for all content. However, not all content types have the same fields or rules for how the sharing data is calculated. Historically, you might:

- Put logic in services with `if ($node->bundle() === 'article') { ... }`.
- Sprinkle some code into a theme’s preprocess functions.
- Add field assumptions to the global node class (which is brittle for bundles that do not have those fields).

This spreads business rules around your codebase, makes testing harder, and encourages lots of bundle-specific `if/else` blocks.

With bundle classes, each bundle can use a subclass of the entity type’s base class that adds new features. For nodes:

- Core uses `\Drupal\node\Entity\Node` by default.
- You can register a different class for the *article* bundle, another for *event*, and so on.
- These bundle classes extend the base class, so they remain real nodes with all core behavior plus your bundle-specific methods.

For this specific use case, you will build a small, site-specific content architecture layer on top of Drupal’s Entity API using bundle classes.

You will define:

- A reusable base bundle class that extends Drupal’s core `Node` entity class.
- A bundle-specific subclass—for example, an `ArticleNode` class that extends the base class just for the article bundle.
- A registration hook that tells Drupal which bundle uses which class so any loaded Article node automatically becomes an instance of `ArticleNode`.

This architecture cleanly separates shared, site-wide behavior from bundle-specific differences. It also keeps the core entity class generic while allowing bundle classes to assume the existence of fields configured through the UI—something global classes cannot safely do.

### Start with a site-specific bundle base class

Because your requirements specify that you want to add some new methods to multiple bundles, start with a base class that implements a generic version of the functionality. This approach works especially well if you have common fields used throughout most content types, with a few outliers.

You will create an abstract class, `ShareableNodeBase`, that:

- Extends `\Drupal\node\Entity\Node`.
- Encapsulates share behaviors (`getShareTitle()`, `getShareImageFile()`, `getShareUrl()`, `buildShareMeta()`).
- Assumes the existence of site-specific fields like *field\_share\_image* and *field\_share\_summary* (this is safe because you will only attach this class to bundles that actually have those fields).

This is a site-specific layer: unlike the core-provided `Node` entity base class, it intentionally knows about fields configured via the UI.

Add the file *src/Entity/Node/ShareableNodeBase.php* with the following content:

```
<?php

namespace Drupal\mymodule\Entity\Node;

use Drupal\Component\Serialization\Json;
use Drupal\Core\Cache\CacheableMetadata;
use Drupal\Core\Url;
use Drupal\file\Entity\File;
use Drupal\media\MediaInterface;
use Drupal\node\Entity\Node;

/**
 * Abstract base for share-enabled node bundles.
 *
 * Assumes the presence of site-configured fields:
 * - field_share_image (Media—Image)
 * - field_share_summary (Text—plain)
 */
abstract class ShareableNodeBase extends Node {

  /**
   * Returns a title suitable for sharing.
   */
  public function getShareTitle(): string {
    // Prefer an explicit share summary, fall back to the node title.
    $summary = $this->get('field_share_summary')->value ?? '';
    return $summary !== '' ? $summary : $this->label();
  }

  /**
   * Returns the share image file entity if present.
   */
  public function getShareImageFile(): ?File {
    if (!$this->hasField('field_share_image') || $this->get('field_share_image')->isEmpty()) {
      return NULL;
    }

    /** @var \Drupal\media\MediaInterface $media */
    $media = $this->get('field_share_image')->entity;
    if ($media instanceof MediaInterface && $media->hasField('field_media_image') && !$media->get('field_media_image')->isEmpty()) {
      return $media->get('field_media_image')->entity;
    }

    return NULL;
  }

  /**
   * Returns the canonical URL for sharing.
   */
  public function getShareUrl(): Url {
    return $this->toUrl('canonical', ['absolute' => TRUE]);
  }

  /**
   * Builds a JSON-LD script tag with share metadata.
   *
   * @return array
   *   Render array of a JSON-LD <script> tag.
   */
  public function buildShareMeta(): array {
    $image = $this->getShareImageFile();

    $data = [
      '@context' => 'https://schema.org',
      '@type' => 'WebPage',
      'headline' => $this->getShareTitle(),
      'url' => $this->getShareUrl()->toString(),
    ];

    if ($image) {
      $data['image'] = file_create_url($image->getFileUri());
    }

    $build = [
      '#type' => 'html_tag',
      '#tag' => 'script',
      '#attributes' => [
        'type' => 'application/ld+json',
      ],
      '#value' => Json::encode($data, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE),
    ];

    // Collect and apply cacheability in one place.
    $cache = CacheableMetadata::createFromObject($this);
    if ($image) {
      $cache->addCacheableDependency($image);
    }
    $cache->applyTo($build);

    return $build;
  }

}
```

This class:

- Inherits everything from `Node` but adds share-specific helper methods that any bundle can reuse.
- Builds a small render array for JSON-LD metadata that you can attach in a preprocess function or a controller.
- Assumes that the fields it references already exist, added via the Field UI. Normally, you do not want to assume the existence of a field because it is subject to site-specific configuration. Here, you ensure that this base class is only associated with node types that you know have these fields, so the assumption is safe.
- Is intentionally `abstract`. Each bundle extends it, and you can override specifics where needed. You can adjust the class definition depending on your use case.

### Add a node-type-specific class that extends the base

Next, create a concrete `ArticleNode` class to fine-tune behavior. For example, you might override the `getShareTitle()` method so that it appends `| Last Update: {DATE}` to the title of every *Article*, and customize the share URL with tracking parameters.

Add the file *src/Entity/Node/ArticleNode.php* with the following content:

```
<?php

namespace Drupal\mymodule\Entity\Node;

use Drupal\Core\Url;

/**
 * Article bundle class with share behavior.
 */
final class ArticleNode extends ShareableNodeBase {

  /**
   * Customize share title for Articles to append last update date.
   */
  public function getShareTitle(): string {
    // Use parent share title and append last update date.
    $parent = parent::getShareTitle();
    return $parent . ' | Last Update: ' . date('Y-m-d');
  }

  /**
   * Customize share URL for Articles to add tracking parameters.
   */
  public function getShareUrl(): Url {
    $url = parent::getShareUrl();
    $options = $url->getOptions();
    $options['query']['utm_source'] = 'share';
    $options['query']['utm_content'] = 'article';
    $url->setOptions($options);
    return $url;
  }

}
```

This class:

- Extends `ShareableNodeBase` and inherits the helper methods it provides.
- Overrides `getShareTitle()` to append the last update date (in `Y-m-d` format) to the share title for every article.
- Overrides `getShareUrl()` to add tracking parameters.

### Register bundle classes for specific bundles

You must tell Drupal which class to use for each bundle. When you are working with bundles defined via configuration (such as content types created in the UI), the recommended pattern is to alter bundle information with `hook_entity_bundle_info_alter()`.

Add the following implementation to *mymodule.module*:

```
<?php

use Drupal\mymodule\Entity\Node\ArticleNode;

/**
 * Implements hook_entity_bundle_info_alter().
 */
function mymodule_entity_bundle_info_alter(array &$bundles): void {
  // Register ArticleNode as the bundle class for the 'article' node type.
  if (isset($bundles['node']['article'])) {
    // Tell Drupal to use the ArticleNode class for nodes of bundle 'article'.
    $bundles['node']['article']['class'] = ArticleNode::class;
  }

  // You can register additional bundle classes in the same way:
  // if (isset($bundles['node']['event'])) {
  //   $bundles['node']['event']['class'] = \Drupal\mymodule\Entity\Node\EventNode::class;
  // }
}
```

This hook:

- Receives the existing `$bundles` information for all entity types.
- Checks that the *article* node bundle exists.
- Sets the `class` key so Drupal instantiates `ArticleNode` whenever it loads a node of bundle *article*.

If you are defining your own bundles programmatically, you can also use `hook_entity_bundle_info()` to declare the bundle and its class in one place. For bundles defined through configuration (such as standard node types), use the alter hook pattern shown here.

**Notes about registering bundle classes:**

- Each bundle class must be a subclass (directly or indirectly) of the entity type’s base class (`\Drupal\node\Entity\Node` for nodes).
- Classes are per bundle, not per entity instance.
- Use `hook_entity_bundle_info_alter()` if another module (for example, Node module, Paragraphs, or a custom module) defines the bundle and you want to add or swap the class.
- After changing bundle class registrations, run `drush cr` to rebuild the discovery and routing caches.

### Use the logic: add meta tags in a preprocess

Once bundle classes are registered, loaded nodes of bundle *article* will be instances of `ArticleNode`. Anywhere you have a node object for that bundle, you can call the new methods that your bundle class provides.

To attach the JSON-LD script generated by `buildShareMeta()` to the `<head>` of your pages, you can use `hook_preprocess_html()` and the `html_head` attachment.

1. Add a preprocess function in *mymodule.module* to attach the meta tags.
2. Call `buildShareMeta()` on the node object and attach the resulting render array via `#attached['html_head']`.

```
<?php

use Drupal\node\NodeInterface;

/**
 * Implements hook_preprocess_html().
 */
function mymodule_preprocess_html(array &$variables): void {
  $route_match = \Drupal::routeMatch();
  $node = $route_match->getParameter('node');

  if ($node instanceof NodeInterface && method_exists($node, 'buildShareMeta')) {
    // Build the JSON-LD script tag render array.
    $element = $node->buildShareMeta();

    // Attach it to the HTML head.
    $variables['#attached']['html_head'][] = [
      $element,
      'mymodule_share_meta',
    ];
  }
}
```

This code:

- Retrieves the current route’s `node` parameter.
- Checks that the parameter is a `NodeInterface` and that it has a `buildShareMeta()` method. This allows you to fail gracefully for bundles that do not extend `ShareableNodeBase`.
- Attaches your render array to `#attached['html_head']` so Drupal renders the JSON-LD `<script>` tag in the `<head>` of the HTML document.

## Why bundle classes are great for site-specific logic

Core entity classes must remain generic. A global `Node` class cannot assume the presence of `field_share_image` because not all bundles have it. Bundle classes can assume those fields exist because you only assign them to bundles that have them.

Using bundle classes gives you several practical advantages. You keep business logic close to the data model for each bundle, reduce scattered conditionals across services, controllers, and preprocess functions, and make it easier to write tests that load real content entities and assert on strongly typed methods such as `getShareTitle()` or `buildShareMeta()`.

**Practical tips**

- **Fail safely:** Even in site-specific code, always check `hasField()` and `isEmpty()` before you access field values.
- **Codify your UI:** If a bundle needs a field, export configuration and commit it to your repository. Your bundle class then reflects that contract.
- **Prefer methods over conditionals:** Move logic like “What is the share title?” into the bundle class rather than into `if ($node->bundle() === 'article')` blocks scattered throughout your code.

## Recap

In this tutorial, you saw how bundle classes let you attach site-specific behavior to individual bundles while keeping core entity classes generic. You created a `ShareableNodeBase` class that encapsulates reusable share behavior based on UI-configured fields and implemented an `ArticleNode` bundle class that extends the base with article-specific behavior. Finally, you registered the bundle class using `hook_entity_bundle_info_alter()` so Drupal automatically uses the correct class for each node type and used `buildShareMeta()` in a preprocess function to attach JSON-LD metadata to the HTML head.

## Further your understanding

- Add an `EventNode` class that overrides `getShareUrl()` to point to a calendar view or event listing.
- Add a `preSave()` override in `ShareableNodeBase` to auto-populate `field_share_summary` when it is empty, based on other fields.
- Write Kernel tests that load entities of each bundle and assert on the output of `getShareTitle()` and `buildShareMeta()`.
- Extend the JSON-LD payload to use more specific schema types such as `Article` or `Event`, and override `buildShareMeta()` per bundle where needed.

## Additional resources

- [Introducing bundle classes](https://www.drupal.org/node/3191609) (drupal.org)
- [Drupal’s bundle classes empower better code](https://www.lullabot.com/articles/drupals-bundle-classes-empower-better-code) (lullabot.com)
- [Dedicated entity bundle classes in Drupal 9.3](https://www.webomelette.com/dedicated-entity-bundle-classes-drupal-9) (webomelette.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Modify Existing Entities with Alter Hooks](/tutorial/modify-existing-entities-alter-hooks?p=2607)

Next
[Entity Validation API](/tutorial/entity-validation-api?p=2607)

Clear History

Ask Drupalize.Me AI

close
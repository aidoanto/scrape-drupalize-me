---
title: "Use a Component in a Module via Render Arrays"
url: "https://drupalize.me/tutorial/use-component-module-render-arrays?p=3329"
guide: "[[frontend-theming]]"
order: 58
---

# Use a Component in a Module via Render Arrays

## Content

As a module developer, you output themed content from your module in the form of [renderable arrays](https://drupalize.me/tutorial/render-api-overview). When doing so, you can make use of *single directory components* (SDCs) by using the `#type => 'component'` render element type. This allows modules to dynamically select and configure a component based on configuration or specific PHP logic. You'll use this as the return value of a controller, or a configurable plugin related to display building, like custom blocks or field formatters. As an example, we'll author a custom block plugin that loads a specific node and outputs it using the *card* SDC we [defined in a previous tutorial](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc). We'll build a render array that supplies the values for the component's props and slots, and add some caching logic to the output.

In this tutorial, we will:

- Build a render array that targets an SDC via the `#component` property.
- Pass data into the component's **props** and **slots**, and demonstrate optional `#propsAlter` and `#slotsAlter` callbacks.
- Validate the output and cache it properly.

By the end of this tutorial, you'll be able to render any SDC via a module's PHP code using a well-structured and cache-friendly render array.

## Goal

Use a render array to output a *card* component as the content of a custom block plugin.

## Prerequisites

- Familiar with the [Render API](https://drupalize.me/tutorial/render-api-overview)
- Know how to [Implement a Block Plugin](https://drupalize.me/tutorial/implement-block-plugin)
- A *card* component living in a module or theme with [the schema shown earlier](https://drupalize.me/tutorial/add-component-yaml-file-drupal-sdc).
- A custom module. In this tutorial, we'll name the module, `card_block`.

## Create a render array with a `#component` element

Render element types are plugins, and the `#component` type is provided by `\Drupal\Core\Render\Element\ComponentElement`.

We're going to create a custom block plugin, and then use it to render a node via the *card* component. You can use components provided by a theme, another module, or your module can provide its own components. If you rely on a component provided by another module, add that as a dependency to your [module's *.info.yml* file](https://drupalize.me/tutorial/overview-info-files-drupal-modules).

### Scaffold a block plugin with Drush

Start by using Drush to generate a new block plugin in a custom module named `card_block`. (Drush will scaffold the custom module if it doesn't already exist.)

```
drush generate plugin:block
```

- Module machine name: **`card_block`**
- Block admin label: **`Card block`**
- Plugin ID: **`card_block_block`**
- Plugin class: **`CardBlock`**
- Block category: **Custom**
- Make the block configurable: **No**
- Inject dependencies? **Yes**
  - Service name: **`entity_type.manager`**
- Access callback? **No**

### Inspect the component schema

Inspect the schema for the component you plan to use (see *card.component.yml*), look for:

- **Required props**: `heading`, `url`, and their data types.
- **Optional props**: `card_links`, `show_flip_button`, `count`, `metadata`, and their expected data types.
- **Slots**: `content` and `body`.

You'll use those exact keys in your render array when passing props and slots to the component. Anything else will fail schema validation.

### Load a node to display

In your block plugin use dependency injection to get the `entity_type.manager` service, and then use that to load a node. In this example, the ID of the node to load is hard coded, but you could make this configurable in your block. Learn more in [Use a Service in a Plugin](https://drupalize.me/tutorial/use-service-plugin).

Example of loading a node via `entity_type.manager` service:

```
$node = $this->entityTypeManager->getStorage('node')->load(24);
```

### Render the node using the `card` SDC

Next, we'll define a render array that uses a `#type => 'component` element to display the node.

To render a Drupal SDC via a render array, you need to know a couple of things:

- The SDC provider and component name, e.g. `{provider}:{component} => my_module:card`.
- The names of any slots.
- The names, and data types, of any props.

Assuming a custom module named `card_block`, this `Block` plugin code lives in *modules/custom/card\_block/src/Plugin/Block/CardBlock.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\card_block\Plugin\Block;

use Drupal\Component\Utility\Unicode;
use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\Cache\Cache;
use Drupal\Core\Datetime\DateFormatterInterface;
use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Drupal\Core\Session\AccountProxyInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Symfony\Component\DependencyInjection\ContainerInterface;

#[Block(
  id: 'card_block_block',
  admin_label: new TranslatableMarkup('Card block'),
  category: new TranslatableMarkup('Custom'),
)]
final class CardBlock extends BlockBase implements ContainerFactoryPluginInterface {

  public function __construct(
    array $configuration,
    $plugin_id,
    $plugin_definition,
    private readonly EntityTypeManagerInterface $entityTypeManager,
    private readonly DateFormatterInterface $dateFormatter,
    private readonly AccountProxyInterface $currentUser,
  ) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
  }

  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition): self {
    return new self(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('entity_type.manager'),
      $container->get('date.formatter'),
      $container->get('current_user'),
    );
  }

  public function build(): array {
    $node = $this->entityTypeManager->getStorage('node')->load(5);
    if (!$node) {
      return ['#markup' => $this->t('No node found.')];
    }

    $raw = (string) ($node->body->summary ?? $node->body->value ?? '');
    $excerpt = Unicode::truncate($raw, 200, TRUE, TRUE) . ' …';

    $build['featured_card'] = [
      '#type' => 'component',
      '#component' => 'neo_brutalism:card',
      '#props' => [
        'heading' => $node->label(),
        'url' => $node->toUrl()->toString(),
        'metadata' => [
          'author' => $node->getOwner()->getDisplayName(),
          // RFC 3339 full-date: YYYY-MM-DD
          'date' => $this->dateFormatter->format($node->getCreatedTime(), 'custom', 'Y-m-d'),
        ],
      ],
      '#slots' => [
        'content' => ['#markup' => $excerpt],
      ],
      '#propsAlter' => [
        function (array $props): array {
          if ($this->currentUser->isAnonymous()) {
            $props['url'] .= (str_contains($props['url'], '?') ? '&' : '?') . 'utm_source=anon';
          }
          return $props;
        },
      ],
      '#cache' => [
        'tags' => Cache::mergeTags($node->getCacheTags(), ['component:card']),
        'contexts' => ['url', 'user.roles:anonymous', 'timezone'],
      ],
    ];

    return $build;
  }

}
```

**Note**: In `getStorage('node')->load(5);` We are hard-coding retrieving a node by its ID. Change the `5` to an ID that exists on your site.

The code above adds a `#type => 'component'` element to the render array for the block, and tells it to use the `neo_brutalism:card` component (`neo_brutalism` is the machine name of the theme that contains this `card` SDC). It maps `#props` and `#slots` values by creating associative arrays where the key is the prop or slot name taken from the component's schema. This also demonstrates the use of a `#propsAlter` callback property. And while not specific to the use of an SDC it's always a good idea to specify a `#cache` property when rendering dynamic content.

For more information about creating render arrays, and how callbacks work, see:

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)
- [Render API Callback Properties](https://drupalize.me/tutorial/render-api-callback-properties)

### Add a dependency on the component provider

If you're going to hard-code the value of `#component`, update your module's *info.yml* file to add a dependency on the module that provides the component. Failing to do so could result in your module being installed without the required component available, causing an error.

Since you can't list a theme under the dependencies key in a module's *info.yml* file, the most reliable approach is to move the component to a module, which can then be declared as a proper dependency.

If your module must use a component from an enabled theme, document that requirement clearly and consider adding a runtime check to enforce the dependency.

### Enable the module and place the block on the page

To test that it is working, enable the module, and place the custom block into a visible region and confirm it displays the node using the card component.

When viewing any page with the new block enabled, you should see the relevant node displayed using the card component. You can test the effects of the `#propsAlter` logic by viewing the page both logged in, and as an anonymous user.

Image

![The Card block using the card SDC](../assets/images/use-sdc-render-array--card-block.png)

## Recap

In this tutorial, we learned that the `ComponentElement` render element (`#type => 'component'`) connects PHP render arrays to Drupal single directory components. We learned how to use `#component` to choose which component to render, and `#props`, and `#slots` to feed data into the component while respecting its schema. We also learned that `#propsAlter` and `#slotsAlter` callbacks let you adjust data at runtime, and why it's important to add meaningful `#cache` metadata reflecting your dynamic inputs. You should now be able to author render arrays in a module that displays content using an SDC.

## Further your understanding

- Can you think of a scenario where a module would want to provide an SDC, and then use it?

## Additional resources

- [Render API Overview](https://drupalize.me/tutorial/render-api-overview) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add CSS and JavaScript to a Drupal SDC](/tutorial/add-css-and-javascript-drupal-sdc?p=3329)

Next
[Use a Component in a Twig Template](/tutorial/use-component-twig-template?p=3329)

Clear History

Ask Drupalize.Me AI

close
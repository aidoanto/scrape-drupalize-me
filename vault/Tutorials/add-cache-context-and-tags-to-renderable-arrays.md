---
title: "Add Cache Context and Tags to Renderable Arrays"
url: "https://drupalize.me/tutorial/add-cache-context-and-tags-renderable-arrays?p=3244"
guide: "[[drupal-module-developer-guide]]"
---

# Add Cache Context and Tags to Renderable Arrays

## Content

Whenever your custom code outputs a render array, you need to use the `#cache` property to define the cacheability of the content. This includes providing information about any related context that informs Drupal about how the content varies, and tags that help Drupal know what circumstances might require the cached data to be invalidated. We can add `#cache` properties to the render arrays output by both the custom block, and the weather page controller, to ensure they are properly cached.

In this tutorial, we'll:

- Learn how to use the `#cache` property of a render array to provide cacheability data to Drupal.
- Provide context about the data that's being displayed.
- Tell Drupal about any dependencies of the content.

By the end of this tutorial you should be able to use the `#cache` property to define the cacheability of the content contained in a render array.

## Goal

Update the render arrays in the custom block and weather page controller with `#cache` data.

## Prerequisites

- [Concept: Caching](https://drupalize.me/tutorial/concept-caching)
- [Concept: Render API](https://drupalize.me/tutorial/concept-render-api)
- [Use a Service in a Plugin](https://drupalize.me/tutorial/use-service-plugin)

## Video tutorial

Sprout Video

## The `#cache` property

The `#cache` Render API property is used to define the cache context, tags, and max-age of an element and its children. This information is used by the renderer to determine a strategy for caching the rendered output of branches of the render tree. It's bubbled up to the page level as part of determining appropriate HTTP cache headers for the response.

There are a few places in our modules where we output render arrays that need cache information added:

- The `HelloWorldBlock` plugin outputs the string `Hello, @name!` for logged-in users, and `Hello world!` for anonymous users. This means the block's content depends on whether the user is logged in or not, and on the specific user.
- The `WeatherPage` controller returns a render array with a list of closures. We need to tell Drupal that it's okay to cache this content as long as it invalidates when an admin updates the configuration.
- The `Attending` controller builds a list of vendors, and if any of those vendor entities are edited, the page should be invalidated.

### Update the `HelloWorldBlock` plugin

Edit the file *src/Plugins/Block/HelloWorldBlock.php* and add the `#cache` property if it's not there already:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Plugin\Block;

use Drupal\Core\Block\Attribute\Block;
use Drupal\Core\Block\BlockBase;
use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Drupal\Core\Session\AccountProxyInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Provides a hello world block.
 */
#[Block(
  id: 'anytown_hello_world',
  admin_label: new TranslatableMarkup('Hello World'),
  category: new TranslatableMarkup('Custom')
)]
class HelloWorldBlock extends BlockBase implements ContainerFactoryPluginInterface {

  /**
   * The current user.
   *
   * @var \Drupal\Core\Session\AccountProxyInterface
   */
  private $currentUser;

  /**
   * The entity type manager service.
   *
   * @var \Drupal\Core\Entity\EntityTypeManagerInterface
   */
  private $entityTypeManager;

  /**
   * Construct a HelloWorldBlock.
   *
   * @param array $configuration
   *   A configuration array containing information about the plugin instance.
   * @param string $plugin_id
   *   The plugin_id for the plugin instance.
   * @param mixed $plugin_definition
   *   The plugin implementation definition.
   * @param \Drupal\Core\Session\AccountProxyInterface $current_user
   *   The current user service.
   * @param \Drupal\Core\Entity\EntityTypeManagerInterface $entity_type_manager
   *   The entity type manager service.
   */
  public function __construct(array $configuration, $plugin_id, $plugin_definition, AccountProxyInterface $current_user, EntityTypeManagerInterface $entity_type_manager) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
    $this->currentUser = $current_user;
    $this->entityTypeManager = $entity_type_manager;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition) {
    return new static(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('current_user'),
      $container->get('entity_type.manager')
    );
  }

  /**
   * {@inheritdoc}
   */
  public function build(): array {
    if ($this->currentUser->isAuthenticated()) {
      $build['content'] = [
        '#markup' => $this->t('Hello, @name! Welcome back.', ['@name' => $this->currentUser->getDisplayName()]),
      ];
    }
    else {
      $build['content'] = [
        '#markup' => $this->t('Hello world!'),
      ];
    }

    $build['content']['#cache'] = [
      // We're creating markup that depends on the current user. So we need
      // to tell Drupal to use the 'user' cache context. This will ensure that
      // the block content will vary per-user. Additionally, since we're adding
      // the user's name to the markup we add a cache tag for the current user.
      // This will ensure that if the user edits their account and changes their
      // name that the block will be updated.
      'contexts' => ['user'],
      'tags' => $this->entityTypeManager->getStorage('user')->load($this->currentUser->id())->getCacheTags(),
    ];

    return $build;
  }

}
```

Because the block content includes the name of the user (if you're logged in), we need to tell Drupal that it varies per-user. That is, you can cache this, but the cached version only applies to the specific user. In the `#cache` property, that's why we set the `context` to `['user']`.

Learn about available contexts, and how to define new ones, in the [Cache contexts | Cache API](https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts) documentation.

We can also use the `tags` key to tell Drupal what specific user object was used to create the content. If that user object gets edited, Drupal will know to invalidate the cached content and re-create it with the potentially new username. In most cases, the data you'll be using in the render array will come from an entity, and entity objects all have a `getCacheTags()` helper method that will return the cache tags for that specific entity. We use this to populate the `#cache` property.

Learn more about possible values for cache tags in the [Cache tags | Cache API](https://www.drupal.org/docs/drupal-apis/cache-api/cache-tags) documentation.

### Update the `WeatherPage` controller

Edit the file *src/Controller/WeatherPage.php* to add `#cache` metadata:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Controller;

use Drupal\anytown\ForecastClientInterface;
use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Controller for anytown.weather_page route.
 */
class WeatherPage extends ControllerBase {

  /**
   * Forecast API client.
   *
   * @var \Drupal\anytown\ForecastClientInterface
   */
  private $forecastClient;

  /**
   * WeatherPage controller constructor.
   *
   * @param \Drupal\anytown\ForecastClientInterface $forecast_client
   *   Forecast API client service.
   */
  public function __construct(ForecastClientInterface $forecast_client) {
    $this->forecastClient = $forecast_client;
  }

  /**
   * {@inheritDoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('anytown.forecast_client')
    );
  }

  /**
   * Builds the response.
   */
  public function build(string $style): array {
    // Style should be one of 'short', or 'extended'. And default to 'short'.
    $style = (in_array($style, ['short', 'extended'])) ? $style : 'short';

    $settings = $this->config('anytown.settings');

    // This is hypothetical, but shows how you could use the location setting
    // in constructing the API query.
    $url = 'https://module-developer-guide-demo-site.ddev.site/modules/custom/anytown/data/weather_forecast.json';
    if ($location = $settings->get('location')) {
      $url .= '?location=' . $location;
    }

    $forecast_data = $this->forecastClient->getForecastData($url);

    $table_rows = [];
    $highest = 0;
    $lowest = 0;
    if ($forecast_data) {
      // Create a table of the weather forecast as a render array. First loop
      // over the forecast data and create rows for the table.
      foreach ($forecast_data as $item) {
        [
          'weekday' => $weekday,
          'description' => $description,
          'high' => $high,
          'low' => $low,
          'icon' => $icon,
        ] = $item;

        // Create one table row for each day in the forecast.
        $table_rows[] = [
          // Simple text for a cell can be added directly to the array.
          $weekday,
          // Complex data for a cell, like HTML, can be represented as a nested
          // render array.
          [
            'data' => [
              '#markup' => '<img alt="' . $description . '" src="' . $icon . '" width="200" height="200" />',
            ],
          ],
          [
            'data' => [
              '#markup' => $this->t('%description with a high of @high and a low of @low', [
                '%description' => $description,
                '@high' => $high,
                '@low' => $low,
              ]),
            ],
          ],
        ];

        $highest = max($highest, $high);
        $lowest = min($lowest, $low);
      }

      // Extended forecast as a table.
      $weather_forecast = [
        '#type' => 'table',
        '#header' => [
          'Day',
          '',
          'Forecast',
        ],
        '#rows' => $table_rows,
        '#attributes' => [
          'class' => ['weather_page--forecast-table'],
        ],
      ];

      // Summary forecast.
      $short_forecast = [
        '#type' => 'markup',
        '#markup' => '<p>' . $this->t('The high for the weekend is @highest and the low is @lowest.', [
          '@highest' => $highest,
          '@lowest' => $lowest,
        ]) . '</p>',
      ];

    }
    else {
      // Or, display a message if we can't get the current forecast.
      $weather_forecast = ['#markup' => '<p>' . $this->t('Could not get the weather forecast. Dress for anything.') . '</p>'];
      $short_forecast = NULL;
    }

    $build = [
      // Which theme hook to use for this content. See anytown_theme().
      '#theme' => 'weather_page',
      '#attached' => [
        'library' => ['anytown/forecast'],
      ],
      // When passing a render array to Twig template file any top level array
      // element that starts with a '#' will be a variable in the template file.
      // Example: {{ weather_intro }}.
      '#weather_intro' => [
        '#markup' => "<p>" . $this->t("Check out this weekend's weather forecast and come prepared. The market is mostly outside, and takes place rain or shine") . "</p>",
      ],
      '#weather_forecast' => $weather_forecast,
      '#short_forecast' => $short_forecast,
      '#weather_closures' => [
        '#theme' => 'item_list',
        '#title' => 'Weather related closures',
        '#items' => explode(PHP_EOL, $settings->get('weather_closures')),
      ],
      '#cache' => [
        // This content will vary if the settings for the module change, so we
        // specify that here using cache tags.
        //
        // This will end up looking like 'config:anytown.settings' but when
        // available it's better to use the getCacheTags() method to retrieve
        // tags rather than hard-code them.
        'tags' => $settings->getCacheTags(),
        // Remember, this page can be accessed via multiple URLs, like /weather
        // and /weather/extended. And varies depending on the URL, so we also
        // need to add a cache context for the URL so that the content is cached
        // per-url.
        'contexts' => ['url'],
      ],
    ];

    return $build;
  }

}
```

This updated code sets the `#cache['tags']` value. This tells Drupal that the content of the */weather* page depends on the settings for the page. The settings are set by the configuration form created in [Create a Settings Form For the Anytown Module](https://drupalize.me/tutorial/create-settings-form-anytown-module). The controller now uses the `#cache['contexts']` property to vary the content based on the URL, because the controller's logic outputs different content for */weather* versus */weather/extended*.

### Update the `Attending` controller

Edit the *src/Controller/Attending.php* file and add `#cache` metadata:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Controller;

use Drupal\Core\Controller\ControllerBase;

class Attending extends ControllerBase {

  /**
   * Callback to display list of vendors attending this week.
   *
   * @return array
   *   List of vendors attending this week.
   */
  public function build(): array {
    // Build a query to get vendor IDs.
    $query = $this->entityTypeManager()->getStorage('node')->getQuery()
      // Only vendors this user has the permission to view.
      ->accessCheck()
      // Only published entities.
      ->condition('type', 'vendor')
      ->condition('field_vendor_attending', TRUE);

    $node_ids = $query->execute();
    if (count($node_ids) > 0) {
      // Load the actual vendor node entities.
      $nodes = $this->entityTypeManager()
        ->getStorage('node')
        ->loadMultiple($node_ids);

      $view_builder = $this->entityTypeManager()->getViewBuilder('node');

      // We're going to display each vendor twice. Once in an unordered list
      // that we'll use for a summary at the top of the page. And then again
      // using the configured 'teaser' view mode below that list. This allows us
      // to demonstrate both rendering individual fields and complete entities.
      $vendor_list = [];
      $vendor_teasers = [];

      foreach ($nodes as $vendor) {
        // For the summary list we want their name, which is the label field.
        $vendor_list[$vendor->id()] = [];
        $vendor_list[$vendor->id()]['name'] = [
          '#markup' => $vendor->label(),
        ];
        // And, the email address from the field_vendor_contact_email field
        // rendered using the configured formatter for the 'default' view mode.
        // But we're also going to explicitly hide the field label regardless of
        // what's configured for the view mode.
        // See \Drupal\Core\Field\FieldItemListInterface::view().
        // Calling view() on the field is a wrapper for using the viewBuilder
        // like so
        // $view_builder->viewField($vendor->field_vendor_contact_email);
        // The most common options here are likely 'label', and 'type' which
        // should be the ID of a field formatter plugin to use. If not type is
        // specified the field types `default_formatter` is used.
        $vendor_list[$vendor->id()]['contact'] = $vendor->get('field_vendor_contact_email')
          ->view(['label' => 'hidden']);

        // Add cache tags for the vendor to the render array so that if the
        // vendor node gets edited this content gets invalidated.
        $vendor_list[$vendor->id()]['#cache'] = [
          'tags' => $vendor->getCacheTags(),
        ];

        // Then, we also want to render the entire node, using the 'teaser'
        // view mode. This will return the render array for displaying the node
        // content.
        $vendor_teasers[$vendor->id()] = $view_builder->view($vendor, 'teaser');
      }

      // Alternatively, we could render teasers for all vendors at once using
      // $vendor_teasers = $view_builder->viewMultiple($nodes, 'teaser');

      $build = [
        'vendor_list' => [
          '#theme' => 'item_list',
          '#items' => $vendor_list,
        ],
        'vendor_teasers' => $vendor_teasers,
      ];
    }
    else {
      $build = [
        '#markup' => $this->t('No vendors are currently attending this week.'),
      ];
    }

    return $build;
  }

}
```

In this case, the page content depends on the vendor entities being displayed. We use the `getCacheTags()` method of the `$vendor` entity to populate a `#cache['tags']` entry for each vendor in the list. Now, when any of the vendors are edited, Drupal will know it needs to invalidate this list and rebuild it.

## Always add the `#cache` property

Whenever you start writing a render array in your custom code you should take a moment to think about cacheability. Doing so ensures that Drupal can be as efficient as possible. And also prevents possible data leaks and other bugs. For example, a user sees another user's name instead of their own because they were served the wrong cached data.

## Recap

In this tutorial, we added caching to our module's output by updating render arrays to include the `#cache` property. This tells Drupal about the cacheability of the content and helps it make informed decisions about what to cache and when. We used **cache context** to tell Drupal how the data varies, and **cache tags** to tell Drupal what other data our content depends on, improving performance and user experience of our module.

## Further your understanding

- When would you use the `#cache['max-age']` property?
- Explore the code in Drupal core and find other examples of `#cache` being used.

## Additional resources

- [Add Cache Metadata to Render Arrays](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) (Drupalize.Me)
- [Cache contexts](https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts) (Drupal.org)
- [Cache tags](https://www.drupal.org/docs/drupal-apis/cache-api/cache-tags) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Cache Data Retrieved from the Weather API](/tutorial/cache-data-retrieved-weather-api?p=3244)

Clear History

Ask Drupalize.Me AI

close
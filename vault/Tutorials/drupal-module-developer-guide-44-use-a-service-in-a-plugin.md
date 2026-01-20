---
title: "Use a Service in a Plugin"
url: "https://drupalize.me/tutorial/use-service-plugin?p=3241"
guide: "[[drupal-module-developer-guide]]"
order: 44
---

# Use a Service in a Plugin

## Content

Implementing plugins often involves accessing Drupal services to use their functions. Since plugins are PHP classes, we can use dependency injection to access services in our class. This tutorial demonstrates injecting dependencies into plugin classes. We'll update the `HelloWorldBlock` class to use the `current_user` service through dependency injection.

In this tutorial, we'll:

- Learn how to inject dependencies into plugin classes.
- Update the `HelloWorldBlock` class to use dependency injection for accessing the `current_user` service.

By the end of this tutorial, you should understand how to use dependency injection within plugin classes.

## Goal

Modify the "Hello, World!" block plugin and personalize its greeting by injecting the current user service into the plugin.

## Prerequisites

- [Create a Custom "Hello, World!" Block](https://drupalize.me/tutorial/create-custom-hello-world-block)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)
- [Implement a Block Plugin](https://drupalize.me/tutorial/implement-block-plugin)

## Video tutorial

Sprout Video

## Accessing the current user

To access the current user's username, we can access the `current_user` service. This could be done directly. For example:

```
$current_user = \Drupal::currentUser();
$name = $current_user->getDisplayName();
```

This works because `\Drupal::currentUser()` is the `current_user` service. But, it would be better to use the dependency injection pattern and inject the service into our plugin, instead of using the global `\Drupal` object. We can use this approach for any plugin type, not just blocks.

Let's refactor our example code to inject the `current_user` service into our `HelloWorldBlock` plugin.

### Implement `ContainerFactoryPluginInterface`

First, ensure your plugin class implements `Drupal\Core\Plugin\ContainerFactoryPluginInterface`. This interface requires the static `create()` method, and tells the block plugin manager to use this factory method for instantiation.

### Define the `__construct()` and `create()` methods

Introduce a constructor in your plugin class to accept the services as arguments. The `create()` method retrieves the necessary services from the container and passes them to the constructor.

### Adjust the `build()` method

Revise the `build()` method to use the injected `$currentUser` service for personalizing the greeting and replace the use of the `\Drupal` global object.

### Final code

The complete revised plugin code in *anytown/src/Plugin/Block/HelloWorldBlock.php* looks like the following:

```
<?php 

declare(strict_types=1);

namespace Drupal\anytown\Plugin\Block;

use Drupal\Core\Block\BlockBase;
use Drupal\Core\Entity\EntityTypeManagerInterface;
use Drupal\Core\Plugin\ContainerFactoryPluginInterface;
use Drupal\Core\Session\AccountProxyInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

/**
 * Provides a hello world block.
 *
 * @Block(
 *   id = "anytown_hello_world",
 *   admin_label = @Translation("Hello World"),
 *   category = @Translation("Custom"),
 * )
 */
class HelloWorldBlock extends BlockBase implements ContainerFactoryPluginInterface {

  /**
   * The current user.
   *
   * @var \Drupal\Core\Session\AccountProxyInterface
   */
  private $currentUser;

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
   */
  public function __construct(array $configuration, $plugin_id, $plugin_definition, AccountProxyInterface $current_user) {
    parent::__construct($configuration, $plugin_id, $plugin_definition);
    $this->currentUser = $current_user;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container, array $configuration, $plugin_id, $plugin_definition) {
    return new static(
      $configuration,
      $plugin_id,
      $plugin_definition,
      $container->get('current_user')
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

    // This block contains content that is different depending on the user so
    // we don't want it to get cached.
    $build['content']['#cache'] = [
      'max-age' => 0,
    ];

    return $build;
  }

}
```

When you reload the page, the output should be the same. But your code now uses the best practice of using dependency injection to access a service within a class.

## Recap

This tutorial illustrated how to refactor a block plugin to use dependency injection for accessing Drupal services, enhancing the plugin's modularity and testability. This practice is in line with Drupal's best practices, preparing you to implement similar techniques in other plugin types.

## Further your understanding

- Explore how other Drupal core plugins use dependency injection. Note which services they inject and how they use them.
- Attempt to inject a custom service, like the weather forecast service from [Define a Weather Forecast Service](https://drupalize.me/tutorial/define-weather-forecast-service), into a block plugin to increase your understanding of dependency injection's flexibility.

## Additional resources

- [Inject Services Into a Form Controller](https://drupalize.me/tutorial/inject-services-form-controller) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Implement a Block Plugin](/tutorial/implement-block-plugin?p=3241)

Clear History

Ask Drupalize.Me AI

close
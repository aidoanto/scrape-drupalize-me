---
title: "Create a Route and Controller"
url: "https://drupalize.me/tutorial/create-route-and-controller?p=3134"
guide: "[[develop-custom-pages]]"
---

# Create a Route and Controller

## Content

If you want to define a new URL that a user can navigate to, and custom PHP code that will generate the content of the page, you need a *route* and a *controller*. Most of the time you'll want to do something more complex than hard code the content of the page. This will require using *services* in your controller. This can be accomplished in different ways.

In this tutorial we'll:

- Provide the definition for a new route which maps a path to the callback method of a controller class.
- Create a controller that returns a hard coded string.
- Look at examples of using both `ControllerBase` and dependency injection to access services from a controller, and discuss the benefits of both approaches.

By the end of this tutorial, you should be able to define a new route that maps to a controller and displays content on the page as a result of your custom logic.

## Goal

Define a new route that allows a user to access the path `/journey/example` in their browser and access the custom content displayed there.

## Prerequisites

- [Overview: Routes, Controllers, and Responses](https://drupalize.me/tutorial/overview-routes-controllers-and-responses)
- Create a new custom module *journey* in *modules/custom*. See [Overview: Info Files for Drupal Modules](https://drupalize.me/tutorial/overview-info-files-drupal-modules) or use `drush generate module`.

Contents of this tutorial:

- [Define a route that maps to a controller](#define-a-route-that-maps-to-a-controller)
- [Using services in a controller](#using-services-in-a-controller)
- [Route definition reference](#route-definition-reference)

## Quickstart

If you're already familiar with routing, and controllers, you can use `drush generate controller` to get started. [Learn about Drush generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators).

## Watch: Create a Route and Controller

Sprout Video

## Define a route that maps to a controller

Both routes and controllers live in modules. In this tutorial, we'll use an example module named *Journey* (`journey`). As you follow along, you can either add routes to an existing module, or start a new one.

### Create a routing YAML file and define a route

Route definitions live in a *{MODULE\_NAME}.routing.yml* file in the root directory of your module, where `{MODULE_NAME}` is the machine name of your module. If the file doesn't already exist you can create it.

Our example *modules/custom/journey/journey.routing.yml* file looks like this:

```
# Every route needs a unique name. It's common to include the name of the module
# where the route is defined in the route's name to ensure its uniqueness.
journey.example:
  # Every route needs to define a unique path. This is the URL at which the
  # route will be accessible relative to the TLD. The following would result in
  # https://example.com/journey/example.
  path: '/journey/example'
  defaults:
    # The full name of the class (controller) and method that are responsible
    # for building the response for this route.
    _controller: '\Drupal\journey\Controller\ExampleController::build'
    # A human-readable title for the route. Will appear in the HTML <title> tag.
    _title: 'Routing Example'
  requirements:
    # Require that a user has the 'access content' permission in order to view
    # this route.
    _permission: 'access content'
```

This is the most basic definition of a route. It consists of:

- A unique route name: `journey.example`.
- A path to access the route: `/journey/example`.
- A callback declaration that defines which method on which controller should be used to get a response for the route: `\Drupal\journey\Controller\ExampleController::build`.
- Requirements for accessing the route. In this case, that the user has the `access content` permission.

There are a lot of additional possible configuration options for routes. Continue reading to learn more.

### Define the controller that will build the response

Next you'll need to write the code that will get called when a user accesses the path defined by the route. In this example, that's `\Drupal\journey\Controller\ExampleController::build`. Specifically, the `build()` method of a class named `ExampleController` in the *src/Controller/ExampleController.php* file in the `journey` module.

Go ahead and create the file, *modules/custom/journey/src/Controller/ExampleController.php*, with the following contents:

```
<?php
/**
 * @file
 * Controller for the journey.example route.
 */

namespace Drupal\journey\Controller;

class ExampleController {

  public function build() {
    return [
      '#markup' => '<p>This is the content of the journey.example route!</p>',
    ];
  }
  
}
```

The most basic implementation of a controller is a class with a method that returns a [renderable array](https://drupalize.me/tutorial/what-are-render-arrays), a hierarchical associative array that represents the content to display on the page. A Drupal application's modules namespace their controller classes to `Drupal\{MODULE_NAME}\Controller`. Whatever renderable array content is returned from the `build()` method (the method the route points to) will become the primary content of the page.

The method name doesn't matter. Using `build` or `view` as method names is common practice. These methods can be named whatever you want as long as they're public, and the chosen name matches what's in the route definition.

To complete the page, Drupal will render the array to HTML and wrap the content with the blocks and regions defined by the current theme, then convert the result to a `Response` object. The `Response` object is converted to HTTP and sent to the user's browser.

**Tip:** The callback method of a controller can return either a renderable array (good for HTML content), or a `Response` object (good for content in either non-HTML formats or HTTP status codes).

### Verify it worked

To verify your route and controller work [install your module](https://drupalize.me/tutorial/user-guide/config-install?p=3069), or [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache), so that Drupal will pick up your new route definition. Then, navigate to the path you defined for your route (the value of `path`). In this case that would be `/journey/example`. You should see a page like the following:

<drupal-media data-entity-type="media" data-entity-uuid="a352707a-e3db-433a-ae96-4a59198de7c3" alt="Page with title "Routing Example" and content "This is the content of the journey.example route!" rendered using the Olivero theme">

Note the page title is derived from the value of `_title` in your route definition. The page's content is defined by whatever renderable array is returned from the controller's `build()` method.

For more examples of routing, check out the *menu\_examples* module in the [Examples for Developer's project](https://www.drupal.org/project/examples).

## Using services in a controller

The above example controller is plain and merely returns a hard-coded string. Often you'll need to access different [Drupal services](https://drupalize.me/topic/services) in your controller, in order to perform the logic required to calculate the content of a page. There are 3 ways to accomplish this for a controller class:

1. Use `AutowireTrait` for automatic dependency injection (Drupal 10.2+)
2. Extend `\Drupal\Core\Controller\ControllerBase`
3. Implement `\Drupal\Core\DependencyInjection\ContainerInjectionInterface`

Before deciding which approach to take, ask yourself:

- Am I using Drupal 10.2 or later?
- Am I going to write unit tests for the code in this controller?
- Does `ControllerBase` provide the service(s) I need?

**For Drupal 10.2+**, using `AutowireTrait` is the recommended approach as it requires less boilerplate code and automatically injects services based on type hints. This is the most modern and concise option.

For simple controllers where you need to add "glue code" or relatively easy-to-compute content to the page, you can extend `ControllerBase`. It has a bunch of utility methods for common tasks. But keep in mind that extending `ControllerBase` can make your own controller **a lot harder to unit test**, because you'll have to mock all the different services it uses.

If your own controller contains a bunch of its own complex logic, and you want to *unit test the controller*, it might be easier to implement `ContainerInjectionInterface` instead and manually specify which services to inject. Alternatively, you could also define your logic in a unit-testable service and then use that service in your controller.

The `ControllerBase` class has helpers for:

- Accessing the current user
- Loading entities via the *Entity Type Manager*
- Handling cache and state data
- Accessing configuration
- Logging and displaying messages
- Translating content
- Dealing with redirects

Below are three controllers that do the same thing: use the `current_user` service to include the current user's name in the page's content and make the content translatable. The first uses `AutowireTrait` (Drupal 10.2+), the second uses `ControllerBase` to access the necessary services, and the third implements `ContainerInjectionInterface`. The route definition for each is the same, except for the class name.

### Example using `AutowireTrait` (Drupal 10.2+)

This is the recommended approach for Drupal 10.2 and later. It requires the least boilerplate code and automatically injects services based on constructor type hints. This example shows a controller that uses `AutowireTrait` directly without extending `ControllerBase`.

Example *src/Controller/ExampleControllerAutowired.php*:

```
/**
 * @file
 * Example of using AutowireTrait for dependency injection.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\DependencyInjection\AutowireTrait;
use Drupal\Core\Session\AccountInterface;
use Drupal\Core\StringTranslation\StringTranslationTrait;

class ExampleControllerAutowired {

  use AutowireTrait;
  use StringTranslationTrait;

  /**
   * The current user service.
   *
   * @var \Drupal\Core\Session\AccountInterface
   */
  protected AccountInterface $currentUser;

  /**
   * Construct a controller object.
   *
   * @param \Drupal\Core\Session\AccountInterface $current_user
   *   The current user service.
   */
  public function __construct(AccountInterface $current_user) {
    $this->currentUser = $current_user;
  }

  public function build() {
    $name = $this->currentUser->getDisplayName();

    return [
      '#markup' => $this->t('<p>Welcome @name. This is the content of the journey.example route!</p>', ['@name' => $name]),
    ];
  }
}
```

This example demonstrates:

- Using `AutowireTrait` to enable automatic service injection
- Type-hinting the constructor parameter with `AccountInterface` so the `current_user` service is automatically injected
- Using `StringTranslationTrait` for the `$this->t()` method (which `ControllerBase` would normally provide)

**Note:** If you extend `ControllerBase`, it already uses `AutowireTrait` (as of Drupal 10.2), so you don't need to explicitly add it. However, if you're creating a controller that doesn't extend `ControllerBase`, you must add `use Drupal\Core\DependencyInjection\AutowireTrait;` to your class as shown above.

With autowiring, you don't need to manually define a `create()` method. The trait automatically handles service injection based on the type hints in your `__construct()` method.

#### Using the #[Autowire] attribute

When a service cannot be resolved by its interface alone (for example, when you need a specific cache bin), you can use the `#[Autowire]` PHP attribute to specify the service ID manually:

```
use Drupal\Core\Cache\CacheBackendInterface;
use Drupal\Core\DependencyInjection\Attribute\Autowire;
use Drupal\Core\DependencyInjection\AutowireTrait;

class ExampleControllerWithAttribute {

  use AutowireTrait;

  /**
   * Construct a controller object.
   *
   * @param \Drupal\Core\Cache\CacheBackendInterface $cache
   *   The cache service.
   */
  public function __construct(
    #[Autowire(service: 'cache.default')]
    protected CacheBackendInterface $cache,
  ) {}

  public function build() {
    // Use $this->cache here
    return ['#markup' => 'Example content'];
  }
}
```

In this example, the `#[Autowire]` attribute explicitly tells Drupal to inject the `cache.default` service, even though `CacheBackendInterface` could refer to multiple cache backends.

### Example of extending `ControllerBase`

This approach is useful when you need quick access to common services and aren't concerned about unit testing the controller. `ControllerBase` provides several utility methods out of the box.

Example *src/Controller/ExampleControllerFromBase.php*:

```
/**
 * @file
 * Example of extending ControllerBase to create a new controller.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\Controller\ControllerBase;

class ExampleControllerFromBase extends ControllerBase {
  public function build() {
    // The current_user service, and others, are included by the ControllerBase
    // class. This is helpful to easily access common services, and when you're
    // not worried about unit testing your controller. See the definition of
    // \Drupal\Core\Controller\ControllerBase to learn more about the available
    // services.
    $name = $this->currentUser()->getDisplayName();

    return [
      '#markup' => $this->t('<p>Welcome @name. This is the content of the journey.example_base route!</p>', ['@name' => $name]),
    ];
  }
}
```

### Example of implementing `ContainerInjectionInterface`

This is the most explicit approach and gives you full control over which services are injected. It's useful when you need to unit test your controller or when autowiring isn't available (pre-Drupal 10.2).

With this approach, you only need to mock the `current_user` service for unit testing the logic in the controller. You can learn more about unit testing controllers in [Implement a Unit Test in Drupal](https://drupalize.me/tutorial/implement-unit-test-drupal) which has an example of mocking services for a thin controller.

Example *src/Controller/ExampleControllerContainerInjection.php*:

```
/**
 * @file
 * Example of creating a new Controller using container injection.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\DependencyInjection\ContainerInjectionInterface;
use Drupal\Core\Session\AccountInterface;
use Drupal\Core\StringTranslation\StringTranslationTrait;
use Symfony\Component\DependencyInjection\ContainerInterface;

class ExampleControllerContainerInjection implements ContainerInjectionInterface {

  use StringTranslationTrait;

  /**
   * The current user service.
   *
   * @var \Drupal\Core\Session\AccountInterface
   */
  protected $currentUser;

  /**
   * Construct a controller object.
   *
   * @param \Drupal\Core\Session\AccountInterface $current_user
   *   The current user service.
   */
  public function __construct(AccountInterface $current_user) {
    $this->currentUser = $current_user;
  }

  /**
   * {@inheritdoc}
   */
  public static function create(ContainerInterface $container) {
    return new static(
      $container->get('current_user')
    );
  }

  public function build() {
    // The current_user service is included via dependency injection. The
    // $this->t() method is provided by StringTranslationTrait.
    $name = $this->currentUser->getDisplayName();
    return [
      '#markup' => $this->t('<p>Welcome @name. This is the content of the journey.example route!</p>', ['@name' => $name]),
    ];
  }

}
```

#### Understanding the legacy create() method pattern

The `ContainerInjectionInterface` approach shown above uses the `create()` factory method pattern, which was the standard way to implement dependency injection in controllers before Drupal 10.2. While autowiring is now the recommended approach for Drupal 10.2+, you'll still encounter the `create()` method pattern frequently in:

- Existing Drupal core code
- Contributed modules
- Documentation and tutorials written before Drupal 10.2
- Situations where you need more control over service initialization

The `create()` method works by:

1. Drupal sees that your controller implements `ContainerInjectionInterface`
2. Instead of instantiating the class directly, Drupal calls the static `create()` method
3. The `create()` method receives the service container as a parameter
4. You use `$container->get('service_id')` to retrieve specific services
5. The method returns a new instance of the controller with services passed to the constructor

This legacy approach is still fully supported and works in all versions of Drupal. However, for Drupal 10.2 and later, using `AutowireTrait` is the recommended approach as it requires less boilerplate code and is more maintainable.

## Route definition reference

There are different configuration options that can be included in your route definition. There is a comprehensive list in the documentation at [Structure of routes](https://www.drupal.org/docs/drupal-apis/routing-system/structure-of-routes). It is worth reading through this list to familiarize yourself with the options.

A few things to be aware of:

- When a configuration option is prefixed with an underscore (`_`), that indicates it's a Drupal-specific option and not part of the standard Symfony routing component. For example, `_title_callback` or `_permission`.
- Routes must always specify the thing that is called, e.g. `_controller` or `_form`. This can be any PHP callable, though methods on a controller are the most common. You can also call a method of a Drupal service using the syntax `{service_id}:method`, e.g. `my_module.data:display`.
- Some options like `_title_callback`, and `_custom_access` also take a callable, allowing you to dynamically set the value. For example, use `_title_callback` if you want to compute the page title instead of hard coding it. Learn more in [Set a Dynamic Title for a Route](https://drupalize.me/tutorial/set-dynamic-title-route)
- Not all configuration options are documented, especially those for the `requirements` section, because they are calculated at runtime based on the installed modules. Any module can add custom access checking services, tag the service definition with a unique tag like `_mymodule_check_access`, and then reference the service tag in the route definition. Learn more in [Add Access Checking to a Route](https://drupalize.me/tutorial/add-access-checking-route)

Here are a few more examples:

```
examples.use_url_arguments:
  # A path can include multiple placeholders, which can be at any position in
  # the path.
  path: '/example/use-url-arguments/{arg1}/{arg2}'
  defaults:
    _title: 'URL Arguments'
    _controller: '\Drupal\menu_example\Controller\MenuExampleController::urlArgument'
    # You can provide default values for hard coded arguments.
    arg1: '550e8400-e29b-41d4-a716-446655440000'
    arg2: ''
  requirements:
    _permission: 'access content'
    # You can require that arguments match a regex, or a 404 will be thrown.
    # This example requires arg1 to be a UUID formatted string.
    arg1: '[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}'

# Title of this menu entry will be altered by controller method defined by
# key '_title_callback'.
examples.title_callbacks:
  path: '/examples/title-callbacks'
  defaults:
    # It's common to have additional callback arguments be methods on the same
    # controller as specified by the primary _controller option.
    _title_callback: 'Drupal\menu_example\Controller\MenuExampleController::titleCallback'
    _controller: '\Drupal\menu_example\Controller\MenuExampleController::titleCallbackContent'
  requirements:
    _permission: 'access content'

# Parameters can be converted to complex data types using upcasting.
examples.upcasting:
  # Example /examples/upcasting/42
  path: '/examples/upcasting/{node}'
  defaults:
    _title: 'Upcasting Example'
    _controller: '\Drupal\menu_example\Controller\MenuExampleController::upcastingExample'
  requirements:
    _permission: 'access content'
    node: '\d+'
  options:
    parameters:
      # Convert the {node} parameter to a $node object, but only if the node is
      # an article.
      node:
        type: 'entity:node'
        bundle: article

# Point to a form controller to display a Form API form.
examples.simple_form:
  path: 'examples/form-api-example/simple-form'
  defaults:
    _form: '\Drupal\form_api_example\Form\SimpleForm'
    _title: 'Simple form'
  requirements:
    _permission: 'access content'
```

## Recap

In this tutorial, we learned how to define a new route and controller, exposing a new URL that displays content generated by our custom code. We also learned about three different approaches to accessing Drupal services in a controller: using `AutowireTrait` (Drupal 10.2+), extending `ControllerBase`, or implementing `ContainerInjectionInterface`. For modern Drupal development (10.2+), `AutowireTrait` is the recommended approach.

## Further your understanding

- When should you use `ControllerBase` versus using container injection to access all the services you need in your custom logic?
- Can the same controller class be used to build the content for multiple different URLs?
- How would you adapt this code if the content of the custom page was a form?

## Additional resources

- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) (Drupalize.Me)
- [Introductory Drupal routes and controllers example](https://www.drupal.org/docs/drupal-apis/routing-system/introductory-drupal-routes-and-controllers-example) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[How to Find a Route in Drupal](/tutorial/how-find-route-drupal?p=3134)

Next
[Overview: Parameters and Value Upcasting in Routes](/tutorial/overview-parameters-and-value-upcasting-routes?p=3134)

Clear History

Ask Drupalize.Me AI

close
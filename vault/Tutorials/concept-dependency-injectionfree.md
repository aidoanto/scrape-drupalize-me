---
title: "Concept: Dependency Injectionfree"
url: "https://drupalize.me/tutorial/concept-dependency-injection?p=3238"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Dependency Injectionfree

## Content

Dependency injection is an object-oriented programming design pattern widely used in Drupal. Instead of a class creating an object directly, dependency injection provides services or objects to a class externally, and is an example of the [Inversion of Control principle](https://stackoverflow.com/questions/3058/what-is-inversion-of-control).

In this tutorial, we'll:

- Explain dependency injection in the context of Drupal.
- Take a look at examples of constructor and setter injection in Drupal code.

By the end of this tutorial, you'll recognize dependency injection patterns and understand how it's used in Drupal module development.

## Goal

Understand and identify dependency injection in Drupal.

## Prerequisites

- [Concept: Services and the Container](https://drupalize.me/tutorial/concept-services-and-container)

## How is dependency injection used in Drupal?

Dependency injection is a design pattern where objects are passed into a class rather than the class creating them. This approach externalizes the object's initialization and configuration, and can make module code more flexible, reusable, and easier to test.

In Drupal, dependency injection enables modules to request services like the database or current user service without knowing specifics. This allows Drupal to determine details, such as the database type, based on configuration. Using a service provided by core or other modules should be done via dependency injection, which facilitates loose coupling between components.

### Constructor injection

Dependencies (services) are supplied as arguments to a class constructor. For example, a service querying a third-party API might depend on the `http_client` service for making HTTP requests, the `cache` service for caching responses, and the `logger` service for logging errors.

Here's an example:

```
class ExampleService {
  protected $cache;
  protected $http_client;
  protected $logger;

  public function __construct($cache, $http_client, $logger) {
    $this->cache = $cache;
    $this->http_client = $http_client;
    $this->logger = $logger;
  }
}
```

To initialize `ExampleService`, each dependency must be instantiated.

Example:

```
$cache = new Cache();
$http_client = new Guzzle();
$logger = new Logger();
$example = new ExampleService($cache, $http_client, $logger);
```

**Tip:** When accessing a service via the service container, dependencies are automatically initialized. This is the preferred approach in Drupal modules.

Example:

```
$example = Drupal::container('example_service');
```

### Constructor injection via a `create()` factory method

Drupal commonly uses a static `create()` factory method for constructor injection. This is the pattern you'll see most often in Drupal modules. The pattern is used in controllers and plugins and is part of the `Drupal\Core\DependencyInjection\ContainerInjectionInterface`. It allows a class to instantiate itself with necessary services from the container.

Here's an example:

```
use Drupal\Core\Database\Connection;
use Drupal\Core\DependencyInjection\ContainerInjectionInterface;
use Symfony\Component\DependencyInjection\ContainerInterface;

class ExampleService implements ContainerInjectionInterface {
   protected $database;
   
   public function __construct(Connection $database) {
     $this->database = $database;
   }
   
   public static function create(ContainerInterface $container) {
     return new static($container->get('database'));
   }
}

// To initialize an instance of this class ...
$example = ExampleService::create($container);
```

### Setter injection

Setter injection uses setter methods to set dependencies after object instantiation. This method is less common but useful in specific scenarios.

Example:

```
use Drupal\Core\Logger\LoggerChannelInterface;

class AnotherExampleService {
   protected $logger;
   
   public function setLogger(LoggerChannelInterface $logger) {
     $this->logger = $logger;
   }
}
```

## Recap

This tutorial explains the basics of dependency injection in Drupal. We examined constructor and setter injection examples, showing how dependencies are supplied to classes and discussing how this works in the context of a Drupal module.

You'll get opportunities to practice using these patterns throughout this guide, so that you can learn to develop flexible and maintainable Drupal modules.

## Further your understanding

- Can you explain the `create()` factory method pattern described above?
- Discuss the benefits and drawbacks of constructor vs. setter injection in Drupal module development.
- Explore the [*Drupal\new\_dependency\_test* classes](https://api.drupal.org/api/drupal/namespace/Drupal%21new_dependency_test/) (`InjectedService`, `Service`, `ServiceWithDependency`, `SetterInjection`) for more examples of services and dependency injection.

## Additional resources

- [Services and dependency injection guide](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Services and the Container](/tutorial/concept-services-and-container?p=3238)

Next
[Locate and Identify Existing Services](/tutorial/locate-and-identify-existing-services?p=3238)

Clear History

Ask Drupalize.Me AI

close
---
title: "Discover and Use Existing Services"
url: "https://drupalize.me/tutorial/discover-and-use-existing-services?p=3254"
guide: "[[alter-drupal-modules]]"
order: 17
---

# Discover and Use Existing Services

## Content

It's best practice to access any of the services provided by Drupal via the service container to ensure the decoupled nature of these systems is respected. In order to do so, you need to know what services exists, and then, where possible, use dependency injection to use them in your code.

This tutorial walks through the process of:

- Discovering existing services and learn their machine name
- Using the machine name of service to request a copy from the service container

## Goal

Find the Drupal core or contributed module-provided service that performs a specific function and instantiate it via the service container.

## Prerequisites

- [Understand the Service Container](https://drupalize.me/series/dependency-injection-and-art-services-and-containers)

## Commonly used services

There are hundreds of services in Drupal. As a quick reference here is a list of some of the ones we end up using most frequently in custom code.

| Service ID | Associated Class | Description |
| --- | --- | --- |
| `cache.default` | `Drupal\Core\Cache\CacheBackendInterface` | Used for working with cached data. |
| `config.factory` | `Drupal\Core\Config\ConfigFactory` | Read, write, and update configuration data. |
| `current_user` | `Drupal\Core\Session\AccountProxy` | Provides information about the currently logged-in user. |
| `database` | `Drupal\Core\Database\Connection` | Query the database. |
| `entity.query` | `Drupal\Core\Entity\Query\QueryFactory` | Query entities. |
| `entity_type.manager` | `Drupal\Core\Entity\EntityTypeManager` | Read, write, and update entities. |
| `form_builder` | `Drupal\Core\Form\FormBuilder` | Builds and processes forms. |
| `http_client` | `GuzzleHttp\Client` | Make HTTP requests. |
| `logger.factory` | `Drupal\Core\Logger\LoggerFactory` | Handle logging within the system. |
| `module_handler` | `Drupal\Core\Extension\ModuleHandler` | Handles module related functionality like invoking hooks. |
| `path.alias_manager` | `Drupal\path_alias\AliasManager` | Manages URL path aliases. |
| `renderer` | `Drupal\Core\Render\Renderer` | Responsible for rendering arrays into HTML. |
| `route_match` | `Drupal\Core\Routing\CurrentRouteMatch` | Provides information about the current route and parameters. |
| `state` | `Drupal\Core\State\State` | Manage state information, for data not saved in config. |
| `string_translation` | `Drupal\Core\StringTranslation\TranslationManager` | Manage string translation across the system. |
| `url_generator` | `Drupal\Core\Routing\UrlGenerator` | Generate internal and external URLs. |

## Find services in Drupal's API documentation

There's a comprehensive list of all the services in Drupal core available at <https://api.drupal.org/api/drupal/services>. Use the filter at the top of the page to find what you're looking for. The first column in the table contains the unique machine name of the service which you can use to request it from the service container.

Image

![Example of using search tool to discover services on api.drupal.org](../assets/images/services-list-filtered.png)

## Find services with Drush and Devel

With [Drush](https://drupalize.me/tutorial/what-drush-0) and the contributed [Devel module](https://drupalize.me/topic/devel) installed, you can get a list of all services, or a subset of services that share a partial name.

Get a complete list:

```
drush devel:services
```

The `drush devel:services` command has 2 aliases:

1. `drush devel-container-services`
2. `drush dcs`

Get a list of the services that share a partial name by choosing any part of a service name and pass it as an additional argument. This is a nice shortcut to using `grep`. For example to get a list of all the [plugin.manager](https://drupalize.me/tutorial/plugin-managers) services:

```
drush dcs plugin.manager
```

Or, use `grep` verbosely:

```
drush dcs | grep plugin.manager
```

Once you see the long list of services returned by `drush dcs`, you'll see the value of adding a keyword argument to narrow that list down and make it more useful to you.

## Read the code

You can discover existing services by reading through the source code of your Drupal site.

Services are defined in YAML files, for example the *core.services.yml* file (in the top-level core directory). Some Drupal core modules and contributed modules also define services in *MODULENAME.services.yml* files.

A typical service definition in a *\*.services.yml* file looks like this:

```
path.alias_manager:
  class: Drupal\Core\Path\AliasManager
  arguments: ['@path.crud', '@path.alias_whitelist', '@language_manager']
```

The first line of a service definition gives the unique machine name of the service. `path.alias_manager` in this case. This is often prefixed by the module name if provided by a module; however, by convention some service names are prefixed by a group name instead, such as `cache.\*` for cache bins and `plugin.manager.\*` for plugin managers.

## Using a service

Services should be loaded via the services container.

Example:

```
$alias_manager = \Drupal::service('path.alias_manager');
```

Better yet, use dependency injection to inject one or more services into your controller.

Sprout Video

## Recap

It's best practice to access any of the services provided by Drupal via the service container to ensure the decoupled nature of these systems is respected. In this tutorial, we learned how to discover an existing service's machine name and how to request a copy of that service from the service container.

## Further your understanding

- [Understand the Service Container](https://drupalize.me/videos/understand-service-container)
- [Get a Service From the Container](https://drupalize.me/videos/get-service-out-controller)
- [Create a New Service](https://drupalize.me/videos/create-service)
- [Dependency Injection and the Art of Services and Containers](https://drupalize.me/series/dependency-injection-and-art-services-and-containers) - A complete guide to understanding services and dependency injection

## Additional resources

- [Services and Dependency Injection Container](https://api.drupal.org/api/drupal/core%21core.api.php/group/container) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close
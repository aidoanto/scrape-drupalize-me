---
title: "Locate and Identify Existing Services"
url: "https://drupalize.me/tutorial/locate-and-identify-existing-services?p=3238"
guide: "[[drupal-module-developer-guide]]"
---

# Locate and Identify Existing Services

## Content

To access services in Drupal through the service container, you'll need to know the unique machine name of the service. We'll use the example of making HTTP requests to a weather forecast API in the *anytown* module to demonstrate several methods you can use to identify an existing service's ID.

In this tutorial, we'll:

- Discover existing services and their machine names.
- Take a look at an example service definition.

By the end of this tutorial, you should be able to locate and use existing services in your Drupal module.

## Goal

Learn to find existing services and their unique names, focusing on the HTTP client service.

## Prerequisites

- [Concept: Services and the Container](https://drupalize.me/tutorial/concept-services-and-container)

## Video tutorial

Sprout Video

## Find services on api.drupal.org

**Note:** There's a known issue with the services list for Drupal 11.x on api.drupal.org. [See this issue](https://www.drupal.org/project/api/issues/3464159). While this is being resolved, we recommend that you switch to Drupal 10.3 on api.drupal.org and filter for services using that version.

Drupal core's comprehensive list of services is available on [api.drupal.org](https://api.drupal.org/api/drupal/services). This list only includes Drupal core services and not those provided by custom or contributed modules. Use the filter to search for specific services. The first column in the table displays the service's unique machine name.

Image

![Screenshot of the api.drupal.org services list, filtered for http services](/sites/default/files/styles/max_800w/public/tutorials/images/services--locate-a-service_list-filtered.png?itok=vtyx71Rp)

To find the HTTP client service, visit [api.drupal.org](https://api.drupal.org), select *Services* in the *API Navigation* block, filter by *http*, and locate the *http\_client* service. Note its name for later use.

## Use Devel to list current site's services

Since *api.drupal.org* doesn't list services from custom or contributed modules, we'll need to use another approach for those. To find all available services provided by installed modules on your site, install the [Devel module](https://www.drupal.org/project/devel) and use its Drush command, `drush devel:services`:

```
# Download and install Devel
composer require --dev drupal/devel
drush en devel

# List all services
drush devel:services
```

## Locate service definitions in files

Once you know the name of a service, if you want to figure out the PHP class that is associated with it, or the service's arguments, you'll need to search for the service name in *.yml* files. Locate the service definition file that contains the service's name and configuration.

Services are defined in *\*.services.yml* files, such as *core.services.yml* in Drupal core and in module-specific *MODULE\_NAME.services.yml* files.

A typical service definition looks like the following:

```
path.alias_manager:
  class: Drupal\Core\Path\AliasManager
  arguments: ['@path.crud', '@path.alias_whitelist', '@language_manager']
```

In this case `path.alias_manager` is the service's unique machine name. The indented lines provide configuration for the service. We'll learn more in [Define a Weather Forecast Service](https://drupalize.me/tutorial/define-weather-forecast-service).

Once we've identified the service name, we'll practice accessing it in [Use a Service in a Controller](https://drupalize.me/tutorial/use-service-controller).

## What does this service do?

Once you've found the service's definition in a *\*.services.yml* file, use your IDE to navigate to the class associated with the service, and see which PHP interface the service class implements.

For example, the `http_client` service, found in *core/core.services.yml* is provided by `GuzzleHttp\Client` class which implements `\GuzzleHttp\ClientInterface`. This should give you information about what methods are available to you, and potentially point you to additional documentation.

## Recap

In this tutorial we explored methods to discover services and their unique names, including using *api.drupal.org*, the Devel module, and reading service definition files (*\*.services.yml*). Identifying the unique name of a service is crucial for accessing it via the service container.

## Further your understanding

- Try finding the service name for accessing current user information.
- Why aren't all services in your Drupal site listed on *api.drupal.org*?

## Additional resources

- [Discover and Use Existing Services](https://drupalize.me/tutorial/discover-and-use-existing-services) (Drupalize.Me)
- [List of services provided by Drupal core](https://api.drupal.org/api/drupal/services/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Dependency Injection](/tutorial/concept-dependency-injection?p=3238)

Next
[Use a Service in a Controller](/tutorial/use-service-controller?p=3238)

Clear History

Ask Drupalize.Me AI

close
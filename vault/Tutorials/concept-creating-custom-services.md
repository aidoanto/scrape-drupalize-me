---
title: "Concept: Creating Custom Services"
url: "https://drupalize.me/tutorial/concept-creating-custom-services?p=3238"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Creating Custom Services

## Content

Custom services in Drupal modules encapsulate specific business logic or functionality. In our example, we'll demonstrate moving code required to access a weather forecast API from a controller into a service. This will help make our controller *thin* and our module code more reusable, testable, and maintainable.

In this tutorial, we'll:

- Explore the advantages of custom services for managing business logic.
- Define the components of a custom service.

By the end of this tutorial, you'll understand why creating custom services is a beneficial practice in Drupal module development.

## Goal

Understand the benefits of creating a custom service in a Drupal module.

## Prerequisites

- [Concept: Services and the Container](https://drupalize.me/tutorial/concept-services-and-container)
- [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection)

## What are custom services in Drupal?

Custom services in Drupal are PHP objects that encapsulate distinct business logic or functionalities, separate from Drupal's core or contributed module services. They offer a structured approach to organizing and managing code containing complex and reusable logic.

### Why custom services?

**Reusability:** Defined services can be reused in different parts of a module or across modules, reducing code duplication and promoting the Don't Repeat Yourself (DRY) principle. For example, converting weather forecast logic currently in the `WeatherPage` controller into a service means we can use that logic in a block plugin without duplicating code.

**Testing:** Services allow for independent and efficient testing. Isolating business logic in services simplifies unit testing and ensures reliable application behavior. For instance, testing a weather forecast client becomes more manageable when isolated from the controller.

**Maintainability:** Services contribute to thinner controllers and other components by separating business logic. Controllers should focus on request processing and delegate business logic to services, leading to more maintainable and manageable code.

### Practical examples

**Reusable weather forecast block:** Extending the module to include a block for displaying the weather forecast becomes simpler if the fetching and processing logic is in a custom service, allowing code reuse in both the block and the controller.

**Integrating third-party libraries:** Wrapping external libraries from Composer in a Drupal service ensures seamless integration and accessibility of the library's functionalities throughout the module.

**Configurable API selection:** A service can adapt to different third-party weather API integrations, allowing site administrators to choose the preferred API. This flexibility ensures the controller and block remain unaffected by the choice of API.

## Components of a service

A service includes:

- A PHP **interface** that defines the service's publicly accessible methods, and provides a template for service implementation.
- A PHP **class** that implements the service's interface.
- A **service definition** in the *MODULE\_NAME.services.yml* file, which is used by the service container for discovery and management.

In the next tutorial, [Define a Weather Forecast Service](https://drupalize.me/tutorial/define-weather-forecast-service), we'll guide you through defining and using a custom service.

## Recap

Custom services in Drupal organize a module's business logic, enhancing testability, reusability, and maintainable code architecture. They are key to efficient Drupal module development. Whenever business logic creeps into a controller or block, consider encapsulating it in a service.

## Further your understanding

- Can you identify a scenario where a custom service could streamline module development?
- Reflect on how custom services might influence the overall structure of a Drupal application.

## Additional resources

- [Services and Dependency Injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use a Service in a Controller](/tutorial/use-service-controller?p=3238)

Next
[Define a Weather Forecast Service](/tutorial/define-weather-forecast-service?p=3238)

Clear History

Ask Drupalize.Me AI

close
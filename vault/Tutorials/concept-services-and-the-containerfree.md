---
title: "Concept: Services and the Containerfree"
url: "https://drupalize.me/tutorial/concept-services-and-container?p=3238"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Services and the Containerfree

## Content

As a development framework, Drupal core includes services for doing common things like accessing the database, sending email, or making HTTP requests. You can make use of these services to perform certain tasks, instead of recreating them in your own code. This means less custom code that you need to write and maintain. Generally speaking, almost everything that Drupal does is actually done by one of these objects. In Drupal, these objects are called services and in order to make working with them easier, they are primarily accessed through the service container.

In this tutorial, we'll:

- Explain the role of services in Drupal.
- Introduce the service container.

By the end of this tutorial, you'll understand the basics concepts of services and the service container in Drupal module development.

## Goal

Understand the role of services and the service container in Drupal module development.

## Prerequisites

- None.

## What are services?

Services in Drupal are modular, reusable, and interface-driven PHP objects that can do common tasks for a module.

A service in Drupal is a PHP object that encapsulates functionality or business logic. Services are flexible, reusable components designed to interact with various aspects of Drupal and external systems.

Services in Drupal implement interfaces, which means services that implement the same interface are interchangeable. This design enables Drupal to interface with different systems, like various database servers, or to modify certain functionalities, such as email handling, through custom modules.

As a developer, you’ll frequently use the service container to access and **use existing services**. You may also **define new services** for unique application logic. Services provide modular, reusable functionalities for easy integration into custom modules.

## Custom services

Custom modules often contain a combination of application-specific business logic and the code required to integrate that logic with Drupal. For example, accessing a third-party weather API in a weather forecast module is custom logic. Formatting the returned value as a renderable array and displaying it on the page via a controller is Drupal integration code.

Isolating the weather forecast API code into a custom service will make it easier to isolate problems, maintain, and test our code. We'll explore creating custom services in [Concept: Creating Custom Services](https://drupalize.me/tutorial/concept-creating-custom-services).

## The service container

The service container in Drupal acts as a repository and manager for all services. As a developer you can ask the service container for the service you need, and it will do the work of initializing it. For example, if you want to work with cached data, the service container will return a cache object already configured to connect to the caching backend specified by your Drupal site's unique configuration. It ensures that each service is instantiated only once, and only if requested.

Accessing a service can be done through:

- **Dependency injection:** Injecting services into a class via the constructor. More on this in [Concept: Dependency Injection](https://drupalize.me/tutorial/concept-dependency-injection).
- **Static methods:** In procedural code (like in hook implementations), access services using static methods such as `\Drupal::currentUser()` or `\Drupal::service('{SERVICE_ID}')`.

If the service you're requesting has dependencies on other services, the container will take care of ensuring those dependencies are loaded and instantiated.

## Defining new services in a module

To define a new services, modules must:

- Define a PHP interface for the service that dictates the publicly-available methods that code using the service can call.
- Provide one or more classes that implement that interface and perform the service's custom logic.
- Give the service a unique name and describe it in a *MODULE\_NAME.services.yml* file.

## Recap

In this tutorial, we learned that services are reusable objects that perform specific tasks and that the service container manages these services efficiently. Developers writing custom modules can put their application-specific *business logic* into a custom service isolating it from the Drupal-specific integration code, making it easier to test and maintain.

## Further your understanding

- Can you think of a scenario where a custom service would enhance a Drupal module? What function would it serve?
- Read the *core/core.services.yml* file. What can you learn about Drupal's core services and their roles?

## Additional resources

- [Services](https://drupalize.me/topic/services) (Drupalize.Me)
- [Services and Dependency Injection](https://www.drupal.org/docs/drupal-apis/services-and-dependency-injection) (Drupal.org)
- [Services and Dependency Injection](https://api.drupal.org/api/drupal/core%21core.api.php/group/container/) (api.drupal.org)
- [List of services provided by Drupal core](https://api.drupal.org/api/drupal/services/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Concept: Dependency Injection](/tutorial/concept-dependency-injection?p=3238)

Clear History

Ask Drupalize.Me AI

close
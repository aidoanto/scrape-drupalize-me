---
title: "Concept: Entity API and Data Storage"
url: "https://drupalize.me/tutorial/concept-entity-api-and-data-storage?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Entity API and Data Storage

## Content

Entities are the building blocks of Drupal's data structures. As module developers, the Entity API provides a way to manage custom data with minimal code. You'll use it when altering or enhancing existing content or when managing custom data sets. Instead of writing SQL, you'll be using the Entity API to manage data within a Drupal application.

In this tutorial, we'll:

- Define entities and their significance in Drupal.
- Distinguish between content entities and configuration entities.
- Explore entity-related terminology such as bundles, fields, annotations, plugins, and handlers.

By the end of this tutorial, you'll have a foundational understanding of the Entity API and how it's used for data management in Drupal.

## Goal

Get a high level overview of the Entity API, focusing on content and configuration entities, and the advantages of using it to manage your custom data.

## Prerequisites

- [Concept: Data Types in Drupal](https://drupalize.me/tutorial/concept-data-types-drupal)
- [2.3. Concept: Content Entities and Fields](https://drupalize.me/tutorial/user-guide/planning-data-types) (Drupal User Guide)
- [Concept: What Are Plugins?](https://drupalize.me/tutorial/concept-what-are-plugins)

## Managing entities with Entity API

Entities are a fundamental part of Drupal's structure, serving as a standardized method for storing and managing content and configuration data. In most cases module developers who want to store records should use the Entity API to do so. For example, by creating custom entity types, or by writing single-use-case "glue code" that can make assumptions about the user-configured content types and fields on a Drupal site.

Glue code refers to custom code in a module that uses Drupal APIs to implement specific business logic. Glue code in custom modules makes assumptions about how your site is structured; for example, the machine names of certain fields. Or by creating a custom entity that serves a unique business requirement. Glue code is used when a core or contributed module *almost* addresses a problem you need to solve, but you need a bit more customization to complete the solution.

There are 2 primary kinds of entities: content entities and configuration entities.

### Content entities

*Content entities* are instances of data that are meant to store content meant to be displayed on the site. These entities are often user-facing and are created, managed, and deleted through the Drupal UI or programmatically. Examples include nodes (basic content pages or articles), users, comments, and taxonomy terms. Content entities are:

- **Content-centric**: Primarily focused on storing and managing user-generated content.
- **Fieldable**: They can have fields added to them, allowing for the customization of the data structure.
- **Translatable**: Support multilingual content, allowing for the translation of content into different languages.
- **Revision-supported**: Can enable revisions, storing updates as new revisions, able to be reverted, and manageable by content moderation and workflow modules.

## Configuration entities

*Configuration entities* are instances of data that store the configuration information of the site. Unlike content entities, configuration entities are used to configure the behavior and functionality of the site itself rather than holding content meant to be displayed. Examples include views, content types, and field definitions. Configuration entities are:

- **Configuration-centric**: Focused on storing settings and configurations for site functionality.
- **Deployable**: Can be exported and imported between different environments (e.g., from development to production).
- **Not fieldable**: Typically do not support the addition of fields in the same way content entities do.
- **Not content**: Store settings that affect how the site operates, not content displayed to end-users.
- **Translatable**: Support localization of configuration settings.

## Entity API terminology

When working with entities, it's important to understand the following terms.

### Entity

An individual unit of data, like a content item (node), taxonomy term, or comment.

### Entity types

A broad category of data with common base properties, access controls, and a storage mechanism. For example, "Node" is an entity type that represents content items like articles or blog posts, "User" is an entity type for user accounts, and "Taxonomy term" is an entity type for categorization terms.

### Bundle

A subtype of an entity type, allowing for variations of an entity type that share a common data structure but serve distinct purposes. For instance, content types (article, basic page) for a Node entity.

### Plugins and handlers

Entity types are defined as plugins. Plugins are also used to extend and customize entity behavior. The Entity API delegates specific operations for entities, such as access control, form display, and storage to plugins and handlers.

### Fields

Data storage attached to entities. Fields can store various types of data, from simple text to references to other entities or images. The data that an entity contains is a combination of its *base fields* (hard coded) and *attached fields* (defined and configured by the user on a per-site basis).

Learn more in [Concept: Field API and Fieldable Entities](https://drupalize.me/tutorial/concept-field-api-and-fieldable-entities).

### Querying

Entities are read, and queried, via the API. This abstraction ensures the actual storage of data is swappable. And that performance strategies like caching can be applied universally.

### Validation

Validation of an entity happens at the Entity API level rather than the Form API level ensuring that validation logic is applied regardless of whether the entity is created via an HTML form, a JSON:API request, or in code.

## Using the Entity API to manage data

The Entity API abstracts direct database access, offering a set of tools for performing CRUD (Create, Read, Update, Delete) operations on entities. These standard methods ensure that entities can integrate with Drupal's core and contributed modules.

For module developers, this means you should use the Entity API to interact with both content and configuration data to ensure your module can reliably manage entity data.

## Benefits of using the Entity API

Using the Entity API for data storage instead of managing your own tables and using direct database queries offers several advantages:

- **Standardization**: The Entity API provides a unified way to handle data ensuring consistency, and familiarity.
- **Interoperability**: By using entities, your data automatically becomes compatible with other parts of Drupal's ecosystem, such as revision tracking, workflows, views, Search API, and RESTful web services.
- **Extensibility**: Entities and fields are extensible through the UI and code, allowing site builders and developers to customize and extend data structures.
- **Security**: Entities automatically handle common security concerns such as SQL injection, making your code safer by default.
- **Localization and translation**: The Entity API natively supports multilingual content, making it possible to build multilingual sites.

By abstracting the complexity of data storage and operations, the Entity API allows developers to focus on their application-specific needs while still getting tight integration with the rest of the Drupal ecosystem. And when all modules are using the same abstraction for data storage the entire ecosystem is more tightly integrated.

In the remaining tutorials in this chapter, we'll work through common examples of using the Entity API in custom code.

## Recap

This tutorial provided an overview of the Entity API, differentiating between content and configuration entities and explaining essential entity-related concepts. As developers, you'll often interact with entities in your module code and make use of the Entity API.

## Further your understanding

- How do entities and the Entity API enhance Drupal's content management system compared to direct database manipulation?
- What are some practical examples of how custom modules can use entities?

## Additional resources

- [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview) (Drupalize.Me)
- [Configuration Data Types](https://drupalize.me/tutorial/configuration-data-types) (Drupalize.Me)
- [Entity API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a Configuration Schema and Default Values](/tutorial/define-configuration-schema-and-default-values?p=3243)

Next
[Concept: Field API and Fieldable Entities](/tutorial/concept-field-api-and-fieldable-entities?p=3243)

Clear History

Ask Drupalize.Me AI

close
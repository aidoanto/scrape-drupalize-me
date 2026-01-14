---
title: "Concept: Data Types in Drupalfree"
url: "https://drupalize.me/tutorial/concept-data-types-drupal?p=3243"
guide: "[[drupal-module-developer-guide]]"
order: 52
---

# Concept: Data Types in Drupalfree

## Content

Drupal uses 4 primary information types for canonical data storage: content, configuration, session, and state. Content encompasses the site's visible data, such as articles, images, and files. Content data are called content entities in Drupal. Configuration data stores site settings including site name, content types, and views. Session data tracks user interactions, including login status. State data holds temporary information like the last cron execution time.

In this tutorial, we'll:

- Define the 4 main information types and their use cases.
- Get a high-level overview of when module developers should expect to encounter each data type.

By the end of this tutorial you should be able to recognize each of the 4 main information types used in Drupal.

## Goal

To differentiate and understand the roles of content, session, state, and configuration data in Drupal.

## Prerequisites

- None

## Understanding Drupal's data types

The 4 types of information in Drupal are distinct because of their methods of storage and retrieval. We'll also distinguish them by how they are used in a Drupal site (their use cases).

### Content

Content is the most recognizable data type in Drupal, represented through content entities like nodes (articles, blog posts), users, and taxonomy terms. It's the primary data displayed on the site and is stored in the database. It's searchable and manageable through Drupal's administrative interface. As module developers, we'll use the Entity API to list, update, and alter user-generated content entities.

### Configuration

Configuration data defines the structure and behavior of the site across environments. This includes site settings, content types, field definitions, and views configurations. Unlike content, configuration data is meant to be deployed across environments, from development to production, ensuring consistency in site structure and behavior. As module developers, we'll use the Configuration API to save and retrieve settings for our modules.

### Session

Session data pertains to individual user sessions, maintaining information such as authentication status and temporary user data across page requests. Sessions are used to personalize user experiences and control access by identifying logged-in users and their permissions. As module developers, we'll use the session management subsystem to personalize the experience based on the current user.

### State

State data stores temporary, state-specific information not requiring backup, such as the last time cron jobs were executed or the time of the most recent site maintenance. Unlike configuration data, state data is meant to be transient and specific to a particular state of the site. As module developers, we'll use the State API to keep track of transient data.

## How each data type is managed

Module developers write code that interacts with all of these data types. Knowing the difference between them will help inform which data API to use and when. Each serves a distinct purpose.

- **Content** is dynamic, user-facing data that is managed via the Entity API.
- **Configuration** data outlines the site's structure and settings, shared across environments for consistency, and is managed via the Entity API and the configuration management workflow.
- **Session** data is temporary and user-specific, used to personalize experiences and enforce access control. It's managed through the session subsystem (part of Symfony's HttpFoundation component).
- **State** data stores transient information specific to the site's current state and environment, and isn't exported nor deployed. It's managed via the State API.

## Recap

This tutorial outlined the 4 main data types in Drupal: content, configuration, session, and state. Each plays a unique role in the structure and functionality of a Drupal site, from managing user interactions and content to configuring site settings and behavior. Recognizing and leveraging these data types appropriately is essential for building and managing robust, scalable, and secure Drupal sites.

## Further your understanding

- While navigating a Drupal site can you identify examples of each of the 4 data types in use?
- How might the choice between storing information in state vs. configuration impact a site's deployment process?
- Consider a scenario where using session data could enhance user experience on a Drupal site. What are the security considerations?

## Additional resources

- [1.5. Concept: Types of Data](https://drupalize.me/tutorial/user-guide/understanding-data) (Drupalize.Me)
- [Information types](https://api.drupal.org/api/drupal/core%21core.api.php/group/info_types/) (api.drupal.org)
- [Entity API](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/group/entity_api) (api.drupal.org)
- [Configuration API](https://www.drupal.org/docs/drupal-apis/configuration-api) (Drupal.org)
- [State API](https://www.drupal.org/docs/drupal-apis/state-api) (Drupal.org)
- [Sessions topic](https://api.drupal.org/api/drupal/core!core.api.php/group/session) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Concept: Configuration API](/tutorial/concept-configuration-api?p=3243)

Clear History

Ask Drupalize.Me AI

close
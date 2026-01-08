---
title: "Concept: Permissions"
url: "https://drupalize.me/tutorial/concept-permissions?p=3236"
guide: "[[drupal-module-developer-guide]]"
---

# Concept: Permissions

## Content

Permissions in Drupal control access to features and functions. Modules define permissions, which allow site administrators to grant or restrict access based on user roles. As a module developer, you'll create new permissions to restrict access to your module's custom features, independent of existing permissions defined by other modules.

In this tutorial, we'll:

- Explore how and where permissions are defined within a module.
- Discuss the concept of static and dynamic permissions in Drupal.

By the end of this tutorial, you'll have a clear understanding of how permissions function in Drupal and their implementation in modules.

## Goal

Understand how permissions are defined and managed within Drupal modules.

## Prerequisites

- [Chapter 7. Managing User Accounts](https://drupalize.me/series/user-guide/user-chapter) (Drupal User Guide)

## Understanding permissions in Drupal

Permissions in Drupal are part of its access control system, and determine whether a user can perform specific actions or access content. Permissions, usually assigned to roles, are inherited by users with those roles.

Modules define permissions in a *MODULE\_NAME.permissions.yml* file and use conditional logic to check if a user possesses a required permission.

### Static permissions

Static permissions are defined by modules and are immutable. We declare them in our module's *MODULE\_NAME.permissions.yml* file. This file contains a list of permissions with a machine-readable name, a human-readable title, and an optional description.

For instance, a module could define a permission for managing weather forecasts as follows:

```
manage weather forecast:
   title: 'Manage weather forecasts'
   description: 'Allows users to create, edit, and delete weather forecasts.'
```

### Dynamic permissions

Often the information required to define a permission is not static, or readily cacheable. Modules can define a permission callback in the *MODULE\_NAME.permissions.yml* file. For instance, a module that manages weather data for multiple locations might generate permissions for each location allowing for more granular access control.

## Permission checking

Modules perform permission checks to control access to functionalities. These checks can occur in various contexts:

- Permission checks can be specified directly in route definitions. For example, deny access to the entire form if the user doesn't have permission to edit weather forecast.
- Permissions can be used anywhere `AccessResult` objects are used via `\Drupal\Core\Access\AccessResult::allowedIfHasPermission`.
- PHP logic can perform more granular permissions checks within the logic of a service or controller using `\Drupal\Core\Session\AccountInterface::hasPermission`. For example, display a link to edit the forecast alongside the public display of the forecast if the current user has permission to edit it.

## Recap

This tutorial highlighted key aspects of permissions in Drupal modules, including the difference between static and dynamic permissions and their module-level definitions. We also learned the importance of permission checks in maintaining effective access control.

## Further your understanding

- When should you create a new permission instead of using an existing one from another module?
- Imagine a scenario where dynamic permissions are more suitable than static ones. How would that be structured?

## Additional resources

- [User Guide: Managing User Accounts](https://drupalize.me/series/user-guide/user-chapter) (Drupalize.Me)
- [User accounts, permissions, and roles](https://api.drupal.org/api/drupal/core%21core.api.php/group/user_api/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define a Menu Item](/tutorial/define-menu-item?p=3236)

Next
[Define a New Permission](/tutorial/define-new-permission?p=3236)

Clear History

Ask Drupalize.Me AI

close
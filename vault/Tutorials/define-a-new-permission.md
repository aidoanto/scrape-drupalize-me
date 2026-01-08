---
title: "Define a New Permission"
url: "https://drupalize.me/tutorial/define-new-permission?p=3236"
guide: "[[drupal-module-developer-guide]]"
---

# Define a New Permission

## Content

Modules can define custom permissions to restrict access to specific routes or page sections. This control allows module developers to provide granular access while enabling site administrators to manage user privileges. We'll add a `view weekly weather` permission via the *anytown* module to limit access to the weather page.

In this tutorial, we'll:

- Create an *MODULE\_NAME.permissions.yml* file.
- Define a new permission.
- Use the new permission to restrict access to a route.

By the end of this tutorial, you should be able to define a new permission in a module and use it to control access to a route.

## Goal

Add a `view weekly weather` permission to manage access to the weather forecast page.

## Prerequisites

- [Concept: Permissions](https://drupalize.me/tutorial/concept-permissions)
- [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page)
- [Assigning Permissions to a Role](https://drupalize.me/tutorial/user-guide/user-permissions?p=2441)

## Video tutorial

Sprout Video

## Define a custom permission

We'll define a `view weekly weather` permission and associate it with the `anytown.weather_page` route to restrict access to the `/weather` page.

**Tip:** Use `drush generate permissions` to add new permissions. Remember to update any code that references these permissions.

### Create a permissions file

Create the *anytown.permissions.yml* file in the root of your module directory.

### Define a new permission

Add the following to the *anytown.permissions.yml* file:

```
# Permissions for anytown module.

# Permission names need to be unique.
view weekly weather:
  title: 'View weekly weather'
  description: 'Allows the user to view the weekly weather at the market.'
```

This code defines a new permission named `'view weekly weather'`. When used in code, permissions are referenced by their name as a string. When listed in the administrative UI, the human-readable `title` and `description` are used.

### Update the route definition to use the permission

Update the route created in [Create a Route for the Weather Page](https://drupalize.me/tutorial/create-route-weather-page) to use the new permission by modifying the *anytown.routing.yml* file.

```
# Route definitions for the anytown module.

# Each route needs a unique identifier. We recommend prefixing the route name
# with the name of your module. Indented under the route name is the definition
# of the route. A routing.yml file can contain any number of routes.
anytown.weather_page:
  # The URL path where this page will be displayed. {style} represents a
  # placeholder and will be populated by whatever is entered into that position
  # of the URL. Its value is passed the controller's build method.
  path: '/weather/{style}'
  defaults:
    # Title of the page used for things like <title> tag.
    _title: 'Weather at the market'
    # Defines which method, on which class, should be called to retrieve the
    # content of the page.
    _controller: '\Drupal\anytown\Controller\WeatherPage::build'
    # Default value for {style} if it's not present.
    style: 'short'
  requirements:
    # What permissions a user needs to have in order to view this page.
    _permission: 'view weekly weather'
```

This change adds a permission check for `view weekly weather` to the `anytown.weather_page` route.

### Clear the cache

Permissions are cached, so you'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) before Drupal will find your new permission or any changes to existing permissions.

### Verify it works

To test the new permission, assign it to a role, sign in as a user with that role, and then navigate to the */weather* page. Ensure users with the `view weekly weather` permission can view it, while others cannot.

## Recap

This tutorial showed how to add a new permission to the *anytown* module and use it to control access to a specific route. We modified both the permissions and route files to add this permission check.

## Further your understanding

- What are the pros and cons of using a custom permission to control access to the weather page?
- If you wanted to use `access content` for the route and `view weekly weather` for specific parts of the page, what changes would you make?

## Additional resources

- [Define Permissions for a Module](https://drupalize.me/tutorial/define-permissions-module) (Drupalize.Me)
- [`PermissionHandler` class documentation covers the .permissions.yml file](https://api.drupal.org/api/drupal/core!modules!user!src!PermissionHandler.php/class/PermissionHandler/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Permissions](/tutorial/concept-permissions?p=3236)

Clear History

Ask Drupalize.Me AI

close
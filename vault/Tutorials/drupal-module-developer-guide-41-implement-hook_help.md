---
title: "Implement hook_help()"
url: "https://drupalize.me/tutorial/implement-hookhelp?p=3240"
guide: "[[drupal-module-developer-guide]]"
order: 41
---

# Implement hook_help()

## Content

To use a hook in a Drupal module, we need to add a class with a method for each hook we want to implement and a `#[Hook]` attribute that declares which specific hook we're implementing. Each hook has unique arguments and an expected return value. In this tutorial, we'll walk through the process of implementing a hook by adding end-user help text for the *anytown* module, which Drupal's administrative UI will display. The process we'll use here applies to any hook implementation.

In this tutorial, we'll:

- Locate the documentation for `hook_help()`.
- Implement the hook in the *anytown* module.
- Verify our hook implementation.

By the end, you'll have implemented `hook_help()` to display help text in the Drupal UI.

## Goal

Add an Anytown module overview listed on *admin/help* by implementing `hook_help()`.

## Prerequisites

- [Concept: What Are Hooks?](https://drupalize.me/tutorial/concept-what-are-hooks)
- [Discover Hooks and Their Documentation](https://drupalize.me/tutorial/discover-hooks-and-their-documentation)

## Video tutorial

Sprout Video

## Adding a module overview for the Anytown module

The Help module defines `hook_help()` which allows other modules to provide "module overviews" which are listed on the administrative Help page at *admin/help*. This is an example of a hook that gathers information from other modules and uses it internally. We'll use it to add documentation about our module's features.

In this tutorial, we'll implement `hook_help()` to practice implementing hooks in a module. We've already seen `hook_theme()` when we added in [Add a Template File](https://drupalize.me/tutorial/add-template-file). And we'll see more hooks later in this guide, for example, in [Concept: Altering Existing Forms](https://drupalize.me/tutorial/concept-altering-existing-forms) and [Reset Vendor Status with Cron](https://drupalize.me/tutorial/reset-vendor-status-cron).

## Implementing a hook

Here's an overview of the process of implementing a hook:

1. Identify the appropriate hook.
2. Find its documentation and reference implementation.
3. Copy the reference to your module.
4. Add your custom logic.

### Locate the documentation for `hook_help()`

Find `hook_help()` documentation on [api.drupal.org](https://api.drupal.org/api/drupal/) or in the *help.api.php* file. The documentation tells us that `hook_help()` requires 2 arguments:

- `$route_name`: Use the route name for page-specific help or `help.page.MODULE` (e.g. `help.page.anytown`) to add a module overview to the administrative Help page (*admin/help*).
- `$route_match`: The current route match.

The function should return a render array, localized string (wrapped in `t()`), or renderable object.

### Define a new file for your hook code

Create the file *src/Hook/AnytownHelp.php* and add some boilerplate code to it.

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

class AnytownHelp {

}
```

### Copy and paste the reference implementation

Paste the `hook_help()` reference implementation from the documentation into the `AnytownHelp` class. This ensures you're using the correct arguments and type hinting. Then delete the `hook_` prefix from the function name, and add the `public` keyword, so it's a proper class method.

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

use Drupal\Core\Routing\RouteMatchInterface;

class AnytownHelp {

  /**
   * Implements hook_help().
   */
  public function help($route_name, RouteMatchInterface $route_match) {

  }

}
```

### Add a `#[Hook]` attribute to the method

For the attribute, you'll need to know the *short name* of the hook. This can be determined by removing the `hook_` prefix from the full hook name.

So `hook_help` has a short name of `help`.

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

use Drupal\Core\Hook\Attribute\Hook;
use Drupal\Core\Routing\RouteMatchInterface;

class AnytownHelp {

  /**
   * Implements hook_help().
   */
  #[Hook('help')]
  public function help($route_name, RouteMatchInterface $route_match) {

  }

}
```

### Add your custom code

Update the `help()` method to match the following code:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

use Drupal\Core\Hook\Attribute\Hook;
use Drupal\Core\Routing\RouteMatchInterface;
use Drupal\Core\Session\AccountProxyInterface;

class AnytownHelp {

  /**
   * Current user service.
   *
   * @var \Drupal\Core\Session\AccountProxyInterface
   */
  private $currentUser;

  public function __construct(AccountProxyInterface $current_user) {
    $this->currentUser = $current_user;
  }

  /**
   * Implements hook_help().
   */
  #[Hook('help')]
  public function help($route_name, RouteMatchInterface $route_match) {
    if ($route_name === 'help.page.anytown') {
      $name = $this->currentUser->getDisplayName();
      return '<p>' . t("Hi %name, the anytown module provides code specific to the Anytown Farmer's market website. This includes the weather forecast page, block, and related settings.", ['%name' => $name]) . '</p>';
    }
  }

}
```

This contains our new implementation of `hook_help`. In the custom code, we:

- Checked the value of `$route_name`. If it matches the pattern, `help.page.anytown`, we return the string of text we want to display on the help page. (We could have returned a render array instead.)
- Accessed the `current_user` service via using dependency injection. Drupal will recognize the type hinted arguments to the constructor method and autowire the appropriate services from the container. We learned about services in [Use a Service in a Controller](https://drupalize.me/tutorial/use-service-controller).
- Created and returned a localized string by wrapping our output with the `t()` function.

### Verify it works

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) since we added a new hook. Ensure the core *Help* module is installed on your site. Then, in the *Manage* administration menu navigate to *Help* (*admin/help*), and choose *Anytown* from the *Module overviews* section. On the resulting page you should see the help text you added in `anytown_help()`.

Image

![Screenshot shows text for anytown module overview](../assets/images/hooks-events--hooks-implement_help-page.png)

See an example of hook\_help() implemented using a function (Drupal 11.0 and earlier).

Create the file *anytown.module*, if it doesn't already exist, in the root directory of your module. Then add the following code:

```
<?php

/**
 * @file
 * Hook implementations for anytown module.
 */

use Drupal\Core\Routing\RouteMatchInterface;

/**
 * Implements hook_help().
 */
function anytown_help($route_name, RouteMatchInterface $route_match) {
  // Primary help page for the module will be at "help.page.$modulename".
  if ($route_name === 'help.page.anytown') {
    // Example of accessing a service via a hook, where you can't perform
    // dependency injection.
    /** @var \Drupal\Core\Session\AccountProxyInterface $current_user */
    $current_user = \Drupal::service('current_user');

    return '<p>' . t("Hi %name, the anytown module provides code specific to the Anytown Farmer's market website. This includes the weather forecast page, block, and related settings.", ['%name' => $current_user->getDisplayName()]) . '</p>';
  }
}
```

In this example, pay close attention to the function name, which is derived by taking the hook name `hook_help()` and replacing the `hook` prefix with the name of the module `anytown`.

## Recap

In this tutorial, we implemented `hook_help()` in the *anytown* module in order to provide help text for the module in the Drupal user interface. We practiced the steps required to implement a hook, and saw an example of how to read the hook's documentation and reference implementation to help get us started.

## Further your understanding

- Where else can you find examples of hook usage beyond the *MODULE\_NAME.api.php* file?
- How might you extend this `hook_help()` implementation to include help text on specific pages like */weather*?

## Additional resources

- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook) (Drupalize.Me)
- [Hooks](https://api.drupal.org/api/drupal/core%21core.api.php/group/hooks/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Discover Hooks and Their Documentation](/tutorial/discover-hooks-and-their-documentation?p=3240)

Clear History

Ask Drupalize.Me AI

close
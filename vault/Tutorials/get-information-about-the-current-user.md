---
title: "Get Information about the Current User"
url: "https://drupalize.me/tutorial/get-information-about-current-user?p=3252"
guide: "[[output-and-format-data-code]]"
---

# Get Information about the Current User

## Content

Want to know if the person that's viewing your custom block is authenticated? Need to change the elements visible on the page based on a user's permissions or roles? Want to display a welcome message for users returning to your site?

All of these things require knowing who the user is that's currently accessing a page. This can be accomplished by using the `current_user` service to load an object that contains information about the current user as well as methods for checking permissions and retrieving additional information.

In this tutorial we'll:

- Define what "current user" means
- Use the `current_user` service to retrieve an implementation of `\Drupal\Core\Session\AccountInterface`
- Retrieve information about, and check the permissions of, the current user
- Add cacheability metadata when rendering user-specific output

By the end of this tutorial you should be able to retrieve and make use of information about the application's current user in order to perform logic in your code that customizes the response for different users.

## Goal

Use the `current_user` service to retrieve an object that represents the current user.

## Prerequisites

- [Discover and Use Existing Services](https://drupalize.me/tutorial/discover-and-use-existing-services)

## Working with the current user

Accessing information related to the user that is currently accessing your application requires retrieving an object that represents the user and then using the provided methods to retrieve the desired information. This works for both authenticated (logged in) and anonymous users.

Retrieving the current user object can be achieved via the `current_user` service provided by `Drupal\Core\Session\AccountProxy`.

"Current user" is specific to the request that's currently being processed. Your Drupal application could have any number of different users accessing pages simultaneously. Juampy from Madrid and Alice from New York could both be accessing the site as the anonymous user at the same time. But "current user" is context-sensitive and depends on who initiated the request being fulfilled.

## Use the `current_user` service

```
$current_user = $this->container()->get('current_user');
```

Read more about [discovering and using existing services](https://drupalize.me/tutorial/discover-and-use-existing-services).

Any controller extending `\Drupal\Core\Controller\ControllerBase` can use the `ControllerBase::currentUser()` helper method.

## Global access

When dependency injection isn't an option, you can use the global `Drupal` object which has a shortcut for accessing the `current_user` service.

```
$current_user = \Drupal::currentUser();
```

## Common use cases

After retrieving the `$current_user` object here some common things you might do next.

### Get the name of the current user

```
$current_user_name = $current_user->getDisplayName();
```

### Check if the current user is authenticated (logged in) or anonymous

```
$authenticated = $current_user->isAuthenticated();
$anonymous = $current_user->isAnonymous();
```

### Check if the current user has a specific permission

```
$administer_content = $current_user->hasPermission('administer content');
```

## Get the complete `User` entity

All of the above techniques do not supply a complete `User` entity. Instead, they return instances of `\Drupal\Core\Session\UserSession`. If you want additional information about a user (for example, profile fields attached to the account), or if you want to make changes to the account, then you need to load the full `\Drupal\user\Entity\User` object.

Example:

```
use \Drupal\user\Entity\User;
$current_user = \Drupal::currentUser();
$account = User::load($current_user->id());
$account->setEmail('[email protected]');
$account->save();
```

## Add cacheability metadata when rendering user-specific output

When you render information about the current user—such as a personalized welcome message—your render array needs the correct cacheability metadata so Drupal can vary and invalidate the output properly. Although you can manually add `#cache` contexts and tags, a simpler and more reliable approach is to use `Renderer::addCacheableDependency()`. This method automatically merges the cacheability metadata from any object that implements `CacheableDependencyInterface`, such as the current user's `User` entity.

Example:

```
use Drupal\user\Entity\User;

// Retrieve the full User entity for the current user.
$current_user = \Drupal::currentUser();
$user = User::load($current_user->id());

$build = [
  '#markup' => t('Welcome back, @name!', ['@name' => $user->getDisplayName()]),
];

// Add cacheability metadata from the User entity.
\Drupal::service('renderer')->addCacheableDependency($build, $user);

return $build;
```

By passing the `User` entity to `addCacheableDependency()`, Drupal automatically adds the correct cache contexts (so each user sees their own name) and cache tags (so the output updates if the user changes their account information). This avoids manually adding cache metadata and helps ensure the rendered output stays accurate.

## How this compares to manually adding cacheability metadata

Before `addCacheableDependency()` was commonly used, you might see examples that manually added cache contexts and tags to the render array. This still works and helps illustrate what Drupal is doing under the hood, but it's easier to make a mistake or forget required metadata.

```
$current_user = \Drupal::currentUser();

$build['example'] = [
  '#markup' => t('Hello @name', ['@name' => $current_user->getDisplayName()]),
  '#cache' => [
    // Vary the output by user so each visitor sees their own name.
    'contexts' => ['user'],

    // Invalidate when the user updates their account.
    'tags' => $current_user->getCacheTags(),
  ],
];

return $build;
```

This version shows the two important pieces Drupal needs to cache personalized output correctly:

- Cache contexts vary the rendered result by different users.
- Cache tags ensure the output is invalidated when the associated user changes.

However, using `addCacheableDependency()` is recommended because it collects and merges the correct metadata automatically.

## Recap

In this tutorial you learned how to use the `current_user` service to retrieve information about the user accessing your application. You saw how to check authentication status, permissions, and user properties, and how to load the full `User` entity when needed. You also learned how to add the correct cacheability metadata to user-specific output using `addCacheableDependency()` so Drupal can vary and invalidate the markup correctly.

## Further your understanding

- Can you create a controller that displays the name of the currently logged-in user at */whoami*?
- Update the controller to use `addCacheableDependency()` so the output updates when a user changes their display name.

## Additional resources

- [AccountInterface](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Session%21AccountInterface.php/interface/AccountInterface) (api.drupal.org)
- [Issue: global $user deprecated in favor of current\_user service](https://www.drupal.org/node/2032447) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Generate URLs and Output Links](/tutorial/generate-urls-and-output-links?p=3252)

Next
[Use #access to Show/Hide Elements in a Render Array](/tutorial/use-access-showhide-elements-render-array?p=3252)

Clear History

Ask Drupalize.Me AI

close
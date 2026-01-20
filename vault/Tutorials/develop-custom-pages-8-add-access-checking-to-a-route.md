---
title: "Add Access Checking to a Route"
url: "https://drupalize.me/tutorial/add-access-checking-route?p=3134"
guide: "[[develop-custom-pages]]"
order: 8
---

# Add Access Checking to a Route

## Content

Every route should define its access control parameters. When you define routes in a module, you can limit who has access to those routes via different access control options. Route-level access control applies to the path. If your route defines a path like `/journey/example`, the access control configuration will determine whether to show the current user the page at the path defined by the route, or to have Drupal serve an "HTTP 403 Access Denied" message instead.

In this tutorial we'll look at different ways of adding access control to a route including:

- Access based on the current user's *roles and permissions*
- Access based on custom logic in a *callback method*
- Logic in an *access checker service*

By the end of this tutorial, you should be able to add access control logic to your custom routes that will meet any requirement.

## Goal

Configure a route with access control that determines who can view the page, and who should see an "access denied" message.

## Prerequisites

- [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller)
- [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes)

## Overview: Ways to perform access checking on routes

Every route should define access control. Here are the ways to perform access checking on routes. You may select a link to go to that section.

- [Permission based](#grant-access-based-on-permissions): You specify a permission(s), and only users with that permission will be granted access.
- [Role based](#grant-access-based-on-roles): You specify a role(s) and only users with that role will be granted access.
- [Authenticated users only](#grant-or-deny-access-to-any-logged-in-user): Only logged-in users will be given access.
- [Entity CRUD operation based](#entity-based-access-control): In cases where an entity is part of the route access will be granted if the user has permission to perform the specified operation (e.g. "edit" or "view all revisions") on the specified entity.
- [Bypass access control for a route](#bypass-access-control-for-a-route): You may want to bypass access control for a route, in which case, you'll need to explicitly declare that in your route.
- [Custom access control logic](#custom-access-control-logic): Access is granted based on a callback that performs custom logic.
  - [Custom access via a method on the controller class](#custom-access-via-a-method-on-the-controller-class)
  - [Custom access via an access checker service](#custom-access-via-an-access-checker-service)
- [Multiple access control requirements](#multiple-access-control-requirements)

Let's take a look at examples of each of these access control methods.

## Grant access based on permission(s)

Use the `requirements._permission` option to limit access to a route based on a user's **permissions**.

The following example updates the `journey.example` route from [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller) so that the path can only be accessed by a user who has the `access content` permission.

Example: *journey.routing.yml*:

```
journey.example:
  path: '/journey/example'
  defaults:
    _controller: '\Drupal\journey\Controller\ExampleController::build'
    _title: 'Routing Example'
  requirements:
    # Require that a user has the 'access content' permission to view
    # this route.
    _permission: 'access content'
```

### Specifying multiple permissions

**Separate multiple permissions** with a comma ("AND" logic) or a plus sign ("OR" logic).

| Access check | Separator | Example |
| --- | --- | --- |
| Require **ALL** listed permissions | `,` | `_permission: 'access content overview,view all revisions` |
| Require **ANY** listed permissions | `+` | `_permission: 'access content overview+view all revisions` |

To require the user has **all** listed permissions separate permissions with a comma. For example, `_permission: 'access content overview,view all revisions` means the current user must have `access content overview` **AND** `view all revisions` permissions to access the route.

To allow access to a user with **any** of the listed permissions, separate permissions with a plus sign. For example, `_permission: 'access content overview+view all revisions` means the current user must have `access content overview` **OR** `view all revisions` permissions, in order to access the route.

Using permissions for access control allows [user access to be configured by a site administrator](https://drupalize.me/course/user-guide/user-chapter).

### Permission-based access with custom logic

If you have custom access checking logic, but also want to allow a site administrator to be able to configure access to the route, you can [define a new permission in your module](https://drupalize.me/tutorial/define-permissions-module) and then reference that in your route definition. This could be combined with custom access checking (see below). This enables you to link the access checking service to the *permission* rather than directly to the *route*.

## Grant access based on role(s)

Use the `requirements._role` option to limit access to a route based on *roles*.

The following example updates the `journey.example` route from [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller) so that it can only be accessed by a user who is logged in, and has the *administrator* role.

Example *journey.routing.yml*:

```
journey.example:
  path: '/journey/example'
  defaults:
    _controller: '\Drupal\journey\Controller\ExampleController::build'
    _title: 'Routing Example'
  requirements:
    # Require that a user has the 'administrator' role in order to view
    # this route.
    _role: 'administrator'
```

### Specifying multiple roles

**Separate multiple roles** using a comma ("AND" logic), or a plus sign ("OR" logic).

| Access check | Separator | Example |
| --- | --- | --- |
| Require **ALL** listed roles | `,` | `_role: 'administrator,owner` |
| Require **ANY** listed roles | `+` | `_role: 'administrator+owner` |

- To require the user has **all** the listed roles, separate roles with a **comma**.
  - For example, `_role: 'administrator,owner` means current user must belong to **both** `administrator` **AND** `owner` roles.
- To allow access to a user in **any** of the listed roles, separate roles with a **plus** sign.
  - For example, `_role: 'administrator+owner` means current user must belong to **either** `administrator` **OR** `owner roles.

### Permission-based or role-based route access checking?

You might be wondering, should I use *permission-based* or *role-based* access checking for my route? Here's some food for thought:

When using role-based access, keep in mind that **roles are configuration**, and can be added or removed via the administrative UI. *There is no guarantee* that a role like "editor" will exist, because roles are dependent on the site's configuration. A role-based access use case might be suitable for site-specific custom code. However, in most cases, using **permission-based access is probably better** because it's less fragile. [Learn how to define custom permissions in a module](https://drupalize.me/tutorial/define-permissions-module).

## Grant (or deny) access to any logged-in user

| Access check | Option |
| --- | --- |
| Authenticated users only | `requirements._user_is_logged_in: 'TRUE'` |
| Anonymous users only | `requirements._user_is_logged_in: 'FALSE'` |

You can grant access to any authenticated user using the `requirements._user_is_logged_in: 'TRUE'` option. Or, alternatively, require that the user is anonymous with `requirements._user_is_logged_in: 'FALSE'` (thereby denying access to logged-in users).

<a name="bypass-access-control-for-a-route" id-"bypass-access-control-for-a-route">

## Bypass access control for a route

You can bypass access control and have the route be always accessible **to everyone** using the `requirements._access` configuration option.

The following example updates the `journey.example` route from [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller) so that its path can be accessed by anyone.

Example *journey.routing.yml*:

```
journey.example:
  path: '/journey/example'
  defaults:
    _controller: '\Drupal\journey\Controller\ExampleController::build'
    _title: 'Routing Example'
  requirements:
    # Bypass any access control for this route. Note that 'TRUE' needs to be in
    # single quotes for this to be valid.
    _access: 'TRUE'
```

## Entity based access control

In the case where a route is for an entity, you might want to base the access control off the specific entity type. For example, a user who has permission to edit their own nodes but not another user's nodes. To do this you can use the `requirements._entity_access`, and `requirements._entity_create_access` configuration options.

This requires understanding how *parameters* and *upcasting* work in routes.

Example:

```
example.upcasting:
  path: '/examples/upcasting/{node}'
  defaults:
    _title: 'Upcasting Example'
    _controller: '\Drupal\menu_example\Controller\MenuExampleController::upcastingExample'
  requirements:
    # Limit access to users who have the 'view' permission for the 'node' that
    # is currently being used in the route.
    _entity_access: 'node.view'
    node: '\d+'
  options:
    parameters:
      node:
        type: 'entity:node'
```

The `_entity_access` requirement must follow the pattern `'{slug}.{operation}'`. Where `{slug}` is an entity type ID, but it can be any slug defined in the route. The route match parameter corresponding to the slug is checked to see if it is "entity-like". (Does it implement `EntityInterface`?) The `{operation}` is one of `view`, `update`, or `delete`. (To check "create" access, you'd use `_entity_create_access`; see the "Entity create access" section below.)

In the above example, the `node` is the `{slug}`, and `node.view` says, "Check that the current user has "view" access for the node object that is currently being used as the `{node}` parameter in this path: `'/examples/upcasting/{node}'`". The actual access checking logic is performed by the access handler for the entity. This is usually defined as part of the entity type's annotation.

Learn more about how parameters and upcasting work in [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes).

### Entity create access

To check if a user has "create" access, use `_entity_create_access`. This supports specifying a bundle as either a static value or as a reference to a given route parameter. This example from the Drupal core Taxonomy module illustrates this:

```
taxonomy.vocabulary_add:
  path: '/admin/structure/taxonomy/add'
  defaults:
    _entity_form: 'taxonomy_vocabulary'
  requirements:
    _entity_create_access: 'taxonomy_vocabulary'

taxonomy.term_add:
  path: '/admin/structure/taxonomy/manage/{taxonomy_vocabulary}/add'
  defaults:
    _controller: '\Drupal\taxonomy\Controller\TaxonomyController::addForm'
  requirements:
    # Format is {entity_type}:{slug_from_route}. So this would resolve to
    # something like taxonomy_term:42.
    _entity_create_access: 'taxonomy_term:{taxonomy_vocabulary}'
```

## Custom access control logic

If you need to write custom PHP logic to calculate whether the current user should be able to access a route you can do so either via a custom access checker service, or a callback to a method on the controller. You should learn about both approaches and pick the one that's right for your use case.

As an example, let's say we want to limit access to the route to users who have a username that is 5 or more characters long. (It's a contrived example, but lets us show how access checking works without a bunch of unrelated code.)

### Custom access via a method on the controller class

One approach is to add a custom access callback method to the controller that's responsible for the route. This is a good approach if your access logic is only ever going to apply to this route. It's a little simpler, and keeps the code all in one place.

### Add `_custom_access` configuration for the route

First, you'll need to add a `requirements._custom_access` entry that points to a callback that is responsible for determining access.

Example from *journey.routing.yml*:

```
journey.example_access:
  path: '/journey/example-access'
  defaults:
    _controller: '\Drupal\journey\Controller\ExampleControllerCustomAccess::build'
    _title: 'Routing Example with Custom Access Control'
    # This is an example of passing a static value to both the build and access
    # methods.
    min_username_length: 5
  requirements:
    _custom_access: '\Drupal\journey\Controller\ExampleControllerCustomAccess::access'
```

The value of `_custom_access` should be the name of a method on the same class as the primary `_controller` that will perform the access checking. The method should return an instance of `\Drupal\Core\Access\AccessResultInterface`.

In our example, we make the minimum username length configurable by having the `access` method take an argument, and then using a static route parameter to set a value for that argument via the `min_username_length` option. Learn more about route parameters in [Overview: Parameters and Value Upcasting in Routes](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes).

### Define the access callback method

Next, define the method you just configured above. This will be a method on the same class as the `build()` method that returns content for the route. The one requirement is that the specified method must return an instance of `\Drupal\Core\Access\AccessResultInterface`.

Here's an example of *src/Controller/ExampleControllerCustomAccess.php* that provides both `build` and `access` methods:

```
<?php
/**
 * @file
 * Example of extending ControllerBase to create a new controller.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\Access\AccessResult;
use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Session\AccountInterface;

class ExampleControllerCustomAccess extends ControllerBase {

  /**
   * Content callback for route.
   *
   * @param int $min_username_length
   *   Minimum username length.
   *
   * @return array
   */
  public function build(int $min_username_length) {
    $name = $this->currentUser()->getDisplayName();

    return [
      '#markup' => $this->t('<p>Welcome @name. You have a user name that is at least @min characters long!</p>', ['@name' => $name, '@min' => $min_username_length]),
    ];
  }

  /**
   * Custom access control callback.
   *
   * This callback is used to check access for the route that shows the content
   * of the build() method above. It is used as the value of the _custom_access
   * configuration for the journey.example-access route.
   *
   * @param \Drupal\Core\Session\AccountInterface $account
   *  The user trying to access the route.
   * @param int $min_username_length
   *   Minimum username length.
   *
   * @return \Drupal\Core\Access\AccessResultInterface
   *   The access result.
   */
  public function access(AccountInterface $account, int $min_username_length) {
    // When performing access control checks you should always work with the
    // supplied AccountInterface object and not Drupal::currentUser().
    $name = $account->getDisplayName();
    if (strlen($name) >= $min_username_length) {
      return AccessResult::allowed();
    }

    return AccessResult::forbidden('Your username is not long enough. Must be at least 5 characters.');
  }
}
```

In the example above, the `$account` argument for the `access` method will be automatically populated by the controller resolver, which is the code responsible for calling the controller. And the `$min_username_length` argument will be populated with the value from the route `options.min_username_length` configuration in the routing YAML file.

The `_custom_access` method can have arguments passed to it, similar to how the default `_controller` method does. The following optional arguments will be populated if they are properly type hinted:

- The [slugs](https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes), upcasting for which is performed in accordance with the parameters on the route's controller, not the access checker.
- `\Symfony\Component\Routing\Route $route`
- `\Drupal\Core\Routing\RouteMatch $route_match`
- `\Drupal\Core\Session\AccountProxy $account`

### Custom access via an access checker service

If your access control logic will be used in other places, and isn't just one-off logic for the specific controller, you should implement a custom access checker service. For example, if you wanted to use the same logic to limit access to multiple different routes. Or if you'll need to use the same logic to check access for a route and whether to display a custom block.

We'll reuse the example from above, and refactor it to be an access checker service instead. For a detailed look at defining new services see [Create a Service](https://drupalize.me/tutorial/create-service)

**Tip:** Use `drush generate access-checker` to generate code scaffolding to get you started.

### Create the service class

Create a new class to contain the logic for your access checker service. The file containing the class should be located in your module's *src/Access/* directory.

Example *src/Access/MinUsernameLengthAccessChecker.php*:

```
<?php

namespace Drupal\journey\Access;

use Drupal\Core\Access\AccessResult;
use Drupal\Core\Routing\Access\AccessInterface;
use Drupal\Core\Session\AccountInterface;

/**
 * Checks if passed parameter matches the route configuration.
 */
class MinUsernameLengthAccessChecker implements AccessInterface {

  /**
   * Custom access control logic. Check minimum username length.
   *
   * @param \Drupal\Core\Session\AccountInterface $account
   *  The user trying to access the route.
   * @param int $min_username_length
   *   Minimum username length.
   *
   * @return \Drupal\Core\Access\AccessResultInterface
   *   The access result.
   */
  public function access(AccountInterface $account, int $min_username_length) {
    // When performing access control checks, you should always work with the
    // supplied AccountInterface object and not Drupal::currentUser().
    $name = $account->getDisplayName();
    if (strlen($name) >= $min_username_length) {
      return AccessResult::allowed();
    }

    return AccessResult::forbidden('Your username is not long enough. Must be at least 5 characters.');
  }

}
```

The logic is the same as the previous example. And the resolution of arguments for the `access` method works the same way.

### Add an entry to the module's services YAML file

You'll need to tell Drupal about your new access checker service by adding an entry to the *MODULE.services.yml* file for your module.

Example *journey.services.yml*:

```
services:
  access_check.journey.min_username_length:
    class: Drupal\journey\Access\MinUsernameLengthAccessChecker
    tags:
      - { name: access_check, applies_to: _min_username_length }
```

Set the `name` service tags value to `access_check` so that Drupal knows this is an access checker service and that it'll implement `AccessInterface`. And use the `applies_to` tag to give your service a unique name, which will be used later in the route definition (under `requirements`). This should be prefixed with an underscore (`_`).

### Use the new access checker service in a route definition

Finally, we need to use the newly created access checker service in a route definition. Do this by adding the value of the `applies_to` service tag we set above nested under `requirements`.

Example *journey.routing.yml*:

```
journey.example_access_service:
  path: '/journey/example-access-service'
  defaults:
    _controller: '\Drupal\journey\Controller\ExampleControllerCustomAccess::build'
    _title: 'Routing Example with Custom Access Control'
    # Value passed to access checker service's 'access' method.
    min_username_length: 5
  requirements:
    # Name of the access checker service to use to check access for this route.
    # Defined by the applies_to service tag.
    _min_username_length: 'TRUE'
```

Access to the route will now be checked using the new service. And, code elsewhere in your site can make use of the service via the service container like `\Drupal::service('access_check.journey.min_username_length')` to perform access checking.

If you need to make use of other services in your access checker other than those that are made available by type hinting, you can use standard dependency injection. For example, if you needed the `http_client` service to perform your access checking logic you would:

- Update your service definition in the *.services.yml* file to include an arguments line like `arguments: ['@http_client']`.
- Add a constructor to your class that accepts the injected service.

  ```
  public function __construct(\GuzzleHttp\Client $client) {
    $this->client = $client;
  }
  ```

Learn more in [Discover and Use Existing Services](https://drupalize.me/tutorial/discover-and-use-existing-services).

## Multiple access control requirements

In the case where you've specified more than one access control requirement (for example, `_role` and `_custom_access`), the [`andIf` operation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Access%21AccessResultInterface.php/function/AccessResultInterface%3A%3AandIf/) is used to combine the results. All methods must return a result of `AccessResult::allowed()` or access will be denied.

## Recap

In this tutorial we learned how to add access control to a route using a variety of different approaches including permissions, roles, and custom logic. As well as discussed the use case, and advantages, of each approach. We learned that adding access control to a route starts with configuration in the *MODULE.routing.yml* file, and in some cases, also requires writing PHP code to perform custom logic.

## Further your understanding

- Could you refactor the above custom access control logic so that your module defined a new permission, and access to the route was based on that permission? Why would you choose that approach? See [Entity Access Control](https://drupalize.me/tutorial/entity-access-control) to learn more.
- Why is access control for routes with entities unique?

## Additional resources

- [Structure of routes](https://www.drupal.org/node/2092643#section-requirements) (Drupal.org)
- [Access checking on routes](https://www.drupal.org/docs/8/api/routing-system/access-checking-on-routes) (Drupal.org)
- [AccessResultInterface API documentation](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Access!AccessResultInterface.php/interface/AccessResultInterface/) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Define Permissions for a Module](/tutorial/define-permissions-module?p=3134)

Next
[How Drupal Turns a Request into a Response](/tutorial/how-drupal-turns-request-response?p=3134)

Clear History

Ask Drupalize.Me AI

close
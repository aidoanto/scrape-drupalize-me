---
title: "Overview: Parameters and Value Upcasting in Routes"
url: "https://drupalize.me/tutorial/overview-parameters-and-value-upcasting-routes?p=3134"
guide: "[[develop-custom-pages]]"
---

# Overview: Parameters and Value Upcasting in Routes

## Content

The routing system can get dynamic values from the URL and pass them as arguments to the controller. This means a single route with a path of `/node/{node}` can be used to display any node entity. Route parameters can be validated, and *upcast* to complex data types via *parameter conversion*. If you ever want to pass arguments to the controller for a route, you'll use parameters to do so.

In this tutorial we'll:

- Define what parameters (slugs, placeholders) are and what they are used for in a route definition.
- Explain how URL parameters are passed to a controller.
- Define parameter upcasting.

By the end of this tutorial, you should be able to explain how to define a route that uses parameters to pass dynamic values to the route controller, and explain how parameter upcasting works.

## Goal

Describe what route parameters are and provide enough detail about how they work that a developer can figure out how to define a route that uses parameters.

## Prerequisites

- [Overview: Routes, Controllers, and Responses](https://drupalize.me/tutorial/overview-routes-controllers-and-responses)

## Watch: Parameters and Value Upcasting in Routes

Sprout Video

## What are route parameters

Parameters are values passed from the route to the controller as arguments to the specified callback method.

Let's take the following route as an example:

```
entity.node.canonical:
  path: '/node/{node}'
  defaults:
    _title: 'Show a node'
    _controller: '\Drupal\node\Controller\NodeViewController::view'
  requirements:
    _permission: 'access content'
```

It is common to define routes where one or more parts of the path are variable. For example, if the URL to display a node is `/node/42`, the corresponding route is `/node/{node}`. The variable part (`{node}` in this example), also known as a *slug*, is used to create a PHP variable where the value from the URL is stored and passed to the controller. If a user visits `/node/42`, internally Drupal executes the `\Drupal\node\Controller\NodeViewController::view` method and passes `$node = '42'` as an argument to the method. The code can then figure out which node to load and display it.

Route parameters like `{node}` are also often referred to as a *slug* or a *placeholder* when defined as part of the route's `path` value.

Routes can define any number of parameters, but each of them can only be used once on each route (e.g. `/journey/{category}/page/{pageNum}`).

## Parameter validation

Parameter validation allows you to use **regular expressions** to validate the value present in a slug. This can be used to trigger an HTTP 404 in the case of a bad value. It provides the route matching system with a way to differentiate between 2 similar routes like `/blog/{slug}`, and `/blog/{pageNumber}`.

Validation is done in the `requirements` section of the route definition.

Example:

```
entity.node.canonical:
  path: '/node/{node}'
  defaults:
    _title: 'Show a node'
    _controller: '\Drupal\node\Controller\NodeViewController::view'
  requirements:
    _permission: 'access content'
    # REGEX, ensures the {node} slug is an integer like /node/42, and not
    # /node/foo-bar.
    node: '\d+'
```

## Default values and static parameters

In the previous example, the URL path is `/node/{node}`. If users visit */node/1*, it will match. But if they visit */node*, it will not match. As soon as you add a parameter to a route, it must have a value or an "HTTP 404 not found" error will be thrown.

You can make */node* work by adding a default value for the `{node}` parameter under `defaults` in the route definition.

You can also use this feature to pass arbitrary values to the controller as long as the default value name matches the name of an argument on the executed method.

Example of `defaults`:

```
entity.node.canonical:
  path: '/node/{node}'
  defaults:
    _title: 'Show a node'
    _controller: '\Drupal\node\Controller\NodeViewController::view'
    # Default to /node/42 if no value is provided for {node}.
    node: 42
    display_mode: 'full'
  requirements:
    _permission: 'access content'
    node: '\d+'
```

Corresponding controller `view` method:

```
class NodeViewController {
  public function view(NodeInterface $node, string $display_mode) {
    // Code goes here ...
  }
}
```

## Type hinted parameters

You can access a few additional, common, parameters by adding type hinted arguments to the controller method. These will be populated using reflection, and do not need to be listed in the YAML definition of the route:

- `\Symfony\Component\HttpFoundation\Request`: The raw Symfony request object. It is generally only useful if the controller needs access to the query parameters (e.g. `/example?page=2`) of the request.
- `\Drupal\Core\Routing\RouteMatchInterface`: The "route match" data from this request. This object contains various standard data derived from the request and routing process. To inspect the actual route (for example, to check for parameters, default values, or options), use `$route_match->getRouteObject()`.
- `\Psr\Http\Message\ServerRequestInterface`: The raw request, represented using the PSR-7 ServerRequest format.

Example:

```
class MyController {
  function getPage(\Symfony\Component\HttpFoundation\Request $request) {
    // Read /example?page=2.
    $page_number = $request->query->get('page');
  }
}
```

## Parameter upcasting

A common routing need is to convert the value stored in some parameter (e.g. an integer acting as the Node ID) into another value (e.g. the `Node` object that represents the node). This feature is called *upcasting*. It helps simplify code logic, enhances performance, and facilitates smoother integration of entities.

Let's analyze the example above and focus on the parameter upcasting process. If a user visits `/node/42`, internally, Drupal identifies that the value of the `{node}` slug is an entity ID, loads the corresponding `Node` entity, and **passes that object** to the `\Drupal\node\Controller\NodeViewController::view` method **instead of the raw value** of `'42'`.

This upcasting works for any entity type so long as the following conditions are satisfied:

- The `{slug}` in the path is a **valid entity type** like `{user}`, `{taxonomy_term}`, or `{block}`.
- The controller method called by the route must have **arguments whose names match that of the slug** (e.g. `{node}` matches with `$node`).
- The controller method's arguments are properly **type hinted** (e.g. `NodeInterface $node`).

For **non-entity parameters in a route** you can implement your own custom parameter converter service to perform upcasting of custom values. Though this is likely pretty rare. [Read more about how to accomplish this in the documentation on Drupal.org.](https://www.drupal.org/docs/8/api/routing-system/parameters-in-routes/implementing-custom-parameter-converters).

### Deep dive: how parameter-upcasting works

For a detailed explanation of how upcasting works keep reading, but it's okay to just know that it works without having to know the details. You already know enough to move onto the next tutorial where you will [practice using parameters in a route](https://drupalize.me/tutorial/use-parameters-route).

Consider a route with a path like `/examples/routing/{node}`, with configuration that states the `{node}` parameter must be an integer value. When the route is compiled, the `path` from the route definition is converted to a regular expression.

In our example this looks like:

```
^/examples/routing/(?P<node>\d+)$
```

The URL of the request is matched against all available routes in order to determine which one to use. For static routes with no slugs, once a match is found it'll move on to calling the controller. For routes with slugs in the path, that expression is evaluated and used to determine parameter values. When that expression is evaluated via `preg_match` it'll return an associative array of matches which will contain a key, `node`, with the value found in that position in the path, e.g. `$matches['node'] = 42`.

After parameter values have been extracted, the route object gets *enhanced*. This route enhancement is performed by services tagged with `route_enhancer`. They can be used to change the request before it's handed to the specified controller. One such service is the "param converter manager", `\Drupal\Core\ParamConverter\ParamConverterManager`. This route enhancer loads all available parameter converters, and then based on the route definition, will execute the appropriate converter(s).

The `\Drupal\Core\ParamConverter\EntityConverter`, for example, will take the Node ID in a URL like `/node/42`, know that it's a Node ID based on the route configuration, load the corresponding `Node` object, and return it. Effectively replacing the raw value `42` with the object returned by a call to `Node::load(42)`.

You can tell the routing system to upcast, or convert, a parameter using the `options.parameters.SLUG.type` configuration key. Where `{SLUG}` matches the name of the `{SLUG}` in the `path`.

Consider the following example:

```
dme.release_day_blog_post_stubs:
  path: '/node/{node}/release-day-stub'
  defaults:
    _title: 'Release day blog post stub'
    _controller: '\Drupal\dme\Controller\ReleaseDayBlogPostStubs::build'
  requirements:
    _entity_access: 'node.update'
  options:
    parameters:
      # Declare the {node} slug represents of an entity of type node.
      node:
        type: entity:node
```

In this example, the `ReleaseDayBlogPostStubs::build` method will receive an argument, `NodeInterface $node`. (Remember, the variable name has to match the slug name.)

Doing this with entities in Drupal is super common. So much so that Drupal allows you to skip the parameter type declaration in your route as long as the controller method type hints the arguments. This magic happens because the `\Drupal\Core\Entity\EntityResolverManager` will use reflection to determine the types of the parameters being passed from the route to the controller, and if they are type hinted as an entity type it will upcast the parameter. The route below has the exact same behavior as the one above so long as `ReleaseDayBlogPostStubs::build` has proper type hinting because the parameter type data configuration is automatically added to the route when it is compiled:

```
dme.release_day_blog_post_stubs:
  path: '/node/{node}/release-day-stub'
  defaults:
    _title: 'Release day blog post stub'
    _controller: '\Drupal\dme\Controller\ReleaseDayBlogPostStubs::build'
  requirements:
    _entity_access: 'node.update'
```

Example `ReleaseDayBlogPostStubs` definition:

```
namespace Drupal\dme\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\node\NodeInterface;

class ReleaseDayBlogPostStubs extends ControllerBase {

  public function build(NodeInterface $node) {
    // Code goes here ...
  }

}
```

In the case that a route has multiple slugs for the same entity type, you will have to include the full configuration for the parameter conversion to work.

Example:

```
dme.release_day_blog_post_stubs:
  # /node/42/release-day-stub/31337
  path: '/node/{node}/release-day-stub/{another_node}'
  defaults:
    _title: 'Release day blog post stub'
    _controller: '\Drupal\dme\Controller\ReleaseDayBlogPostStubs::build'
  requirements:
    _entity_access: 'node.update'
  options:
    parameters:
      node:
        type: entity:node
      another_node:
        type: entity:node
        # You can optionally limit upcasting by entity bundle, so only nodes of
        # type 'article' would be valid here.
        bundle:
          - article
```

## Recap

In this tutorial we learned what route parameters are and how they are defined. We saw how parameters in the path of a route can act like a wildcard so that one route can serve many different URLS. And that the values from the slug in a path can be passed to the route controller, validated, and upcast from a simple ID-like values to complex objects.

## Further your understanding

- What is the use case for parameters in a route? Can you give some examples how you might use it in your own code?
- How does the routing system handle figuring out what order to pass the parameters from the `path` to the controller's callback method?
- Practice using parameters in a route in the next tutorial: [Use Parameters in a Route](https://drupalize.me/tutorial/use-parameters-route).

## Additional resources

- [Symfony Route parameters documentation](https://symfony.com/doc/current/routing.html#route-parameters) (symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a Route and Controller](/tutorial/create-route-and-controller?p=3134)

Next
[Use Parameters in a Route](/tutorial/use-parameters-route?p=3134)

Clear History

Ask Drupalize.Me AI

close
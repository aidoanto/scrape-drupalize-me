---
title: "How Drupal Turns a Request into a Response"
url: "https://drupalize.me/tutorial/how-drupal-turns-request-response?p=3134"
guide: "[[develop-custom-pages]]"
---

# How Drupal Turns a Request into a Response

## Content

Every web framework, including Drupal, has basically the same job: provide a way for developers to map URLs to the code that builds the corresponding pages. Drupal uses Symfony's *HTTPKernel* component. Kernel events are dispatched to coordinate the following tasks:

- Process the incoming request
- Figure out what to put on the page
- Create a response
- Deliver that response to the user's browser

Knowing a bit more about how Drupal handles the request-to-response workflow will help you better understand how to use routes and controllers to create your own custom pages or deal with authentication, access checking, and error handling in a Drupal module.

In this tutorial we'll:

- Walk through the process that Drupal uses to convert an incoming request into HTML that a browser can read
- See how the Symfony `HTTPKernel` helps orchestrate this process
- Learn about how the output from a custom controller gets incorporated into the final page

By the end of this tutorial, you should be able to describe the process that Drupal goes through to convert an incoming request for a URL into an HTML response displayed by the browser.

## Goal

Examine the workflow that Drupal uses to convert an HTTP request into an HTML response.

## Prerequisites

- [What Are Events?](https://drupalize.me/tutorial/what-are-events)

## Drupal's request-to-response workflow

Drupal's request-to-response workflow uses the Symfony `HTTPKernel` (wrapped by `\Drupal\Core\StackMiddleware\StackedHttpKernel`), which provides a solid foundation for handling HTTP requests and responses, including routing, controllers, and various HTTP-related tasks. Here's how the `HTTPKernel` is used in Drupal's request-serving process.

### HTTPKernel coordinates `Request` and `Response` objects

The user enters a URL into their browser, and the web server forwards the request to Drupal's *index.php* file.

The *index.php* file bootstraps the `HTTPKernel` (Drupal has its own kernel process that extends the Symfony `HTTPKernel`), and the `HTTPKernel` processes the incoming request, creating an instance of a `Request` object that encapsulates the request data, such as headers, parameters, and URL path.

Finally, the `HTTPKernel` dispatches a series of [events](https://drupalize.me/tutorial/what-are-events) in a specific order and coordinates the flow of the `Request`, and eventual `Response` objects. The kernel handles core aspects of the HTTP protocol, while Drupal-specific *event subscribers* listen for these events and handle the content generation, rendering, and theming tasks.

`\Symfony\Component\HttpKernel\KernelEvents` ([source code](https://github.com/symfony/symfony/blob/6.4/src/Symfony/Component/HttpKernel/KernelEvents.php)):

| Constant | Event | Occurs when... |
| --- | --- | --- |
| `REQUEST` | `kernel.request` | The request dispatch process begins |
| `EXCEPTION` | `kernel.exception` | An uncaught exception appears |
| `CONTROLLER` | `kernel.controller` | A controller was found for handling a request |
| `CONTROLLER_ARGUMENTS` | `kernel.controller_arguments` | Controller arguments have been resolved |
| `VIEW` | `kernel.view` | The return value of a controller is **not** a `Response` instance |
| `RESPONSE` | `kernel.response` | A response was created for replying to a request |
| `FINISH_REQUEST` | `kernel.finish_request` | A response was generated for a request |
| `TERMINATE` | `kernel.terminate` | A response was sent |

### Request resolution

During the `KernelEvents::REQUEST` event, Drupal's routing system, built on the [Symfony Routing component](https://symfony.com/doc/current/routing.html), uses the `Request` object to match the requested URL path to a defined route. The route is used to determine which controller should be invoked to generate the response.

Request resolution includes the following tasks, each of which is provided by a different event subscriber in Drupal core:

- Handle HTTP `OPTIONS` requests.
- Redirect paths containing successive slashes to those with single slashes; for example, redirecting `//node/42` to `/node/42`.
- Perform authentication and enhance the `Request` object with data about the current user.
- Figure out the current visitor's timezone, if applicable.
- Set the error handler, allowing for the use of different error handling mechanisms in different environments. Log and display vs. log only, for example.
- Check if it's an AJAX request and add details to the `Request` object if necessary.
- Find a route that matches the `Request` object (this is known as "routing"), which also performs access checking. After this, Drupal has a fully resolved routing plan, but there are a few more steps before the controller is called.
- Verify the route allows the authentication provider used.
- Check to see if the site is in maintenance mode and display maintenance page if it is.
- Invoke the *Dynamic Page Cache* and checked for cached data.
- Check and disable any replica database server if appropriate. For example, when a node is `POST`-ed you want to hit the main database server only.
- Load a list of all compiled routes before executing the controller to make it faster to generate links with fewer database queries.
- Dispatch to the controller defined by the route.

### Controller resolution and execution

The matched route definition specifies the controller responsible for handling the `Request`. This controller is typically a method within a class. The necessary class is located and instantiated. Parameters from the route are passed to the controller as arguments. The controller processes the data, logic, and business rules related to the requested page and returns a response.

In Drupal, the return value from the controller can be either a [renderable array](https://drupalize.me/tutorial/what-are-render-arrays), or a Symfony `\Symfony\Component\HttpFoundation\Response` object, or things that extend it, like `\Symfony\Component\HttpFoundation\JsonResponse` or `\Drupal\Core\Cache\CacheableJsonResponse`.

### Controller return value rendering

If the controller returns a renderable array Drupal's theming system takes over the rendering process and converts the renderable array into the relevant HTML. If the controller returned a `Response` that already contains HTML content, this step is skipped.

The content provided by the controller is then wrapped with the regions, blocks, and other elements that make up the full page. This is added to the `Response` object. The response object now encapsulates the generated content, headers, and other response-related information.

### Final output

The `HTTPKernel` finalizes the response generation process and sends the response back to the user's browser via the web server. The browser renders the HTML content, applies CSS styling, and executes any JavaScript interactions associated with the page.

## Routes and controllers

For most Drupal developers working on custom modules, what's most relevant about routes and controllers is the use of routes to map to controllers, and controllers to generate custom responses.

In Drupal, controllers are used to generate the content that is displayed on a specific page in response to a user's request. A complete HTML page consists of the content returned from the controller wrapped in the theme system templates that display any blocks placed into regions in the primary page template.

Where the controller's output will end up depends on where the system content block is placed for the active theme.

Example:

Image

![Screenshot of region demonstration for Olivero with an arrow that points to the main content region and indicates this is where controller output is likely to be placed.](../assets/images/routing_controller_output_placement.png)

Learn more in [Overview: Routes, Controllers, and Responses](https://drupalize.me/tutorial/overview-routes-controllers-and-responses).

## Recap

In this tutorial, we learned that the Symfony `HTTPKernel` (via `\Drupal\Core\StackMiddleware\StackedHttpKernel` in Drupal) handles incoming HTTP requests by dispatching a series of events that coordinate the process of finding a route to match the request, executing the associated controller, rendering the results returned from the controller to HTML, generating a response, and finally returning that response to the user's browser.

## Further your understanding

- What happens when a Drupal controller returns a renderable array? How does that get turned into HTML for the browser?
- Install the [Webprofiler module](https://www.drupal.org/project/webprofiler) and use it to inspect the events dispatched during the process of building a page. Can you see the various Kernel events and define what's happening during each one?

## Additional resources

- [The Drupal Story: Request In, Response Out](https://x-team.com/blog/drupal-8-request-in-response-out/) (x-team.com)
- [Drupal 8/9: Request to Response Simplified](https://mohitweb.medium.com/drupal-8-9-request-to-response-simplified-7903a5965b9) (medium.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Access Checking to a Route](/tutorial/add-access-checking-route?p=3134)

Next
[Return JSON, Plain Text, and Other Non-HTML Responses](/tutorial/return-json-plain-text-and-other-non-html-responses?p=3134)

Clear History

Ask Drupalize.Me AI

close
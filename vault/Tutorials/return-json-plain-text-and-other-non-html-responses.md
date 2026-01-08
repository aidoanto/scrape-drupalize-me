---
title: "Return JSON, Plain Text, and Other Non-HTML Responses"
url: "https://drupalize.me/tutorial/return-json-plain-text-and-other-non-html-responses?p=3134"
guide: "[[develop-custom-pages]]"
---

# Return JSON, Plain Text, and Other Non-HTML Responses

## Content

Sometimes we need the response returned from a controller to be something other than HTML content wrapped with the rest of a Drupal theme. Maybe we need to return plain text, or JSON structured data for an application to consume. Perhaps we need greater control over the HTTP headers sent in the response. This is possible by building on the fact that controllers can return generic `Response` objects instead of renderable arrays, allowing you to gain complete control over what is sent to the requesting agent.

In this tutorial we'll:

- Look at how to return a plain text response, and JSON data
- Show how to make your responses cacheable by adding cacheability metadata
- Learn about how to use a generic Symfony `Response` to gain greater control over what gets returned

By the end of this tutorial, you should be able to return responses from a controller in a Drupal module that are not HTML content wrapped in a Drupal theme.

## Goal

Walk through examples of returning plain text and JSON responses with cacheability metadata from a controller as a way to learn how to return other types of responses.

## Prerequisites

- [How Drupal Turns a Request into a Response](https://drupalize.me/tutorial/how-drupal-turns-request-response)
- [Create a Route and Controller](https://drupalize.me/tutorial/create-route-and-controller)

Note: The code examples in this tutorial assume you have created a demo module called *journey* located in *DRUPALROOT/modules/custom/journey* or *DRUPALROOT/modules/journey*.

## Overview

In most cases, a Drupal controller associated with a route will return content in the form of a [renderable array](https://drupalize.me/tutorial/what-are-render-arrays). That content is wrapped in the rest of the Drupal theme resulting in a complete page, and that's what the user sees. This works because Drupal has some logic that will convert that return value from the controller into a `Response` object that the HTTP Foundation component knows how to handle.

If you want more control over the returned response you can directly return a `Response` object from your controller instead of renderable array. In this tutorial, we'll use `Response` generically to represent any class that extends the `\Symfony\Component\HttpFoundation\Response` class. Of which Drupal has many, to help with response formats like JSON, and for adding Drupal-specific things like cacheability metadata to the response.

## Return a plain text value

If you want to return plain text, or another textual data format like CSV, you can modify the `Content-Type` response headers, and Drupal will skip the step where it wraps the page content with the theme.

```
/**
 * @file
 * Example controller that returns plain text responses.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\HttpFoundation\Response;

class ExamplePlainTextController extends ControllerBase {

  /**
   * Return a plain text response.
   */
  public function build() {
    // Create a response object with just a string of text.
    $response = new Response($this->t('Nothing but text, baby!'), 200);

    // Set the content type header to text/plain.
    $response->headers->set('Content-Type', 'text/plain');

    return $response;
  }

}
```

## Return a cacheable plain text value

When a controller returns a renderable array the render array will contain [cacheability data](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) in `#cache` properties on elements of the array. Drupal will use that information to set the appropriate HTTP caching headers, which allows the user's browser and any CDN or proxy server to cache the response.

When you return your own `Response` object it will be uncacheable by default. Because Drupal doesn't know anything about whether it can be cached. If you want the response to be cacheable you'll need either manually set the appropriate HTTP cache headers on the `Response` object, or use a `Drupal\Core\Cache\CacheableResponse` object instead.

Here's an example of a controller that returns a **cacheable plain text response** that says "Hello `{user}`", where `{user}` is the name of the user who is viewing the page, or "Anonymous" if they are not authenticated. Because the response contains information about the current user, we need to vary the response (*cache context*) on the user. And, because it contains data from the user entity we need to add that as dependency (*cache tag*) to the response, so that if, for example, a user changes their name, the cached data is invalidated, and they see their updated name.

Example *src/Controller/ExamplePlainTextControllerCacheable.php*:

```
/**
 * @file
 * Example controller that returns plain text responses.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\Cache\CacheableMetadata;
use Drupal\Core\Cache\CacheableResponse;
use Drupal\Core\Controller\ControllerBase;
use Symfony\Component\HttpFoundation\Response;

class ExamplePlainTextControllerCacheable extends ControllerBase {

  /**
   * Return a cacheable plain text response.
   */
  public function buildCacheableResponse() {
    // Load the complete user object because we need the data in a form that
    // implements \Drupal\Core\Cache\CacheableDependencyInterface.
    $current_user = $this->entityTypeManager()
      ->getStorage('user')
      ->load($this->currentUser()->id());

    // Create the response with some content and an HTTP 200 status code. And
    // set it to plain text.
    $response = new CacheableResponse($this->t('Hello @name', ['@name' => $current_user->getDisplayName()]), 200);
    $response->headers->set('Content-Type', 'text/plain');

    // Then, we need to add cacheability data to the response. Usually you
    // would do this in the #cache property of the renderable array.
    //
    // Add the current user as a cache dependency because the output contains
    // the username, so we want it to vary by user. The effect is that
    // a cache tag for the user:{UID} is added. If the user edits their name
    // it will invalidate the cache.
    $response->addCacheableDependency($current_user);

    // We also need to tell the cache to vary per user who is viewing the page.
    // That's because this page shows you information about the currently
    // logged-in user. The effect of this is a cache context for 'user' is
    // added, so Drupal will make sure and vary the cache for each logged-in
    // user.
    $cacheContexts = new CacheableMetadata();
    $cacheContexts->addCacheContexts(['user']);
    $response->addCacheableDependency($cacheContexts);

    return $response;
  }

}
```

To make the response cacheable, return a `Drupal\Core\Cache\CacheableResponse` object (or anything that implements `\Drupal\Core\Cache\CacheableResponseInterface`) from your controller. You can add cacheability data to the response via the `$response->addCacheableDependency()` method. In the example above, we demonstrate both how to add a data dependency (cache tags) and a cache context. Check out [Add Cache Metadata to Render Arrays](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) to learn more about the various forms of cacheability metadata

In this screenshot you can see the appropriate HTTP headers set for the response (when viewing the page as anonymous) the page is `plain/text` and cacheable.

Image

![](/sites/default/files/styles/max_800w/public/tutorials/images/routing_cacheable_text_response_example.png?itok=7lRRGWLv)

**Note:** If you want Drupal to return appropriate HTTP headers for cacheable data, make sure you have Drupal's caching modules configured correctly. Learn more in [Overview: Drupal's Cache Modules and Performance Settings](https://drupalize.me/tutorial/overview-drupals-cache-modules-and-performance-settings).

## Return JSON formatted data

Sometimes it's useful to return data from Drupal in a structured format. JSON is the most commonly used format for doing so, and as such there's a dedicated `JsonResponse` type. It's a wrapper around the standard `Response` object that sets an appropriate header, and has logic to encode an array passed to the response as JSON. You could also do this in your own code, but the helper makes it easier.

Example *journey.routing.yml*:

```
journey.example_json_cached:
  path: '/journey/json-response-cached'
  defaults:
    _controller: '\Drupal\journey\Controller\ExampleJsonController::buildCacheableResponse'
    _title: 'Example JSON response cached'
  requirements:
    _access: 'TRUE'
```

Example *src/Controller/ExampleJsonController.php*:

```
<?php
/**
 * @file
 * Example controller that returns JSON responses.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\Cache\CacheableJsonResponse;
use Drupal\Core\Cache\CacheableMetadata;
use Drupal\Core\Controller\ControllerBase;

class ExampleJsonController extends ControllerBase {

  /**
   * Return a cacheable plain text response.
   */
  public function buildCacheableResponse() {
    // Load the complete user object because we need the data in a form that
    // implements \Drupal\Core\Cache\CacheableDependencyInterface.
    $current_user = $this->entityTypeManager()
      ->getStorage('user')
      ->load($this->currentUser()->id());

    // Create some data for the response.
    $output = [
      'user' => [
        'id' => $current_user->id(),
        'name' => $current_user->getDisplayName(),
        'email' => $current_user->getEmail(),
        'roles' => $current_user->getRoles(),
      ],
    ];

    // Create the response with some content and an HTTP 200 status code. The
    // array will be converted to JSON format.
    $response = new CacheableJsonResponse($output, 200);

    // See \Drupal\journey\Controller\ExamplePlainTextControllercacheable for
    // details about adding cacheability data like this.
    $response->addCacheableDependency($current_user);
    $cacheContexts = new CacheableMetadata();
    $cacheContexts->addCacheContexts(['user']);
    $response->addCacheableDependency($cacheContexts);

    return $response;
  }

}
```

The big difference here is the use of `\Drupal\Core\Cache\CacheableJsonResponse` (or `\Symfony\Component\HttpFoundation\JsonResponse` if you don't need cacheable responses), which takes an associative array as its first argument instead of a string. The array will be converted to JSON, and the HTTP response will get a `Content-type: application/json` header added to it.

JSON output example:

Image

![Screenshot of JSON response shown in browser with network console showing HTTP headers.](/sites/default/files/styles/max_800w/public/tutorials/images/routing_json_response.png?itok=dinYcvNs)

You can also use `CacheableJsonResponse` and `JsonResponse` as an example of how to create your own non-HTML `Response` objects. For example, if you needed to create a lot of different XML responses you might create your own custom `Response` subclass that sets the appropriate headers in the constructor, and adds some logic for converting an array of data to an XML string.

## Return HTML without a theme

When you return a renderable array from a controller Drupal will wrap the content with the active theme to display it as a complete HTML page. And then convert that to an `\Drupal\Core\Render\HtmlResponse`. If you return a `Response` object from your controller Drupal, will skip the step where it wraps the page content with the theme.

If you want to return un-themed HTML, we recommend returning a `\Drupal\Core\Render\HtmlResponse` from your controller. A standard Symfony `Response` will also display as HTML by default, but the Drupal-specific `HtmlResponse` will provide support for Drupal's caching concepts. This is covered above in the section about returning cacheable plain text responses.

Example of returning HTML without Drupal's theme wrapped around it:

```
/**
 * @file
 * Example controller that returns plain HTML responses.
 */

namespace Drupal\journey\Controller;

use Drupal\Core\Controller\ControllerBase;
use Drupal\Core\Render\HtmlResponse;

class ExamplePlainHtmlController extends ControllerBase {

  /**
   * Return a plain HTML response.
   */
  public function build() {
    // Create a response object with just a string of HTML.
    $response = new HtmlResponse('<marquee>Nothing but HTML, baby</marquee>', 200);
    return $response;
  }

}
```

## Recap

In order to gain more control of the content and HTTP headers sent when someone accesses a route, controllers can return a `Response` object. That is, any object that extends the `\Symfony\Component\HttpFoundation\Response` class. Doing so allows you to return plain text, JSON, and any other non-HTML format. Drupal provides some helper classes that implement `\Drupal\Core\Cache\CacheableResponseInterface` which allow you to add cacheability metadata to the response. This make it possible for Drupal's dynamic page cache and downstream proxies and CDNs to cache the response.

## Further your understanding

- How would you return a `text/csv` response from a Drupal controller? How would you make it cacheable? How would you make it reusable?
- Learn about how *early rendering* effects controllers that return a `Response` in [Early Rendering: A Lesson in Debugging Drupal 8](https://www.lullabot.com/articles/early-rendering-a-lesson-in-debugging-drupal-8).
- The Symfony HTTP Foundation component, which provides that standard `Response` objects, has some additional response formats that it can return. Take a look at those options to familiarize yourself with how to return streamed data, binary files, and more.

## Additional resources

- [Responses overview](https://www.drupal.org/docs/drupal-apis/responses/responses-overview) contains a list of the other Drupal specific `Response` subclasses. (Drupal.org)
- [Documentation for the Symfony HTTP Foundation component's Response class](https://symfony.com/doc/current/components/http_foundation.html#response) (symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[How Drupal Turns a Request into a Response](/tutorial/how-drupal-turns-request-response?p=3134)

Clear History

Ask Drupalize.Me AI

close
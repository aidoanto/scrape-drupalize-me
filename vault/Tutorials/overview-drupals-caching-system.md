---
title: "Overview: Drupal's Caching System"
url: "https://drupalize.me/tutorial/overview-drupals-caching-system?p=3091"
guide: "[[drupal-site-administration]]"
---

# Overview: Drupal's Caching System

## Content

Drupal has robust Cache API, and various caching layers (both internal and external to Drupal), that work together to decrease application load and boost performance. Drupal's APIs allow developers to declare the cacheability of data. How long can this be stored before it becomes stale? And under what conditions should it be invalidated? Drupal uses that information during the process of building a page to cache as much of the work it does as is possible so that it won't need to do it again. Additionally, Drupal bubbles up the cacheability data from everything required to build a page into HTTP response headers that caching layers external to Drupal can also use to cache the rendered HTML.

When these APIs are combined (and used appropriately), Drupal can be extremely fast for both anonymous and authenticated traffic. But doing so requires understanding the various caching layers, their roles, and their interconnections.

In this tutorial, we'll:

- Review the caching layers and systems behind them
- Learn about components of the Drupal cache system

By the end of this tutorial, you should have a broad understanding of the Drupal caching system, its layers, and a better understanding of where in the stack you should look to optimize for different scenarios.

## Goal

Introduce the Drupal caching system to developers.

## Prerequisites

- None

## Serving a request with cached data

Image

![Illustration showing the layers of the cache detailed below](/sites/default/files/styles/max_800w/public/tutorials/images/cache-layers.png?itok=z8qxQRvJ)

When a user visits your site and requests a page from Drupal, as the request travels on its way to being processed by Drupal and your PHP code, there's a long list of different applications (or layers) that help service the request. After receiving the request, Drupal processes it, calculates the response, renders it as HTML, and then sends it back up the stack to the user's browser. Each of these layers work together to deliver a response as quickly as possible. Efficient caching occurs when each layer in the stack is able to inspect an incoming request, determine if it's safe to serve a copy of a previously calculated response, and if so, return that response, halting the request from proceeding down the stack.

It's faster to view a page if there's a copy stored in Varnish from the last time someone visited the site than it is to wait for your request to travel all the way down the stack to Drupal and then back again.

But this only works if each of the caching layers have a way to know:

- Which data is safe to store?
- For how long can it be stored?
- When is Drupal required to invalidate the cached data?

For example, the [about page](https://drupalize.me/about) of this site rarely changes, and the page's content is the same no matter who visits it (logged-in or not). If the about page content does change, it's fine if a user doesn't see those changes immediately. This makes it safe to cache the entire completed page as long as the cache *varies* depending on whether you're signed in to your account or not (because the navigation in the top menu changes if you are). Caching layers external to Drupal that can respect this variance (Varnish, CDN, browser cache) can cache the entire response and might not even need to involve Drupal for subsequent visits.

Your account dashboard, however, is unique to you--and changes frequently. Some content on the page is the same for every user (like the list of recent blog posts) but other content (like the list of recently completed tutorials) is unique to you. This means Drupal probably needs to be involved in calculating the response for each visit. But even then, it doesn't have to do so from scratch. Assuming the page contains well-crafted *cacheability metadata* Drupal can assemble the page from a combination of reused chunks, and chunks calculated in real time. The block of HTML that contains the list of blog posts can be calculated once and shared by many users. The list of recently-read tutorials or items in your queue, can be calculated and reused as well--but only for your account. These chunks all get combined to form the completed rendered page. Later, when you read a new tutorial or add something to your queue, Drupal can tell the various caching layers that they need to invalidate the cached version of those lists and recalculate them the next time you visit your dashboard.

Caching responses are complex and involve many layers. Luckily Drupal excels at handing this for us automatically--as long as we provide accurate *cacheability metadata*, and configure the other layers in the stack to work in conjunction with Drupal.

Let's take a look at the common layers in the caching stack starting from the user's browser and working down to Drupal itself.

## Browser cache

All modern browsers are set up to store copies of static assets such as CSS, scripts, and images to minimize network traffic and optimize page load time. On every request, the browser checks the cache headers to understand if the data can be pulled from the cache memory/storage or the server. The *browser cache* is the cache layer that developers have the least direct control over, but it's still an important part of the stack, and we should know how make use of it.

Drupal will set an appropriate `Cache-Control` header for each HTTP response based on the content of that response and the current application state (anonymous versus authenticated, for example). [Cache control directives set by the Render API](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) for each content fragment on the current page are bubbled up and taken into account when determining a page's *cacheability* and what value to use for the HTTP header. If, for example, a content fragment on the page is designated as non-cacheable, Drupal will add `Cache-Control` and `Expires` headers so that the cache can be appropriately flushed.

It's possible for code in a Drupal module to manually specify `Cache-control` and `Expires` headers for a request, and Drupal will respect those. But in most cases it's better to use Drupal's API to describe the cacheability of the response and let Drupal handle assigning the appropriate headers.

The user's browser will determine whether to store the response data based on the supplied `Cache-control` directive. Below is a list of the possible values Drupal will set, and what they mean. *Resource* (below) refers to any target of an HTTP request, like a document, image, or anything with a URI. See also [Identifying resources on the web](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Identifying_resources_on_the_Web) (developer.mozilla.org).

### Drupal's cache-control directives

- `Cache-Control: public`: The resource can be cached by any caching layer; for example, browser, CDN, proxy, and so on.
- `Cache-Control: private`: The resource can only be cached by the browser.
- `Cache-Control: no-store`: The resource should always be requested from the server
- `Cache-Control: no-cache`: Cache the resource, but check with the webserver to ensure we have the latest version. The browser will go down through the chain of the cache layers and validate the resource. If any cache layers indicate that the cached resource is the latest copy, the browser will use it.
- `Cache-Control: max-age=180`: Sets an explicit expiration time of the cache since the resource was initially cached. This time is in seconds. The example here (`max-age=180`) means that the resource will be cached for 3 minutes.
- `Cache-Control: must-revalidate`: The browser must validate the status of the resource and not use a stale version.

Drupal exposes a configuration setting for the `max-age` parameter on the *Performance* configuration page at: *Manage* > *Configuration* > *Development* > *Performance* (*/admin/config/development/performance*).

Image

![Screenshot of Drupal performance tab](/sites/default/files/styles/max_800w/public/tutorials/images/performance_tab_screenshot.png?itok=33WSnNOq)

To achieve the benefits of browser caching, we recommend setting a long `max-age` time, like 6 hours or more.

The `Cache-control` and `Expires` headers are part of the HTTP specification and not specific to Drupal. Drupal's job in this case is to set appropriate values so that the browser--and any other layer in the stack that relies on these headers--knows what to do.

## Varnish and CDNs (reverse proxy services)

[Varnish](https://varnish-cache.org/intro/) is a type of reverse proxy. It sits between Drupal and the browser, caches the entire page, and sends a snapshot to subsequent users. It's functionally similar to the browser cache with the benefit of being able to reuse the same cached data for multiple different users. The Varnish layer typically only works for anonymous users; though it's possible to configure it otherwise in very specific applications. If you are hosting your site on one of the web operations platforms such as Acquia, Pantheon, or Platform.sh (among others), chances are the Varnish layer is already set up for your application and will just work without you needing to configure it.

Drupal applications send an array of cacheable metadata that Varnish purgers use to invalidate the cache intelligently. Depending on your hosting platform, a variety of Drupal contributed modules may be installed on your system to help with cache purging. Check the documentation for your platform to learn more about the requirements for optimizing this setup. Another difference between Varnish and browser caches is that Drupal can ping the Varnish server and ask it to flush its cached data or to invalidate specific resources on-demand.

Content Distribution Networks (CDNs) operate in a similar way. They sit between Drupal and browser and interpret the HTTP cache headers that Drupal returns. Some CDNs have APIs that allow Drupal to request data to be invalidated when changes occur in Drupal. To learn more, see: [Overview: Content Delivery Networks (CDNs) and Drupal](https://drupalize.me/tutorial/overview-content-delivery-networks-cdns-and-drupal).

## Opcode cache

Compiled languages like Java, or C++, have a compilation step before code deployment and execution. Unlike those, PHP is a scripting language which means the code is processed before execution. Processed PHP code is converted to *Opcode*, and then Opcode files are read and executed by the server.

Processing every PHP file before page rendering creates significant overhead. Furthermore, the Opcode cache keeps a copy of the compiled script in memory, improving your Drupal application's performance. This cache is configured at the server level, and if your application is hosted on one of the specialized Drupal web operations platforms, it’s probably already configured for your application. You don’t need to do anything special to take advantage of this caching layer.

Running your own server? PHP has the Zend Opcache extension built-in, but it may not be enabled by default. It's worth checking to make sure it's enabled and configured. Read more about doing so in this Stack Exchange answer: [How to use PHP OpCache?](https://stackoverflow.com/questions/17224798/how-to-use-php-opcache)

## Application cache

The *application cache* layer is a layer within your Drupal application. As Drupal developers, we have the most control over this layer. We are responsible for how well this layer is configured and performing.

The Drupal application cache layer consists of 2 major components: cache backends and render caching.

### Drupal cache backends

*Drupal cache backends* are defined as services and are part of Drupal's Cache API. Code in Drupal can use a cache backend service to store and retrieve cacheable data. A common scenario: module code performs a complex computation to first check for a cached result and use it if it exists. If not, then perform the computation and cache the result for next time. Think of cache backends as defining where/how the data will be stored. Different backends are better for different use cases depending on the data being stored, how big a chunk it is, and how frequently it's needed.

Drupal core contains the following backends, and contributed modules can define new ones:

- `DatabaseBackend`: Drupal's default cache implementation. It uses the database to store cached data. Each cache bin corresponds to a database table by the same name.
- `ChainedFastBackend`: Defines a backend with a fast and consistent backend chain. This cache allows a fast backend to be put in front of a slower backend. For example, a static in-memory cache in front of a slower database cache.
- `MemoryBackend`: Stores cache items in memory using a PHP array. It should be used only for unit tests and specialist use cases and doesn't store cached items between requests.
- `PhpBackend`: Stores cache items in a PHP file using a storage that implements `Drupal\Component\PhpStorage\PhpStorageInterface`. It works together with the Opcode cache mechanism.
- `NullBackend`: Defines a stub cache implementation. Mostly used in development and for testing purposes. Using it in production will harm performance as it doesn't actually perform any caching and just passes all requests through.
- `ApcuBackend`: Stores cache items in the *Alternative PHP Cache User Cache (APCu)*. APCu is a fast backend and is usually configured per cache bin. APCu is typically bound to a single web node and doesn't require a network round-trip to fetch a cache item.

Many web operations platforms provide integrations with additional cache backends, such as Memcache and Redis. Depending on your server configuration, you may also consider installing a contributed module that allows for the integration of these additional backends with Drupal.

As a developer you should use the Drupal cache service either through `\Drupal::cache()` or via dependency injection. By using the service you can write code that is more agnostic about what backend is used and allow the backend configuration to vary per environment.

### Drupal render cache

The Drupal rendering process can cache parts of the rendered output at any level in a render array hierarchy. It ensures that not all HTML is rendered every time. This allows expensive calculations to be done infrequently and speeds up page loading. The Render cache relies on the various types of cacheable metadata defined in renderable arrays. Drupal's render cache comprises:

- *Cache keys*: Identifiers for cacheable portions of render arrays.
- *Cache contexts*: Contexts that may affect rendering, such as user role, page URL, and so on.
- *Cache tags*: Tags for data upon which rendering depends (like individual nodes or user accounts) so that when these are updated, the cache can be automatically invalidated.
- *Cache max-age*: The maximum duration for which a render array may be cached. By default, all render arrays are permanently cached.

Learn more about renderable array caching and cache bins in [Cache API Overview](https://drupalize.me/tutorial/cache-api-overview).

## Recap

Sending a request from the browser to Drupal and back again is a complex system that relies on each caching layer to perform at its best. The layers of caching start with the browser cache and go down to Drupal's application level caching. As developers, we have the most control over the application level cache, like setting cacheability metadata in render arrays that define the volatility of the data for which our code is responsible. Drupal bubbles this info up to HTTP `Cache-control` headers that other layers of the stack can use. Even though we have less control over them, it's a good idea to be aware of what those other layers are, and how they can help make our Drupal application as fast as possible.

## Further your understanding

- Load a Drupal site, open the network tab in the browser development tools, reload the page, and check the cache headers. Can you see how your application is configured and what it tells the browser about caching?
- Try configuring various cache backends and benchmarking each. Do you see a difference in performance?

## Additional resources

- [Cache API Overview](https://drupalize.me/tutorial/cache-api-overview) (Drupalize.Me)
- [Cacheability of render arrays](https://www.drupal.org/docs/8/api/render-api/cacheability-of-render-arrays) (Drupal.org)
- [Drupal Wiki: Cache API](https://www.drupal.org/docs/drupal-apis/cache-api) (Drupal.org)
- [API Topic: Cache API](https://api.drupal.org/api/drupal/core%21core.api.php/group/cache/) (api.drupal.org)
- [Clear Drupal's Cache](https://drupalize.me/tutorial/clear-drupals-cache) (Drupalize.Me)
- [Caching in Drupal (topical resources)](https://drupalize.me/topic/caching-drupal) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Drupal's Cache Modules and Performance Settings](/tutorial/overview-drupals-cache-modules-and-performance-settings?p=3091)

Next
[Debug Drupal Cache Misses and Low Hit Rates](/tutorial/debug-drupal-cache-misses-and-low-hit-rates?p=3091)

Clear History

Ask Drupalize.Me AI

close
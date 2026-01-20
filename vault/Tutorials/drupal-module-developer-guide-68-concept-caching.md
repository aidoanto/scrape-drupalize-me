---
title: "Concept: Cachingfree"
url: "https://drupalize.me/tutorial/concept-caching?p=3244"
guide: "[[drupal-module-developer-guide]]"
order: 68
---

# Concept: Cachingfree

## Content

Caching is an essential piece of website performance and user experience. Drupal's Cache API enables you as a module developer to specify cacheability information for data rendered through the Render API. By storing previously calculated data or page renderings, Drupal can skip complex backend processes for subsequent requests and deliver content faster. Drupal's Cache API provides services to store, retrieve, and invalidate cached data.

In this tutorial, we'll:

- Learn why caching is important.
- Cover key terms and concepts associated with the Cache API.
- Explore how and when custom modules can implement caching.

By the end of this tutorial, you should understand the core features of Drupal's Cache API and when to use them.

## Goal

Learn the basics of Drupal's caching system to understand how you could optimize the performance of a custom module.

## Prerequisites

- [Concept: Render API](https://drupalize.me/tutorial/concept-render-api)
- [Concept: Entity API and Data Storage](https://drupalize.me/tutorial/concept-entity-api-and-data-storage)

## What is caching?

Caching is the process of storing and reusing previously calculated data to speed up subsequent requests. Drupal's caching system reduces server load and decreases page load times. It includes response caching for full pages and fragment caching for parts of a page.

## Drupal's Cache API

The Cache API in Drupal allows modules to store data from time-consuming operations. It supports multiple *cache bins* for organizing cached data and enables you to swap the cache storage system for more efficient solutions like Redis or Memcache.

### Key concepts of the Cache API

- **Cacheability**: Describes under what conditions specific data can be cached.
- **Response caching**: Stores the complete HTML response for a page. Used by Drupal's Internal Page Cache module and external systems like Varnish.
- **Fragment caching**: Caches parts of the data used to build a page, such as render arrays or API request results.
- **Cache tags**: Invalidate cache entries when specific events occur, such as adding a new blog post.
- **Cache contexts**: Define cache entry variations based on context, ensuring users see content relevant to their specific circumstances.
- **Cache max-age**: Specifies how long an item can be cached, controlling cache refresh rates.
- **Cache bins**: Cache storage is separated into "bins", each containing various cache items. This separation allows for more efficient lookups.

## Rendered content caching

Drupal's Render API applies caching to render arrays. Developers can specify cache metadata in render arrays using cache tags, contexts, and max-age. If you add content to the page via a render array, you should define its cacheability. For example, the *Hello, World!* block we created in [Create a Custom "Hello, World!" Block](https://drupalize.me/tutorial/create-custom-hello-world-block) displays the name of the currently logged-in user. We need to tell Drupal that this page's content is dependent on the user (context), so that it knows that it can serve the same user a cached version of the page. A different user will need a different version of the same page.

We'll practice applying this concept in [Add Cache Context and Tags to Renderable Arrays](https://drupalize.me/tutorial/add-cache-context-and-tags-renderable-arrays).

### Bubbling of cache metadata

Cache metadata in render arrays can "bubble up," allowing Drupal to aggregate caching requirements of nested elements. This ensures the final page's cache entry respects the cacheability of each of its components. This information is also used to set appropriate HTTP cache headers for the page that the browser or proxy cache (between the user and Drupal) can use to cache responses.

## Cache backend service

Drupal's cache backend service interacts with cache storage. Developers can use this service to cache custom data or interact with cache bins programmatically. As a developer, you'll use this to cache the results of complex operations. For example, making a request to the weather forecast API requires a *slow* HTTP request. Your module could make the request once and cache the results locally.

We'll apply this concept in [Cache Data Retrieved from the Weather API](https://drupalize.me/tutorial/cache-data-retrieved-weather-api).

## Cache invalidation

Drupal automatically invalidates cache entries when data changes, ensuring up-to-date content. Developers use cache tags to specify which entries to invalidate upon entity updates or deletions.

## Recap

In this tutorial, we learned about Drupal's Cache API. Drupal's Cache API enhances website performance by allowing us to store previously calculated data or page renderings, helping us skip complex backend processes for faster content delivery. We explored key concepts such as response caching, fragment caching, cache tags, contexts, and max-age.

## Further your understanding

- How can cache contexts personalize content for different user segments?
- Explore cache max-age's impact on dynamic content. How do developers balance content freshness and performance?

## Additional resources

- [Fast by Default](https://drupalize.me/tutorial/fast-default) (Drupalize.Me)
- [Overview: Drupal's Caching System](https://drupalize.me/tutorial/overview-drupals-caching-system) (Drupalize.Me)
- [Overview: Drupal's Cache Modules and Performance Settings](https://drupalize.me/tutorial/overview-drupals-cache-modules-and-performance-settings) (Drupalize.Me)
- [Add Cache Metadata to Render Arrays](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Cache Data Retrieved from the Weather API](/tutorial/cache-data-retrieved-weather-api?p=3244)

Clear History

Ask Drupalize.Me AI

close
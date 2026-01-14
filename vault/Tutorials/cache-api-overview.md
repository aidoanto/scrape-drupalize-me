---
title: "Cache API Overview"
url: "https://drupalize.me/tutorial/cache-api-overview?p=2723"
guide: "[[output-and-format-data-code]]"
order: 18
---

# Cache API Overview

## Content

Many of the processes that Drupal performs when responding to a request are cached in order to increase performance. Creating the HTML for the page that a user sees or the JSON response to a REST request can require thousands of operations. Some operations are time consuming, memory heavy, CPU intense, or all 3. By performing the operation once, and then caching the result for next time, subsequent requests can be fulfilled faster. In order to make it easier to store, retrieve, and invalidate cached data, Drupal provides cache-related services you can use in your code. Drupal also enables you to provide information about the cacheability of data to the Render API to improve the performance of page rendering.

In this tutorial we'll:

- Cover the terms and concepts you should be familiar with when working with the Cache API
- Point to additional resources for more information about how to perform specific tasks with the Cache API

By the end of this tutorial, you should be able to define the concepts of bubbling and cache invalidation, and know how cache keys, tags, context, and max-age are used to provide cacheability metadata for items.

## Goal

List the primary concepts of the Cache API, explain their role, and point to where to find more information.

## Prerequisites

- [Render API Overview](https://drupalize.me/tutorial/render-api-overview)
- [Entity API Overview](https://drupalize.me/tutorial/entity-api-overview)

## Contents

- [Render cache vs. Response cache](#types)
- [Cacheability](#cacheability)
- [Bubbling](#bubbling)
- [Cache keys](#keys)
- [Cache tags](#tags)
- [Cache contexts](#contexts)
- [Cache max-age](#max-age)
- [Invalidating cached items](#invalidating)
- [Debugging Drupal's cache](#debugging)

## Render cache vs. Response cache

### Render caching (aka fragment caching)

The Render API uses cacheability metadata (see below) embedded in [render arrays](https://drupalize.me/tutorial/what-are-render-arrays) to perform caching and increase performance. As a [renderer](https://drupalize.me/tutorial/render-api-renderers) converts the array to HTML it starts from the innermost item and works outwards. Each step is cached, and includes the element and its children. Future passes on rendering this same tree will used cached versions of an element whenever possible in order to speed things up.

In addition to render caching, fragments of work that are not related to a render array can be cached [using the `\Drupal::cache()` service](https://api.drupal.org/api/drupal/core%21core.api.php/group/cache/). Code that makes requests to an external API like Twitter could cache the results of that request locally and re-use them for a fixed period of time. For instance, if this time period is 5 minutes, it is probably fine to serve a list of content from Twitter that is 5 minutes old. This would increase the performance of the page by eliminating one or more requests that take a lot longer than just looking up a record in the cache.

### Response caching

Once the complete HTML for a page is rendered, the cacheability metadata used by the Render API bubbles all the way up to the `Response` object. Response caching is the act of storing the complete response for later use. This way future requests can bypass all of the logic necessary to build the page and simply return a cached version -- assuming it's still valid.

This is what allows Drupal's [Page Cache](https://www.drupal.org/documentation/modules/internal_page_cache) and [Dynamic Page Cache](https://www.drupal.org/documentation/modules/dynamic_page_cache) modules to work.

If you've ever used a reverse proxy cache like Varnish or CloudFlare, these are implementations of response caching.

## Cacheability

In Drupal's documentation, in the code, and thus in our tutorials, we use the term *cacheability* to describe the conditions under which a specific thing can, and can not, be cached.

"Can that data be cached? I don't know; check its cacheability."

## Bubbling

Bubbling, or "bubbleable metadata", refers to the way that a parent item in a render array inherits the cacheability data of its children. This ensures that if something lower in the tree changes, the whole branch is re-rendered.

## Cache keys

Cache keys serve as unique identifiers for cached data. Think of a cache key as a name or an address for a piece of data stored in the cache. When Drupal wants to cache something, it uses this key to store and retrieve the cached data. The cache key ensures that each piece of cached data can be uniquely identified and accessed.

Consider the code for rendering a node. The result will be different depending on the specific node, and the view mode used. The cache key should take this into account to ensure that you don't accidentally get the cached version of the 'full' node when you wanted to display the 'teaser'. Example cache keys for this scenario might be `['node', 5, 'teaser']`, and `['node', 5, 'full']`.

Cache keys do not effect that cachability of an item. On the other hand, cache tags, cache contexts, and cache max-age are types of cache metadata that Drupal uses to manage cache invalidation and variation.

## Cache tags

Cache tags vary the cache based on the data that was used to build the element. For example, entities, users, or configuration.

Using cache tags you could associate some cached data with a specific node. When that node is edited, and the content of it changes, the related cached data becomes outdated and no longer valid.

When thinking about cache tags, ask yourself, "What does this item depend on in order to derive its content?" When those things change the cache needs to be invalidated so we can rebuild the item with the new data.

The node teaser shows the node title, authoring date, author, author's profile picture, and body. The dependencies are the node itself, the user entity associated with the author, the file entity associated with the profile picture and the text format associated with the body field. If any of them change, then the cached HTML for the node 5 teaser must be regenerated. So my cache tags would be: `['node:5', 'user:3', 'file:4', 'config:filter.format.basic_html']`.

Data objects should in most cases have a `::getCacheTags()` method that returns any tags for that object. So, `$node->getCacheTags()` would return `node:5`. Rather than hard coding these, or trying to memorize patterns, use these methods instead.

Example: your content displays the user name, and you want to add the appropriate tags: `$user->getCacheTags()`.

If you are defining your own data model, or using something other than the Entity API or Configuration API for data storage, you should consider adding your own custom cache tags, and then invalidating them at the appropriate times.

[Read more about cache tags in the official docs](https://www.drupal.org/docs/drupal-apis/cache-api/cache-tags), and in [Drupal: cache tags for all, regardless your backend](https://mglaman.dev/blog/drupal-cache-tags-all-regardless-your-backend) by Matt Glaman.

## Cache contexts

Cache contexts vary the cache based on contextual information. This could be the day of the week, the current user's last login date, or the value of a setting in the administrative UI. Cache contexts are analogous to the HTTP `Vary` header.

When determining cache contexts, ask yourself, "Does the thing that is being rendered vary based on contextual information?" For example if permissions, language, user-configured settings, or day of the week change, is this content still going to be valid? If an element varies based on whether or not the current user is authenticated, using a cache context of `['user.role:anonymous']` would instruct the cache to store multiple variations of this object: one for users with the anonymous role, and another for everyone else.

A practical example from Drupal core: the teaser of a node is rendered differently for users in different timezones because the "authored on" date field is displayed using a localized time. So the cache contexts for the teaser would be `['timezone']`.

There is a fixed list of contexts provided by core. You can [see that list and read more about how to use each context in the documentation](https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts).

You can create your own context by defining a new tagged service. Cache contexts are services tagged with `'cache.context'`, whose classes implement `\Drupal\Core\Cache\Context\CacheContextInterface`.

[Read more about cache contexts](https://www.drupal.org/docs/drupal-apis/cache-api/cache-contexts).

## Cache max-age

Cache max-age varies the cache based on time. For example, "Valid for 1 hour."

Max-age is a either a positive integer expressing a number of seconds, `0`, or `Cache::PERMANENT`. `Cache::PERMANENT` is the default.

`0` means cacheable for zero seconds, which is the same as saying not cacheable at all or disabled. Use this to prevent an item from ever being cached.

`\Drupal\Core\Cache\Cache::PERMANENT` means cache forever, only invalidate based on cache tags.

[Read more about cache max-age](https://www.drupal.org/docs/drupal-apis/cache-api/cache-max-age).

## Invalidating cached items

Caches that vary on max-age, tags, or contexts, that are provided by core or another module should already be invalidated at the appropriate times. You can always manually invalidate any of these as needed.

If you define your own custom [cache tags](#tags), you'll also need to define when they are invalidated. Generally this would be when the data they represent is updated. If your code has `$custom_object->save()` or `$custom_object->update()` methods you would trigger something like the following in those methods to invalidate cached items and force them to be rebuilt the next time they are used.

```
\Drupal\Core\Cache\Cache::invalidateTags(['custom_object:1']);
```

Or via the `cache_tags.invalidator` service.

```
$this->container('cache_tags.invalidator')->invalidateTags(['custom_object:1']);
```

Note: for the most part you should be using either the Entity or the Configuration systems to store your module's data. Both of those already handle the required invalidation for `{entity_type}:{entity_id}` and `configuration:{config_id}` tags.

## Debugging Drupal's cache

With [your site in development mode](https://drupalize.me/tutorial/configure-your-environment-theme-development), you'll see some additional HTTP headers that show you what is in the context and tags for each page.

Look for the `X-Drupal-Cache-Contexts` and `X-Drupal-Cache-Tags` HTTP headers.

Image

![Screenshot shows x-drupal-cache-contexts and x-drupal-cache-tags headers in the chrome web inspector. Each contains a list of the Drupal contexts and tags used respectively.](../assets/images/cache-debug.png)

This feature is controlled by the `http.response.debug_cacheability_headers: true` setting in *sites/default/services.yml* or *sites/development.services.yml* depending on your setup. It is off by default, and should stay off on production.

## Recap

In this tutorial we covered the basic concepts and terminology used in Drupal's Cache API, including cache tags, contexts, keys, and max-age. We looked at how bubbling allows for elements in a render array to be cached, and how a particular branch of the tree can be invalidated. The resources above are intended to give you an overview, and we recommend following the provided links to learn more.

## Further your understanding

- If I want to vary the cache so that when the title of a taxonomy term is updated, do I want to use max-age, tags, context, or keys? Can you explain the differences?
- Can you explain how fragment caching, and response caching, could be used together to improve response time?
- Read more about using the `\Drupal::cache()` service to store and retrieve cached data in [the documentation](https://api.drupal.org/api/drupal/core%21core.api.php/group/cache/)

## Additional resources

- [Add Cache Metedata to Render Arrays](https://drupalize.me/tutorial/add-cache-metadata-render-arrays) (Drupalize.Me)
- [Ensuring Drupal 8 Block Cache Tags bubble up to the Page](https://www.previousnext.com.au/blog/ensuring-drupal-8-block-cache-tags-bubble-up-page) (previousnext.com)
- [Drupal: cache tags for all, regardless your backend](https://mglaman.dev/blog/drupal-cache-tags-all-regardless-your-backend) (mglaman.dev)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Add Cache Metadata to Render Arrays](/tutorial/add-cache-metadata-render-arrays?p=2723)

Clear History

Ask Drupalize.Me AI

close
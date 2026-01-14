---
title: "Debug Drupal Cache Misses and Low Hit Rates"
url: "https://drupalize.me/tutorial/debug-drupal-cache-misses-and-low-hit-rates?p=3091"
guide: "[[drupal-site-administration]]"
---

# Debug Drupal Cache Misses and Low Hit Rates

## Content

Drupal site performance relies heavily on caching. Optimal caching (and invalidation) requires that each page is rendered with the correct cacheable metadata. This metadata allows for intelligent caching -- but when something isn't working correctly, it can be tricky to figure out where exactly the metadata was generated from.

When debugging Drupal cache issues, you're usually trying to answer 1 of 2 primary questions:

- Why is this cached? If the information gets stale, why isn’t it updated?
- Why is this *not* cached? And why is our cache hit rate low?

The Drupal cache system [consists of many layers](https://drupalize.me/tutorial/overview-drupals-caching-system), each of which may contribute to the problem. This tutorial focuses on debugging the Drupal application cache layer, and strategies for debugging Varnish. Given that most external to Drupal layers rely on the use of HTTP headers for caching, you should be able to use similar techniques to those used for debugging Varnish.

In this tutorial, we'll:

- Learn strategies for debugging the Drupal application cache and render cache
- Share strategies for debugging low hit rates when using Varnish

By the end of this tutorial, you should know how to enable and use various cache debugging mechanisms in Drupal to help identify problems in your site performance and resolve them.

## Goal

Introduce Drupal application cache and Varnish cache debugging strategies to developers.

## Prerequisites

- [Overview: Drupal's Caching System](https://drupalize.me/tutorial/overview-drupals-caching-system)
- [Cache API Overview](https://drupalize.me/tutorial/cache-api-overview)

## Drupal cache headers and metadata debugging strategies

The Drupal application cache relies on 2 pieces of information to store data in the cache and invalidate it when necessary. These are *cache headers* and *cacheable metadata*. Cache headers are HTTP headers sent by Drupal core as part of the response to fulfill a request to view a page. They are set on the page level. They are responsible for the page cache for anonymous and authenticated users.

Cache metadata refers to *cache tags* and *cache contexts* used by the Drupal core Dynamic Page Cache module and the render caching system.

Both of these are primarily calculated by the rending system which inspects the `#cache` key of renderable arrays as it builds the HTML for the page.

Before you start debugging your Drupal application cache, verify that your site has the recommended performance and cache settings. Navigate to *Admin*>*Configuration*>*Development*>*Performance* (/admin/config/development/performance) to see current settings for your site. Ensure you have *Browser and proxy caching* time set to a value other than `<no-caching>`. If you're working on a local development environment, it's common to force-disable some or all of the caching mechanisms through a combination of a *settings.local.php* file and a *development.services.yml* file. Make sure these aren't interfering with the expected results.

If you're debugging cache invalidation and your content is too stale, set the value of the browser cache to something low. We recommend starting with 15 minutes. After finding and fixing the problem, increase the value to at least an hour (or a setting that's appropriate for your specific site).

If you're debugging a low cache rate, set the value to a higher number. We recommend going with 1 or 3 hours to start.

Ensure that the Dynamic Page Cache module is enabled. Enable Internal Page Cache module if your site doesn't use Varnish or another reverse proxy.

To identify if your page is appropriately cached, open your page in a browser, open the browser's development tools, switch to the network monitoring tab, and view the response headers returned for the page. In the image below, we show an example result for a site in Firefox:

Image

![Cache headers in Firefox](../assets/images/cache_response_firefox.png)

And in Chrome:

Image

![Cache headers in Chrome](../assets/images/cache_response_chrome.png)

### Cache headers

The Drupal application sets different types of cache headers. Common (standard) headers, not specific to Drupal or web operations platform:

*age* - age of the content in cache. If after multiple requests it says 0, the pages are never cached.

*cache-control* - determines caching behaviors for the given request, set by Drupal

*expires* - the time after which the response will be considered stale. In Drupal, it’s set to Dries’ birthday.

Drupal-specific headers:

*x-drupal-cache* - cache header provided by Internal Page Cache module.

*x-drupal-dynamic-cache* - cache header provided by Dynamic Page Cache module.

Values of Drupal-specific headers can be `HIT`, `MISS`, and `UNCACHEABLE`. If you receive `HIT`, your cache is working as expected.

If you get `MISS`, you may have `<no-cache>` value in the Performance settings of your site, or your cache backend is set to `NULL`. `MISS` value is also possible if the page is served fully from Varnish and didn’t reach the Drupal cache layer.

If you get `UNCACHEABLE`, some of the render array cacheable metadata bubbles to the page level and prevents caching of the page. In this case, you need to dive deeply into your cacheable metadata.

You can enable additional debugging headers with detailed information about the *cache context* and *cache tags* applied to a page via service configuration. If you have a `development.services.yml` file, update it to include `http.response.debug_cacheability_headers: true` under the `parameters` key. If you don’t have a `development.services.yml`, this could also go in your `services.yml` file.

Example *sites/development.services.yml* file:

```
# Local development services.
#
# To activate this feature, follow the instructions at the top of the
# 'example.settings.local.php' file, which sits next to this file.
parameters:
  http.response.debug_cacheability_headers: true
```

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) so Drupal picks up these configuration changes. Then refresh the page in your browser. In the network tab, you should see cache contexts and tags in the headers section:

Image

![Screenshot of cache tags and contexts](../assets/images/cache_tags_contexts.png)

The cache tags and contexts allow seeing which blocks and render elements contribute to the cache status of the particular page. From there, you need to narrow it down to a specific offender. It might be a slow process. We recommend using XDebug and setting a breakpoint on the `shouldCacheResponse()` method of `DynamicPageCacheSubscriber`. You need to catch when the method returns `FALSE`. Work backwards from there.

Deeply dive into the code and check what causes the cache invalidation. The goal is to identify which render element is being processed and then temporarily disable the block, or somehow remove the render element from the page. Keep repeating this process until you receive a `HIT` header value. After that, turn the blocks back on one by one until you see the `UNCACHEABLE` header. Once you've identified the culprit you'll need to investigate the problematic logic and brainstorm potential fixes. They are likely to be specific to your application and use-case.

### Additional tooling coming

Drupal 9.5 includes a new render cache debugging setting that will output cache tags and context as inline HTML comments -- similar to how Twig template suggestion debugging currently works. This feature is also enabled via a setting in your *development.services.yml* file. [See the relevant change record](https://www.drupal.org/node/3162480).

If this feature is available in the version of Drupal you're using, we highly recommend using it to track down which render element(s) has the wrong cacheability metadata applied.

## A note on cookies and sessions

Often the headers described above have good values, but the page is still not cached. Your server setup or web operations platform configuration **could be configured not to cache any pages with cookie or session values**. Specific platforms might not cache the page if the `set-cookie` header is present.

Additionally, any page that contains a PHP session is always uncacheable. The assumption here is that if the session is used to generate the content of the page it's possible that the content contains session-specific data and is therefore uncacheable.

The PHP Session is set as a `PHPSESSID` key in the `set-cookie` header. In Drupal, sessions should only be set for authenticated users. If you see a session cookie set for anonymous users, you need to scan custom and contributed code for the source of the session and investigate how to remove it from the anonymous scope.

## Varnish debugging strategies

Web application platforms typically provide a standard Varnish configuration optimized for their server setup. Unless you have a custom Varnish setup, there is probably not much under your control in this cache layer. To see if your site is cached properly, check the `varnish` header in the response headers of your page request.

If your `varnish` header returns `MISS`, we recommend reviewing the platform’s documentation to identify if you have any incompatible modules or Drupal settings. Then you should examine Drupal application headers and standard headers and see if they return a `HIT` value. If Drupal sends `no-cache` values, the Varnish layer will not cache the page.

Pages with cookies or sessions are usually not cached unless your Varnish layer has unique settings to exclude certain cookies or unset sessions. This involves advanced VCL configuration; you’ll usually need to work with your web hosting provider or system administrator to set up the conditions specific to your application.

**Tip**: Don't forget to verify that Varnish is also caching static sources like images, CSS files, and JS files in addition to the HTML for the page.

## Recap

Drupal sets both the standard HTTP caching headers, and some Drupal-specific headers, to communicate with browsers and reverse proxies and allow them to serve the page or its parts from the cache. To debug cacheability problems, you need to explore these headers and cache metadata provided by Drupal, identify which part of the system is sending the unexpected responses, and then correct it. You can use your browser's development tools and the network tab as a staring point to examine headers, and then dig deeper into the code to determine the next steps.

## Further your understanding

- Review the caching-related headers for your site. Do you see any surprising values? Can you explain why the values are what they are?
- Investigate cache headers we didn't mention today. What are they? What's their provider?

## Additional resources

- [Cacheable Response Interface Debugging documentation](https://www.drupal.org/docs/8/api/responses/cacheableresponseinterface#debugging) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Drupal's Caching System](/tutorial/overview-drupals-caching-system?p=3091)

Next
[Extend Drupal Site Monitoring with Contributed Modules](/tutorial/extend-drupal-site-monitoring-contributed-modules?p=3091)

Clear History

Ask Drupalize.Me AI

close
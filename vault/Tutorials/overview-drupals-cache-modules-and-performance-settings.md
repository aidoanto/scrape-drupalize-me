---
title: "Overview: Drupal's Cache Modules and Performance Settings"
url: "https://drupalize.me/tutorial/overview-drupals-cache-modules-and-performance-settings?p=3091"
guide: "[[drupal-site-administration]]"
---

# Overview: Drupal's Cache Modules and Performance Settings

## Content

The performance optimization settings and modules provided by Drupal core are intended to work for the broadest possible set of use cases. From an administrator's perspective they provide minimal configuration options, and are designed to just work by being enabled. But behind that simplicity are some powerful features that will help speed up any Drupal-powered application.

The core *Dynamic Page Cache* and *Internal Page Cache* modules are designed to provide a base cache setup for any site. These modules are responsible for the static page cache, dynamic page cache, and lazy loading optimizations.

For developers, Drupal provides a complete and well-designed Cache API. You can, and should, integrate it into your custom code. This integration includes defining the *cacheability* of any content your module outputs so that Drupal can be smart about how that affects how and when a page that incorporates the output can be cached -- as well as storing and retrieving the results of complex or long-running operations. The API also helps with setting appropriate HTTP headers for the responses Drupal generates for each request so that the user's browser and other layers in the stack can appropriately cache the output.

The entire system is flexible, and there are many contributed modules that can aid in making the default caching system even faster for specific use cases.

In this tutorial, we'll:

- Learn about the caching-related modules in Drupal core
- Review the Drupal core performance settings and recommended values

By the end of this tutorial you should be familiar with the Drupal core modules responsible for caching, their settings, and recommended values.

## Goal

Learn about the Drupal core performance modules and their settings, functions, and use-cases.

## Prerequisites

- None

## Drupal core performance modules

Caching of Drupal site is a **multilayer system** that differs based on the type of user visiting your site. Drupal site users can be divided into 2 main categories: anonymous or authenticated users.

- **Authenticated users** receive dynamic content based on their roles and permissions.
- **Anonymous users** receive static versions of pages.

With the correct setup (which we explore in this course), these pages may be fully served by the cache, bypassing Drupal database requests and improving performance.

Drupal comes with 2 main cache modules:

- [Internal Page Cache](https://www.drupal.org/docs/administering-a-drupal-site/internal-page-cache)
- [Dynamic Page Cache](https://www.drupal.org/docs/8/core/modules/dynamic-page-cache/overview)

### Internal Page Cache

This module caches whole pages for anonymous users and assumes the pages are identical for all anonymous users. You can think of this as asking Drupal to generate the HTML for a request, then caching the entire HTML document in the database so that the next time it's needed it doesn't need to be generated again.

### Dynamic Page Cache

This module caches parts of the page minus personalized dynamic pieces. This module provides a caching layer for authenticated and anonymous users. Sometimes it's not possible to cache the entire HTML output of the page as one large document. Instead, the page is broken up into chunks, some of which can be cached and some of which need to be calculated each time. Page requests are then filled by re-using the cached chunks and combining them into a complete HTML document with newly calculated values for other chunks.

Drupal core also comes with the [BigPipe](https://www.drupal.org/docs/8/core/modules/big-pipe) module based on the [BigPipe technique](https://engineering.fb.com/2010/06/04/web/bigpipe-pipelining-web-pages-for-high-performance/) that allows lazy loading parts of the page after the initial page rendering is finished. Think of all those Facebook pages where the main content loads really quick and then the app displays some gray bars while the other parts of the page are dynamically filled in.

### Internal Page Cache module

The *Internal Page Cache* module is well suited for small- to medium-sized web applications. The module is turned on by default. It stores static copies of pages and serves them to anonymous users. When a user visits the page for the first time, the page is captured and stored in the cache. For the next visit of the anonymous user, the cached version of the page is stored. The module stores the snapshot of the entire page and assumes that all pages are identical for all anonymous requests. Cached data is stored in database tables by default, though this functionality can be augmented with faster data-stores like Memcached or Redis.

If your site serves personalized information – shopping cart, countdown, notifications or dynamic alerts, etc. – to anonymous users, this module needs to be disabled. Otherwise, the personalized information of the first user to view the page will be cached and displayed to subsequent visitors. This limitation can be overcome by personalizing with JavaScript instead of server-level personalization.

If your site is on a larger scale or has complicated dynamic components that require timely updates and cache expiration, it's recommended to disable this module and use the an external Varnish cache layer or CDN instead. Internal Page Cache module ignores `Cache-Control` headers and stores the pages permanently until the cache invalidates or comes with an `Expires` header.

The module does not have any user-configurable settings. We recommend you enable this module if your site serves non-personalized content to anonymous users.

### Dynamic Page Cache module

The *Dynamic Page Cache* module is recommended for sites of all sizes. It caches parts of the page that don't include dynamic, personalized parts and provides cached content to anonymous and authenticated users. During the caching process, dynamic parts of the page are excluded and automatically turned into *placeholders*. The placeholders can, later on, be rendered through the traditional mechanism or via BigPipe. This module doesn’t have any configuration; it uses [Drupal's cacheability metadata](https://drupalize.me/tutorial/cache-api-overview?p=2766) to determine whether the particular component can be cached.

This module improves performance for authenticated users of sites hosted on shared hosting without an advanced back-end cache layer. But even if you host on an enterprise-level platform, the module will still significantly boost performance, and improve the experience of authenticated users.

We recommend you turn this module on for all sites unless you can point to a specific issue it's causing.

## BigPipe module

The *BigPipe* module uses the BigPipe technique for rendering placeholders. It works best in conjunction with the Dynamic Page Cache module. BigPipe doesn’t require any configuration and only needs to be turned on. It improves the front-end/perceived performance of a page. When BigPipe is used with the Dynamic Page Cache module, it allows your application to perform a fast initial page load and then stream the rendering of placeholders.

The BigPipe technique can cause a jarring experience for users if placeholders are loaded in places that create a significant content shift once they are populated. It may not work with dynamic components that rely on JavaScript for content rendering. Ultimately, the experience your users get depends on the configuration and setup of your theme. You may want to strategically consider the location of dynamic placeholders and potentially show loading animation to minimize content shift.

We recommend taking time to test the experience for both anonymous and authenticated users, before enabling BigPipe. Once enabled it can make a big difference for pages that contain personalized chunks of content. It's especially suited to scenarios where the main content of the page is the same for all users but 1 or more sidebar blocks, or dynamic field formatters like *Flag module* links, are user-specific.

The success of your BigPipe setup depends on the theme structure and settings, site requirements, and complexity of components.

## Performance page and settings

The performance settings page in Drupal can be accessed by navigation to *Administration*>*Configuration*>*Development*>*Performance* (/admin/config/development/performance) in the main menu.

Image

![Screenshot of the performance settings for the site](/sites/default/files/styles/max_800w/public/tutorials/images/drupal_performance_page.png?itok=72VYaesv)

Core provides settings for the `Cache-Control` headers. This sets the `max-age` header that Drupal outputs and passes it to browsers and CDNs. This defines an expiration period for the cached version of the page. For sites on shared hosting, or platforms without additional system-level cache or Varnish, it's recommended to set this value to at least a day. Your site configuration and business requirements may vary, and you may want to set the value to be less than a day if you have pages with fast-expiring content that needs to stay fresh. Think of this as how long something external to Drupal should be allowed to cache a page that Drupal has determined is cachable before it is required to check back for a new version.

Below the cache settings are bandwidth optimization settings. Drupal core provides mechanisms to aggregate CSS and JavaScript files. Essentially, it combines all your CSS files into a small number of CSS files and links those instead of dozens of individual files. This helps optimize the requests to assets used for each page since the user's browser will only issue a couple of HTTP requests for CSS files instead of dozens.

For sites without a CDN, it's a good idea to turn those settings on. Depending on the setup, you may want to turn off aggregation for sites with a CDN. If your CDN serves the asset files, and the pages are served from the edge, asset aggregation may not be the best approach; it might be better to leave the setting off. Each setup is different and we recommend testing your site's performance with and without aggregation turned on to determine what works best for your site.

## Cache API

Each of the modules above relies on module developers using Drupal's Cache API to appropriately define the *cacheability* of the data their modules are responsible for, and that they make use of cache bins to store the results of complex operations. Learn more about the Cache API and implementing it in your custom code starting with the [Cache API Overview](https://drupalize.me/tutorial/cache-api-overview) tutorial.

## Recap

Drupal core comes with a powerful Cache API, and some broadly applicable performance optimization modules. This includes the Internal Page Cache, Dynamic Page Cache, and BigPipe modules. These modules allow sites to serve pages, or parts of the pages, to anonymous or authenticated users from the cache, bypassing much of the work required to construct the page from scratch. This can drastically improve the performance of a site, and the sustainability of the server.

Drupal core exposes a `max-age` `Cache-Control` header value in the performance settings, and allows aggregating JavaScript and CSS files used on the site.

## Further your understanding

- We talked about the `Cache-Control` header; explore other cacheable metadata available in Drupal's HTTP responses.
- If your site shows a weather forecast with updates of the weather prediction every 15 minutes, what settings need to be adjusted, and modules enabled, to optimize performance but allow for freshness of the content?
- Learn about disabling caching options on your localhost to help speed up theme development in [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)

## Additional resources

- [Cache API Overview](https://drupalize.me/tutorial/cache-api-overview) (Drupalize.me)
- [Drupal Cache API](https://www.drupal.org/docs/8/api/cache-api/cache-api) (Drupal.org)
- [BigPipe technique overview](https://www.facebook.com/notes/10158791368532200/) (facebook.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Analyze Drupal Site Performance with WebPageTest](/tutorial/analyze-drupal-site-performance-webpagetest?p=3091)

Next
[Overview: Drupal's Caching System](/tutorial/overview-drupals-caching-system?p=3091)

Clear History

Ask Drupalize.Me AI

close
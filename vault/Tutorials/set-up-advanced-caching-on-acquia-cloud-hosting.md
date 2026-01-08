---
title: "Set Up Advanced Caching on Acquia Cloud Hosting"
url: "https://drupalize.me/tutorial/set-advanced-caching-acquia-cloud-hosting?p=3091"
guide: "[[drupal-site-administration]]"
---

# Set Up Advanced Caching on Acquia Cloud Hosting

## Content

**Note:** This tutorial is specific to Drupal sites hosted on the [Acquia](https://www.acquia.com) platform and covers integrating its features to improve performance.

The Acquia platform includes Memcache, Varnish, and Content Delivery Network (CDN) integration. In order for these to be as effective as possible, they should be configured and tuned for your specific use case. This tutorial provides an introduction to these utilities and common configuration. For more detail, you should consult the Acquia documentation.

In this tutorial, we'll:

- Learn what caching utilities are included in the Acquia platform
- Set up and tune different parts of Acquia's application caching level including Memcache and Varnish

By the end of this tutorial, you'll know what application-level caching options exist on Acquia's platform. And how to configure it, and your Drupal application, for better performance.

## Goal

Set up application-level caching on the Acquia Cloud platform.

## Prerequisites

- [Overview: Drupal's Caching System](https://drupalize.me/tutorial/overview-drupals-caching-system)
- [4.3. Installing a Module](https://drupalize.me/tutorial/user-guide/config-install?p=3069)

## Acquia application-level cache system overview

Application-level caching on Acquia consists of three components: Memcache, Varnish, and optional Content Delivery Network (CDN) caching.

[Memcached](https://memcached.org/) (Memcache daemon) is available for all applications on the Acquia Cloud platform. It allows moving common cached data (cache bins) out of the SQL database and into memory. Queries that are performed from memory are faster than from the database.

The most common use of Memcached for the Drupal application is to store Drupal cache tables in Memcached instead of the application's database layer. This is especially beneficial for sites with a high volume of authenticated traffic, or other scenarios where caching the full HTML document isn't an option and Drupal gets invoked for every page request. But it is worth setting up for any Drupal site.

[Varnish cache](https://varnish-cache.org/) is a caching reverse proxy installed in front of all Acquia Cloud Platform load balancers. Varnish caches anonymous user content and serves it from memory instead of making requests to the webserver (Apache + Drupal). Varnish also caches static assets such as images, JavaScript, and CSS files. Static assets are cached for anonymous and authenticated users. Files that are served using the Drupal private file system are not cached by Varnish.

The Acquia platform CDN is only available for select Acquia Enterprise cloud subscriptions. CDN allows delivering cached static assets and pages worldwide at over 65 points of presence (POPs). Global visitors will receive cached pages and assets from the POP closest to their current location.

## Use Memcache on Acquia

A quick aside, because the terminology can be confusing:

- *Memcache* is the PHP-SDK that integrates with the Memcached data cache
- *Memcached* is the free, open source, high-performance distributed memory object caching daemon

### Install Memcache integration module

To set up Memcache on Acquia, you need to install the [Memcache API and Integration module](https://www.drupal.org/project/memcache).

```
composer require drupal/memcache
```

Learn more about [installing modules with Composer](https://drupalize.me/tutorial/user-guide/install-composer?p=3074) and [downloading and installing modules from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install?p=3072).

### Download Acquia's memcache-settings package

After the module is downloaded, you do not need to enable it. It'll be enabled and configured through the *settings.php* file.

Follow the [Acquia documentation for enabling memcache](https://docs.acquia.com/cloud-platform/performance/memcached/enable/) for Drupal 9 or later.

- Add the composer package that contains the Acquia Memcache settings to your project with `composer require acquia/memcache-settings`

### Update *settings.php* to include Acquia's memcache settings

- Edit your site's *settings.php* to include Acquia's memcache settings.

Example updated *settings.php*:

```
if (file_exists('/var/www/site-php')) {
   require('/var/www/site-php/mysite/mysite-settings.inc');

   // Memcached settings for Acquia Hosting
   $memcache_settings_file = DRUPAL_ROOT . "/../vendor/acquia/memcache-settings/memcache.settings.php";
   if (file_exists($memcache_settings_file)) {
     require_once $memcache_settings_file;
   }
}
```

This updates the block that *requires* Acquia settings for your site. This way, Memcache settings are not applied to your local environments. Caching via the database will operate as usual.

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) after deploying your changes to Acquia Git or through Acquia SFTP.

This will effectively replace Drupal cache tables in the database with equivalents in the Memcached layer of the application-level caching.

## Use Acquia Purge for better Varnish Integration

Acquia has a preconfigured shared Varnish installation in front of all available load balancers. Custom Varnish configurations can be used by Enterprise level customers with dedicated load balancers.

You can control purging of the data your Drupal site stores in the Varnish cache, and then set a higher time to live (TTL) value for your cached content and improve the cache hit rate.

### Install the Acquia Purge module

Install the contributed [Acquia Purge module](https://www.drupal.org/project/acquia_purge). The Acquia Purge module invalidates cached content on Acquia Cloud and allows you to set Drupal's time to live (TTL) to a high value. This makes your Drupal application more resilient since the stack does less work.

```
composer require drupal/acquia_purge
```

### Enable the required modules

Enable the module with Drush (`drush en acquia_purge`) or through the UI.

Acquia Purge has a dependency on the [Purge](https://www.drupal.org/project/purge) contributed module that'll be installed and enabled together with the Acquia Purge module.

Enable all of the required submodule components with Drush or through Extend UI.

```
drush en purge_drush purge_queuer_coretags purge_processor_lateruntime purge_processor_cron purge_ui
```

This command enables the Drush Purge, Purge Queueur Core Tags, Purge Processor Late Runtime, Purge Processor Cron, and Purge UI modules.

### Configure one or more purgers

Add Acquia Cloud Purger to your configuration by running the following Drush command:

```
drush p:purger-add --if-not-exists acquia_purge
```

If you are using Acquia Cloud CDN, you'll need a second purger:

```
drush p:purger-add --if-not-exists acquia_platform_cdn
```

By design, this module doesn't have any exposed UI since only administrators should be able to make any changes. Changes to the purger configuration may affect the site's performance if done in the wrong way.

### Validate the settings and configuration

Since the Acquia Purge module doesn't have an exposed configuration, it relies on a series of Drush commands to validate settings and purge the queue.

To get the list of all purgers available on the site run the following command `drush p:purger-ls`. This returns a list of all available purgers and their instances.

Example:

```
drush p:purger-ls

------------ --------------------- ----------------------------
Instance     Plugin                Label
------------ --------------------- ----------------------------
f0eed62sf9   acquia_platform_cdn  Acquia Platform CDN
bcddfb627d   acquia_purge          Acquia Cloud
------------ --------------------- ----------------------------
```

To invalidate the cache, run the following command `drush p:purger-mvu {purger_instance}` where `{purger_instance}` is an ID returned in the "Instance" column of the purgers list.

To validate the purger setup run the diagnostics command `drush p:diagnostics --fields=title,severity`.

Example:

```
drush p:diagnostics --fields=title,severity

------------------------------ ----------
Title                          Severity
------------------------------ ----------
Acquia Purge Recommendations   OK
Acquia Platform CDN            OK
Acquia Cloud                   OK
Queuers                        OK
Page cache max age             OK
Page cache                     OK
Purgers                        OK
Capacity                       OK
Queue size                     OK
Processors                     OK
------------------------------ ----------
```

This returns the status of all of the purging components, queues, processors, and related best practices checked by the Acquia Purge module.

## Recap

The Acquia Cloud platform provides an application level caching layer consisting of 3 components: Memcached, Varnish, and an optional CDN. Making use of these additional caching layers requires installing the necessary contributed modules and configuring them to work with the Acquia platform. Once completed, this will add additional layers of caching, that are more efficient than Drupal's built-in caching, and help improve the performance of your application.

There is also a CDN component, which functions much like the Varnish layer, but it is only available on select Enterprise level subscriptions. It allows you to cache and serve pages and static assets from global POPs.

## Further your understanding

- What roles does Varnish play, and what benefits can you gain by using a custom Varnish configuration instead of the preconfigured default?
- Explore the Purge UI module and its settings.

## Additional resources

- [Improving application performance on Acquia Cloud official documentation](https://docs.acquia.com/cloud-platform/performance/) (docs.acquia.com)
- [Memcached](https://memcached.org/) (memcached.org)
- [Varnish cache official documentation](https://varnish-cache.org/) (varnish-cache.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Set Up Advanced Caching on Pantheon Hosting](/tutorial/set-advanced-caching-pantheon-hosting?p=3091)

Next
[Overview: Content Delivery Networks (CDNs) and Drupal](/tutorial/overview-content-delivery-networks-cdns-and-drupal?p=3091)

Clear History

Ask Drupalize.Me AI

close
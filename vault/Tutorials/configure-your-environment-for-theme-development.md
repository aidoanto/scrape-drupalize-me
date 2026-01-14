---
title: "Configure Your Environment for Theme Development"
url: "https://drupalize.me/tutorial/configure-your-environment-theme-development?p=3267"
guide: "[[frontend-theming]]"
---

# Configure Your Environment for Theme Development

## Content

Making Drupal [fast by default](https://drupalize.me/tutorial/fast-default) implies having caching layers and CSS and JavaScript aggregation utilities enabled out-of-the-box. As a theme developer this can be annoying, because you must clear these various caches in order to preview any changes. In addition, inspecting variables with debugging tools often produces PHP errors. We'll make some recommendations for PHP settings on your local environment that can prevent these errors from happening so often.

By the end of this tutorial, you should be able to:

- Set up your local Drupal site for theme development
- Prepare your local development environment for working on and debugging themes

## Goal

Access theme information in HTML comments for every template on a page and output variable debugging information for any active template file.

## Prerequisites

- None

Sprout Video

## Enable Twig debugging and disable the cache via the UI

**New as of Drupal 10.1**: Enable Twig's debug mode and disable Drupal's caching via the administrative UI. This is much easier than the process outlined below, but there are 2 important caveats:

1. The settings are stored as application state in the database. Because it's state you don't have to worry about accidentally deploying them as configuration. But, it means anytime you down-sync a copy of the database to your production environment you'll lose those changes.
2. **Render cache debugging** needs to be enabled separately via *development.services.yml*. (See below for instructions.)

To enable Twig debugging, in the *Manage* administration menu navigate to *Configuration* > *Development* (*admin/config/development/settings*), check the *Twig development mode* box, and then press the *Save settings* button. [Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).

Image

![Settings form with checkbox for enabling Twig debugging mode and disabling markup caching](../assets/images/twig-debug-ui-settings.png)

*Note*: When you turn off *Twig development mode* using the UI, [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) for it to take effect.

## Disable render caching to see template changes quickly

Render caching prevents seeing your Twig template changes without a cache clear.

Before enabling the Twig engine's debug mode you'll probably want to start with disabling Drupal's render cache. The first time Drupal renders an element, it uses the Twig template, and caches the resulting HTML output. Any subsequent request for the rendered version of that element is filled from the cached data, until the cache is invalidated. Disable render caching in order to bypass this cache and use the theme layer every time an element is rendered. If you don't, changes to the Twig template associated with an element will not be displayed until the cache has been cleared.

Image

![Flow chart showing how render api and themes find template files](../assets/images/render-api-lookup-flow.png)

The above diagram shows the process used to determine where HTML is retrieved from when rendering an `#element`.

## Disable render caching and JavaScript/CSS aggregation

Both render caching, and JavaScript/CSS aggregation can be disabled by making modifications to configuration variables in your *settings.php* file.

In addition, aggregation can be turned off in the UI by navigating to *Configuration* > *Performance* (*admin/config/development/performance*).

When setting up a development environment, change these settings directly in your *settings.php* file. (This is the preferred method.) The best way to do this is to enable the use of a *settings.local.php* file. Then put your environment-specific settings into this local file. From there, you can also include the *development.services.yml* file that comes with core, and use that as a location for your environment-specific services settings.

Follow these steps to disable render caching and CSS/JavaScript aggregation:

### Edit your settings.php file

Edit your *sites/default/settings.php* file and un-comment the code that includes an optional *settings.local.php* file. Make sure this code is at the bottom of your *settings.php* file so that local settings can override default settings.

The code at the bottom of your *sites/default/settings.php* file should look like this:

```
if (file_exists(__DIR__ . '/settings.local.php')) {
  include __DIR__ . '/settings.local.php';
}
```

### Copy example.settings.local.php

Copy *sites/example.settings.local.php* to *sites/default/settings.local.php*, and [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).

### Use settings.local.php

Drupal will now locate your *sites/default/settings.local.php* file, if it exists, when *sites/default/settings.php* is loaded. Since the local settings file is loaded last, any variables set there will override settings in the default file.

### Use development.services.yml

Using the *sites/default/settings.local.php* file will also include and use *sites/development.services.yml*.

### Uncomment lines in *settings.local.php*

Ensure that the following lines are uncommented by removing the `#` character from the beginning of the line.

This first set disables the CSS and JavaScript aggregation features.

```
$config['system.performance']['css']['preprocess'] = FALSE;
$config['system.performance']['js']['preprocess'] = FALSE;
```

And uncommenting this line effectively disables, or rather, bypasses the Render API cache:

```
$settings['cache']['bins']['render'] = 'cache.backend.null';
```

This disables Drupal's Render API caching by telling Drupal to use the *cache.backend.null* cache service instead of the default. This new service is defined in the *sites/development.services.yml* and essentially returns a `MISS` for every cache request, thus bypassing the Render API cache.

You can also disable the Dynamic Page Cache by uncommenting this line:

```
$settings['cache']['bins']['dynamic_page_cache'] = 'cache.backend.null';
```

Note: One point of possible confusion is that on the *admin/config/development/performance* page, in the Bandwidth Optimization settings, the checkboxes to enable CSS and JavaScript aggregation remain checked, even if you have turned these values off in *sites/default/settings.local.php*. So how do you know if your development settings are working? View source on your site's home page and if you see a long list of CSS files with recognizable names, aggregation is turned off. If you only see a few CSS files with filenames consisting of a bunch of random characters, then aggregation is on. Same goes for JavaScript files.

## Enable Twig debugging options

Enabling Twig debugging involves locating the `twig.config[debug]` settings in your *services.yml* or *development.services.yml* file and changing their values.

### Which services file should I use?

- These variables can be edited **either** directly in *sites/default/services.yml* **or** added to the *sites/development.services.yml* file (if you followed the steps above to use a *settings.local.php* file).
- If you want to use *sites/default/services.yml*, and it doesn't already exist, copy *sites/default/default.services.yml* and rename the copied file: *sites/default/services.yml*.

Since these are *development* settings, it makes a lot of sense to put these settings in *development.services.yml*, but either will technically work. You might want to think about the implications of accidentally deploying a *settings.yml* file to production with debug settings enabled in it.

### Enable Twig debug mode

Choose whether to edit *services.yml* or *development.services.yml*.

#### Turning on Twig debug mode in services.yml

If you copied *default.services.yml* to *services.yml*, **edit** the `twig.config` section as follows:

```
twig.config:
  debug: true
  auto_reload: true
  cache: false
```

#### Turning on Twig debug mode in development.services.yml

If you're using *sites/development.services.yml*, **add** the following `twig.config` configuration nested under the `parameters:` key. (Under the `http.response.debug_cacheability_headers: true` line will work.) Be sure to check that everything is properly indented or an error will result.

```
parameters:
  twig.config:
    debug: true
    auto_reload: true
    cache: false
```

Your *sites/development.services.yml* file now looks something like this:

```
# Local development services.
#
# To activate this feature, follow the instructions at the top of the
# 'example.settings.local.php' file, which sits next to this file.
parameters:
  http.response.debug_cacheability_headers: true
  twig.config:
    debug: true
    auto_reload: true
    cache: false
services:
  cache.backend.null:
    class: Drupal\Core\Cache\NullBackendFactory
```

### (Optional) Enable render caching debugging

As of Drupal 9.5.0 and Drupal 10.0.0, a new `debug` container parameter is available for `renderer.config`. You can find the default values for this in *sites/default/default.services.yml*.

To enable render caching debugging, update `renderer.config` and set its `debug` parameter value to `true` in your site's *services.yml* or *development.services.yml*.

Here's what our updated *development.services.yml* looks like after copying the `renderer.config` array from *default.services.yml* and stripping out the comments (which you can keep if you like):

```
parameters:
  http.response.debug_cacheability_headers: true
  twig.config:
    debug: true
    auto_reload: true
    cache: false
  renderer.config:
    required_cache_contexts: ['languages:language_interface', 'theme', 'user.permissions']
    auto_placeholder_conditions:
      max-age: 0
      contexts: ['session', 'user']
      tags: []
    debug: true
```

Note: We nested the `renderer.config` array under the `parameters` key in *development.services.yml*.

When render cache debugging is on, a new set of HTML comments containing information about cache tags, cache contexts, and cache keys will wrap each rendered element.

Like this:

```
<!-- START RENDERER -->
<!-- CACHE-HIT: No -->
<!-- CACHE TAGS:
   * node:1
   * node_view
   * user:1
   * user_view
-->
<!-- CACHE CONTEXTS:
   * languages:language_interface
   * theme
   * timezone
   * url.site
   * user.permissions
   * user.roles
   * user.roles:anonymous
   * user.roles:authenticated
-->
<!-- CACHE KEYS:
   * entity_view
   * node
   * 1
   * full
-->

<article data-history-node-id="1" data-quickedit-entity-id="node/1" role="article" class="contextual-region node node--type-page node--
...
</article>

<!-- END RENDER -->
```

See also this change record: [Render cache debug output](https://www.drupal.org/node/3162480).

### Check to make sure Twig debug mode is on

View source of any page on a local installation of your Drupal site, and you should see new HTML comments with information about template names and theme debugging information. For example:

```
<!-- THEME DEBUG -->
<!-- THEME HOOK: 'html' -->
<!-- FILE NAME SUGGESTIONS:
   * html--node--2.html.twig
   * html--node--%.html.twig
   * html--node.html.twig
   x html.html.twig
-->
<!-- BEGIN OUTPUT from 'core/themes/classy/templates/layout/html.html.twig' -->
```

Try [clearing/rebuilding the cache](https://drupalize.me/tutorial/clear-drupals-cache) if you've completed the above steps but don't see these theme debugging HTML comments yet.

## What do Twig debug settings mean?

```
twig.config:
  debug: true
  auto_reload: true
  cache: false
```

This is what each of the Twig debug settings is used for:

- **debug**: (boolean) Enable various debugging features in the Twig engine.
- **auto\_reload**: (boolean) When set to `true`, Twig will automatically recompile all templates when their source code changes.
- **cache**: (boolean) Disabling the Twig cache by setting this to `false` will recompile the templates from source each time they are used. In most cases the `auto_reload` setting above should be enabled rather than disabling the Twig cache.

With Twig debugging enabled, changes you make to your theme should show up the first time you refresh the page.

## PHP settings

[Inspecting variables in a template file](https://drupalize.me/tutorial/inspect-variables-available-template) is often a PHP-memory-intensive task. You may encounter a white screen with no helpful information when trying to access a page containing a template with debugging information. This white screen often indicates a fatal PHP memory limit error or maximum execution time limit, if you're inspecting many variables in a template file at once with Twig `{{ dump() }}`. Variables, especially with Drupal's render arrays, often contain extensively nested arrays and objects. You can view these errors (instead of a white screen) by adding or changing some configuration in your local environment's *php.ini* file.

Recommendations:

- Increase the PHP `memory_limit` value on your localhost to at least `128M`.
- Increase the PHP `max_execution_time` value to at least `60` (seconds).
- Set `error_reporting` to `E_ALL` so that all errors are caught.
- Set `display_errors` to `TRUE` so that PHP errors are displayed, instead of a white screen.
- Set `display_startup_errors` to display any errors during PHP's startup sequence.
- Set `html_errors` to `1` so that errors contain HTML tags and contain clickable links, making errors more readable and useful.

Your localhost *php.ini* would then contain the following values:

```
memory_limit = 256M
max_execution_time = 60
error_reporting = E_ALL
display_errors = TRUE
display_startup_errors = TRUE
html_errors = 1
```

You may need to increase the `memory_limit` (trying increasing by 128M at a time) or `max_execution_time` (trying increasing by 30 seconds at a time) if you're still running into memory limit errors.

To learn more about the implications of increasing the memory limit and the trade-off it has with concurrent processes, see this page on Drupal.org: [Changing PHP memory limits](https://www.drupal.org/docs/7/managing-site-performance-and-scalability/changing-php-memory-limits).

**Tip:** If `{{ dump() }}` or its alternatives are producing memory limit errors, try `{{ dump(_context|keys) }}` instead to discover the variable keys. Then inspect the keys one at a time with `{{ dump(variable_key) }}`.

## Debugging tools

Tools available for Drupal theme debugging:

- [Devel](https://www.drupal.org/project/devel), a Drupal project which provides a bunch of developer tools including the ability to configure which variable-dumping tool you want to use. It also provides Twig functions such as `{{ devel_dump() }}` and `{{ devel_breakpoint }}`. (For example, in a page template file you could use: `{{ devel_dump(page) }}` to see the `page` variable array and in conjunction with Xdebug, use `{{ devel_breakpoint }}` to set a breakpoint.)
- [Kint](https://github.com/kint-php/kint), a tool that was previously bundled with Devel, now its own PHP project that you download with Composer (`composer require kint-php/kint --dev`).

Learn more about installing and using these tools to inspect variables in the following tutorial:

- [Inspect Variables Available in a Template](https://drupalize.me/tutorial/inspect-variables-available-template)

### Xdebug

We recommend enabling Xdebug on your localhost and using it for debugging a theme or module. To install Xdebug, see the [documentation](https://xdebug.org/docs/install). Your local PHP installation may already have Xdebug installed. Learn how to [use Xdebug to inspect variables here](https://drupalize.me/tutorial/inspect-variables-available-template) or learn more about [how Xdebug displays PHP variable information here](https://xdebug.org/docs/display).

If you're using DDEV, see [Step Debugging with Xdebug](https://ddev.readthedocs.io/en/latest/users/debugging-profiling/step-debugging/).

## Recap

In this tutorial, you learned how to configure your local environment for theme development and template debugging. There were several facets to this configuration including enabling Twig debugging and turning off various caches in your local Drupal site's settings and services configuration files, editing some PHP variables to show errors, optimize variable inspection, and increase memory limit and max execution time, and installing various tools such as Devel, Kint, Twig Vardumper, and Xdebug.

With these tools and the above configuration in place, you are ready to [discover theme hook suggestions](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions) and [inspect variables available in a template file](https://drupalize.me/tutorial/inspect-variables-available-template).

## Further your understanding

- Why should you use a *settings.local.php* file instead of just editing *settings.php* directly?
- In which file do I change the settings that enables the Twig engines debugging output?
- Enable theme debugging for your own development environment and poke around a bit. What changed?

## Additional resources

- [DDEV: Providing custom PHP configuration (php.ini)](https://ddev.readthedocs.io/en/stable/users/extend/customization-extendibility/#providing-custom-php-configuration-phpini)
- [Discover Existing Theme Hook Suggestions](https://drupalize.me/tutorial/discover-existing-theme-hook-suggestions) (Drupalize.Me)
- [Inspect Variables Available in a Template](https://drupalize.me/tutorial/inspect-variables-available-template) (Drupalize.Me)
- [Fast by Default](https://drupalize.me/tutorial/fast-default) (Drupalize.Me)
- [Change all default settings and config to fast/safe production values](https://www.drupal.org/node/2259531) (Drupal.org)
- [Debugging Twig templates](https://www.drupal.org/node/1906392) (Drupal.org)
- [YAML syntax](https://drupalize.me/videos/introduction-yaml) (Drupalize.Me)
- [Rebuilding POP in D8 - Development Environments](https://www.lullabot.com/articles/rebuilding-pop-in-d8-development-environments) (Lullabot.com) - Covers setting up a localhost environment for a Drupal 8 project
- [Install Xdebug](https://xdebug.org/docs/install) (xdebug.org)
- [About Xdebug's PHP Variable Inspection](https://xdebug.org/docs/display) (xdebug.org)
- Change record: [Render cache debug output](https://www.drupal.org/node/3162480) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Fast by Default](/tutorial/fast-default?p=3267)

Clear History

Ask Drupalize.Me AI

close
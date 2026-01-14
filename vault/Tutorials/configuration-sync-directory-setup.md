---
title: "Configuration Sync Directory Setup"
url: "https://drupalize.me/tutorial/configuration-sync-directory-setup?p=2478"
guide: "[[drupal-site-administration]]"
---

# Configuration Sync Directory Setup

## Content

Before we start synchronizing configuration, let's take a look at the default, out-of-the-box file location for staging and synchronizing configuration. Then we'll walk through how to change that directory to a location outside our project's *docroot* and update *settings.php* appropriately.

In this tutorial, we'll cover:

- The default location of the configuration sync directory
- How the configuration sync directory is secured
- How to change the location of the sync directory

## Goal

Understand where Drupal puts the configuration sync directory upon installation and how to change that location, if desired.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

## Default configuration sync location

When you install Drupal, the system creates a directory that handles the importing of a configuration. By default, this directory lives in *DRUPALROOT/sites/default/files*.

## How the configuration sync directory is secured

It might strike you as odd to place a directory that will contain important information about your site in a web-accessible location. So to increase security, two steps have been taken:

1. The directory Drupal creates is named *config* and is appended with a long, unique hash. This makes it difficult for someone to mistakenly or maliciously navigate to the directory.
2. The config directory contains another directory named *sync*, which contains a hidden file called *.htaccess*. This file, read by the web server, contains instructions to ignore the existence of the directory altogether.

**Tip:** When navigating to your project's config directory, type `cd config` then press **tab** to autocomplete the full name of the directory with its long unique hash. (Don't try to copy and paste the name of the directory in this tutorial, as your project's config directory hash will be unique.)

Image

![Default file structure for configuration sync](../assets/images/files_0.png)

The configuration sync directory does not contain any configuration files when you first install Drupal. As you will learn later on in this series, when performing a synchronization, an exported archived file is imported and unarchived into this synchronization directory. After the import is complete, you can navigate to this directory and see the YAML files that describe the configuration of your site (assuming a *full export*).

The *sync* directory is used to stage configuration for import. It is the place where you put configuration that you would like to import into the site. You can view all the configuration that's ready to be imported at Configuration > Configuration synchronization (*admin/config/development/configuration*).

Image

![Alert message about configuration changes](../assets/images/synchronize_configuration_management.png)

*Screenshot shows an example of an alert message that displays on the "Configuration synchronization" administrative page when there are configuration changes.*

## Changing Drupal's configuration sync directory location

Now that we've looked at the default location of the configuration sync directory, let's learn how we can change this location to somewhere outside the web-accessible *docroot*.

### Navigate to the project root

As you can see in the example code repo, we've created a project directory (*demo-config-entities-8.x*) which contains a *docroot* directory, and is where our Drupal codebase lives. (Our Drupal document root is not the top-most directory of our project.)

First, if necessary, navigate to the level just above *docroot*, to the root of the project. When you list the files, you should see *docroot* (among other items) listed.

```
$ ls
README.md	composer.json	composer.lock	data		docroot		vendor
```

### Create new config and sync directories in the project root

Since we're assuming *docroot* is our web-accessible directory, let's now create configuration sync directories in the project root, outside *docroot*, in a non-web-accessible location.

```
$ mkdir config
$ mkdir config/sync
$ ls
README.md	composer.json	composer.lock	config		data		docroot		vendor
$ ls config
sync
```

### Create a README for future reference

To help us remember what this directory is for, let's copy the README from the default configuration sync directory into our newly created *sync* directory.

```
$ cp docroot/sites/default/files/config_USE_YOUR_LONG_UNIQUE_HASH/sync/README.txt config/sync/README.txt
```

Now we need to edit our Drupal project's *settings.php* to tell Drupal where the new configuration sync directory we want to use is located.

### Update *settings.php*

In *DRUPALROOT/sites/default/settings.php*, find the line that defines the value of `$settings['config_sync_directory']` (new as of 8.8.0) or `$config_directories['sync']` (deprecated and will be removed in Drupal 9). This is created during installation and is likely at the end of your *DRUPALROOT/sites/default/files/settings.php* file.

If your *settings.php* uses the deprecated `$config_directories['sync']`, change this to `$settings['config_sync_directory']`.

Then change the value of `$settings['config_sync_directory']` with your custom location. If you're following along, change the value to:

```
$settings['config_sync_directory'] = '../config/sync';
```

Otherwise, change the value to a location relative to your *DRUPALROOT* directory, which is accurate for your setup.

Now, in future configuration sync operations, configuration files will be staged in *PROJECTROOT/config/sync*.

## Check with your hosting provider

**Tip:** Before officially changing your configuration sync directory, be sure to check with your hosting provider to make sure you are not restricted from putting the configuration sync directory outside your Drupal root directory.

## Recap

In this tutorial, you learned the default location of the configuration sync directory and how it is secured from prying eyes. You also learned how to move that directory to a location outside a web-accessible site root location and update *settings.php* accordingly.

## Further your understanding

- What are the reasons why you might want to change your configuration sync directory location? What might prevent you from doing so?

## Additional resources

- Change record (24 June 2019): [The sync directory is defined in $settings and not $config\_directories](https://www.drupal.org/node/3018145) (Drupal.org)
- Change record (5 October 2015): [Configuration "staging" directory now moved to "sync"](https://www.drupal.org/node/2574957) (Drupal.org)

Downloads

[Sync folder](/sites/default/files/lewredistetubraprebreclibicebimobretresoluluroswumudredrauastapolophowedacraninitisladasposwibicrothoruspicrewrewrebrepepradricocugipoluprostepovumaprusaprestawraketanonarimimitotrebuwaslicheswibrephothirospostuhishibeprikinudispomaswophusp "lewredistetubraprebreclibicebimobretresoluluroswumudredrauastapolophowedacraninitisladasposwibicrothoruspicrewrewrebrepepradricocugipoluprostepovumaprusaprestawraketanonarimimitotrebuwaslicheswibrephothirospostuhishibeprikinudispomaswophusp")

[Sync alert](/sites/default/files/macitrastopheuawropifruditucloshuswekiualibacliswaprothokiuaphutriswocriuusafrapathilofruphodrophogocovewrijothiguwrevacrilewotocruswetucrachodruwiwufrowabrupimu "macitrastopheuawropifruditucloshuswekiualibacliswaprothokiuaphutriswocriuusafrapathilofruphodrophogocovewrijothiguwrevacrilewotocruswetucrachodruwiwufrowabrupimu")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Configuration Management in Drupal](/tutorial/overview-configuration-management-drupal?p=2478)

Next
[Clone of Your Drupal Site with Drush and Git](/tutorial/clone-your-drupal-site-drush-and-git?p=2478)

Clear History

Ask Drupalize.Me AI

close
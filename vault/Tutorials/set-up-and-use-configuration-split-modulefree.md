---
title: "Set up and Use Configuration Split Modulefree"
url: "https://drupalize.me/tutorial/set-and-use-configuration-split-module?p=2478"
guide: "[[drupal-site-administration]]"
---

# Set up and Use Configuration Split Modulefree

## Content

Modules like [Devel](https://www.drupal.org/project/devel) or [Stage File Proxy](https://www.drupal.org/project/stage_file_proxy) offer key advantages when developing locally, but should never be enabled on a production site. This poses a problem for Drupal as which modules are enabled *is* a configuration. Compounding this problem is the configuration provided by these modules, as well as key configuration that must be set differently locally compared to production.

Fortunately, the [Configuration Split module](https://www.drupal.org/project/config_split) provides a means to accomplish all of these goals. Once set up, configuration can be exported in one or more "splits", enabling you to target different configurations for different environments or situations.

## Goal

Set up and use the Configuration Split module.

## Prerequisites

- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project)
- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup)
- [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management)
- [How to Override Configuration](https://drupalize.me/tutorial/how-override-configuration)

## Install Configuration Split

Installation of the Config Split module is accomplished using Composer.

### Install modules and dependencies

Open a command prompt and navigate to the directory containing your site

```
cd path/to/your/site
```

### Install the required modules

Install [Config Filter module](https://www.drupal.org/project/config_filter) and the [Configuration Split module](https://www.drupal.org/project/config_split):

```
composer require drupal/config_filter drupal/config_split
```

### Enable the modules using Drush

```
drush en -y config_filter config_split
```

## Create the split directories

Once installed and enabled, we can create one or more "splits" in which to divide up our configuration. A typical split to create is one to separate development-specific configurations, from those which are used for production.

Before we can create splits in the UI, we need to create a directory in which to store the split configurations. The Configuration Split module recommends storing the split in a sibling directory to the `sync` directory.

[Earlier](https://drupalize.me/tutorial/configuration-sync-directory-setup), we had updated *settings.php* to specify the location of the sync directory:

```
$settings['config_sync_directory'] = '../config/sync';
```

This means that the `sync` directory is under the `config` directory, which is a sibling directory to our docroot:

```
path/to/our/site_repo
├── config
│   └── sync
└── docroot
    ├── core
    └── index.php
```

To create a new directory for our `development` split, we create a `development` directory in our `config` directory:

```
path/to/our/site_repo
├── config
│   ├── development  # New directory for the split
│   └── sync
└── docroot
    ├── core
    └── index.php
```

Be sure that the new directory has read, write, and execute permissions for the user account under which the web server runs.

## Create the split configuration

With the directory created, we can create the split configuration:

### Login as admin

Login to your site with administrator privileges

### Access Configuration Split settings

In the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration Split Settings*.

### Add a new split

Select *Add Configuration Split Setting*.

### Label the new split

Enter a *Label* of your choice. Try to make the label brief but descriptive.

### Set the directory location for the split

Under *Static Settings*, enter the *docroot*-relative path to the split directory in the *folder* field

```
../config/development
```

### Save the new split

Select *Save* to save the new split.

## Add split configurations

Creating the split alone isn't enough. It only ensures that configuration can be split. To split our configurations, we need to add them.

The Configuration Split module provides two methods to divide configurations:

- **Complete split** removes the configuration from the *config/sync* directory and places it only in the split directory (*config/development* in our example).
- **Conditional Split** retains the setting in the *sync* directory, but allows finer splitting if the split configuration and the *sync* configuration differ.

For modules such as [Devel](https://www.drupal.org/project/devel), [Stage File Proxy](https://www.drupal.org/project/stage_file_proxy), a complete split is preferred. Some production sites also disable core UI modules such as Views UI or Field UI and retain their activation in the split.

### Open the target split for editing

Using the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Configuration Split Settings* and open the target split for editing.

Under *Complete Split*, select the *Modules* and *Configuration Items* to only be available when this split is active.

Repeat the process for any *Conditional Split* settings.

When finished, select the **Save** button.

## Activate a split

Once the split is created, it needs to be activated. The Configuration Split module does not provide a UI for this purpose, but instead prefers that you modify your *settings.local.php* file for when to activate the split:

```
$config['config_split.config_split.the_split_name']['status'] = TRUE;
```

Where:

- **the\_split\_name** is machine name of the split we created earlier.

For our `development` split, we need to have it activated when working on our laptop or local workstation, but not in production. To do so, we add the following to our *settings.local.php* on our local system:

```
$config['config_split.config_split.development']['status'] = TRUE;
```

Our *settings.local.php* file is never tracked by Git, so this change does not require a commit.

For the production site we can choose not to have the line present in the settings file, or to disable it explicitly:

```
$config['config_split.config_split.development']['status'] = FALSE;
```

## Export configurations using split

When using Drush 8.1.11 or higher, there is no need to change your Drush commands. The Configuration Split module naturally plugs in to `drush cim` and drush `cex`, exporting split configurations transparently.

The module does provide a split-specific version of the subcommands to support older versions. The `config-split-export` (csex) subcommand exports configurations, while the `config-split-import` (csim) command imports them.

```
drush config-split-export
drush config-split-import
```

Both subcommands can accept a split name to export a specific split on demand:

To export a specific split:

```
drush config-split-export the_split_name
drush config-split-import the_split_name
```

Where:

- **the\_split\_name** is machine name of the split.

See the documentation page, [Configuration Split: CLI integration](https://www.drupal.org/docs/contributed-modules/configuration-split/cli-integration) for more information.

## Recap

The Configuration Split module is an excellent addition to your configuration management toolkit. It allows you to divide up your configuration such that different situations or different environments may have vastly different configurations. Once configured, importing and exporting splits is done transparently with a recent version of Drush, or by using the `config-split-export` and `config-split-import` subcommands.

## Further your understanding

- When different API keys are used between production and development, should a Complete or a Conditional split be used?

## Additional resources

- [Configuration Split on Drupal.org](https://www.drupal.org/project/config_split) (Drupal.org)
- [Configuration Split documentation guide](https://www.drupal.org/docs/contributed-modules/configuration-split) (Drupal.org)
- Change record (24 June 2019): [The sync directory is defined in $settings and not $config\_directories](https://www.drupal.org/node/3018145) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[How to Override Configuration](/tutorial/how-override-configuration?p=2478)

Next
[Automate Deployment of Configuration](/tutorial/automate-deployment-configuration?p=2478)

Clear History

Ask Drupalize.Me AI

close
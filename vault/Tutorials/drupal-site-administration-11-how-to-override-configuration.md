---
title: "How to Override Configuration"
url: "https://drupalize.me/tutorial/how-override-configuration?p=2478"
guide: "[[drupal-site-administration]]"
order: 11
---

# How to Override Configuration

## Content

Not every environment or copy of a site you may be working on will be created equally. You may want to enable logging on a development site or need to use different API keys depending on the environment. But you also need to make sure that your instance-specific configuration overrides don't make it into the database, mistakenly get exported, or compromise security.

In this tutorial, you will learn how to:

- Override the global `$config` array in *settings.php* (or *settings.local.php*)
- Retrieve overridden (immutable) configuration (read-only mode)
- Retrieve original (mutable) configuration for updating (read/write mode)
- Set dynamic values for configuration instead of overriding values

## Goal

Understand how to override configuration data for a local environment, how to retrieve non-overridden configuration data in a module, and how to set dynamic values for configuration with `hook_install`.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

## Watch: How to Override Configuration

Sprout Video

Note: in this tutorial, we'll be referring to overriding the `$config` array in your Drupal site's *settings.php* file. However, if you are utilizing a *settings.local.php* file or similar environment-specific *settings.php*, then you should use those files instead for your global `$config` overridden values.

Configuration overrides allow you to override your active configuration. As a module developer, you may want to provide different API keys for a remote API that your module talks to, or change some other configuration property by defining an override in your site instance's *settings.php*.

Let's take a look at two methods to override configuration.

## Global overrides

Creating global configuration overrides is done via the global `$config` variable, and uses the following syntax:

```
$config['configuration.prefix']['property_name'] = 'Property Value';
```

So as an example, we could override our site name, by adding the following to *sites/default/settings.php*:

```
$config['system.site']['name'] = 'Overridden Site Name';
```

**Note:** This is the equivalent of using the `$conf` variable in a Drupal 7 *settings.php* file.

Depending on your environment, you may need to provide a variety of overridden configuration. It is extremely important to note that any overridden configuration is not visible either via the Drupal administrative interface, when trying to edit configuration values, or returned by any Drush config commands. Configuration is displayed directly from the database. This is to stop you from committing overridden configuration to your active configuration without realizing you have done so.

## How to determine the `$config` array keys

You can figure out the `$config` array keys of the configuration item you want to override by updating the appropriate configuration form and then using Drush and Git to see what configuration item was changed. This method assumes that you have already exported your configuration with `drush config-export` and have committed the sync files to your git repo.

With the aim of overriding our local development logging setting, let's go figure out what the array key will be for our `$config` array.

### Edit the configuration with a form

On your development instance, edit the configuration that you want to override using its configuration form.

We're editing the logging and errors configuration, so navigate to *Configuration* > *Development* > *Logging and errors* (*admin/config/development/logging*). The default setting is **None**. Change it to **All messages**.

Image

![Logging and errors configuration form](../assets/images/config-form-logging.png)

### Export the configuration

Using Drush, export the configuration. Don't worry, this is just a temporary step so that we can examine the difference in the YAML file.

```
drush config-export
```

Drush will ask if you're sure; type 'y' and enter to continue.

### Inspect the diff

Using git — and assuming that you've already initially committed the files in your configuration sync directory, type the following:

```
git diff
```

If you have more than one modified file, you will want to specify the configuration file after `git diff`, for example: `git diff system.logging.yml`.

### Determine the array keys

Image

![Output of git diff system.logging.yml](../assets/images/config-overrides-git-diff.png)

The base filename of the file that changed is the first array key. In this example, *system.logging.yml* was the file that was changed, and so our first array key is `system.logging`.

The second array key is in the YAML file itself. Look for the line with the `+` sign in front of it in the `git diff` output. The key on this line is the second array key for the `$config` array.

Finally, the value on this same line is the value.

### Add override to settings.php

So, in *settings.php*, I would enter the following to override the `system.logging` value for my local development instance of the site:

```
$config['system.logging']['error_level'] = 'all';
```

### Change the setting back to what it was

Now, go back to the logging and errors form (*admin/config/development/logging*) and change it back to what it was before. Repeat the `drush config-export` process. Your git working directory (as far as that configuration file is concerned) should now be clean again.

## Retrieve configuration with or without overrides

You may wish to fetch configuration data in code, both with and without overrides. To get the most out of this section, you might want to first set up the *transcode\_profile* custom module with a configuration settings form [in this tutorial](https://drupalize.me/tutorial/create-settings-form-module).

A standard `get()` method for some configuration returns the configuration, **with** overrides:

```
$config = $this->config('transcode_profile.adminsettings');
$profile_name = $config->get('profile_name');
```

So if I override my configuration in my *settings.php* like so:

```
$config['transcode_profile.adminsettings']['profile_name'] = '720p h264 aac';
```

Calling `$config->get('profile_name');` as above would return `720p h264 aac`.

You can fetch configuration **without** overrides as follows:

```
$config = $this->config('transcode_profile.adminsettings');
$profile_name = $config->getOriginal('profile_name', FALSE);
```

Returning mutable configuration, which is configuration that is editable, always returns without overrides.

If you have access to `$config` by extending `ConfigFormBase`, then you can use:

```
$config = $this->config('transcode_profile.adminsettings');
$profile_name = $config->getEditable('profile_name');
```

You can also call the method directly:

```
$config = \Drupal::configFactory()->getEditable('transcode_profile.adminsettings');
$profile_name = $config->get('profile_name');
```

In either case, `$profile_name` is returned without overrides, in our example, `1920x1080 h264`.

## Override precedence

Overrides flow in the following manner, where global overrides take precedence:

```
global -> module -> language
```

## Dynamic configuration

While this is not strictly an override, it is worth mentioning that you can set your configuration dynamically from a module.

In [another tutorial](https://drupalize.me/tutorial/create-settings-form-module), we created a configuration form for our demo module called `transcode_profile`. If we were to create a form element to be used to set an email address to send a notification when someone enables transcoding, we might have some configuration in our `transcode_profile.settings.yml` that looks like this:

```
transcode_notify_address: '[email protected]'
```

Setting dynamic configuration must be done by implementing [hook\_install()](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_install/) in your module. However, you must ensure that Drupal is not currently syncing configuring before you make any changes to configuration objects or entities.

If we wanted to set the email to use dynamic data, first, we check to make sure Drupal isn't currently syncing configuration. Then, we set and save the new configuration values.

```
/**
 * Implements hook_install().
 */
function transcode_profile_install() {
  if (!\Drupal::isConfigSyncing()) {
    \Drupal::configFactory()->getEditable('transcode_profile.adminsettings')
      ->set('transcode_notify_address', \Drupal::config('system.site')->get('mail'))
      ->save();
  }
}
```

This would then set the `transcode_notify_address` dynamically, from `system.site mail`.

## Caveat: The problem with config entity overrides

Using configuration overrides with config entities comes with risks. Unlike regular configuration, config entities don't protect overridden values from being unintentionally saved back to storage. Depending on how a page or route loads the entity, Drupal may show override-free values in one place and overridden values in another—or even save the wrong version entirely. This can create confusing UI behavior and unexpected side effects, especially in contributed modules that rely on config entities for operational tasks.

The biggest issue appears when an entity is edited: Drupal may compare the “original” entity with overrides to a saved version without overrides, mistakenly thinking a property changed. That can trigger incorrect updates or data changes in modules that react to entity updates.

**Takeaway:** Use config overrides carefully with config entities. If you're a module developer, make sure your entity load/save paths explicitly use either the overridden or override-free version as needed. If you're a site builder, consider whether an override is truly necessary. For a deeper technical breakdown, read [The problems with config entity overrides](https://drunkenmonkey.at/blog/config_entity_overrides) (drunkenmonkey.at).

## Recap

In this tutorial, you learned how to override configuration data for a local environment, how to retrieve non-overridden configuration data in a module, and how to set dynamic values for configuration with `hook_install`.

## Further your understanding

- Practice finding out the key and value for a configuration item using the method described in this tutorial.
- When might you want to make use of a local *settings.php* file to store configuration overrides, especially if you're on a team?
- Can you think of an example on your site where you might want to create dynamic configuration in `hook_install` instead of overriding the setting in *settings.php*?

## Additional resources

- [Configuration override system](https://www.drupal.org/node/1928898) (Drupal.org)
- [Advanced Drupal 8 Configuration Management (CMI) Workflows](https://www.liip.ch/en/blog/advanced-drupal-8-cmi-workflows) (blog.liip.ch)
- [hook\_install API documentation](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_install/) (api.drupal.org)
- [The problems with config entity overrides](https://drunkenmonkey.at/blog/config_entity_overrides) (drunkenmonkey.at)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Configuration Interdependencies](/tutorial/configuration-interdependencies?p=2478)

Next
[Set up and Use Configuration Split Module](/tutorial/set-and-use-configuration-split-module?p=2478)

Clear History

Ask Drupalize.Me AI

close
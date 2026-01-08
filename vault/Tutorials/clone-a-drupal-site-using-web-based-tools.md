---
title: "Clone a Drupal Site using Web-Based Tools"
url: "https://drupalize.me/tutorial/clone-drupal-site-using-web-based-tools?p=2478"
guide: "[[drupal-site-administration]]"
---

# Clone a Drupal Site using Web-Based Tools

## Content

The configuration system in Drupal was designed to manage and sync configuration between instances of a Drupal site. So before configuration management can be useful, we must have another instance—or clone—of our Drupal site. In this lesson, you will learn:

- Why cloning a Drupal site is necessary in order to manage configuration
- How to clone a Drupal site using web-based tools

If you prefer using web-based or GUI tools [rather than command line tools such as Drush and Git](https://drupalize.me/tutorial/clone-your-drupal-site-drush-and-git), then this lesson is for you.

## Goal

Clone a Drupal site install using GUI tools instead of command-line tools.

## Prerequisites

- [Overview: Configuration Management in Drupal](https://drupalize.me/tutorial/overview-configuration-management-drupal)

**Note:** Feel free to skip this tutorial if you're already comfortable using [command-line tools to create a clone of your site](https://drupalize.me/tutorial/clone-your-drupal-site-drush-and-git).

## Watch: Clone a Drupal Site with GUI Tools

Sprout Video

## Why is cloning a site necessary?

The configuration system in Drupal was designed to manage and sync configuration between instances of a Drupal site, not to move configuration from one site to a completely different one. In order to import configuration, the site and import files must have matching values for the universally unique identifier (UUID) in the `system.site` configuration item (see Figure 1). You will have matching UUIDs if you clone a site. It doesn't matter if you create a development instance first and then clone it to make what will be the production instance, or the other way around.

Image

![Configuration YAML file](/sites/default/files/styles/max_800w/public/tutorials/images/system-site-yml-example.png?itok=hlwrS7rC)

**Figure 1.** An example of simple configuration. This *system.site.yml* was exported from the active configuration of the "live" instance of my demo site and lives in the active configuration directory of the local development instance of my site.\_

## Create a clone of your Drupal site using web-based tools

In this tutorial we'll go through the steps required to clone a Drupal site using graphical user interface (GUI) tools. You can also [clone a Drupal site using command line tools](https://drupalize.me/tutorial/clone-your-drupal-site-drush-and-git) if you prefer.

Note that the process I'm demonstrating here is completed locally. But you'd probably want to transfer this clone to another environment—a staging server, for example.

To start, I'll assume that you already have a Drupal site that you're ready to clone. I'll also assume that you know how to access [phpMyAdmin](https://www.phpmyadmin.net) locally for database management. You don’t need to understand phpMyAdmin, you just need to know how to access it.

### Duplicate the site's root directory

This is an easy process, but it's one that can go wrong quickly. This is because of hidden files, such as *.htaccess*, which are scattered through the file structure of a Drupal site. There are also lots of files with varying permissions that we don’t want to inadvertently modify in the process of copying them to another location. The easiest way to avoid missing files or changing permissions is to copy the root directory of your Drupal installation, instead of trying to select individual files inside the directory, which may cause you to overlook hidden files. Most operating systems will let you copy and paste the directory, which will create a new directory with the same name appended with something like “copy”. So let's do this!

**Duplicate your site's root directory.** For example if it's called *drupal8\_local*, after duplication, the copy is initially named *drupal8\_local copy*.

### Rename the duplicate directory

Rename this new copy of the directory to something like *drupal8\_production*. We now have a copy of our site's files.

Image

![Result of copying and renaming site directory](/sites/default/files/styles/max_800w/public/tutorials/images/copy-site-files.png?itok=EgN0KM2Z)

*Screenshot showing result of copying and renaming the site's root directory to a new location.*

### Duplicate the database using phpMyAdmin

Now we're going to duplicate the database using phpMyAdmin. We're doing this because it's web-based and operating system agnostic. But you can use any database management app you like.

1. Log in to phpMyAdmin.
2. Select the database for the site you're cloning by clicking its name in the sidebar.
3. Select the **Operations** tab located along the top of the page. This **Operations** page has a box labeled **Copy database to:**.

Image

![PhpMyAdmin copy database interface](/sites/default/files/styles/max_800w/public/tutorials/images/localhost_localhost_d8sb_phpmyadmin_4_4_10.png?itok=2j9yGHpn)

1. Complete the text field to give your new database a name. This works much like copying our root directory, where our first database has the name *d8\_local*, and we copy this it to *d8\_production*. The default values in the copy box are sufficient.
2. Click **Go** and a copy of the database will be generated on your local MySQL server to use for your cloned site. If you are just practicing configuration management with two sites on a local instance, then you can stop here.
3. Export the site to use on another server. More than likely the instances of your site will be hosted on two different environments. Select the Export tab and export the cloned database, saving it to your computer, which you can then import on the other MySQL server.

### Edit *settings.php* to point to the new database

Before launching our cloned site, we need to point it to our new database. The *drupal8\_production* site currently wants to read and write to our “local” database because it's a clone. There are two ways to do this: editing *settings.php* or utilizing *settings.local.php*. We'll start with the first method.

1. Change the read-only status of *settings.php* and allow `write (w)` permissions before editing.
2. Locate the `$databases` array in *drupal8\_production/sites/default/settings.php*

   Image

   ![The $databases array in settings.php](/sites/default/files/styles/max_800w/public/tutorials/images/settings_php_-_d8-tutorials.png?itok=eLcVH1EF)
3. Change the value of `'database'` to your new, copied database name:

- Was: `'database' => 'd8_local',`
- Change to: `'database' => 'd8_production',`

1. If your clone of the site is located on another host, you will also need to change the values for host, username, and password as well.

### Or, activate *settings.local.php*

You can also activate and utilize *settings.local.php* to store credentials for each environment and site instance.

1. To activate this feature, copy *sites/default/example.settings.local.php* and rename it to *settings.local.php*. It should be in the same directory as the original *settings.php*. Then, go to the bottom of *settings.php*, uncomment the following commented lines, and move this block to the very end of the file, if it isn't already, to ensure that any overrides in *settings.local.php* are read last.

```
if (file_exists(DRUPAL_ROOT . '/' . conf_path() . '/settings.local.php')) {
  include DRUPAL_ROOT . '/' . conf_path() . '/settings.local.php';
}
```

1. Copy the `$databases` array from *settings.php* to *settings.local.php* and edit the array with the local instance's database credentials. Repeat this process for each clone or instance of your site.

**Tip:** If you are using Git, add *settings.local.php* to your site's *.gitignore* file. If you are using FTP, take care not to overwrite another instance's *settings.local.php* with your local one.

### Change back permissions to read-only

After you are done editing *settings.php* or *settings.local.php*, change back their permissions to read-only, removing any write permissions.

### Verify your site and test an import

You've created a clone of your Drupal site! Open the cloned site in a browser to make sure it's working. You are now ready to test a configuration import. You can use the administrative UI provided by the Configuration Manager module to do this. Proceed to [Synchronize Configuration with the UI](https://drupalize.me/tutorial/synchronize-configuration-ui) to learn how.

## Recap

In this tutorial, you learned how to use GUI tools to clone the database and files of a Drupal site. This was necessary because the configuration system is designed to move configuration from one instance (or clone) of a Drupal site to another.

## Further your understanding

- Try cloning a Drupal site that exists on an external web host to your local environment.

## Additional resources

- [Synchronize Configuration with the UI](https://drupalize.me/tutorial/synchronize-configuration-ui)
- [PhpMyAdmin](https://www.phpmyadmin.net/) and [Quick Install instructions](https://docs.phpmyadmin.net/en/latest/setup.html#quick-install)
- [SequelPro](https://www.sequelpro.com/) - a favorite OS X MySQL database manager amongst Drupalize.Me trainers
- [API documentation for example.settings.local.php](https://api.drupal.org/api/drupal/sites%21example.settings.local.php/11.x) (api.drupal.org)

Downloads

[uuid](/sites/default/files/cranathobraslelepholohebekib "cranathobraslelepholohebekib")

[Database settings](/sites/default/files/cakemothipufrodridratewebriswebrebagetucomicikefrabadreraspocisladrecrapacrusoswichomutulut "cakemothipufrodridratewebriswebrebagetucomicikefrabadreraspocisladrecrapacrusoswichomutulut")

[Hidden files](/sites/default/files/mithistithegapechibesloslohastepinothuuahawotrajiwrewawrochehishejabuwrunesadraspogugushebawislokakosesludrowruproparaprestuswauowreche "mithistithegapechibesloslohastepinothuuahawotrajiwrewawrochehishejabuwrunesadraspogugushebawislokakosesludrowruproparaprestuswauowreche")

[phpMyAdmin copy database to:](/sites/default/files/thecreclodecrihudrihecubapojiswusihaswetishapacivechisweshulireuekonaguchawonurobrigichasoconaphagolududregoslupruphodupocririmereprodocestucracuwrophatrucilicajishoprisekimeluwrajekerewruslusowrucle "thecreclodecrihudrihecubapojiswusihaswetishapacivechisweshulireuekonaguchawonurobrigichasoconaphagolududregoslupruphodupocririmereprodocestucracuwrophatrucilicajishoprisekimeluwrajekerewruslusowrucle")

[Result of copying site files](/sites/default/files/bedriwuwogocrathebolocamispihudrekestuturobriclaspejithobuswesedracadabruwrewreuowrohuthocofraspothuswaslochitresluthohestimawithecrohiuopetrusicrovopaheuotalu "bedriwuwogocrathebolocamispihudrekestuturobriclaspejithobuswesedracadabruwrewreuowrohuthocofraspothuswaslochitresluthohestimawithecrohiuopetrusicrovopaheuotalu")

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Clone of Your Drupal Site with Drush and Git](/tutorial/clone-your-drupal-site-drush-and-git?p=2478)

Next
[Synchronize Configuration with the UI](/tutorial/synchronize-configuration-ui?p=2478)

Clear History

Ask Drupalize.Me AI

close
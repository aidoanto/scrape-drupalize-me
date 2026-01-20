---
title: "Clone of Your Drupal Site with Drush and Git"
url: "https://drupalize.me/tutorial/clone-your-drupal-site-drush-and-git?p=2478"
guide: "[[drupal-site-administration]]"
order: 4
---

# Clone of Your Drupal Site with Drush and Git

## Content

Before you can get started synchronizing configuration between instances of your site, you'll need to create a new instance or "clone" of your Drupal site.

By the end of this tutorial, you should know:

- Why it's necessary to clone your site if you want to manage configuration between environments
- How to find your site's universally unique identifier (UUID)
- What to consider when setting up a directory structure for your project
- How to clone a Drupal site

## Goal

Be able to create a clone of a Drupal site installation with command-line tools Drush and Git.

## Alternative method

If you don't want to use command-line tools for this process, see:

- [Clone a Drupal Site using Web-Based Tools](https://drupalize.me/tutorial/clone-drupal-site-using-web-based-tools)

## Prerequisites

- A local installation of Drupal.
- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup)
- [Working with Remote Git Repositories](https://drupalize.me/tutorial/working-remote-git-repositories)

Sprout Video

## Why is cloning a site necessary?

The configuration system in Drupal was designed to manage and sync configuration between instances of a Drupal site, not to move configuration from one site to a completely different one. In order to import configuration, the site and import files **must have matching values for the universally unique identifier (UUID) in the `system.site` configuration item** (see Figure 1). Otherwise, you will not be able to import configuration.

You will have matching UUIDs if you clone a site. It doesn't matter if you create a development instance first and then clone it to make what will be the production instance, or the other way around.

Image

![Configuration YAML file](../assets/images/system-site-yml-example.png)

**Figure 1.** An example of simple configuration. This *system.site.yml* was exported from the active configuration of the "live" instance of my demo site and lives in the active configuration directory of the local development instance of my site.

## Clone a Drupal site

So, you want to manage configuration between 2 site instances? Let's walk through how to clone a Drupal site.

### Find your site's UUID with Drush

You can find your site's UUID with Drush's `config-get` or `cget` (for short) command. Open Terminal and navigate to the root of your Drupal site. Run the following Drush command:

```
drush config-get system.site uuid
```

**Tip:** Use the shortcut `drush cget system.site uuid`.

Take note of the long string that is returned. This is your site's UUID.

### Determine the directory structure of your project

Before you clone your site, you will want to finalize the directory structure, especially the location of your configuration sync directory.

Consider the following example directory structure for your project:

```
/project_root
/project_root/config // Not web accessible
/project_root/docroot // Web accessible; location of Drupal files
/project_root/tests // And any other directories you might need.
```

**Tip:** Be sure you've updated your *settings.php* with the final location of your configuration sync directory. See [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup) to learn how.

### Initialize Git repo in your project's root directory

Navigate to the project root (which may be a level above your Drupal root) before initializing the Git repository.

```
git init
```

If you're using the example directory structure, then you should see both *config/* and *docroot/* as "Untracked files" after you run `git status`.

### Copy *example.gitignore* to *.gitignore*

Create a *.gitignore* file by copying Drupal's *example.gitignore*. Here, we're assuming your Drupal files are in your project's *docroot* directory.

```
cd docroot
cp example.gitignore .gitignore
```

Notice that *settings.php* is now ignored by Git. This means that we'll have to manually copy this file to our new instance, since it won't be included in our Git repository when we run `git pull` in the new project instance of our site.

### Stage files in Git

```
git add -A
```

If you run `git status` after this, you should see all the files that are staged for commit.

### Commit with a message

```
git commit -m "Initial commit"
```

You can now [push to a remote repository (after adding a remote)](https://drupalize.me/tutorial/working-remote-git-repositories).

```
git push origin master
```

### Create a database backup (dump)

You can use Drush to export your database to a *.sql* text file, like so:

```
drush sql-dump > drupalbackup.sql
```

Where *drupalbackup.sql* is whatever meaningful filename you want to use to name your database export.

We're now ready to set up the new instance. The process will be unique to your environment, but you should be able to follow the next steps, at least in general.

### Pull the files down from your Git repository

On the new instance of your project ([assuming you've set up a remote](https://drupalize.me/tutorial/working-remote-git-repositories)), run:

```
git pull
```

### Copy *settings.php*

Since *settings.php* is ignored by Git (in *.gitignore*), we need to copy it using other means. How you copy it over depends on your setup. But copy it to your new site instance's *DRUPALROOT/sites/default directory*.

If the database credentials are different in this cloned instance, you will need to update the `$database` array at the end of the copied *settings.php*.

### Import the database

Copy the database dump file to the cloned site instance and import it. Assuming that the *drupalbackup.sql* dump file is located in your Drupal root directory, you can run the following Drush command from your Drupal root to import the directory:

```
drush sqlc < drupalbackup.sql
```

### Test the cloned site in a browser

The site should display the home page without needing to go through the Drupal installer script.

## Recap

In this tutorial, you learned how to clone a Drupal site with Drush and Git. This was necessary to learn because the configuration system in Drupal is designed to deploy configuration from one instance (or clone) of a Drupal site to another.

## Further your understanding

- What are the pros and cons of changing the project directory structure from the default structure?
- Why is it good practice to ensure that Git ignores *settings.php*?

## Additional resources

- [Drush](https://drupalize.me/topic/drush) (Drupalize.Me and others)
- [Git](https://drupalize.me/topic/git) (Drupalize.Me)
- [Command Line Basics](https://drupalize.me/series/command-line-basics-series) (Drupalize.Me)
- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup) (Drupalize.Me)
- [Clone a Drupal Site using Web-Based Tools](https://drupalize.me/tutorial/clone-drupal-site-using-web-based-tools) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Configuration Sync Directory Setup](/tutorial/configuration-sync-directory-setup?p=2478)

Next
[Clone a Drupal Site using Web-Based Tools](/tutorial/clone-drupal-site-using-web-based-tools?p=2478)

Clear History

Ask Drupalize.Me AI

close
---
title: "Use Drush for Common Site and Environment Management Tasks"
url: "https://drupalize.me/tutorial/use-drush-common-site-and-environment-management-tasks?p=2593"
guide: "[[command-line-tools-drupal]]"
---

# Use Drush for Common Site and Environment Management Tasks

## Content

Administration and maintenance of Drupal websites consists of many tasks that can both be performed via the command line, and automated, with Drush. Using Drush's site and environment administration commands you can run database updates, check an environment's status, clear (rebuild) the cache, perform Cron-related operations, and manage users. These tasks are repetitive, often require many steps in the UI, and may be tedious in the long run. Learning to execute them with Drush can save you time and allows for more automation of common tasks.

In this tutorial we'll:

- Use Drush to check a site's status
- Learn how to perform database updates with Drush
- Clear the Drupal cache with Drush
- Use Drush to execute Cron tasks for a Drupal site
- Learn how to use Drush to login to a site as any user, and manage existing users

By the end of this tutorial you'll be able to perform many common Drupal environment and administration tasks from the command line with Drush. We're not going to cover all of the environment management commands in this tutorial, just some of the more popular ones. We encourage you to explore further on your own.

## Goal

Introduce common Drush site and environment administration commands to developers. Cover their possible applications and use cases.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [What Is Drush?](https://drupalize.me/tutorial/what-drush-0)

## Quick reference

This tutorial covers the following Drush commands:

- `core:status` - Get an overview of the current environment - Drush and Drupal
- `core:requirements` - Get a full site report similar to the status page in the Drupal administration UI
- `updatedb:status` - Check if any database updates are required
- `updatedb` - Perform any outstanding database updates
- `cache:rebuild` - Rebuilds Drupal's registry, clears Drupal's render cache, clear's Drush's internal cache
- `cache:clear` - Clear a specific named cache bin
- `core:cron` - Run Drupal's cron tasks for a site
- `user:login` - Login as any user

## Check environment and site status with Drush

One of the most often used commands is `drush core:status`. This command returns the status of the environment - Drush and Drupal, providing key information about a site at glance. The output is something like below:

```
 Drupal version   : 8.9.13                                                           
 Site URI         : http://drupal.dev.localhost                                      
 DB driver        : mysql                                                            
 DB hostname      : 127.0.0.1                                                        
 DB port          : 3306                                                             
 DB username      : root                                                             
 DB name          : drupal8                                                          
 Database         : Connected                                                        
 Drupal bootstrap : Successful                                                       
 Default theme    : bartik                                                           
 Admin theme      : seven                                                            
 PHP binary       : /usr/local/Cellar/[email protected]/7.4.34_4/bin/php                       
 PHP config       : /usr/local/etc/php/7.4/php.ini                                   
 PHP OS           : Darwin                                                           
 Drush script     : /Users/enotick/Sites/drupal-project/vendor/drush/drush/drush     
 Drush version    : 10.3.6                                                           
 Drush temp       : /tmp                                                             
 Drush configs    : /Users/enotick/Sites/drupal-project/vendor/drush/drush/drush.yml 
                    /Users/enotick/Sites/drupal-project/drush/drush.yml              
 Install profile  : standard                                                         
 Drupal root      : /Users/enotick/Sites/drupal-project/web                          
 Site path        : sites/default                                                    
 Files, Public    : sites/default/files                                              
 Files, Private   : sites/default/files/private                                      
 Files, Temp      : /tmp
```

This includes: Drush and Drupal core versions, PHP version, database driver and connection information, information about the file system, themes that are used, and more.

This command also informs developers if the site's bootstrap was successful. This is the first indication of the site's health. If bootstrap is unsuccessful, it means that Drupal cannot be initialized and something is wrong with one of its core systems.

Learn more about Drupal's status reports in [12.5. Concept: Status Report](https://drupalize.me/tutorial/user-guide/prevent-status?p=3078).

The `drush core:status` command is commonly used as an "is this thing on?" test, and to retrieve common information like the URL or DB credentials for a development environment.

For a more in-depth report that corresponds to the status report you see through Drupal's UI, use the `drush core:requirements` command. This command produces a full status report of the site's health that can be filtered by severity using `--severity` option, by requirements using the `--ignore` option (with a comma separated list of requirements that need to be excluded from the report), or filtered using the `--filter` option. As with the majority of other Drush commands, the output can be formatted with the `--format` option.

To see the list of all available options, refer to the [official Drush documentation for this command](https://www.drush.org/latest/commands/core_requirements/).

## Update Drupal database

Often times, the status command indicates that the database is out of date and updates need to be run. It's also important to run database updates anytime you update the the code for Drupal core or any contributed modules your site uses. Drush comes with commands that allow you to check if any updates are needed, and to perform updates. These commands are the equivalent of visiting Drupal's update.php script in the browser.

To check the list of pending database updates run `drush updatedb:status`. This command will either provide the list of outstanding updates or confirm that no updates are required.

To execute updates run `drush updatedb`. This command comes with a series of options that can be passed into it.

One of the most useful options is `--no-post-updates`. Database updates include the schema updates themselves, post-update operations, and cache purge operations. In real world scenarios, it's common that database updates return errors during the post-updates cycle. Passing the `--no-post-updates` option helps to break the command down into stages and is very useful for debugging and performing semi-manual update execution when a typical automatic process runs into issues.

Developers can also prevent cache clearing by passing in the `--no-cache-clear` option.

To see the list of all available options, refer to the [official Drush documentation for this command](https://www.drush.org/latest/commands/updatedb/).

## Manage Drupal's cache with Drush

Drush comes with a group of cache-related commands. One of the most popular commands that many developers use daily is `drush cache:rebuild`, or `drush cr` for short. This command rebuilds Drupal's registry (things like routing tables, lists of modules in the codebase, etc.) as well as purging the render cache and Drush's cache.

If you worked with Drupal prior to version 8, you might be familiar with the `drush cache:clear` command. Its shortcut `drush cc all` -- clear all Drupal caches -- was an equivalent to `drush cache:rebuild` for Drupal 7 and below.

Even though `drush cc all` is deprecated, the `drush cache:clear` command itself is not, and it can be used to clear specific caches including drush, theme-registry (rebuilds Twig), CSS and JavaScript caches, or a specific cache bin. This command is mostly used for debugging, specific back-end and front-end development tasks, and its variation `drush cc drush` is often used during the development of custom Drush commands. A theme developer might, for example, use `drush cc theme-registry` after adding new template files so that Drupal will find them but still respond quicker than if all caches were cleared.

Learn more about Drupal's caches and clearing them in [12.1. Concept: Cache](https://drupalize.me/tutorial/user-guide/prevent-cache?p=3078) and [Clear Drupal's Cache](https://drupalize.me/tutorial/clear-drupals-cache).

## Run Drupal's cron

Running Drupal cron through the UI is prone to browser timeouts, especially if the site has heavy processes such as imports or migrations to be executed during a cron run. Running cron via the command line helps to avoid this problem as the CLI is often configured to have no, or a much longer, timeout for PHP tasks.

Drush comes with the `drush core:cron` command that allows you to execute cron on your site. This is a very popular command, so in some tutorials and documentation you may see its alias `drush cron` used more widely.

The command also outputs the statuses of all tasks as they are being executed and allows you to see if any of the processes are failing. Especially useful when trying to author and debug your own custom cron tasks.

Learn more about Drupal cron in [13.1. Concept: Cron](https://drupalize.me/tutorial/user-guide/security-cron-concept?p=3079).

## User management with Drush

Drush comes with the *user* group of commands to allow you to perform common user management tasks via the command line.

One of the most used commands is `drush user:login` or its alias `drush uli`. This command by default allows you to login to the site as a user 1 root administrator. It also takes options allowing you to login as a different user. You can pass in `--name`, `--uid`, `--mail` arguments with username, user id, or user email respectfully. The command will output a one-time login link that you can follow to login as the specified user. This is super handy when working on development environments where you may not know the user 1 credentials, or when the database is sanitized before being copied and all user names and passwords are reset.

One of the common use cases is login to the site as a different user than a super administrator. For instance, running `drush user:login --name=elizabeth`, will let you login as a user with the username `elizabeth`. This is useful if you are trying to test permissions, or see the site from the point of a view of a user with a different set of roles than yours.

To see the list of all available options, refer to the [official Drush documentation for this command](https://www.drush.org/latest/commands/user_login/).

Learn more about the types of tasks involved in Drupal user management in [Chapter 7. Managing User Accounts](https://drupalize.me/series/user-guide/user-chapter). Most of these tasks can be accomplished with Drush including: create, block, unblock, delete users, change user passwords, and add and remove roles. A full list of the commands can be found in the [official Drush documentation](https://www.drush.org/latest/commands/user_block/).

## Recap

Drush comes with lots of commands for common environment and site administration tasks. These commands allow you to check the site and environment status, perform required database updates, clear caches and rebuild the site, initiate a cron run, manage users and login into the site as an administrator -- all from the command line. Learning to use these commands speeds up site maintenance and makes administration tasks easier, faster, and available for scripting solutions.

## Further your understanding

- Can you use Drush to create a user and assign them a new role that exists on the site?
- Use Drush to clear a specific cache bin.
- What is the difference between `drush core:status` and `drush core:requirements`?

## Additional resources

- [Drush official documentation](https://www.drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Enable, Update, and Manage Modules and Themes with Drush](/tutorial/enable-update-and-manage-modules-and-themes-drush?p=2593)

Next
[Use Drush to Speed up Common Drupal Development Tasks](/tutorial/use-drush-speed-common-drupal-development-tasks?p=2593)

Clear History

Ask Drupalize.Me AI

close
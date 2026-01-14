---
title: "planning and preparation"
url: "https://drupalize.me/tutorial/preparing-migration-drupal"
guide: "[[learn-migrate-drupal]]"
---

# planning and preparation

## Content

Before you begin a Drupal 6 or 7 (source) to Drupal 9 or 10 (destination) migration there are a number of things you should consider. Taking the time to plan your migration will help to ensure that you're successful. In this tutorial we'll take a high-level look at:

- Evaluating your existing Drupal 6/7 site for migration feasibility
- Preparing your source Drupal 6/7 site for a migration
- Preparing the destination Drupal site you're migrating to

By the end of this tutorial you should be ready to start assessing the feasibility of performing a successful migration, and begin making a migration plan.

## Goal

Create a plan for performing a Drupal-to-Drupal migration.

## Prerequisites

- [Introduction to Migrations with Drupal](https://drupalize.me/tutorial/introduction-migrations-drupal)

## Drupal 6 vs Drupal 7

Throughout this section of the guide we'll be primarily talking about migrating from Drupal 7 to the latest version of Drupal, because that's the use case in our example project. The Drupal core migrate system also supports migrating from Drupal 6, though to a lesser degree. While Drupal 6 core is fully supported, because of its age, Drupal 6 contributed modules are less likely to have support. That said, the big one when it comes to data, [CCK](https://www.drupal.org/project/cck), is currently supported.

When migrating from Drupal 6, the process is quite similar, but the exact details vary since Drupal 6 and Drupal 7 are not identical.

## Evaluate your application

Before migrating any data, consider the platform. Unlike an OS upgrade -- where you hit "upgrade", come back in a few hours, and everything just works -- a move to the latest version of Drupal is likely to be as much a rebuild as it is an upgrade. Content can be systematically moved over via scripts (this is what the migration system handles for you), but you'll need to recreate your custom modules, themes, and various other elements, reconfigure views, and more. The more complex the Drupal 7 site you're starting from, the more complicated the migration is going to be.

Here are some questions to prepare with:

- Which modules are you using? Which of those modules are now in core? And, which modules can you just retire?
- Are there new best practices that you should consider using instead of what you're using now? For example, are you using node/user references in Drupal 7? This might be a good time to update them to use the more generic, and supported, entity references.
- How do you like your theme? You're going to have to recreate it so that it works in Drupal 9 or 10, so this might also be a good time to reorganize your CSS, implement a preprocessor like Sass, or even implement a redesign.

Your answers to these questions will likely affect the overall migration plan.

## Consider your content and content types

Now is a great time to step back and think about the overall information architecture of your site. You're already going to be doing a lot of work to migrate your content, so deciding to shuffle things a little bit now might not add any significant extra time. Additionally, starting with Drupal 8, Drupal is a different platform than either Drupal 6 or 7 and there are some new best practices and new ways of doing things that might not have been available before.

Taking the time to do a content audit prior to migration can save you a lot of extra work. Learn more in [Drupal-to-Drupal Migration Planning: Content Inventory](https://drupalize.me/tutorial/drupal-drupal-migration-planning-content-inventory). And if you're considering altering your content types as part of your migrations you're going to need to read up on [Custom Drupal-to-Drupal Migrations](https://drupalize.me/tutorial/custom-drupal-drupal-migrations).

## Are you an administrator?

You're going to need the keys to both the Drupal 7 site, and the future Drupal site in order to perform a successful migration. Make sure you have the information to log in as the user with ID 1 on both sites. On the Drupal 7 side you'll need to this to update modules, and prepare the site for migration. On the destination Drupal site, you'll need this account in order to execute any migrations.

## Make sure your Drupal 7 site is up-to-date

Before you proceed with a migration to the latest Drupal version you'll want to make sure Drupal core and all the contributed modules you're using on your Drupal 7 site are up-to-date and using their latest versions. Making sure you're using the latest version of a module also ensures that any configuration or data that the module is responsible for is up-to-date. Modules can change their schema over time, and it's likely that any latest Drupal version of a module only provides a migration path for Drupal 7 data in the current format.

If you've got a lot of modules that are out of date, or contributed modules that for one reason or another are going to be challenging to update, make sure you take that into account when planning for your migration. These things can take time.

Learn how to [update Drupal 7 core](https://drupalize.me/videos/updating-drupal-core?p=1181), and [Drupal 7 contributed modules](https://drupalize.me/videos/updating-drupal-contributed-modules?p=1181).

## Make a plan for upgrading your code

At a high level, a Drupal codebase consists of:

- Drupal core
- Contributed modules and themes
- Custom modules and themes

In order to migrate to the latest version of Drupal core you'll need versions of all compatible contributed and custom modules and themes. This can be tricky because not all modules have releases for the latest core version. Sometimes popular modules have been incorporated into Drupal core. It's common for new best practices to evolve; for example: Paragraphs instead of Field Collections, CKEditor instead of WYSIWYG, Layout Builder instead of Panels.

Are there features you built a long time ago that you no longer need? What modules can you safely ignore because they provide features you're no longer using?

What about any custom code? Can you replace that features that code provides with a contributed module now? And if not, you'll need to make a plan to upgrade it.

Our suggestion is to start a code inventory, create a list of all the modules you're dealing with, and start tracking the current status of each. This will help create a task list for whoever is working on the migration. It'll help you be able to define when you're done. Learn more in [Drupal-to-Drupal Migration Planning: Code Inventory](https://drupalize.me/tutorial/drupal-drupal-migration-planning-code-inventory).

## Is it time for a facelift?

This is a great opportunity to give your website a facelift. That might mean simply tweaking a few design elements that you've been meaning to address for a while, finally implementing a responsive layout system, or a complete refresh of the design. When you migrate from any system (including prior versions of Drupal) to the latest version of Drupal you're going to end up needing to create a new theme for your site. This is true even if you're building a site without a migration component. Themes are the one thing that is custom for almost every Drupal project.

Creating a new theme by adapting existing design components will almost always be more efficient, simply due to the fact that you've already got some of the CSS and JavaScript written, and you've already done the hard work to figure out where and when to implement certain styles. That said, if you're pondering a design refresh shortly, you might want to consider doing it now since you'll already be spending considerable resources creating your custom theme.

Want to learn more about creating a custom theme in Drupal? Check out [our amazing Drupal theming guide](https://drupalize.me/guide/theme-drupal-sites).

## What's this all going to cost me?

Whether you're moving from a previous version of Drupal, or another data source entirely, it's important to frame this migration as a rebuild and not simply an upgrade. Doing so paints a more accurate picture of the amount of time and money this is going to take.

A migration is much more than just moving data from one place to another. The source data needs to be cleaned and prepared, the new website where data will end up needs to be created, designs updated, the new site needs to have a theme developed, infrastructure will need updating, tests will need to be written, and more. When assessing the cost of a migration we like to treat it as two projects: (1) Create the new site, and (2) Automate the transfer of content from the old site into the new one.

A successful migration will require at least a subset of the following roles among you and/or your team:

- Someone who can do a content audit. A domain specialist who understands the idiosyncrasies of both your site's functionality and your content
- A strong understanding of Drupal site-building and best practices
- Drupal back-end developer
- Drupal front-end developer
- Systems Administrator / DevOps
- Designer
- Copywriter
- QA

Other things to remember:

- Drupal 8 (and continuing in Drupal 9 and 10) introduced major API changes to Drupal's system. Your site building, front- and back-end developers will need to be comfortable working with Drupal's current APIs (many of which were introduced in Drupal 8).
- Your infrastructure needs will likely change with the latest Drupal release
- Staff may need to be retrained how to use the site
- Any new Drupal site, even if you're "just upgrading", is first and foremost a new website and should be handled as such
- Upgrading from Drupal 8+ will be a much less arduous undertaking than Drupal 6 or 7 to the latest version of Drupal. See [Upgrade to Drupal 9](https://drupalize.me/tutorial/upgrade-drupal-9) and [Upgrade to Drupal 10](https://drupalize.me/tutorial/upgrade-drupal-10).

One thing to consider might be whether it's worth it to develop a custom migration path. If you've got a limited amount of data, the cost to develop a migration path may be higher than the cost to pay someone to copy/paste content between the old site and the new Drupal 9 or 10 one.

Image

![Cost to migrate graph](../assets/images/cost-to-migrate_1.png)

For Drupal-to-Drupal migrations I believe that this will be less of an issue as a large part of the work in developing migrations and field mappings is handled automatically. But, it's still worth considering.

## Caveats

The Drupal-to-Drupal migration system is still a work in progress. And as such, there are a few things that simply don't work yet. Before you get too far into your migration planning, take a few minutes to read through our running tally of common "gotchas" and the current status of various components in this [Common Issues with Migrations](https://drupalize.me/tutorial/common-issues-migrations) tutorial.

## Install the latest version of Drupal

During the migration planning phase you'll also want to begin building your destination Drupal site. Contrary to what you may have thought coming into this, preparing your destination Drupal site might be one of the easier tasks. That is, of course, if all your custom modules are already updated, and you've found suitable contributed modules for all your needs after following the steps above.

At this point you should plan to install the latest version of Drupal, and all the contributed modules you've identified that you'll need. The contributed modules need to be installed prior to performing a migration, or their data will not be migrated.

## Do not configure the destination Drupal site...yet

Note that at this point you don't need to create content types, or fields, prior to migrating data. This is all handled by the Migrate Drupal module during the migration process. You do however need the contributed modules you want to make use of to be present so that any migration templates they provide for Migrate Drupal are there.

My suggestion: Automate this as much as possible, as you're likely going to want to be able to return to a clean version of your destination Drupal site prior to any migrations being tested. You should use a [Composer based workflow](https://www.drupal.org/docs/develop/using-composer/using-composer-with-drupal) to include any contributed modules. And, if you do need to make configuration changes at the outset it's a good idea to make snapshots of the database often, so you can easily revert.

## Recap

Executing a successful Drupal-to-Drupal requires quite a bit of up-front planning. You can't just click the button and have it all work. You need to evaluate the contributed modules you're using their migration paths. Think about your content, consider migrating to new best practices, and more. Migrations are a lot of work, but they are also a great opportunity to do some much-needed Spring cleaning.

## Further your understanding

Rather than pose questions to help judge your understanding of this tutorial like we normally would, we'll let you use this time to start creating your own tracking spreadsheet and assessing the readiness of your Drupal 7 site. This tutorial itself has a lot of questions that you'll need to answer about your own site that really don't have a single right or wrong answer. If you get stuck, or have questions, reach out and let us know, and we'll help guide you in the right direction.

## Additional resources

- A list of [common issues with migrations](https://drupalize.me/tutorial/common-issues-migrations) to familiarize yourself with while planning your migration
- [Drupal.org documentation on preparing for a migration](https://www.drupal.org/node/2350603)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close
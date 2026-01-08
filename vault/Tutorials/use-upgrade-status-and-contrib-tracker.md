---
title: "Use Upgrade Status and Contrib Tracker"
url: "https://drupalize.me/tutorial/use-upgrade-status-and-contrib-tracker?p=3116"
guide: "[[learn-migrate-drupal]]"
---

# Use Upgrade Status and Contrib Tracker

## Content

When preparing to migrate from an older version of Drupal (Drupal 7 or previous) to the latest version of Drupal (Drupal 8 or later) you'll need to determine if the contributed modules you use are ready to go. The [Upgrade Status module](https://www.drupal.org/project/upgrade_status) can give you a list of all the modules installed on your site, and information about the availability of a latest Drupal version. It's not perfect, and will still require some manual research for some modules, but it is a great start towards helping you plan for your migration.

In this tutorial we'll:

- Install the Upgrade Status module and use it to generate a status report
- Review the generated report
- Talk about using the Contrib Tracker project, and other methods for getting more details about the status of upgrades for any module

By the end of this tutorial you should be able to evaluate all the installed modules on your existing Drupal site and determine the status of a module release that is compatible with the latest version of Drupal.

## Goal

Create a list of modules in use on a Drupal 7 site and the status of the latest Drupal version of the module.

## Prerequisites

- [Prepare for a Drupal-to-Drupal Migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration)
- [Drupal-to-Drupal Migration Planning: Code Inventory](https://drupalize.me/tutorial/drupal-drupal-migration-planning-code-inventory)

Sprout Video

## Install Upgrade Status module

### Download and install Upgrade Status module

Start by downloading the current stable version of the [Upgrade Status module](https://www.drupal.org/project/upgrade_status), and installing it on a development copy of your Drupal 7 site.

Or, use Drush to do it:

```
drush dl upgrade_status && drush en upgrade_status --yes
```

### Generate a report

In the *Manage* administrative menu, navigate to *Reports* > *Available updates* > *Upgrade status* (*admin/reports/updates/upgrade*).

On this page you're presented with a form where you can choose your target version of Drupal. This is the version that you'll be moving to, not the version you're currently using.

Once you've chosen a target version click the *Check manually* link to trigger the Upgrade Status module to generate a new report.

### Review the report

This report shows one of three statuses for each enabled module.

**Available**, indicating that the module has a stable latest-Drupal-version release. You can consider these ready to use. The next step would be to install the module and confirm it does what you need.

**In development**, indicating that there is at least a development release of the module for the latest version of Drupal available. These are a bit harder to assess, but it's also a good sign. This status indicates that work is ongoing to update the module, and in many cases the development version will likely work well enough that you can start testing your migration. The usual caveats apply here: you're using a development version of a module so it's likely less stable, subject to change, etc. But give it a try and see if it works. Keep notes about what you discover in your module tracking spreadsheet.

**No available update data**, indicates that the Upgrade Status module was not able to find a release, development or other, for a current Drupal version of the module. This means you're going to have to do some detective work on your own to figure out the status.

For each module, make a note in your module tracking spreadsheet about the current status, especially those that do not have a latest Drupal version, as those represent additional work you're going to need to perform in order for your migration to be successful.

## What do to if you need more information

If one or more of the modules you want to use are not listed as **available** by the Upgrade Status module you'll need to do a bit of digging on your own, and then make a decision about how to proceed.

I would start by deciding if this module is really required. If you don't need it, simply check it off your list and move on. Additionally, being aware of which modules have been integrated into the core software will help you to eliminate modules from your list. [This page](https://www.drupal.org/node/1283408) contains a list of the modules in versions 6, 7, and 8 of Drupal core.

For more information on the options available if a module isn't ready, see the "Assessing a module's readiness" section of our [prepare for a Drupal-to-Drupal migration tutorial](https://drupalize.me/tutorial/prepare-drupal-drupal-migration).

## Recap

In this tutorial we look at using the Upgrade Status module and Contrib Tracker project in order to assess whether the modules we're using on our Drupal 7 site are ready to be used in the latest version of Drupal. Or, if they're not, to know what the current status of development is.

## Further your understanding

- Use the information from the Upgrade Status report in conjunction with the [Hacked! module's report](https://drupalize.me/tutorial/check-alterations-hacked), in order to create a [spreadsheet tracking the state of each of your modules](https://drupalize.me/tutorial/prepare-drupal-drupal-migration) as part of your preparation for migrating to the latest version of Drupal.

## Additional resources

- [Upgrade Status module](https://www.drupal.org/project/upgrade_status) and [documentation](https://git.drupalcode.org/project/upgrade_status/-/tree/7.x-1.x)
- [Contrib Tracker project](https://www.drupal.org/project/contrib_tracker)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Drupal-to-Drupal Migration Planning: Code Inventory](/tutorial/drupal-drupal-migration-planning-code-inventory?p=3116)

Next
[Check for Alterations with Hacked](/tutorial/check-alterations-hacked?p=3116)

Clear History

Ask Drupalize.Me AI

close
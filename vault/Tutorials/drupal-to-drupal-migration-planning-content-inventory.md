---
title: "Drupal-to-Drupal Migration Planning: Content Inventory"
url: "https://drupalize.me/tutorial/drupal-drupal-migration-planning-content-inventory?p=3116"
guide: "[[learn-migrate-drupal]]"
---

# Drupal-to-Drupal Migration Planning: Content Inventory

## Content

If you want to be able to say you're done with your Drupal-to-Drupal migration, first you have to be able to define "done". And part of that is doing a content analysis and inventory. Performing a content analysis and inventory will help you ensure that you don't miss any fields or important records. It also gives you an opportunity to spend some time thinking about the overall information architecture of your site. You're already going to be doing a lot of work to migrate your content, so deciding to shuffle things a bit now might not add any significant extra time. Additionally, the latest Drupal (as of Drupal 10) is a different platform than either Drupal 6 or 7, and as such, there are some new best practices and new ways of doing things that might not have been available before.

In this tutorial we'll:

- Provide a set of questions you can ask yourself about the content of your current site to kick-start your analysis.
- Give an example of how we create a content type inventory in a spreadsheet and use that to help define "done" for our projects.

By the end of this tutorial you should be able to get started analyzing the content and content types of your existing site in order to start planning for your Drupal-to-Drupal migration.

## Goal

Make a list of your content types and their fields. Identify any changes you might want to make, and write out in plain language what that data transformation entails.

## Prerequisites

- [Prepare for a Drupal-to-Drupal Migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration)

## Evaluate your current site and make a plan

Ask yourself the following questions as a starting point:

- Which content types on your existing site are actually being used?
- Which content types can be removed?
- Same for things like vocabularies and other entities. Is there content that you could just get rid of instead of migrating?
- Have you been wanting to modify your content types? Perhaps change the name, add/remove fields, or maybe split that catch-all body field into some chunky semantic fields? This might be a good time to tackle these types of tasks as well. The transform phase of a migration is a great place to do this kind of data munging.
- Is this a good time to split a monolithic site into smaller sites? In our example migration we're doing just that: moving the Drupalize.Me blog to its own Drupal installation and upgrading it to the latest version of Drupal at the same time. This isolates it from the main functionality of our site, so it's easier to maintain, and allows us to move things over to the latest Drupal version in segments instead of all at once.
- Are there pieces of functionality on your site that may no longer be important? This is especially important to think about when it comes to custom modules that you're maintaining. If you're not using it, don't bother porting it.
- What about new features in Drupal (think Media module, or Layouts) that you want to be able to use. How will you migrate your Drupal 7 image fields to Drupal 10 media entities?

## Create a spreadsheet

Image

![Spreadsheet showing the fields of a Drupal content type and notes about how to migrate each field](/sites/default/files/styles/max_800w/public/tutorials/images/content-inventory-example.png?itok=4qG0G2Kr)

Create a spreadsheet that lists every content type, and every field for each content type. Add notes about how you intend to deal with that fields content. Are you going to rename it? Merge 2 fields together? Ignore a field completely? Your inventory helps tell you when you’re done, and without it, it's easy to forget to account for important data.

This is especially true when not all contributed modules, and therefore not all field types, have a working migration path. It's easy to miss them when you're using generators to scaffold a migration but the generator skipped a field because it didn't know what to do with it.

I'll generally enter into my spreadsheet every content type, and the fields on each. Then I denote if I intend to migrate the field. When doing a straight Drupal-to-Drupal migration you don't have to worry about creating the fields on the destination end. Migrate module will handle that for you. But if you're changing field names, or remapping things in other ways, you might want to consider creating the content types in your destination Drupal site ahead of time and writing a custom migration path for your data.

Image

![Line graph showing time it takes to manually migrate content relative to amount of content to migrate](/sites/default/files/styles/max_800w/public/tutorials/images/cost-to-migrate_1.png?itok=1I5mShky)

This is also another good time to think about the cost to migrate content. If there are only 5 FAQ nodes it might be easier to copy and paste the data into the new site than to write an automated migration.

Here's a helpful script you can use to create CSV file that lists all the entity types of your Drupal 7 site and their fields and the import it into a spreadsheet. <https://gist.github.com/eojthebrave/2970c474f7fa223d97d84decd609cd9b>

Download the script into the root of your Drupal 7 site, and name it *entity\_fields.php*. Then run it with `drush src entity_fields.php`.

[Here's an example](https://docs.google.com/spreadsheets/d/1Ey1bFb6MJiUHUW3YVVavJiwIxoR_B_Nb1czLGDntO-s/edit#gid=1056290640) of what this looks like after a bit of formatting.

## Recap

The planning phase of a migration is a great time to step back and think about the overall information architecture of your site. You're already going to be doing a lot of work to migrate your content, so deciding to shuffle things a bit now might not add any significant extra time. This will also give you a place to track the progress of migration project; help with quality assurance and acceptance testing; and ensure the project is complete.

## Further your understanding

- Are there any modules you have installed on Drupal 7 for which there's no migration path for Drupal 10? How does this change your content architecture?
- How could you make the content analysis more efficient if you have a lot of sites to migrate?

## Additional resources

- [Drupal-to-Drupal Migration Planning: Code Inventory](https://drupalize.me/tutorial/drupal-drupal-migration-planning-code-inventory) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Check for Alterations with Hacked](/tutorial/check-alterations-hacked?p=3116)

Next
[Common Issues with Migrations](/tutorial/common-issues-migrations?p=3116)

Clear History

Ask Drupalize.Me AI

close
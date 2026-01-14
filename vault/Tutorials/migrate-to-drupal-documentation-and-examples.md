---
title: "Migrate to Drupal: Documentation and Examples"
url: "https://drupalize.me/tutorial/migrate-drupal-documentation-and-examples?p=3117"
guide: "[[learn-migrate-drupal]]"
order: 3
---

# Migrate to Drupal: Documentation and Examples

## Content

Every migration is unique, which means there are loads of great examples you can review and learn from. We'll keep this tutorial up-to-date with our favorites and let you know how we think these examples might help.

## Goal

Learn about useful documentation and examples of working with migrations to the latest version of Drupal.

## Prerequisites

- [Migrate System Terms and Concepts](https://drupalize.me/tutorial/migrate-system-terms-and-concepts)

## Migrate Documentation

The canonical documentation for the Migrate API is on Drupal.org; however, given the rapid pace of iteration on the still-experimental Migrate API, the documentation can be misleading. We recommend you read it, but that when doing so you check the last updated date. Remember that there may be changes to the API that haven't made it to the docs yet.

The [Migrate API overview](https://www.drupal.org/node/2127611) section of the community documentation covers how the system as a whole works as well as tips about writing and running migrations.

The [Migrate API](https://api.drupal.org/api/drupal/core%21modules%21migrate%21migrate.api.php/group/migration/) topic on <api.drupal.org> is a good starting point for understanding more about how the underlying system works. It's especially useful if you're going to be writing source, process, or destination plugins. Additionally, if you want to collaborate on improving the core API or documentation, this is a good place to start familiarizing yourself with the API.

## Migrate Plus

The [Migrate Plus project](https://www.drupal.org/project/migrate_plus) contains two sub-projects, *migrate\_example*, and *migrate\_example\_advanced*. Both of which are a gold mine, and in our opinion the best place to roll up your sleeves and dive in. Both contain copiously documented YAML and PHP files with inline comments.

Each example also comes with sample data, so you can actually run the example migrations and see how they work. For best results, try tweaking the code, running the examples again and seeing what changes. For more information on running migrations see our tutorial, [Run Custom Migrations](https://drupalize.me/tutorial/run-custom-migrations).

### Migrate examples

Start with the *migrate\_example* project. Enable both this module, and the contained *migrate\_example\_setup*. The latter contains sample data and configuration that will set up some new content types, vocabularies, and other things on your site. As such, we highly recommend you do this in a sandbox site.

To best understand the concepts described in a more-or-less narrative form, it is recommended you read the files in the following order:

1. *README.txt*
2. *config/install/migrate\_plus.migration\_group.beer.yml*
3. *config/install/migrate\_plus.migration.beer\_term.yml*
4. *src/Plugin/migrate/source/BeerTerm.php*
5. *config/install/migrate\_plus.migration.beer\_user.yml*
6. *src/Plugin/migrate/source/BeerUser.php*
7. *config/install/migrate\_plus.migration.beer\_node.yml*
8. *src/Plugin/migrate/source/BeerNode.php*
9. *migrations/beer\_comment.yml*
10. *src/Plugin/migrate/source/BeerComment.php*

### Migrate examples advanced

Want to import content from something other than a SQL data source?

The *migrate\_examples\_advanced* project contains additional, equally well-commented, examples. Unlike the narrative format of the *migrate\_examples* examples, the ones in this module are more of a grab bag of various tricks and techniques. So what's here?

The Migrate Plus module contains an awesome *URL source plugin*, capable of reading JSON, XML, or SOAP data from any URL. Start with *config/install/migrate\_plus.migration.wine\_variety\_multi\_xml.yml*, which has the best information about the URL source plugin. There are examples of using each supported format:

- SOAP example - *config/install/migrate\_plus.migration.weather\_soap.yml*
- JSON example - *config/install/migrate\_plus.migration.wine\_role\_json.yml*
- XML example - *config/install/migrate\_plus.migration.wine\_role\_xml.yml*

Read more about the URL source plugin in [this blog post](http://virtuoso-performance.com/blog/mikeryan/drupal-8-plugins-xml-and-json-migrations) by the module's author Mike Ryan.

## In the wild

Other examples of migrations we've come across and learned from:

- This example demonstrates using the [Migrate Source CSV](https://www.drupal.org/project/migrate_source_csv) module to import from a CSV data source.
- [heddn/d8\_custom\_migrate](https://github.com/heddn/d8_custom_migrate)

Got some examples you think we should showcase? [Let us know](https://drupalize.me/support).

## Recap

In this tutorial we pointed out some of our favorite non-Drupalize.Me resources for learning how migrations in Drupal work. Looking at how others have done it is one of the best ways to learn.

## Further your understanding

- Consider subscribing to the [Planet Drupal RSS feed](https://www.drupal.org/planet) or [The Weekly Drop](http://www.theweeklydrop.com/). A lot of folks in the Drupal community blog about their migration experiences and their posts can often be found in these places.

## Additional resources

- [Migrate API overview](https://www.drupal.org/node/2127611) (Drupal.org)
- [Migrate API](https://api.drupal.org/api/drupal/core%21modules%21migrate%21migrate.api.php/group/migration/) (api.drupal.org)
- [Migrate Plus module](https://www.drupal.org/project/migrate_plus) (Drupal.org)
- [Migrate Source CSV](https://www.drupal.org/project/migrate_source_csv) (Drupal.org)
- [heddn/d8\_custom\_migrate](https://github.com/heddn/d8_custom_migrate) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Migrate System: Terms and Concepts](/tutorial/migrate-system-terms-and-concepts?p=3117)

Next
[Core Migration Modules](/tutorial/core-migration-modules?p=3117)

Clear History

Ask Drupalize.Me AI

close
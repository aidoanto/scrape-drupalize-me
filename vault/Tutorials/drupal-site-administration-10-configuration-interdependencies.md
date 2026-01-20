---
title: "Configuration Interdependencies"
url: "https://drupalize.me/tutorial/configuration-interdependencies?p=2478"
guide: "[[drupal-site-administration]]"
order: 10
---

# Configuration Interdependencies

## Content

Drupal creates a line of separation between what is content and what is configuration. The line is such that content is stored only in the database, whereas configuration is maintained by the configuration management system. While cached to the database for performance reasons, configuration can be thought of primarily living in the sync directory as a series of flat files.

This sounds like a perfectly clear distinction in theory, but there are several times where interdependencies appear between content and configuration. Understanding the key places where these interface can help prevent confusion and "disappearing" settings due to a lack of understanding.

## Goal

To understand key cases where configuration interdependencies occur, and how to account for them in your configuration management workflow.

## Prerequisites

- [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush)
- [Drush Site Aliases](https://drupalize.me/tutorial/drush-site-aliases)
- [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management)

## Which came first? The config or the content?

In earlier versions of Drupal, the database was considered the canonical source for all content *and* configuration. If a change was made on the live environment, one would need to create a database dump and import it locally for the same configuration to appear. The [Features module in Drupal 7](https://drupalize.me/videos/introduction-drupal-features-module), used in conjunction with a module such as [Strongarm](https://drupalize.me/videos/exporting-settings-variables-strongarm), allowed some of that configuration to be persisted to generated modules, so that some management of settings could be performed without an exhaustive database comparison.

Drupal separates content and configuration into two separate systems. While content continues to live in the database, configuration is only cached to the database. Copying database dumps back and forth still works in Drupal, but it isn't the recommended workflow.

Instead, it is highly recommended that you export configurations to the file system, and place the [configuration sync directory](https://drupalize.me/tutorial/configuration-sync-directory-setup) under version control. This allows configurations to be managed "as code" as it did with the Features module. It also introduces a new "chicken and the egg" problem, did the content come first, or the config?

## Content depending on config

The majority of content in a Drupal site depends on some sort of configuration. While nodes are content, content (node) types are configuration. This is why we can deploy new content types by only changing the configuration. The same is true for terms and vocabularies, blocks and block types, and menu items and menus.

| Content | Configuration |
| --- | --- |
| Nodes | Content types |
| Terms | Vocabularies |
| Blocks | Block types |
| Menu items | Menus |

In this case, the workflow is straightforward: Import configurations first, and then create content that relies on those configurations. Drupal already does this naturally, since you cannot create a node without first having a content type. When developing new content types, for example, is natural to first create the types on your local environment. When finished, those configurations are deployed to the production site. That deployment can be a fully manual process (uploading the config sync directory and doing a `drush cim`), git deploy followed by a `drush cim`, or a automated process using Continuous Integration.

## Configuration depending on content

The reverse case is also present in Drupal. Configurations may depend on a preexisting piece of content. While this doesn't happen as often compared to content depending on configuration, it does happen in several key places.

Block placement is stored as configuration, but blocks themselves are content. Custom blocks in particular are content and only stored in the database. When these blocks are placed, it affects the site configuration as the theme region configuration stores the presence and weight of the block placement.

Let's imagine creating a custom block on our local environment. We use the block layout UI (Admin > Structure > Blocks) to place the block on our site. When we do a `drush cex`, we see there are configuration changes related to the block placement. If we were to deploy that configuration to the production server, the block would not appear as expected.

A similar case happens with Views. A view can be created that it depends on an existing piece of content. A common case is the view is filtering its display using a taxonomy term. The term itself is content. If we were to push the view to production without creating the term first, the view would be broken.

## Resolving interdependencies

Typically, one does not need to do anything special for content that depends on configuration. Simply deploy the configuration first, then create content. For configurations that depend on content, however, the situation is more complex.

For custom blocks, the block placement system relies on the custom block's *universally unique identifier* (UUID) to know which block is the correct one to place. These UUIDs are generated when content is created. Even if you create the same block at the same time, on two separate copies of the same site, the UUID would be different. When the configuration is pushed from one of these sites to the other, the custom block would "disappear" as the UUIDs are not the same.

This makes it difficult to deploy these configurations as we would new content types, vocabularies, or menus. The solution, however, is to bend a best practice rule, as follows:

### Create the custom block, term, etc. on the live site

Create whatever content is necessary on the production site.

Create a database dump of the live site, and import it into your local environment.

On your local, create the block placement or whatever configuration you need.

Export your local configuration using `drush cex`.

**Immediately** commit the configuration changes to your repository, and push.

Creating the content on the production server does bend best practice in this situation, but it is the only way to ensure the UUID of the block remains constant the live and local environments. Furthermore, the push of configuration changes must be done in a timely manner to ensure both the content in the database and the configuration in the git repository are updated in lockstep.

## Speeding things up with `sql-sync`

Performing a database dump and import can be a time-expensive operation involving several tools (SSH, SFTP, Drush). Fortunately, Drush provides the `sql-sync` subcommand to perform all these operations for us.

Like `drush config-pull`, the `sql-sync` subcommand relies on Drush aliases and SSH keys. See the [Live vs. Local Configuration Management](https://drupalize.me/tutorial/live-vs-local-configuration-management) tutorial on how to set those up.

Once set up, calling the command is simple:

```
drush sql-sync @source_site_alias @target_site_alias
```

Where:

- **source\_site\_alias** is the site alias of the remote site from which we're exporting the database.
- **target\_site\_alias** is the alias of the site into which we're importing the database.

Again, you can use the `self` built-in alias to refer to your local site:

```
$ cd /path/to/your/local/site
$ drush sql-sync @live @self
```

See [Drush Site Aliases](https://drupalize.me/tutorial/drush-site-aliases) for more details.

Note that the database export can be a disk expensive operation. This can cause a performance drop on a large or high-traffic site.

## Recap

The configuration system in Drupal allows us to persist configurations as code. It also introduces a new wrinkle when configurations and content are dependent upon each other. When configuration depends on content, it's best to create the content first on the production server, and then create configurations locally. This ensures the UUID remains consistent throughout the process. Use of the `drush sql-sync` command can help by simplifying the process of obtaining a database dump.

## Further your understanding

- When would you combine `drush cpull` and `drush sql-sync`?

## Additional resources

- [`drush sql-sync` reference on Drush Docs](https://drushcommands.com/drush-8x/sql/sql-sync/)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Live vs. Local Configuration Management](/tutorial/live-vs-local-configuration-management?p=2478)

Next
[How to Override Configuration](/tutorial/how-override-configuration?p=2478)

Clear History

Ask Drupalize.Me AI

close
---
title: "Multiple Search API Indexes"
url: "https://drupalize.me/tutorial/multiple-search-api-indexes?p=2815"
guide: "[[drupal-site-administration]]"
order: 25
---

# Multiple Search API Indexes

## Content

Drupal has the ability to support multiple Search API indexes within a single installation. While adding a new index is easy, we must understand the implications of creating and using multiple Search API indexes.

In this tutorial, we'll:

- Identify when to create multiple indexes in Search API
- Define virtual indexes, and their performance implications

## Goal

To understand the various circumstances in which you would want to create multiple indexes in a Search API Solr setup.

## Prerequisites

- [Create Search API Indexes](https://drupalize.me/tutorial/create-search-api-indexes)

## Why use multiple indexes?

Creating an additional Search API index is straightforward. Login to your Drupal site with appropriate privileges, using hte *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*, and click **Add index**. Once configured, the index is available to add fields and use in views.

The real question is "Why?" Why would you want or need multiple Search API indexes on a Drupal site? Typically, a Drupal site will have at least one Solr-powered index used for global content search. This Search API index will crawl all content types, and be used for most search functions.

There are some circumstances where you may want to create additional Search API indexes, outlined below.

### Creating separate search domains

A common reason to create multiple Search API indexes is to create separate search "domains", often with non-overlapping content.

For example, a company website may have a global search function and a separate search facility for their product knowledge base. The global search crawls landing pages, press releases, and blog posts, while the knowledge base search crawls product quick starts, manuals, notices, and other support pages. While combining the two domains of searches may be effective, it can be overwhelming and render the site's search function "useless" from an end-user perspective.

### Preserving performance

Another reason to use multiple Search API indexes is to distribute different search domains on different Solr servers.

For example, an animal adoption agency may have a great deal of information to index just regarding the animals available, such as breed, age, temperament, color, and so on. The volume of information on the Solr core may simply be too much to share on the same hardware as a core that indexes other site content. Placing each core on different hardware preserves performance.

### Differing schemas or versions

Less often, an existing Drupal site may support multiple Solr cores for legacy reasons. An older search implementation may have required a custom Solr schema, making it incompatible with a newer implementation. This can extend to the server level as well, with different Solr servers of different versions being leveraged by the same site.

While Search API can support this configuration, it is often considered an interstitial phase of migrating off old Solr hardware.

## Virtual indexes and Solr

Search API is capable of creating multiple Search API indexes that support the same backend. When Apache Solr is used as the backend, however, this has additional technical implications.

In Search API Solr, each Search API server corresponds to a single Solr core. In order to support multiple Search API indexes on the same core, Search API relies on creating a *virtual index* within the core. To the site builder, a virtual index works the same way as a regular Search API index. Each may have different field configurations and must be used by different sets of views.

This is an easy configuration to create, but it causes numerous, hard-to-troubleshoot issues with Solr. All the fields from every Search API index sharing the same core are combined into a single index. This enlarges the index and slows obtaining search results. Furthermore, commonly used features like autocomplete and spellcheck may fail to function correctly.

Instead, it is best practice to create a completely separate Solr core for each Search API index. This preserves performance and ensures each index is isolated from every other index.

## Migrating cores from virtual indexes

If your site does rely on multiple Search API indexes sharing the same Solr core, it is best to migrate away from the combined core into multiple discrete cores:

1. Create the new cores on the Solr server, each with the correct schema.
2. Add a new Search API index for each core, adding fields and other configurations as necessary.
3. Re-implement the corresponding views, using the new Search API indexes.
4. Remove the old Search API index, and delete the corresponding Solr core.

## Recap

Search API can support multiple Solr cores and multiple Solr servers easily. Simply create another Search API index or Search API server as needed.

## Further your understanding

- If you clear a virtual index, does it also clear any other index on that Solr core?

## Additional resources

- [Search API project](https://www.drupal.org/project/search_api) (Drupal.org)
- [Adding an index](https://www.drupal.org/docs/8/modules/search-api/getting-started/adding-an-index) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create Search Pages and Blocks with Views](/tutorial/create-search-pages-and-blocks-views?p=2815)

Next
[Processors in Search](/tutorial/processors-search?p=2815)

Clear History

Ask Drupalize.Me AI

close
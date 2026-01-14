---
title: "Create Search API Indexes"
url: "https://drupalize.me/tutorial/create-search-api-indexes?p=2815"
guide: "[[drupal-site-administration]]"
order: 21
---

# Create Search API Indexes

## Content

While Solr compartmentalizes settings into cores, Search API organizes things into *indexes*. Each Search API index can have a unique set of settings and crawl a specified list of content types. Search API indexes can be created in the Search API admin interface.

In this tutorial, we'll:

- Identify a Search API index
- Describe how an index is related to a Solr core

By the end of this tutorial you should be able to create a new Search API Index connected to a Solr backend.

## Goal

Create a Search API index for Solr, and perform initial configuration of the index.

## Prerequisites

- [Install Search API](https://drupalize.me/tutorial/install-search-api)
- [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush)

## Cores, search indexes, and Search API indexes

Solr cores encapsulate a large number of server configurations, as well as the search index generated from submitted data. If you ever need to re-implement the search server elsewhere, you only need to create a core with the same configuration and submit the same data for indexing.

The Search API module requires a number of configurations as well. As Drupal is so versatile, we need to tell Search API about our content types and fields on those types, and how to process each of those fields in order to submit them to Solr.

In Search API, these configurations are encapsulated into a configuration object called an *index*. Do not confuse a Search API index with the generic concept of a search index; the former contains configuration information, while the latter contains search data against which to run searches. To keep the two separate in this series, we'll always refer to the configuration object as a "Search API index".

## Create a Search API index

Creating a new Search API index can be accomplished in the Drupal web UI.

### Create sample content to be indexed

If you don't already have content on your site, you may want to create some sample content to search against. You have a couple of options to do this:

- Create the content manually
- Use the Devel Generate submodule of the [Devel project](https://www.drupal.org/project/devel) to create content.

Creating the content manually is best when you have specific search goals and require true-to-life content to test against. For our purposes, we can use the remaining, automated methods.

To use Devel Generate:

#### Install the Devel module using Composer:

```
composer require drupal/devel
```

#### Enable *devel* and *devel\_generate* modules using Drush:

```
drush en -y devel devel_generate
```

#### Generate some users, terms, and content (in that order).

##### With Drush

```
drush devel-generate:users
drush devel-generate:terms --bundles=tags
drush devel-generate:content
```

##### Via the UI

1. Login to the Drupal web UI with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Devel generate*.
3. Use the provided forms to generate user, then terms, and then content.

### Creating the basic Search API index

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Click **Add Index**.
4. Enter an **Index Name** of your choosing. This tutorial uses `Global content`.
5. For **Datasources**, select **Content**.
6. Scroll down and select the **Server** you created earlier.
7. Press **Save**.

### Export the configuration

1. Use the Drush command to export the configuration:

   ```
   drush cex -y
   ```
2. Add and commit the new site configurations to the repository.

## Recap

Creating a Search API index creates the necessary configuration on the Drupal site to know what content types, languages, and other data could be sent to the Solr server for indexing. You can create a Search API index using the Drupal UI.

## Further your understanding

- What do the other **data source** types do?
- Can one Search API index support multiple Solr servers?

## Additional resources

- [Drush commands for Devel and Devel Generate](https://www.drupal.org/docs/contributed-modules/devel/drush-commands) (Drupal.org)
- [Search API](https://www.drupal.org/project/search_api) (Drupal.org)
- [Adding an index](https://www.drupal.org/docs/8/modules/search-api/getting-started/adding-an-index) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Solr and Multiple Environments](/tutorial/solr-and-multiple-environments?p=2815)

Next
[Populate Search API Indexes](/tutorial/populate-search-api-indexes?p=2815)

Clear History

Ask Drupalize.Me AI

close
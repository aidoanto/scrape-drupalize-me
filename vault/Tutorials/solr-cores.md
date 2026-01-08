---
title: "Solr Cores"
url: "https://drupalize.me/tutorial/solr-cores?p=2815"
guide: "[[drupal-site-administration]]"
---

# Solr Cores

## Content

Solr compartmentalizes itself into cores (or collections if you're using SolrCloud). Each Solr core has its own directory, configuration, and set of search data. While a core can be thought of as an “index”, it is much more.

In this tutorial, we'll:

- Identify the difference between a *Solr core* and an *index*.
- List the various ways a core can be created.
- Explain why Search API needs a custom core configuration.

By the end of this tutorial you should be able to explain what Solr cores are, and how to create a Solr core (or collection) that is compatible with Drupal's Search API module.

## Goal

To understand how Solr uses cores (collections) to compartmentalize configuration and search data.

## Prerequisites

- [Why Solr?](https://drupalize.me/tutorial/why-solr)

## What is a search index?

When you open a large reference book, it can be a bit daunting to find exactly what you need without a lot of tedious page-flipping. Even if you read through the table of contents, you may not find what you are looking for. For this reason, many reference books also offer an *index* at the back. The index is alphabetically organized by topic or keyword. This allows you to find just the page you're looking for quickly and easily.

You can think of a website like a reference book as well; it's a collection of inter-linked pages. Like paging through the chapter list, going through each link in the site's menu may not land you on the page you're looking for. Like the physical book, what we need is an index so we can quickly find our desired page by entering into the search box a handful of keywords.

The goal of search systems like Solr is to create that index automatically. Instead of a human editor going through each page, Solr analyses each page and creates the index. Unlike a physical book, a search index is often more complex than an alphabetic list of key terms and pages. Instead of reading the index directly, you enter your desired terms into the search engine, and the engine examines the index to produce results.

## Schemas

Early search engines often treated all incoming data the same, processed it the same, and stored it the same. This often resulted in less than stellar results when searching the site. Your site is unique, and understandably, you should have your search system customized to suit your application.

Solr is a modern, flexible search system. Solr provides the ability to configure how incoming data is processed and what from that data gets stored in the index. This information is called a *schema*.

Schemas can be very simple or complex, depending on your data and how you intend to leverage the index.

## Solr cores

The index, schema, and other configuration combine into one fundamental unit within Solr -- a Solr *core*. Like a database, each core is a collection of files:

- *core.properties* defines global information about the core itself -- most importantly, the core's name
- *schema.xml* defines the search index schema
- *solrconfig.xml* provides configuration for the core
- The *data* directory houses the index
- Other files depending on need, version, and configuration

The above are typically stored in a subdirectory of `$SOLR_HOME`, named for the core. While `$SOLR_HOME` can be anywhere on the system, the default is */opt/solr/server/solr*:

```
/opt/solr/server/solr/my_core_name
├── core.properties
├── conf/
│   ├── schema.xml
│   └── solrconfig.xml
└── data/
```

The above isn't a complete list of all the files in a Solr core. Many core configurations also reference additional files which are also stored within the core's directory.

## Creating a Solr core

Prior to Solr 6.x, cores needed to be created manually by implementing the necessary files and directories. Solr would then attempt to read the core configurations on start up and allocate the necessary runtime resources to support the core.

Recent versions of Solr now provide a `solr` administration command. This command allows you to create cores by specifying the name:

```
/opt/solr/bin/solr create -c my_core_name
```

This creates all the necessary directories and files, and instructs Solr to create the necessary runtime resources.

The Solr web administration interface provides yet another way to create a Solr core. This method, however, is rarely used. The web UI does not require a login, and as such, is often either heavily restricted at the network level or completely disabled. Furthermore, server-side directories need to be created ahead of time to house the core.

## Search API and Solr

The [Search API module](https://www.drupal.org/project/search_api) provides various enhancements to the search functionality of any Drupal-powered website. One key advantage is that it allows different backends to power search.

The [Search API Solr module](https://www.drupal.org/project/search_api_solr) provides a Solr backend for Search API. It functions as the bridge allowing Drupal data to be easily indexed by Solr in a flexible and effective manner. To support this, Search API Solr provides a custom Solr schema within the module:

```
search_api_solr
├── search_api_solr.info.yml
├── search_api_solr.module
...
└── solr-conf/
    ├── 4.x/
    ├── 5.x/
    └── 6.x/
        ...    
        ├── schema.xml
        └── solrconfig.xml
```

Since different versions of Solr have different capabilities, Search API Solr provides multiple schemas by Solr version.

**Important note:** You **must** use the configuration **provided by the Search API Solr module** when creating your Solr core. Failure to do so can lead to bugs that may not be obvious and are hard to track down.

## Creating a Search API Solr compatible core

Now that we have all the key concepts behind us, creating a new Search API compatible core is fairly straightforward. The gist of it is:

1. Start the Solr server as usual.
2. As the same user under which the Solr server runs, create a directory for your core under `$SOLR_HOME`.
3. Create a *conf/* subdirectory within your core directory.
4. [Install Search API Solr, and configure it to connect to your Solr server](https://drupalize.me/tutorial/install-search-api).
5. Obtain the configuration files from Drupal.
6. Copy them to the core's *conf/* directory you created above.
7. Use `solr create -c your_core_name` to create and load the core.

Depending on your setup you may be able to create the Solr core via the Drupal UI and not have to manually copy the configuration files. In some cases, like when using a hosted Solr solution like on Pantheon or Acquia, you may need to install a host-specific module that will facilitate uploading your configuration for the Solr core.

## Creating a core with the DDEV example

[Earlier in this course](https://drupalize.me/tutorial/use-solr-locally), we provided you with an example showing how to use DDEV as a local development environment which supported Solr. Follow these steps to create a Solr core/collection for use in this environment.

### Install Search API and Search API Solr

If you haven't already [Install Search API Solr, and configure it to connect to your Solr server](https://drupalize.me/tutorial/install-search-api).

### Install Search API Solr Admin module

Install the *Search API Solr Admin* module that comes with Search API Solr. It provides integration with the SolrCloud API that allows a new core to be created (or an existing one updated) via the API. In the *Manage* administration menu navigate to *Extend* (*admin/extend*), choose the *Search API Solr Admin* module from the list, then scroll to the bottom and press the *Install* button.

### Upload the configuration to Solr

In the *Manage* administration menu navigate to *Configuration* > *Search and metadata* > *Search API* (*admin/config/search/search-api*), then select your Solr server from the list. On the next page press the *Upload Configset* button.

### Configure the SolrCloud shards

On the next page you can set the number of shards (`1` for local development). Then press the *Upload* button.

This will send your Drupal-specific Solr configuration to Solr and create the new Solr core/collection for you.

### Confirm the collection was created

In the Solr admin UI at *<http://<projectname>.ddev.site:8983>* (use `ddev describe` to find your Solr admin UI address). You should now see a new collection based on the Search API configuration from Drupal.

Example:

Image

![Screenshot of the Solr web UI showing the drupal collection](/sites/default/files/styles/max_800w/public/tutorials/images/solr-admin-ui-collection.png?itok=r-ny8P7C)

## Recap

Solr is a modern, flexible search system. Different indexes and configurations are organized into different "cores", one core per index. The Search API Solr module provides a flexible and effective Solr schema for Drupal sites. This schema must be deployed to a Solr server manually before being used to create a new core.

## Further your understanding

- What would happen if you used a different schema with Search API Solr?
- How can you set up a non-localhost server with the appropriate Solr core configuration?

## Additional resources

- [Solr docs](https://solr.apache.org/guide/solr/latest/index.html) (solr.apache.org)
- [Search API project page](https://www.drupal.org/project/search_api) (Drupal.org)
- [Search API Solr on Drupal.org](https://www.drupal.org/project/search_api_solr) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Solr Locally](/tutorial/use-solr-locally?p=2815)

Next
[Install Search API](/tutorial/install-search-api?p=2815)

Clear History

Ask Drupalize.Me AI

close
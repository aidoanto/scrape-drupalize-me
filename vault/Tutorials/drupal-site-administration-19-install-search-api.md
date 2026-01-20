---
title: "Install Search API"
url: "https://drupalize.me/tutorial/install-search-api?p=2815"
guide: "[[drupal-site-administration]]"
order: 19
---

# Install Search API

## Content

In order for Drupal to work with Apache Solr, we need to add the Search API module. This module provides a generic interface for search backends, including Solr. Furthermore, it adds several features to search without the need for custom code.

In this tutorial, we'll:

- Describe why Search API is necessary to use Solr with Drupal
- Identify a Search API server

By the end of this tutorial you should be able to install the Search API and Search API Solr modules, and create the Search API server configuration required to connect Drupal and Solr.

## Goal

Install the required modules to use Apache Solr with Drupal.

## Prerequisites

- [What Is Composer?](https://drupalize.me/tutorial/what-composer)
- [Use Composer with Your Drupal Project](https://drupalize.me/tutorial/use-composer-your-drupal-project)
- [Run Sets of Containers](https://drupalize.me/tutorial/run-sets-containers)
- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup)
- [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush)

## Installation and initial configuration

[Search API](https://www.drupal.org/project/search_api) provides a generic search mechanism for Drupal sites with several enhancements, including the ability to use a pluggable **backend** to provide the search functionality. The [Search API Solr module](https://www.drupal.org/project/search_api_solr) provides a Search API compatible backend powered by Apache Solr.

To encapsulate the connection information to the Solr server, Search API allows you to create one or more **servers**. This doesn't create the physical or virtual hardware, of course, but only contains the necessary configuration information. This can be created using the Drupal web UI.

There are 2 parts to connecting Search API to Solr:

1. Configuring Drupal with the information required to connect to Solr
2. Configuring Solr with a Drupal Search API compatible core that Drupal can use

Because the configuration for the Solr core depends on your version of Drupal, the version of the Search API Solr module, and your version of Solr, it is easiest to install the modules in Drupal first, and then use the Solr configuration files they provide to create the compatible Solr core.

The exact values for configuring the Solr server will depend on your environment. We'll use values appropriate for the DDEV setup we created in [Use Solr Locally](https://drupalize.me/tutorial/use-solr-locally).

### Install Search API and Search API Solr using Composer

Use [Composer](https://drupalize.me/tutorial/what-composer) to install the latest, stable version of the modules:

```
composer require drupal/search_api drupal/search_api_solr
```

Validate that the *search\_api* and *search\_api\_solr* directories appear in */path/to/my\_project/docroot/modules/contrib*.

### Enable the modules

You can choose to enable the modules using the web UI or via [Drush](https://drupalize.me/topic/drush).

To install using the web UI:

1. Login to your Drupal site using administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Extend*.
3. Select the *Search API* and *Search API Solr* modules from the list.
4. Press *Save Configuration*.

To install using Drush:

1. Using the command line, navigate to your project's Drupal directory.
2. Use the `drush` command to enable the modules:

   ```
   drush en search_api search_api_solr
   ```
3. Follow any on-screen prompts to enable the modules.

### Configure Search API to connect to the Solr server

Now that the modules are installed, we can configure Drupal to connect to the Solr server.

1. If you are using the example *docker-compose.yml* provided earlier in this class, be sure to start the containers:

   ```
   cd /path/to/my_project
   docker-compose up -d
   ```
2. Login to your Drupal site using administrator privileges.
3. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
4. Click *Add server*.
5. Enter a *Server name* of your choosing. This will be the admin name of the server configuration within the site. This tutorial uses `my_searchapi_solr`.
6. For *Backend* select *Solr*. This backend will allow us to index Drupal content.
7. A fieldset will appear. Select the *Solr connector* as *Solr Cloud with Basic Auth*, or *Standard*, depending on how you have Solr installed.
8. Enter the *Solr host*. This is the URL at which the Solr server is accessible. If using DDEV, this will be the service name of the Solr container, `solr`. If you're not using DDEV try the `status` command like `bin/solr status` to get the Solr host name.
9. For *Default Solr collection* (or *Solr core* if using the *Standard* connector), enter the name of the Solr core/collection. Note that if you already created the Solr core you'll use the existing name. If you haven't yet created the Solr core whatever you enter here will be used as the name when the Search API Solr Admin module creates it.
10. For SolrCloud enter the *HTTP Basic Authentication* username/password `solr / SolrRocks`.
11. Configure remaining fields as necessary, then press *Save*.

Image

![Screenshot of completed Solr server configuration form](../assets/images/solr-server-add-solrcloud.png)

### Validate Search API server creation

Immediately after creating the Search API server configuration, you are taken to the server's status page. To validate the Solr server was contacted and the core properly configured, you should see the following message:

```
The Solr server could be reached.
```

Example:

Image

![Screenshot of Solr server status dashboard](../assets/images/solr-server-status-dashboard.png)

### Export the configuration

The last step is to export the Search API configuration we just created to the file system.

1. Follow the steps in [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup) to ensure the configuration export directory is properly configured.
2. Use Drush to export the configuration:

   ```
   drush cex
   ```
3. Add and commit the exported configuration to your site's Git repository.

### Configure your Solr core

After configuring the Search API server you'll also need to verify the configuration of your Solr core. See [Solr Cores](https://drupalize.me/tutorial/solr-cores).

## Recap

Search API Solr is a backend provider for the Search API module. It allows Search API to integrate with Solr and use it as a search engine. Download the modules using Composer and enable them using Drush. Once installed, you can login to your Drupal site and configure a Search API server to instruct Search API on how to reach your Solr machine.

## Further your understanding

- How would we add multiple Solr servers?
- How could we change the Search API configuration to be different in stage compared to production?

## Additional resources

- [Search API project](https://www.drupal.org/project/search_api) (Drupal.org)
- [Search API Solr project](https://www.drupal.org/project/search_api_solr) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Solr Cores](/tutorial/solr-cores?p=2815)

Next
[Solr and Multiple Environments](/tutorial/solr-and-multiple-environments?p=2815)

Clear History

Ask Drupalize.Me AI

close
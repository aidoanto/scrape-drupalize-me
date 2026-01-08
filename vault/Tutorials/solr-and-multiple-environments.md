---
title: "Solr and Multiple Environments"
url: "https://drupalize.me/tutorial/solr-and-multiple-environments?p=2815"
guide: "[[drupal-site-administration]]"
---

# Solr and Multiple Environments

## Content

When developing a Drupal site, it is best practice to maintain multiple environments: A production environment for your live site, a stage environment for “next version” development, and your local environment for debugging and creating new features. Solr adds further complexity as we should have a separate Solr server for each.

In this tutorial, we'll:

- Describe why different Solr servers should be used for each environment
- Explain why [Config Split](https://www.drupal.org/project/config_split) is not a solution for multiple environments
- Describe how to use config overrides for each environment

By the end of this tutorial you should be able to override your Search API server configuration with environment-specific settings.

## Goal

To understand the complexities of implementing Solr search in a best-practice workflow environment.

## Prerequisites

- [Best Practice Drupal Development](https://drupalize.me/tutorial/best-practice-drupal-development)
- [Install Search API](https://drupalize.me/tutorial/install-search-api)
- [Synchronize Configuration with Drush](https://drupalize.me/tutorial/synchronize-configuration-drush)
- [How to Override Configuration](https://drupalize.me/tutorial/how-override-configuration)

## Why separate Solr installations

When developing a Solr-powered Drupal website, it is essential to have a different Solr installation for each environment. Typically, there are at least 3 environments in the best practice workflow:

- **production**, "prod", or "live", is the canonical instance of your site. It's the one associated with your main domain name, and the one users visit.
- **stage**, sometimes called "dev", or "pre-prod", is a shared environment used for "next version" development. This version is shared by internal staff members for acceptance testing, as well as clients. Regular end-users never interact with this environment.
- **local** is the local development environment on your laptop or workstation.

Each of these environments require their own Solr installation; ideally, each on their own hardware. There are several motives for this, but the underlying reason is the same: isolation.

When developing a search solution, we may place unexpected demand on a Solr server, causing a drop in performance. Often, we as developers will need to re-index all site content as we make changes to fields or the index configuration. Re-indexing a site requires considerable computing resources and can lead to stale index results -- or worse, no results -- until completed. Less often, schema changes are required to the Solr core, involving outage time and requiring corresponding changes to the Drupal site. We want to prevent this from affecting end-users as much as possible. Thus, having a separate server for the production environment is best.

An infrequent, but important motive for using different search servers for each environment is the data on which you are searching. Some Solr applications may involve searching *Personally Identifiable Information* (PII) that should not be available to developers as per legal privacy requirements. In this case, a separate Solr server for local and stage is a requirement. Mock data must be used instead when developing and acceptance-testing the solution.

## Supporting multiple Solr servers in Drupal

Having an environment-specific Solr servers is a must, but this creates an additional problem. When we created the Search API server configuration, we specified the Solr server hostname, port, and other connection information to the Solr core. With a different Solr instance for each environment, we need to change that information to match each environment.

A common method to have per-environment configurations in Drupal is to use the [Config Split](https://www.drupal.org/project/config_split) module. This module allows you to configure one or more "splits", each having additional configuration. A common use for this module is to enable the [Stage File Proxy](https://www.drupal.org/project/stage_file_proxy) module in stage and local, but not in production.

One might think that the solution for Search API is to use Config Split to create a separate Search API server configuration for each environment. While this can work, it has an important drawback.

Later in this course we'll use Views to create new search pages that are powered by Search API and Solr. These views are tightly coupled to each Search API configuration. As a result, we would need to create separate views for each environment. This multiplies our problems as developers.

## Using config overrides for Search API

A better solution is to use *configuration overrides* to dynamically change the connection information. This allows us to target the parts of the Search API configuration that change -- primarily the Solr hostname and core name -- while leaving the remaining configuration unchanged.

### Ensure configurations are exported

By default, Drupal saves a copy of the site configuration to the *sites/default/files* directory of the site. While this is a good default, we want to be sure our configuration is tracked in Git, and the *sites/default/files* directory should be ignored by Git (see your site's *.gitignore*).

Ensure your project has a configuration export directory mapped to *config/sync/* by following the steps in [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup), and that you're familiar with [How to Override Configuration](https://drupalize.me/tutorial/how-override-configuration).

Then, export the configuration using Drush:

```
drush cex
```

### Find the configuration key to override

Now that our configuration is exported, we should be able to find our configuration key.

1. Using a file browser, navigate to your project's *config/sync/* directory.
2. Scroll through the files, looking for a file name starting with `search_api.server`.
3. Note the file name(s). There should be one for each Search API server configuration you have created.

The file name(s) minus the `*.yml` extension are the *configuration key*. We'll need that for the next step.

### Override the configuration

Now we have the Search API server configuration key(s), we can add an override to our *settings.local.php*. For the example containers, we can add the following:

```
$config['search_api.server.my_searchapi_solr']['name'] = 'Solr (Override)';
$config['search_api.server.my_searchapi_solr']['backend_config']['connector_config']['host'] = 'solr';
$config['search_api.server.my_searchapi_solr']['backend_config']['connector_config']['path'] = '/solr';
$config['search_api.server.my_searchapi_solr']['backend_config']['connector_config']['core'] = 'my_drupal_solr';
```

The above does the following for us:

- It overrides the Search API server **name** so we know the override is in effect.
- It changes the Solr **host**. In this case, the new host name is the service name of the Solr container, `solr`.
- It changes the Solr **path** to the core. This is usually not necessary, as the path will be the same across all environments.
- It changes the Solr **core** name.

Be sure to change the settings as appropriate if not using the example containers.

### Validate the override

Once changes to the *settings.local.php* file have been made, we can validate the changes by logging back into our Drupal site:

1. Log into your Drupal site for the target environment using administrator privileges.
2. In the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Examine the list for the Search API server configuration you have overridden. You should see a change in the **Name**, and a green check mark should still appear in the **Status** column.
4. Open the Search API server for editing and validate that other overrides appear as expected.

## Recap

Overriding the Search API Solr configuration isn't difficult. It only requires a few lines of code in your *settings.local.php* or environment-specific settings file. Once done, the change takes effect immediately. Through clever use of multiple environment-specific files, you can support any environment with separate Solr server configurations.

## Further your understanding

- What if you have multiple Search API servers to override?
- When wouldn't you override the configuration?

## Additional resources

- [Stage File Proxy](https://www.drupal.org/project/stage_file_proxy) (Drupal.org)
- [Configuration Sync Directory Setup](https://drupalize.me/tutorial/configuration-sync-directory-setup) (Drupalize.Me)
- [How to Override Configuration](https://drupalize.me/tutorial/how-override-configuration) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Install Search API](/tutorial/install-search-api?p=2815)

Next
[Create Search API Indexes](/tutorial/create-search-api-indexes?p=2815)

Clear History

Ask Drupalize.Me AI

close
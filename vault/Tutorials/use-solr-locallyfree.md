---
title: "Use Solr Locallyfree"
url: "https://drupalize.me/tutorial/use-solr-locally?p=2815"
guide: "[[drupal-site-administration]]"
order: 17
---

# Use Solr Locallyfree

## Content

Just as you would for Drupal, you should always test your search configuration prior to deploying it to production. In this tutorial, we examine the various ways to set up Apache Solr locally on your system. Then we'll walk through setting up DDEV with Solr for local development.

In this tutorial, we'll:

- Describe options for running Solr locally
- List which popular local development environments provide Solr
- Show how to set up a local, DDEV-based local dev environment with Solr

By the end of this tutorial you should be able to list the different ways that Solr can be installed locally, choose an option that works for you, and see how to get started quickly with DDEV.

## Goal

Set up a local web development environment with Solr.

## Prerequisites

- [11.7. Concept: Development Sites](https://drupalize.me/tutorial/user-guide/install-dev-sites)
- [Plan a Solr Installation](https://drupalize.me/tutorial/plan-solr-installation)

If you're using Docker:

- [What Is Docker?](https://drupalize.me/tutorial/what-docker)
- [Dockerize an Existing Project](https://drupalize.me/tutorial/dockerize-existing-project)

## Local development environments that support Solr

Natively installed web development environments like MAMP and Acquia Dev Desktop do **not** support Solr out of the box. Instead, you need to install Solr as you would a standalone server application. This can make these environments less desirable for doing search development. It is possible to install Solr natively, we recommend looking up the official documentation for your OS.

Many virtualized web development environments offer Solr as an optional extra:

- [DDEV](https://ddev.readthedocs.io/en/latest/users/extend/additional-services/)
- [DrupalVM](http://docs.drupalvm.com/en/latest/extras/solr/)
- [Lando](https://docs.lando.dev/solr/)

We'll use DDEV in our example; but, once you've got Solr installed for your environment the only difference in the instructions for the rest of this course will be in entering the environment-specific configuration details that Drupal requires to connect to Solr.

## Solr Cloud versus Single Core

Solr can be run in cloud mode via SolrCloud (modern), or in single core mode (classic). Either will work for local development. The difference is that Solr running in Cloud mode exposes a Configset API that allows Drupal to update Solr's configuration without requiring you to manually update configuration files.

For local development your options are to either run classic standalone Solr with a single core (more on cores later), or Solr in cloud mode with a single node.

The official Solr documentation provides detailed instructions on [installing and running Solr](https://solr.apache.org/guide/solr/latest/deployment-guide/installing-solr.html) and [SolrCloud](https://solr.apache.org/guide/solr/latest/getting-started/tutorial-solrcloud.html). As well as Docker images, and plenty of examples.

## Add Solr to DDEV

For the rest of this series we need Solr running locally so we can walk through integrating it with Drupal. Let's walk through setting up Solr with DDEV for local development.

### Pick a DDEV addon

There are two common approaches to adding Solr to DDEV, pick one:

- [ddev-solr](https://github.com/mkalkbrenner/ddev-solr): Maintained, and recommended, by the Search API Solr module maintainers. Provides Solr (Cloud) using a single Solr node.
- [ddev-drupal9-solr](https://github.com/ddev/ddev-drupal9-solr): Official DDEV plugin, provides Solr running in the "classic standalone" mode using a single core.

### Install the selected addon

Install the addon:

```
ddev get mkalkbrenner/ddev-solr
```

Restart ddev:

```
ddev restart
```

### Verify Solr is running

Once DDEV is up and running, access Solr's UI in browser by opening *<http://<projectname>.ddev.site:8983>*. For example, if the project is named "myproject" the hostname will be *<http://myproject.ddev.site:8983>*.

## Recap

There are many options for running Solr locally on your system. While you can install it natively, most often you will rely on your web development environment's preferred Solr installation method. For this series, we will be using DDEV and the [ddev-solr](https://github.com/mkalkbrenner/ddev-solr) addon to work with Drupal and Search API.

## Further your understanding

- Why use SolrCloud vs. Solr classic for local development?

## Additional resources

- [Search API Solr module's README](https://git.drupalcode.org/project/search_api_solr/-/tree/4.x) (git.drupalcode.org) has instructions for various other approaches to setting up Solr locally, including templates for custom Docker containers. (git.drupalcode.org)
- [DDEV - Additional Service Configuration](https://ddev.readthedocs.io/en/stable/users/extend/additional-services/) (ddev.readthedocs.io)
- [Docker installation on docs.docker.com](https://docs.docker.com/install/) (docs.docker.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Plan a Solr Installation](/tutorial/plan-solr-installation?p=2815)

Next
[Solr Cores](/tutorial/solr-cores?p=2815)

Clear History

Ask Drupalize.Me AI

close
---
title: "Plan a Solr Installationfree"
url: "https://drupalize.me/tutorial/plan-solr-installation?p=2815"
guide: "[[drupal-site-administration]]"
order: 16
---

# Plan a Solr Installationfree

## Content

Apache Solr is not a Drupal module, but a server application like Varnish or MySQL. Before we can use Solr with Drupal, we must plan how we will deploy Solr to our production site.

In this tutorial, we'll:

- List the requirements for Solr installation
- Identify when to install Solr on new hardware
- Describe various installation methods

By the end of this tutorial you should be able to describe a typical Solr install, and begin to list out the various things you'll need to do to install Solr for your environments.

## Goal

Understand the system requirements and general installation steps for installing Apache Solr on a Linux-based web server.

## Prerequisites

- A general understanding of the command line and managing a Linux-based web server.

## Hosted Solr

Your web host might already have Solr available (though you'll still need it locally for development). Most Drupal-centric hosting providers like Pantheon and Acquia do. And there are numerous SaaS hosting options for Solr that might be worth looking into depending on your use case. See the list on the [Search API Solr project page](https://www.drupal.org/project/search_api_solr).

## Server resources

Solr can require substantial computing resources depending on the number of documents (nodes) you need to index, the number of fields for each node, and the amount of searches you expect to run. As every Drupal site will have different search demands, the amount of additional resources necessary is highly variable.

In general, you will want at least:

- 1GB free of memory
- 1 CPU core for each major process on the server

Like the database, Solr can be installed on a standalone server, or on the same server as the web server. For a standalone Solr server, 1 CPU core is enough to start. If Solr is to be installed on the same server as the web server, a minimum of 2 cores is recommended (one for Solr, and one for the web server).

## Solr versions

There are numerous versions of the Solr software, and the Drupal Search API Solr module that connects Drupal to Solr. You'll need to make sure that you're using compatible versions of both. There is a comprehensive version matrix on [the project page for the module](https://www.drupal.org/project/search_api_solr).

If multiple versions of Solr are available, choose the highest version that is also compatible with a version of the Search API Solr module you are using. The 4.2.x versions of the module work for Drupal 9 and 10, and supports a wide range of Solr versions from 3.6 to 8.

## Java requirement

Solr, like Drupal, isn't a standalone executable. It needs a runtime environment in order to function. For Drupal, it's PHP. For Solr, it's Java. For most commodity Linux servers, Java is either pre-installed, or easily installed via the distribution's default package manager.

You can check if Java is installed by running the following command:

```
java -version
```

If the command displays a version, Java is installed. If it returns `Command not found`, you will need to install Java.

## Which Java?

Java is available in a few different distributions. The largest split is between Oracle Java and OpenJDK. The former is considered the official distribution of Java and is supported by Oracle. You may also see this referred to as "Sun Java" referring to the previous maintainer, Sun Microsystems.

Due to licensing reasons, many Linux distributions do not ship with Oracle Java out of the box, and instead ship a fully open source version of Java, called OpenJDK. Solr works equally well with Oracle Java and OpenJDK. This tutorial will assume OpenJDK, although there will be no distinction to the Drupal developer.

## Java version

Solr 7.x and 8.x both require (at least) Java Runtime Environment (JRE) 1.8. Often this will be referred to as "Java 8" or "Java SE 8".

## Installing Solr

Once the correct version of Java is installed, we're ready to install Solr. While many distributions of Linux will offer a package to install Solr, it is recommended you download the latest version of Solr directly from [lucene.apache.org/solr](https://lucene.apache.org/solr/). This will provide you the most flexibility going forward.

**Note:** Make sure you choose a version of Solr compatible with the Drupal Search API Solr module. As of July 2023 the module does not yet support Solr 9.

While the [official Solr documentation](http://lucene.apache.org/solr/guide) can give you detailed steps for installing and configuring Solr, in general the process is as follows:

1. Create a new `solr` user under which to run Solr and own the files.
2. Download and extract the Solr files to */opt/solr*.
3. Start the Solr server using `/opt/solr/bin/solr start`.
4. Use system utilities to configure the Solr server to start at boot-up.

## Validating installation

By default, Solr will provide an admin interface on **port 8983** of whatever server it is installed upon. You can visit the admin interface by navigating to the following address:

```
http://your_solr_server.tld:8983/solr
```

Note that there is no login for this interface. You can configure the Admin UI to require an HTTPAuth login, but many will choose to block all access to the Solr port to prevent tampering.

## Recap

Solr is a server application which relies on Java. In order to run Solr, we first need to install Java, create a Solr user, and then download and extract the Solr software package.

## Further your understanding

- Does Search API require specific versions of Solr?

## Additional resources

- [Official Solr documentation](http://lucene.apache.org/solr/guide) (lucene.apache.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Why Solr?](/tutorial/why-solr?p=2815)

Next
[Use Solr Locally](/tutorial/use-solr-locally?p=2815)

Clear History

Ask Drupalize.Me AI

close
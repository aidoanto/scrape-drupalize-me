---
title: "Set up Demo Site with Views and Contentfree"
url: "https://drupalize.me/tutorial/set-demo-site-views-and-content?p=2670"
guide: "[[views-drupal]]"
---

# Set up Demo Site with Views and Contentfree

## Content

To follow along with our Drupal Views tutorials, set up a Drupal site loaded with our 4 custom views and baseball stats content that will make querying in Views a bit more interesting and meaningful.

By the end of this tutorial, you should choose a solution and follow the instructions for creating a Drupal site loaded with our starting point content and views.

## Goal

- Set up a Drupal site with a starting point containing baseball stats content and 4 custom views.

## Prerequisites

- [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev)

## Install Drupal with demo content and configuration

### Install DDEV and create a new Drupal application

Follow the instructions in [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev) to get an empty Drupal site running. Then follow the remaining steps to populate it with sample data to use while learning Views.

### Create a new directory in your project called *db-dumps*

In the root of your project, create a new directory called *db-dumps*. This is where we'll store a database dump which we'll import and populate the site with content and configuration.

```
mkdir db-dumps
```

### Download our database starting point

- [Drupal 11 database starting point](https://github.com/DrupalizeMe/hands-on/blob/master/db-dumps/START-d11-views.sql.gz)

Select the *Download* button from that page and save the file to your project's *db-dumps* directory.

### Import the database with ddev's import-db command

In a Terminal window, navigate to the root of your project and run the following command:

`ddev import-db --file=db-dumps/START-d11-views.sql.gz`

### Visit the site

Run `ddev launch` and DDEV will open up the local site URL in your browser.

### Log in

Log in (at path *user/login*) with username: `admin`; password: `admin`.

If you notice any un-themed pages, clear all caches by using the *Manage* administrative menu and navigating to *Configuration* > *Performance* (*admin/config/development/performance*) and selecting the **Clear all caches** button.

You are now ready to follow along with any of our [Views: Create Lists with Drupal](https://drupalize.me/course/views-create-lists-drupal) tutorials.

## Recap

In this exercise, we installed Drupal and imported a starting-point database with content and Views. We will be using this as a starting point for the tutorials in [Views: Create Lists with Drupal](https://drupalize.me/course/views-create-lists-drupal).

## Further your understanding

- Do you have a documented, repeatable, and reliable process for setting up a local development environment with Drupal? There are many options to choose from. Take the time to find a solution that works best for your operating system, use case, and knowledge base.

## Additional resources

- [DDEV: System Requirements and Installation](https://ddev.readthedocs.io/en/stable/) (ddev.readthedocs.io)
- [DDEV: Drupal CMS Quickstart](https://ddev.readthedocs.io/en/latest/users/quickstart/#drupal) (ddev.readthedocs.io)
- [Development Environments](https://drupalize.me/topic/development-environments) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Add a REST Endpoint with Views](/tutorial/add-rest-endpoint-views?p=2670)

Clear History

Ask Drupalize.Me AI

close
---
title: "Install Drupal Locally with DDEV"
url: "https://drupalize.me/tutorial/install-drupal-locally-ddev"
guide: "[[docker-drupal-developers]]"
order: 38
---

# Install Drupal Locally with DDEV

## Content

Installing Drupal using the instructions in this tutorial will give you a working Drupal site that can be used for learning, or real-world project development.

Before you can work on a Drupal site locally (on your computer), you'll need to set up a *local development environment*. This includes all the [system requirements](https://www.drupal.org/docs/getting-started/system-requirements) like PHP and a web server, that Drupal needs in order to run. Our favorite way to accomplish this is using DDEV.

In this tutorial we'll learn:

- How to install and configure DDEV for use with a Drupal project.
- How to use DDEV's integrated Composer to download Drupal and Drush.
- How to install Drupal inside DDEV so you can access the site and start doing development.

By the end of this tutorial, you should be able to set up a local development environment for learning Drupal or working on a new Drupal project.

## Goal

Walk through the steps required to get Drupal running on your local machine using DDEV.

## Prerequisites

- You should be comfortable using a command-line terminal. (If you're not comfortable *yet*, you'll get some practice in this tutorial.) See [Moving Around the Command Line](https://drupalize.me/tutorial/moving-around-command-line?p=880).
- [DDEV](https://ddev.com/) is a Docker-based tool that provides a preconfigured local development environment for Drupal. The easiest way to install Docker is via the [Docker Desktop edition](https://docs.docker.com/desktop/) for your OS. DDEV will also work with Docker engine alternatives like [Colima](https://github.com/abiosoft/colima).
- To install DDEV, see the [DDEV installation documentation](https://ddev.readthedocs.io/en/latest/users/install/ddev-installation/).
- If you can run `ddev debug dockercheck` and there are no errors, then you're ready to install Drupal.

This guide is largely copied from [this Drupal.org documentation page](https://www.drupal.org/docs/official_docs/local-development-guide) which we also help maintain.

This is the same approach that we use for developing the Drupalize.Me site. As well as how we set up all our demo sites for recording tutorials and teaching workshops.

**Note**: The steps below will install the *latest* version of Drupal. See the DDEV documentation page, [CMS Quickstarts > Drupal](https://ddev.readthedocs.io/en/latest/users/quickstart/#drupal), to install specific (older) versions of Drupal.

### Create a directory for your project and configure DDEV

Start by creating a directory where you want your Drupal project to live, and then change (`cd`) to that directory in the command line.

In this example, we'll use `my-site` (no spaces or special punctuation) for our new application and run the following commands:

```
mkdir my-site
cd my-site
ddev config --project-type drupal --docroot web
```

This will create a new DDEV project configured to host a Drupal application. DDEV will store the generated configuration in a new *.ddev/* subdirectory. The DDEV project name will be the same as the parent folder (`my-site`).

**Note:** For Drupal 11 sites make sure the PHP version in the *.ddev/config.yml* file is set to 8.3 or greater.

### Start DDEV

Next, start the DDEV container.

```
ddev start
```

You now have a web server and database server configured and running. Configuring DDEV first allows us to run Composer from within DDEV instead of installing it locally.

### Install Drupal with Composer

Next, we use [Composer](https://drupalize.me/tutorial/what-composer) to install Drupal.

Create a new Drupal application with Composer. *Note:* `ddev composer create-project` will unpack and download the files into the current folder, unlike `composer create-project` which downloads Drupal into a separate folder.

```
ddev composer create-project drupal/recommended-project
```

This is the DDEV equivalent of `composer create-project drupal/recommended-project`. It's possible to install Drupal with Composer without using the DDEV environment, but we don't recommended it, since PHP versions in DDEV and your local environment may differ.

You now have a server running, and the Drupal code downloaded.

### Install Drupal (with Drush)

At this point you can launch your Drupal site (`ddev launch`), and you will see Drupal's interactive installer. You have 2 choices:

1. Return to the command line interface and install Drupal using Drush (our recommendation).
2. Proceed with [Drupal's interactive installer](https://drupalize.me/tutorial/user-guide/install-run).

We recommend installing Drush via Composer, and using it to install Drupal. If you practice installing Drupal using Drush, you will speed up your Drupal installation process, and get comfortable using Drush to streamline mundane tasks.

First, [install the latest version of Drush](https://drupalize.me/tutorial/install-drush-using-composer), a command-line utility for Drupal:

```
ddev composer require --dev drush/drush
```

Then, using DDEV and Drush, execute the following command:

```
ddev drush site:install --account-name=admin --account-pass=admin -y
```

Drupal is now installed, with an automatically-generated password for the user 1 administrator account (`admin`).

### Install `drupal/core-dev`

If you're doing custom code development, or working on contributed modules, we recommend installing the `drupal/core-dev` Composer package. This will let you use tools like `phpcs` (code standards checker) and `phpunit` (unit test runner).

```
ddev composer require --dev drupal/core-dev
```

If you plan to work on developing tests, follow the instructions in [Configure Your Environment to Run Tests](https://drupalize.me/tutorial/configure-your-environment-run-tests).

### Log in

Finally, launch your new Drupal site and log in.

```
ddev launch
```

You can also generate a one-time login link for the administrator account, if you need to reset the admin account for any reason:

```
ddev drush user:login
```

*Tip*: At any time, execute `ddev describe` to view the URL of your site. Copy and paste that URL into your web browser to visit it.

### Explore

At this point you should have a Drupal site that you can access in your browser and begin setting up via Drupal's administration UI.

DDEV will synchronize the files that make up your Drupal project into the directory where you ran the initial `ddev config` command. The directory should now contain something like the following:

```
.
├── .ddev
├── composer.json
├── composer.lock
├── vendor
└── web
    ├── INSTALL.txt
    ├── README.md
    ├── autoload.php
    ├── core
    ├── example.gitignore
    ├── index.php
    ├── modules
    ├── profiles
    ├── robots.txt
    ├── sites
    ├── themes
    ├── update.php
    └── web.config
```

You can add, or edit, files in this project and the changes will be reflected in DDEV. So, write a custom module, or theme, and get started developing with Drupal!

### Stop DDEV

When you're done working on your project you can stop DDEV, and quit Docker. This will free up those resources for other application to use.

Stop DDEV:

```
ddev stop
```

And then quit Docker via the Docker UI, or whatever Docker tool you're using.

### Learn how to use DDEV

While the steps above will give you all you need to get started developing a Drupal site, DDEV is capable of a lot more. Learn how to use its other features via the [DDEV documentation](https://ddev.readthedocs.io/en/stable/).

## Restart your DDEV project

Ready to get back to work on a project you previously started using DDEV? In the command line, navigate to the root directory of the project (the same place you ran `ddev config` earlier) and start the project again:

```
cd my-site
ddev start && ddev launch
```

## Why DDEV and not `{insert preference here}`?

There are a lots of really great options out there for setting up a local development environment. We chose to use DDEV for this local development guide because it met the following criteria:

- Must be free and open source, without tying users into a proprietary product or service.
- Must be well maintained, with long-term support.
- Must follow Drupal best practices.
- Must be compatible with MacOS, Windows, and Linux.
- Must be as simple as possible.

And perhaps most of all, because all of us on the Drupalize.Me team use DDEV.

## Recap

In this tutorial, we learned how set up a local development environment using Docker, DDEV, and Composer.

## Further your understanding

- [Learn more about using Composer to manage a Drupal project](https://drupalize.me/tutorial/use-composer-your-drupal-project).
- [Learn more about Docker](https://drupalize.me/tutorial/best-practice-drupal-development). Hint: DDEV is a wrapper around Docker that makes it even easier to use Docker for Drupal development. But under-the-hood, it's Docker. So all your Docker configuration tweaks will work with DDEV.

## Additional resources

- [Local Development Guide](https://www.drupal.org/docs/official_docs/local-development-guide) (Drupal.org)
- [DDEV](https://ddev.com/)

Was this helpful?

Yes

No

Any additional feedback?

Clear History

Ask Drupalize.Me AI

close
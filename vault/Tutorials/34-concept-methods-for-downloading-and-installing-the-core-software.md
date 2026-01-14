---
title: "3.4. Concept: Methods for Downloading and Installing the Core Software"
url: "https://drupalize.me/tutorial/user-guide/install-decide?p=2368"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 14
---

# 3.4. Concept: Methods for Downloading and Installing the Core Software

## Content

### Prerequisite knowledge

- [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")
- [Section 3.2, “Concept: Server Requirements”](https://drupalize.me/tutorial/user-guide/install-requirements "3.2. Concept: Server Requirements")
- [Section 1.4, “Concept: Distributions”](https://drupalize.me/tutorial/user-guide/understanding-distributions "1.4. Concept: Distributions")

### What methods are available for downloading the core software?

Before you can build a site, you will need to first download the core software. Depending on your plans, there are several ways that you can download the core software:

Use Composer
:   If you plan to build a site, and continue to develop it over time you should use Composer to download the core software, because Composer will manage the dependencies properly. If you plan to use the Drush tool (see [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")), using Composer is required. See [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files") for instructions.

Try a free online demo
:   If you are evaluating whether or not to use Drupal to build a site, you can use an online provider to get a demo installation of the core software in 20 minutes or less. See the [*Drupal.org* page "Try Drupal"](https://www.drupal.org/try-drupal).

Use a one-click installer from your hosting provider
:   If you choose to install the core software at your hosting provider, your hosting provider may have specific documentation and/or a one-click install that you can use. See [*Drupal.org’s* list of hosting providers that support Drupal](https://www.drupal.org/hosting).

Use a pre-configured environment
:   Use a pre-configured environment or virtual machine that contains Drupal and all the required supporting software to install Drupal locally. See the section for your operating system under [*Drupal.org* community documentation page "Local server setup guide"](https://www.drupal.org/docs/develop/local-server-setup) for possible options.

### What happens when I install the core software?

*Installing* the core software means setting up some database tables, configuration, and an administrative user account, so that you can build and use your site.

### What methods are available for installing the core software?

There are several ways to install the core software:

Behind-the-scenes installer
:   If you choose to use an online demo or one-click installer from a hosting provider, the core software may be installed for you automatically.

Interactive installer
:   The core software has an interactive installer that presents you with several on-line forms, and then completes the installation using the information you provide in the forms. See [Section 3.1, “Preparing to Install”](https://drupalize.me/tutorial/user-guide/install-prepare "3.1. Preparing to Install") and [Section 3.7, “Running the Interactive Installer”](https://drupalize.me/tutorial/user-guide/install-run "3.7. Running the Interactive Installer").

Command-line tool
:   Command-line tools (see [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")) can also be used to perform the installation steps.

Demo site installer
:   Quickly create a temporary demo site that uses the built-in web server and SQLite database that are part of PHP by running the command below from the root directory of your project. In this case, you will not run the interactive installer. See the [Evaluator Guide](https://www.drupal.org/docs/official_docs/evaluator-guide) to learn more.

    ```literallayout
    ----
    php -d memory_limit=256M core/scripts/drupal quick-start demo_umami
    ----
    ```

**Attributions**

Written and edited by [Drew Gorton](https://www.drupal.org/u/dgorton), [Michael Lenahan](https://www.drupal.org/u/michaellenahan) at [erdfisch](https://erdfisch.de), [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[3.3. Concept: Additional Tools](/tutorial/user-guide/install-tools?p=2368)

Next
[3.5. Setting Up an Environment with DDEV](/tutorial/user-guide/install-ddev?p=2368)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
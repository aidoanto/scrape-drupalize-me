---
title: "3.5. Setting Up an Environment with DDEV"
url: "https://drupalize.me/tutorial/user-guide/install-ddev?p=2368"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 3.5. Setting Up an Environment with DDEV

## Content

### Goal

Set up a local development environment using DDEV to serve the application and Composer to download the required files.

### Prerequisite knowledge

[Section 3.2, “Concept: Server Requirements”](https://drupalize.me/tutorial/user-guide/install-requirements "3.2. Concept: Server Requirements") [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files")

### Why use DDEV?

DDEV is a local development environment for PHP applications built on Docker. It includes all the necessary components to run the core software, and is used by many developers in the Drupal community.

### Steps

1. Follow the [official DDEV installation instructions](https://ddev.readthedocs.io/en/stable/users/install/ddev-installation/) to install DDEV on your local machine. DDEV is available for Windows, Mac, and Linux. The installation process is different for each operating system, so be sure to follow the instructions for your OS.
2. After installing DDEV, follow the [Drupal Quickstart instructions](https://ddev.readthedocs.io/en/stable/users/quickstart/#drupal) to download the core software using Composer and install it in the DDEV environment.
3. Run the command `ddev launch` from the directory created in the previous step to open the site in your web browser and confirm the environment is working correctly.

### Related topics

- [Section 3.2, “Concept: Server Requirements”](https://drupalize.me/tutorial/user-guide/install-requirements "3.2. Concept: Server Requirements")
- [Section 11.7, “Concept: Development Sites”](https://drupalize.me/tutorial/user-guide/install-dev-sites "11.7. Concept: Development Sites")
- [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")

### Additional resources

- [DDEV documentation](https://ddev.readthedocs.io/en/stable/)
- [Install Drupal using DDEV for local development](https://www.drupal.org/docs/getting-started/installing-drupal/install-drupal-using-ddev-for-local-development)

**Attributions**

Written and edited by [Joe Shindelar](https://www.drupal.org/u/eojthebrave) at [Drupalize.Me](https://drupalize.me).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[3.4. Concept: Methods for Downloading and Installing the Core Software](/tutorial/user-guide/install-decide?p=2368)

Next
[3.6. Using Composer to Download and Update Files](/tutorial/user-guide/install-composer?p=2368)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
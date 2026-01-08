---
title: "3.7. Running the Interactive Installer"
url: "https://drupalize.me/tutorial/user-guide/install-run?p=2368"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 3.7. Running the Interactive Installer

## Content

### Goal

Install the core software and create the admin account by running the included installer.

### Site prerequisites

[Section 3.1, “Preparing to Install”](https://drupalize.me/tutorial/user-guide/install-prepare "3.1. Preparing to Install")

Note that if you followed the instructions in [Section 3.5, “Setting Up an Environment with DDEV”](https://drupalize.me/tutorial/user-guide/install-ddev "3.5. Setting Up an Environment with DDEV") the core software was already installed. If you wish to install the core software again, you can run the command `ddev drush sql:drop` and then follow the instructions below.

### Steps

Sprout Video

1. If you are using a 1-click install from a hosting provider or demo site, you will most likely see some or all of the following screens as part of the installation process. If you uploaded the core files manually or using Composer, to start the installer, open a browser and visit the URL that you set up for your hosting.
2. Select a language on the first page of the installer; for example, English. You could optionally choose from any of the other listed languages. The language files for the chosen language will be downloaded and installed so that the rest of the installation process can be finished in the chosen language. After choosing a language, click *Save and continue*.

   Image

   ![Choose a language](/sites/default/files/styles/max_800w/public/user_guide/images/install-run-1.png?itok=Mio3EwQ2)
3. Select an installation profile. Installation profiles provide site features and functions for a specific type of site as a single download containing the core software, contributed modules, themes, and pre-defined configuration. Core contains two installation profiles. Select the core Standard installation profile. Click *Save and continue*.

   Image

   ![Choose an installation profile](/sites/default/files/styles/max_800w/public/user_guide/images/install-run-2.png?itok=LCX6Qa68)
4. The next step in the installer will verify that your system meets the minimum requirements. If it does not, you’ll be presented with an outline of what needs to be corrected in order to proceed. If it does, the installer will automatically advance to the next step.
5. Provide details of the database you created in the [Section 3.1, “Preparing to Install”](https://drupalize.me/tutorial/user-guide/install-prepare "3.1. Preparing to Install") chapter. Then click *Save and continue*.

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Database name | The custom name given to the database | drupal |
   | Database username | Username created | databaseUsername |
   | Database password | Password chosen |  |

   Image

   ![Database configuration form](/sites/default/files/styles/max_800w/public/user_guide/images/install-run-3.png?itok=XlCo_tlx)
6. The next step will display a progress bar under the heading *Installing Drupal*. After the installer has completed, it will automatically advance to the next step.

   Image

   ![Installation progress bar](/sites/default/files/styles/max_800w/public/user_guide/images/install-run-4.png?itok=h1Tu0f-r)
7. The next step is to configure some basic information about your new site (also notice if there is a warning about file permissions, for a later step). Note that the user account you create in this step is the site’s admin account. See [Section 7.2, “Concept: The User 1 Account”](https://drupalize.me/tutorial/user-guide/user-admin-account "7.2. Concept: The User 1 Account") for important information about this unique account. You can safely name this account "admin", and make sure to choose a secure and unique password.

   Fill in the form with the following information:

   | Field name | Explanation | Value |
   | --- | --- | --- |
   | Site name | The name chosen for the site | Anytown Farmers Market |
   | Site email address | The email associated with the site | [[email protected]](/cdn-cgi/l/email-protection#c9a0a7afa689acb1a8a4b9a5ace7aaa6a4) |
   | Username | The designated user’s credentials | admin |
   | Password | The password chosen |  |
   | Confirm password | Repeat the password |  |
   | Email address | The user’s email | [[email protected]](/cdn-cgi/l/email-protection#7213161f1b1c32170a131f021e175c111d1f) |

   The remaining fields can likely be left at their default values.

   Image

   ![Configuration form](/sites/default/files/styles/max_800w/public/user_guide/images/install-run-5.png?itok=s5jbhBxz)
8. Click *Save and continue*.
9. You will be redirected to the front page of your new site and you should see the message *Congratulations, you installed Drupal!* displayed at the top of the page.

   Image

   ![Installation success](/sites/default/files/styles/max_800w/public/user_guide/images/install-run-6.png?itok=AIvdm2F4)
10. You may have seen a warning in the Configuration step about file permissions, and you may continue to see this warning until you fix the permissions. To avoid the warning and make your site more secure, change the permissions on the *sites/default* directory and the *sites/default/settings.php* file so that they are read-only (you may need to consult your hosting company documentation about how to do that).

### Expand your understanding

Alternatively, you can install the software using Drush instead of the UI. Use the following Drush command, from inside the directory that you downloaded the software to, where *DB\_NAME*, *DB\_USER* and *DB\_PASS* are your database’s credentials:

```screen
drush site:install standard --db-url='mysql://DB_USER:DB_PASS@localhost/DB_NAME' --site-name=example
```

Check the Status Report to see if there are any problems with the installation. See [Section 12.5, “Concept: Status Report”](https://drupalize.me/tutorial/user-guide/prevent-status "12.5. Concept: Status Report").

### Related concepts

- [Section 11.7, “Concept: Development Sites”](https://drupalize.me/tutorial/user-guide/install-dev-sites "11.7. Concept: Development Sites")
- [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")

### Additional resources

- [*Drupal.org* community documentation page "Create a database"](https://www.drupal.org/docs/installing-drupal/step-3-create-a-database)
- [*Drupal.org* community documentation section "Webhosting issues"](https://www.drupal.org/server-permissions)

**Attributions**

Written and edited by [Joe Shindelar](https://www.drupal.org/u/eojthebrave) at [Drupalize.Me](https://drupalize.me), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[3.6. Using Composer to Download and Update Files](/tutorial/user-guide/install-composer?p=2368)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
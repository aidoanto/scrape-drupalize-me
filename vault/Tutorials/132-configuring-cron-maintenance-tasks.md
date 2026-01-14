---
title: "13.2. Configuring Cron Maintenance Tasks"
url: "https://drupalize.me/tutorial/user-guide/security-cron?p=2404"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 32
---

# 13.2. Configuring Cron Maintenance Tasks

## Content

### Goal

Check whether cron maintenance tasks are run regularly, and if not, either install the core Automated Cron module or run cron maintenance tasks from outside the website.

### Prerequisite knowledge

[Section 13.1, “Concept: Cron”](https://drupalize.me/tutorial/user-guide/security-cron-concept "13.1. Concept: Cron")

### Steps

Sprout Video

1. Review the *Status report* (see [Section 12.5, “Concept: Status Report”](https://drupalize.me/tutorial/user-guide/prevent-status "12.5. Concept: Status Report")) to see when cron maintenance tasks were last run.

   If you installed the website using the core Standard installation profile (or similar), then cron maintenance tasks might already be running via the core Automated Cron module. By default, these tasks are run about every three hours.
2. Choose whether to run cron maintenance tasks using the core Automated Cron module, or by other means. The core Automated Cron module might not be suitable for some websites because:

   - Each time someone accesses a page on the site, the module checks how long it has been since cron maintenance tasks have last run, and then runs them if necessary. If no one visits the website for a long time, cron maintenance tasks will not be run.
   - Cron maintenance tasks are run after the page has been generated. This means there is less time for the tasks to be run before various server timeouts are reached (for example, PHP execution timeout). If this happens, the logs (see [Section 12.4, “Concept: Log”](https://drupalize.me/tutorial/user-guide/prevent-log "12.4. Concept: Log")) will show error messages that cron is unable to complete.
   - There is a small [scalability](https://en.wikipedia.org/wiki/Scalability) cost associated with the core Automated Cron module. This is because one of the web server’s processes is occupied (and can’t serve other web pages) until the cron maintenance tasks are complete.
3. If you want to use the core Automated Cron module, first make sure it is installed (it is installed with the core Standard install profile; see [Section 4.3, “Installing a Module”](https://drupalize.me/tutorial/user-guide/config-install "4.3. Installing a Module") if it is not installed).

   Next, configure the module to control how frequently cron maintenance tasks are run. In the *Manage* administrative menu, navigate to *Configuration* > *System* > *Cron* (*admin/config/system/cron*). Select the desired interval from the *Run cron every* field under *Cron settings*, and click *Save configuration*.

   Image

   ![Configure the core Automated Cron module](../assets/images/security-cron.png)
4. If you want to run cron maintenance tasks from outside the website, uninstall the core Automated Cron module (see [Section 4.4, “Uninstalling Unused Modules”](https://drupalize.me/tutorial/user-guide/config-uninstall "4.4. Uninstalling Unused Modules")). Next, find the cron URL. This URL is shown in the *Status report* (see [Section 12.5, “Concept: Status Report”](https://drupalize.me/tutorial/user-guide/prevent-status "12.5. Concept: Status Report")), and in the *Cron* administration page (see previous step). The URL looks like this: *[http://www.example.com/cron/0MgWtfB33FYbbQ5UAC3L0LL3RC0PT3RNUBZILLA0Nf1…](http://www.example.com/cron/0MgWtfB33FYbbQ5UAC3L0LL3RC0PT3RNUBZILLA0Nf1Re)*

   Whenever this URL is visited, cron maintenance tasks will run. Set up one of the following schedulers to access this URL regularly:

   - [The Cron daemon](https://www.drupal.org/docs/7/setting-up-cron/configuring-cron-jobs-using-the-cron-command) (Linux, OS X, Solaris, BSD)
   - [Scheduled Tasks](https://www.drupal.org/docs/7/setting-up-cron-for-drupal/configuring-cron-jobs-with-windows) (Windows)
   - A cron SASS provider (software as a service)
   - A cron manager provided by your web hosting provider (see the documentation provided by your provider)

### Related concepts

[Section 13.3, “Concept: Security and Regular Updates”](https://drupalize.me/tutorial/user-guide/security-concept "13.3. Concept: Security and Regular Updates")

### Additional resources

- [Drush page "Running Drupal cron tasks from Drush"](https://www.drush.org/latest/cron/)
- [*Drupal.org* community documentation page "Setting up cron"](https://www.drupal.org/docs/7/setting-up-cron/overview)

**Attributions**

Written and edited by [Dave Hansen-Lange](https://www.drupal.org/u/dalin) at [Advomatic](https://www.advomatic.com/), [Boris Doesborg](https://www.drupal.org/u/batigolix), and [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[13.1. Concept: Cron](/tutorial/user-guide/security-cron-concept?p=2404)

Next
[13.3. Concept: Security and Regular Updates](/tutorial/user-guide/security-concept?p=2404)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
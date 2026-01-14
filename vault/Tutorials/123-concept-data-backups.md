---
title: "12.3. Concept: Data Backups"
url: "https://drupalize.me/tutorial/user-guide/prevent-backups?p=2398"
guide: "[[acquia-certified-drupal-front-end-specialist-exam]]"
order: 13
---

# 12.3. Concept: Data Backups

## Content

### Prerequisite knowledge

- [Section 1.1, “Concept: Drupal as a Content Management System”](https://drupalize.me/tutorial/user-guide/understanding-drupal "1.1. Concept: Drupal as a Content Management System")
- [Section 3.1, “Preparing to Install”](https://drupalize.me/tutorial/user-guide/install-prepare "3.1. Preparing to Install")

### What is a site backup?

If something happens to the computer (or computers) that your site and its database are running on, or if you lose access to this computer, you could lose some or all of your site’s data. You could also lose data if your site is hacked, or if someone with administrative privileges on your site deletes or alters data mistakenly from the administrative interface. In order to prevent scenarios like this from being permanent, expensive data losses, it is important to make regular backups of your site’s data, and to store them in a location that is separate from the computer where your site is running.

The frequency with which you should make data backups, and how many backups you should keep, depends on how frequently your site is changing. If you have a very large amount of content on your site that is being added to or updated many times per day, you would want to make more frequent backups than you would for a site that changes rarely. Also consider that some time could pass between when a data problem occurs and when you notice that it is a problem, so storing a sequence of backups (so that you can go back to the last known good data and retrieve that), rather than overwriting a single backup repeatedly, is a good practice.

Another consideration is that whatever format you store your backups in, it is a good idea to verify that you can actually retrieve lost data from your backups. You might want to test several possible data loss scenarios, and make sure that your data can be restored to the site in all cases.

In order to make a complete backup of your site, you will need to make copies of the following:

- The data in the *sites* directory, including the *sites/default/settings.php* file.
- The data in your site’s database. A few tables can be truncated, such as those storing the temporary data cache and user login session information, but it is always safe to back up the entire database.
- Uploaded files, such as images and other attachments. The location of these files is configurable; the standard location is the *sites/default/files* directory under your site root. In the *Manage* administrative menu, navigate to *Configuration* > *Media* > *File system* (*admin/config/media/file-system*) to check the file upload locations; to change them, you’ll need to edit your *settings.php* file.
- Modules, themes and any other software files you have customized. You can find customized modules and themes in the *modules* and *themes* directories respectively. Some people prefer to back up all software files, including core files and contributed modules and themes (which you could recover by downloading them again from the source), rather than trying to pick out specific files that definitely need to be backed up.

You can perform a test to confirm whether your backup has been done right by making a development copy of the site (see [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site")).

### Related topics

- [Section 13.5, “Updating the Core Software”](https://drupalize.me/tutorial/user-guide/security-update-core "13.5. Updating the Core Software")
- [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site")
- [Section 12.1, “Concept: Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache "12.1. Concept: Cache")

### Additional resources

- [*Drupal.org* community documentation page "Backing up a site"](https://www.drupal.org/docs/7/backing-up-and-migrating-a-site/backing-up-a-site)
- The [contributed Backup and Migrate module](https://www.drupal.org/project/backup_migrate), which can be used to set up automatic backups of the database and uploaded files.

**Attributions**

Written by [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[12.2. Clearing the Cache](/tutorial/user-guide/prevent-cache-clear?p=2398)

Next
[12.4. Concept: Log](/tutorial/user-guide/prevent-log?p=2398)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
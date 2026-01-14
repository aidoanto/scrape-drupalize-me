---
title: "13.5. Updating the Core Software"
url: "https://drupalize.me/tutorial/user-guide/security-update-core?p=2404"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 35
---

# 13.5. Updating the Core Software

## Content

### Goal

Update the core software, either through the administrative interface or by using Drush.

### Site prerequisites

- If you want to use Drush, Drush must be installed. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools").
- If your site is live, you should test this process in a development environment before running it on your production site. See [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site").

### Steps

Sprout Video

1. Make a complete backup of your site. Refer to [Section 12.3, “Concept: Data Backups”](https://drupalize.me/tutorial/user-guide/prevent-backups "12.3. Concept: Data Backups").
2. Open *settings.php* (*/sites/default/settings.php*) in any plain text editor. Find the line with the *$settings[*update\_free\_access*]* variable. By default, it is set to "FALSE" due to security reasons. Change the setting to "TRUE":

   ```screen
   $settings['update_free_access'] = TRUE;
   ```
3. Disable any caching technique (memcache, varnish, and so on) your application might be using.
4. Put your site in maintenance mode. See [Section 11.2, “Enabling and Disabling Maintenance Mode”](https://drupalize.me/tutorial/user-guide/extend-maintenance "11.2. Enabling and Disabling Maintenance Mode").
5. If you are using Composer to manage dependencies, skip the next six steps, and instead see [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files") for instructions on downloading updated files. Continue with the *update.php* step.
6. Download the tar.gz or zip file archive for the latest version of Drupal core for the branch you are currently using (such as 8.x or 9.x) from [*Drupal.org* Drupal Core Downloads](https://www.drupal.org/project/drupal). See [Section 3.1, “Preparing to Install”](https://drupalize.me/tutorial/user-guide/install-prepare "3.1. Preparing to Install") for more details on how to find the latest version.
7. Upload the archive file to your web hosting server.
8. Extract the archive file to a temporary directory on your server (should be outside the directory where the site is hosted). Your hosting control panel’s file manager should provide a way to extract the files. Or, if you have terminal access to your hosting server (running Linux), you can use a command like:

   ```screen
   tar -xzf drupal-8.3.2.tar.gz
   ```
9. In your site hosting directory, delete the *core* and *vendor* directories, and all files that are not in a subdirectory, including *.htaccess*, *composer.json*, and *autoload.php*. Don’t delete custom and customized files because you may end up losing the custom functionality stored in them.
10. Copy the *core* and *vendor* directories and the non-custom/non-customized files that you deleted in the preceding step from the temporary directory to your site directory.
11. Run the *update.php* script using either of the following:

    - Visit *<http://www.example.com/update.php>* in your browser (where *[www.example.com](http://www.example.com)* is your site’s URL). Click *Continue* in the first screen to run the updates and successfully complete the script.
    - Run the following Drush command: `drush updatedb`
12. If you get any error or warning, re-run the *update.php* script again till all the updates have been completed successfully.
13. Open *settings.php* (*/sites/default/settings.php*) in a text editor. Find the line with the *$settings[*update\_free\_access*]* variable and update it to "FALSE":

    ```screen
    $settings['update_free_access'] = FALSE;
    ```
14. Click *Administration pages* to return to the administration section of your site.
15. Take your site out of maintenance mode. See [Section 11.2, “Enabling and Disabling Maintenance Mode”](https://drupalize.me/tutorial/user-guide/extend-maintenance "11.2. Enabling and Disabling Maintenance Mode").
16. Clear the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache").
17. Re-enable any caching technique you disabled at Step 3.
18. You should have the updated version running. You can verify the current version of your software by checking the *Status report* (see [Section 12.5, “Concept: Status Report”](https://drupalize.me/tutorial/user-guide/prevent-status "12.5. Concept: Status Report")).

### Expand your understanding

- [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")
- [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site")
- [Section 12.3, “Concept: Data Backups”](https://drupalize.me/tutorial/user-guide/prevent-backups "12.3. Concept: Data Backups")

### Related concepts

[Section 12.5, “Concept: Status Report”](https://drupalize.me/tutorial/user-guide/prevent-status "12.5. Concept: Status Report")

### Additional resources

- ["Drupal Core Downloads" page on *Drupal.org*](https://www.drupal.org/project/drupal)
- ["Registry Rebuild" page on *Drupal.org*](https://www.drupal.org/project/registry_rebuild)
- The file */core/UPDATE.txt* within your installation.

**Attributions**

Written and edited by [Surendra Mohan](https://www.drupal.org/u/surendramohan), [Boris Doesborgh](https://www.drupal.org/u/batigolix), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[13.4. Keeping Track of Updates](/tutorial/user-guide/security-announce?p=2404)

Next
[13.6. Updating a Module](/tutorial/user-guide/security-update-module?p=2404)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
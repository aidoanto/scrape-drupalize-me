---
title: "12.2. Clearing the Cache"
url: "https://drupalize.me/tutorial/user-guide/prevent-cache-clear?p=2398"
guide: "[[acquia-certified-drupal-front-end-specialist-exam]]"
---

# 12.2. Clearing the Cache

## Content

### Goal

Clear or rebuild your site’s internal caches to ensure they are up-to-date with the most recent data, using the user interface or Drush.

### Prerequisite knowledge

- [Section 12.1, “Concept: Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache "12.1. Concept: Cache")
- [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools")

### Site prerequisites

If you want to use Drush to clear the cache, Drush must be installed. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools").

### Steps

Sprout Video

You can use the administrative interface or Drush to clear the cache. You can also use the rebuild script or Drush to do a more complete cache rebuild.

#### Using the administrative interface to clear the cache

1. In the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Performance* (*admin/config/development/performance*). If you cannot access this page in the administrative interface, use one of the other methods to clear or rebuild the cache.
2. Click *Clear all caches*.
3. A message saying the cache has been cleared appears at the top of the page.
4. If this doesn’t resolve the problem that caused you to want to clear the cache, try a rebuild instead.

#### Using the rebuild script

1. Open *settings.php* (*/sites/default/settings.php*) in any plain text editor. Add this line to the end of the file and save it:

   ```screen
   $settings['rebuild_access'] = TRUE;
   ```
2. Visit *<http://www.example.com/core/rebuild.php>* in your browser (where *[www.example.com](http://www.example.com)* is your site’s URL). After a short pause, you should be redirected to the home page of your site, and the cache should be rebuilt.
3. Open *settings.php* (*/sites/default/settings.php*) in a text editor. Find the line you added with *$settings[*rebuild\_access*]*, remove this line, and save the file.

#### Using Drush to rebuild or clear the cache

You can use one of two commands:

- Use the command `drush cache:rebuild` to clear and rebuild all cached data for a site. After running this command, you will see the output message "Cache rebuild complete."
- Use the command `drush cache:clear` to see a list of individual caches and then choose the specific cache you would like to clear. Running this command should produce output like the following:

  ```screen
  > drush cache:clear
  Enter a number to choose which cache to clear.
   [0]  :  Cancel
   [1]  :  drush
   [2]  :  theme-registry
   [3]  :  menu
   [4]  :  css-js
   [5]  :  block
   [6]  :  module-list
   [7]  :  theme-list
   [8]  :  render
   [9]  :  views
  ```

Choose a cache to clear by entering the number associated with that cache. Press "Enter" to continue.

To clear a specific cache type, you can specify it in the cache:clear command. For example to clear the render cache:

```screen
drush cache:clear render
```

### Additional resources

[*Drupal.org* community documentation page "Clearing or rebuilding Drupal’s cache"](https://www.drupal.org/docs/7/administering-drupal-7-site/clearing-or-rebuilding-drupals-cache)

**Attributions**

Adapted and edited by [Joe Shindelar](https://www.drupal.org/u/eojthebrave) and [Jack Haas](https://www.drupal.org/u/jerseycheese) from ["Clearing or rebuilding Drupal’s cache"](https://www.drupal.org/docs/7/administering-drupal-7-site/clearing-or-rebuilding-drupals-cache), copyright 2000-2026 by the individual contributors to the [Drupal Community Documentation](https://www.drupal.org/documentation).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[12.1. Concept: Cache](/tutorial/user-guide/prevent-cache?p=2398)

Next
[12.3. Concept: Data Backups](/tutorial/user-guide/prevent-backups?p=2398)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
---
title: "12.1. Concept: Cache"
url: "https://drupalize.me/tutorial/user-guide/prevent-cache?p=2398"
guide: "[[acquia-certified-drupal-front-end-specialist-exam]]"
---

# 12.1. Concept: Cache

## Content

### Prerequisite knowledge

[Section 1.1, “Concept: Drupal as a Content Management System”](https://drupalize.me/tutorial/user-guide/understanding-drupal "1.1. Concept: Drupal as a Content Management System")

### What is the page cache?

The software that runs your site, on each page request, must perform calculations and retrieve data from the database, in order to compose the page that is sent to the web browser or other application that is accessing the site. These calculations take time, which can mean that your page load time is longer than would be desirable.

There are several ways that page load time can be sped up, including installing software on the server. The system includes the core Internal Page Cache and Dynamic Page Cache modules, which do not require any additional server software; they use a *database cache* mechanism to speed up your site. The way these modules work is that during page calculations, intermediate results and the final page output are stored in a special database area (known as the *cache*). Then the next time a compatible request is made, intermediate or final results, as appropriate, can be retrieved and used rather than redoing the entire calculation. In addition, when content or data that affects a particular calculation is updated, the affected cached data is removed from the cache, forcing that part of the calculation to be redone the next time it is needed.

These caching modules normally work reasonably well, and offer at least some speed-up for most sites. However, sometimes the page cache can have problems, such as:

- Corrupted data in the cache, leading to garbled or incorrect page output
- Old data remaining in the cache too long, leading to outdated page output
- Insufficient caching, leading to slow page loads

### What other data is cached?

Independent of whether the two page cache modules are installed on your site, the software that your site runs will still cache the output of many internal calculations. The core systems that cache data include:

- The theme system caches information in the database cache about which template files are used to render various types of data. If you are developing a new theme and add a new template file, you’ll need to clear this cache to have your theme file recognized.
- CSS and JavaScript files can optionally be optimized and compressed (depending on your site settings). If so, the compressed versions are stored in the file system so that they don’t have to be re-optimized too often. If you are developing a module or theme, you may need to either turn off or clear this file cache to have changes to CSS or JavaScript files be recognized.
- The system locates certain low-level PHP functions and classes, such as *hook implementations* and *plugin classes*, from your installed modules and stores information about which module has which functionality. If you are developing a new module or adding features to an existing module, you may need to clear this cache to have your new features be recognized.

### Related topics

If you have problems with your site, the first thing to try to fix it is usually to clear the cache. See [Section 12.2, “Clearing the Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache-clear "12.2. Clearing the Cache") for more information.

### Additional resources

Learn about additional caching and performance optimization methods in the [*Drupal.org* community documentation page "Caching overview"](https://www.drupal.org/docs/7/managing-site-performance-and-scalability/caching-to-improve-performance/caching-overview).

**Attributions**

Written by [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Next
[12.2. Clearing the Cache](/tutorial/user-guide/prevent-cache-clear?p=2398)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
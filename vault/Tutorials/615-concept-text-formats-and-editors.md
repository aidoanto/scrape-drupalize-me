---
title: "6.15. Concept: Text Formats and Editors"
url: "https://drupalize.me/tutorial/user-guide/structure-text-formats?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 6.15. Concept: Text Formats and Editors

## Content

### What are text formats and filters?

*Text formats* change how HTML tags and other text are processed and displayed on your site. Text formats are composed of a series of *filters*, each of which transforms text. When users create content, a text format is associated with the content, and the full, original text is stored in the database. The content is then passed through the filters in the text format before it becomes output on the site.

The core Filter module provides text format functionality, and the core Standard installation profile sets up *Basic HTML*, *Restricted HTML*, and *Full HTML* text formats. Each text format has an associated permission, so that you can allow only trusted users to use permissive text formats. This restricts untrusted users to text formats like *Basic HTML*, which filters out dangerous HTML tags.

### What are the editors associated with text formats?

Each text format can be associated with an editor, such as a visual WYSIWYG (What You See Is What You Get) HTML editor. The core Text Editor module provides the ability to associate editors with text formats, and to configure the editors (such as adding and removing buttons from their toolbars). The core CKEditor module provides the industry-standard editor known as CKEditor, so that it can be used to edit HTML content on your site.

### What is cross-site scripting?

Cross-site scripting (XSS) is a security vulnerability typically found in websites. In a site that is not well protected, malicious users can enter script into web pages that are viewed by other users (for example, in a comment or in the body of a page). A cross-site scripting vulnerability may be used by attackers to login as another user. It is important to configure the text formats of your website to prevent such abuse.

### Related topics

[Section 13.3, “Concept: Security and Regular Updates”](https://drupalize.me/tutorial/user-guide/security-concept "13.3. Concept: Security and Regular Updates")

### Additional resources

- [*Drupal.org* community documentation page "Filter module overview"](https://www.drupal.org/docs/core-modules-and-themes/core-modules/filter-module/filter-module-overview)
- [Wikipedia page "Cross-site scripting"](https://en.wikipedia.org/wiki/Cross-site_scripting)

**Attributions**

Written and edited by [Boris Doesborg](https://www.drupal.org/u/batigolix) and [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.14. Concept: Responsive Image Styles](/tutorial/user-guide/structure-image-responsive?p=2412)

Next
[6.16. Configuring Text Formats and Editors](/tutorial/user-guide/structure-text-format-config?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
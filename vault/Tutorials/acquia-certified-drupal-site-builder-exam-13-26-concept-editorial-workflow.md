---
title: "2.6. Concept: Editorial Workflow"
url: "https://drupalize.me/tutorial/user-guide/planning-workflow?p=2341"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 13
---

# 2.6. Concept: Editorial Workflow

## Content

### Prerequisite knowledge

- [Section 1.1, “Concept: Drupal as a Content Management System”](https://drupalize.me/tutorial/user-guide/understanding-drupal "1.1. Concept: Drupal as a Content Management System")
- [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields")

### What is an editorial workflow?

An *editorial workflow* is the process organizations follow to create, review, edit, and publish content. Multiple people in different roles in the organization can be part of the process. For example, content creators could collect information and write content; editors could review, edit, ask for changes, and publish the content once it’s ready to be shared with the audience. Later on, content revisions could go through a simple process for small changes, or a more complex process with reviews for larger changes.

### What tools are available for managing workflows?

Published/Unpublished status
:   The Content item entity type supports marking each content item as either Published or Unpublished. Viewing permissions are separate for published and unpublished content; for example, all site visitors might be able to see published content items, while only content creators and editors can see unpublished content items.

Revision tracking
:   Some content entity types support revision tracking, meaning that as content is revised, the software stores the older revisions, so that they can be compared or reverted.

Workflows
:   The core Workflows module lets you define workflow states and transitions, beyond just having content be published or unpublished. The companion core Content Moderation module lets you assign permissions and roles to the workflow transitions. Both can be used with both Content item and Custom block entity types.

Block placement
:   The Custom block content entity lets you create a custom block and edit it, but only make it visible on the site once it is ready.

### Related topics

- [Section 5.2, “Creating a Content Item”](https://drupalize.me/tutorial/user-guide/content-create "5.2. Creating a Content Item")
- [Section 5.3, “Editing a Content Item”](https://drupalize.me/tutorial/user-guide/content-edit "5.3. Editing a Content Item")
- [Section 8.2, “Creating A Custom Block”](https://drupalize.me/tutorial/user-guide/block-create-custom "8.2. Creating A Custom Block")
- [Section 8.3, “Placing a Block in a Region”](https://drupalize.me/tutorial/user-guide/block-place "8.3. Placing a Block in a Region")

**Attributions**

Written and edited by [Diána Lakatos](https://www.drupal.org/u/dianalakatos) at [Pronovix](https://pronovix.com//), [Grant Dunham](https://www.drupal.org/u/gdunham), and [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[2.5. Planning your Content Structure](/tutorial/user-guide/planning-structure?p=2341)

Next
[2.7. Concept: User Interface, Configuration, and Content translation](/tutorial/user-guide/language-concept?p=2341)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
---
title: "11.7. Concept: Development Sites"
url: "https://drupalize.me/tutorial/user-guide/install-dev-sites?p=2357"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 11.7. Concept: Development Sites

## Content

### What are Development Sites?

Development Sites are different copies of the same site used for developing, updating, and testing a site without risking the integrity of the live site.

An example deployment workflow for site building will usually include the sites mentioned below:

Local environment
:   The development process starts with developers working on new features, bug fixes, theming, and configuration in their local environment. The recommended tool for setting up a local environment is DDEV. See [Section 3.5, “Setting Up an Environment with DDEV”](https://drupalize.me/tutorial/user-guide/install-ddev "3.5. Setting Up an Environment with DDEV").

Development site
:   Developers push the changes they’ve been working on to the development site. For a team of more than one developer, version control is usually used. Git is a version control system that tracks your files for any changes. You can then commit those changes to a repository. Using Git allows team members to work on the same site without overriding each other’s work. It also makes it possible to easily roll back to previous stages of the development.

Staging site
:   The staging site can be used for testing, or presenting the changes to the client for approval. QA (Quality Assurance) and UAT (User Acceptance Testing) are most often carried out on the staging site. It is recommended to have live content on both the development and staging sites, so that you can test how the new features will work with the existing content.

Production site
:   The live site on the web available to visitors. It contains new features that have been proven safe to go live.

Based on the project’s size, scope, requirements, or stakeholders, stages from the above workflow can be removed, or additional stages can be added. For example, a testing site before staging can be added to separate testing and user acceptance processes.

### Related topics

- [Section 11.8, “Making a Development Site”](https://drupalize.me/tutorial/user-guide/install-dev-making "11.8. Making a Development Site")
- [Section 3.5, “Setting Up an Environment with DDEV”](https://drupalize.me/tutorial/user-guide/install-ddev "3.5. Setting Up an Environment with DDEV")
- [Section 2.6, “Concept: Editorial Workflow”](https://drupalize.me/tutorial/user-guide/planning-workflow "2.6. Concept: Editorial Workflow")
- [Section 11.11, “Managing File and Configuration Revisions with Git”](https://drupalize.me/tutorial/user-guide/extend-git "11.11. Managing File and Configuration Revisions with Git")

**Attributions**

Written and edited by [Diána Lakatos](https://www.drupal.org/u/dianalakatos), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com), and [Joe Shindelar](https://www.drupal.org/u/eojthebrave) at [Drupalize.Me](https://drupalize.me).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[11.6. Manually Installing Module or Theme Files](/tutorial/user-guide/extend-manual-install?p=2357)

Next
[11.8. Making a Development Site](/tutorial/user-guide/install-dev-making?p=2357)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
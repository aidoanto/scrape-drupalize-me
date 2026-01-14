---
title: "7.5. Assigning Permissions to a Role"
url: "https://drupalize.me/tutorial/user-guide/user-permissions?p=2441"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 44
---

# 7.5. Assigning Permissions to a Role

## Content

### Goal

Change the permissions for the Vendor role so that users can create, edit, and delete Recipe and Vendor content, format the content, and contact each other.

### Prerequisite knowledge

- [Section 7.1, “Concept: Users, Roles, and Permissions”](https://drupalize.me/tutorial/user-guide/user-concept "7.1. Concept: Users, Roles, and Permissions")

### Site prerequisites

The Vendor role must exist on your site. See [Section 7.3, “Creating a Role”](https://drupalize.me/tutorial/user-guide/user-new-role "7.3. Creating a Role").

### Steps

Sprout Video

1. In the *Manage* administrative menu, navigate to *People* > *Roles* (*admin/people/roles*). The *Roles* page appears.
2. Click *Edit permissions* in the dropdown for the Vendor role. The *Edit role* page appears where you can see all the available actions for the website such as, for example, *Post comments* or *Administer blocks*. The available permissions depend on the modules that are installed in the site. Note: Some permissions may have security implications. Be cautious while assigning permissions to roles.
3. Check the boxes for the following permissions, listed by module:

   | Module | Permission |
   | --- | --- |
   | Contact | Use users' personal contact forms |
   | Filter | Use the Restricted HTML text format |
   | Node | Recipe: Create new content |
   | Node | Recipe: Edit own content |
   | Node | Recipe: Delete own content |
   | Node | Vendor: Edit own content |

   Image

   ![Granting users with the Vendor role the rights to create, delete and edit Recipes](../assets/images/user-permissions-check-permissions.png)
4. Click *Save permissions*. You will get a message saying your changes have been saved.

   Image

   ![Confirmation message after updating permissions](../assets/images/user-permissions-save-permissions.png)

### Expand your understanding

- Log in as one of the new users you created in [Section 7.4, “Creating a User Account”](https://drupalize.me/tutorial/user-guide/user-new-user "7.4. Creating a User Account"). Verify whether you have the correct permissions.
- [Section 7.6, “Changing a User’s Roles”](https://drupalize.me/tutorial/user-guide/user-roles "7.6. Changing a User’s Roles")

### Related concepts

[Section 7.2, “Concept: The User 1 Account”](https://drupalize.me/tutorial/user-guide/user-admin-account "7.2. Concept: The User 1 Account")

### Additional resources

[*Drupal.org* community documentation page "Managing Users"](https://www.drupal.org/docs/7/managing-users)

**Attributions**

Adapted and edited by [Boris Doesborg](https://www.drupal.org/u/batigolix), [Brian Emery](https://www.drupal.org/u/bemery987), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com), and [Joe Shindelar](https://www.drupal.org/u/eojthebrave) at [Drupalize.Me](https://drupalize.me), from ["User Roles"](https://www.drupal.org/docs/7/managing-users/user-roles), copyright 2000-2026 by the individual contributors to the [Drupal Community Documentation](https://www.drupal.org/documentation).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[7.4. Creating a User Account](/tutorial/user-guide/user-new-user?p=2441)

Next
[7.6. Changing a User’s Roles](/tutorial/user-guide/user-roles?p=2441)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
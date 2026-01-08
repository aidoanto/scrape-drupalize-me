---
title: "7.1. Concept: Users, Roles, and Permissions"
url: "https://drupalize.me/tutorial/user-guide/user-concept?p=2441"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
---

# 7.1. Concept: Users, Roles, and Permissions

## Content

### What are Users?

Anyone who visits your website is a *user*, including you. There are three groups of users:

- Users who are not logged in, or *anonymous users*
- Users who are logged in, or *authenticated users*
- The administrative user account that was automatically created when you installed your site, or User 1. See [Section 7.2, “Concept: The User 1 Account”](https://drupalize.me/tutorial/user-guide/user-admin-account "7.2. Concept: The User 1 Account").

### What are Permissions?

The ability to do actions on your site (including viewing content, editing content, and changing configuration) is governed by *permissions*. Each permission has a name (such as *View published content*) and covers one action or a small subset of actions. A user must be granted a permission in order to do the corresponding action on the site; permissions are defined by the modules that provide the actions.

### What are Roles?

Rather than assigning individual permissions directly to each user, permissions are grouped into *roles*. You can define one or more roles on your site, and then grant permissions to each role. The permissions granted to authenticated and anonymous users are contained in the *Authenticated user* and *Anonymous user* roles, and depending on the installation profile you used when you installed your site, there may also be an *Administrator* role that is automatically assigned all permissions on your site.

Each user account on your site is automatically given the *Authenticated user* role, and may optionally be assigned one or more additional roles. When you assign a role to a user account, the user will have all the permissions of the role when logged in.

It is a good practice to make several roles on your site. In the farmers market site example, you might want the following roles:

- A Vendor role that allows vendors to edit their own vendor listing page
- A Content editor role for editing the general farmers market pages
- A User manager role for managing the vendor accounts
- The *Administrator* role that was installed with your site, for expert users to manage the site configuration

### Related topics

- [Section 7.3, “Creating a Role”](https://drupalize.me/tutorial/user-guide/user-new-role "7.3. Creating a Role")
- [Section 7.5, “Assigning Permissions to a Role”](https://drupalize.me/tutorial/user-guide/user-permissions "7.5. Assigning Permissions to a Role")
- [Section 7.6, “Changing a User’s Roles”](https://drupalize.me/tutorial/user-guide/user-roles "7.6. Changing a User’s Roles")
- [Section 7.4, “Creating a User Account”](https://drupalize.me/tutorial/user-guide/user-new-user "7.4. Creating a User Account")
- [Section 7.2, “Concept: The User 1 Account”](https://drupalize.me/tutorial/user-guide/user-admin-account "7.2. Concept: The User 1 Account")
- [Section 7.7, “Assigning Authors to Content”](https://drupalize.me/tutorial/user-guide/user-content "7.7. Assigning Authors to Content")

### Additional resources

- [*Drupal.org* community documentation page "Managing Users"](https://www.drupal.org/docs/7/managing-users)
- [*Drupal.org* community documentation page "User Roles"](https://www.drupal.org/docs/7/managing-users/user-roles)

**Attributions**

Adapted by [Mark LaCroix](https://www.drupal.org/u/mark-lacroix), [Boris Doesborg](https://www.drupal.org/u/batigolix), and [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon) from ["User Roles"](https://www.drupal.org/docs/7/managing-users/user-roles), copyright 2000-2026 by the individual contributors to the [Drupal Community Documentation](https://www.drupal.org/documentation).

Was this helpful?

Yes

No

Any additional feedback?

Next
[7.2. Concept: The User 1 Account](/tutorial/user-guide/user-admin-account?p=2441)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
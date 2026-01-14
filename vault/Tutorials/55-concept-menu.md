---
title: "5.5. Concept: Menu"
url: "https://drupalize.me/tutorial/user-guide/menu-concept?p=2350"
guide: "[[acquia-certified-drupal-site-builder-exam]]"
order: 28
---

# 5.5. Concept: Menu

## Content

### What is a menu?

Menus are a collection of links used to navigate a website. The core Menu UI module provides an interface to control and customize the menu system. Menus are primarily displayed as a hierarchical list of links. By default, new menu links are placed inside a built-in menu labeled *Main navigation*, but administrators can also create custom menus.

The core Standard installation profile contains five menus:

Main navigation
:   Links to sections intended for site visitors. They are usually created by site administrators.

Administration
:   Links to administrative tasks. This menu mainly contains links supplied by modules on your site.

User account menu
:   Links to tasks associated with the user account such as *My account* and *Log out*.

Footer
:   Links to important pages within the site intended for the footer. They are usually created by site administrators.

Tools
:   Links to tasks necessary for site visitors. Some modules feature their links here.

You can customize menus in the following ways, using the menu administration functionality:

- Creating new custom menus.
- Adding new menu links.
- Reordering menu links by setting their "weight" or by dragging them into place.
- Renaming menu links (link title).
- Changing the link description (the tooltip that appears when you mouse over a menu link).
- Moving a menu link into a different menu by editing its *Parent link* property.

A menu link will only be shown to a visitor if they have the rights to view the page it links to. For example, the admin menu link is not shown to visitors who are not logged in.

### Related topics

- [Section 5.6, “Adding a Page to the Navigation”](https://drupalize.me/tutorial/user-guide/menu-link-from-content "5.6. Adding a Page to the Navigation")
- [Section 5.7, “Changing the Order of Navigation”](https://drupalize.me/tutorial/user-guide/menu-reorder "5.7. Changing the Order of Navigation")
- To display a menu, you will need to place the block that corresponds to the menu in a region of your theme; see [Section 8.1, “Concept: Blocks”](https://drupalize.me/tutorial/user-guide/block-concept "8.1. Concept: Blocks"), [Section 2.1, “Concept: Regions in a Theme”](https://drupalize.me/tutorial/user-guide/block-regions "2.1. Concept: Regions in a Theme"), and [Section 8.3, “Placing a Block in a Region”](https://drupalize.me/tutorial/user-guide/block-place "8.3. Placing a Block in a Region"). The core Standard installation profile places all of the menus it defines except Administration in regions of the core Bartik theme. The core Toolbar module, which is installed by the core Standard installation profile, displays the Administration menu; it is also displayed by the contributed Admin Toolbar module.

**Attributions**

Written and edited by [Ajay Viswambharan](https://www.drupal.org/u/ajayvi), [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com), [Jennifer Hodgdon](https://www.drupal.org/u/jhodgdon) and [Bill Seremetis](https://www.drupal.org/u/bserem).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[5.4. Designating a Front Page for your Site](/tutorial/user-guide/menu-home?p=2350)

Next
[5.6. Adding a Page to the Navigation](/tutorial/user-guide/menu-link-from-content?p=2350)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
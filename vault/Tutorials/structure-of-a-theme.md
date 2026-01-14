---
title: "Structure of a Theme"
url: "https://drupalize.me/tutorial/structure-theme?p=3267"
guide: "[[frontend-theming]]"
order: 35
---

# Structure of a Theme

## Content

Each theme is a collection of files that define a presentation layer for Drupal. While only a *THEMENAME.info.yml* file is required, most themes will contain other files as well. Some are Drupal-specific, and need to follow a strict naming convention and be placed in the appropriate place for Drupal to find them. Others are standard front-end web assets like CSS, JavaScript, and image files that can be placed anywhere within the theme's code.

In this tutorial we'll learn about:

- The various types of files you can expect to find in a theme directory
- Where in the Drupal code base your theme directory should live
- Keeping the directory and all the files within organized

By the end of this tutorial you should be able to explain where a Drupal theme should be placed in a project's code base, and the types of files one can expect to find in a theme.

## Goal

Explain the different types of files that make up a Drupal theme and where they are located in a project's code base.

## Prerequisites

- [What Is a Theme?](https://drupalize.me/tutorial/what-theme)

Sprout Video

## Where should your themes go so Drupal can find them?

Each theme is contained within a single directory. The directory name should match the theme's unique name. If your theme is named *icecream*, your theme's code would all lives within the directory *icecream/*. The name must be all lowercase, start with a letter, and use an underscore (\_) instead of spaces.

Themes that you develop yourself, or any that you download from Drupal.org should be placed in the *themes/* folder in the root of your Drupal project. Additionally, we recommend further sub-dividing the *themes/* folder into *themes/contrib/* for all themes downloaded from drupal.org, and *themes/custom/* for your own custom themes. In a multi-site install themes can also optionally be installed in *sites/\*/themes/*, where Drupal will also locate them.

Placing your custom themes in the root *themes/* directory instead of the *core/themes/* directory ensures that when you need to update Drupal core you can replace the contents of the *core/* directory without worrying about losing any of your personal additions.

Themes in Drupal are located in any of the following directories:

```
Drupal root
├── core
│   └── themes
│       ├── claro
│       ├── engines
│       ├── olivero
│       ├── stable9
│       ├── stark
│       └── starterkit_theme
├── sites
│   └── *
│       └── themes
│           └── my_custom_theme
└── themes
    └── contrib
        └── zen        
    └── custom
        └── icecream
```

*Note:* You can place custom or contributed themes directly in *DRUPALROOT/themes* as well. As outlined in the directory tree above, you can also further organize */themes* by creating a */themes/contrib* directory for contributed themes and */themes/custom* directory for custom themes and Drupal will recognize themes in those sub-directories. Usually a project will only use 1 or 2 themes (a base theme and a custom theme, for example), so it's not usually especially helpful to create this extra layer of hierarchy and organization in your *themes* directory. But you'll see examples of both theme organization schemes in our tutorials. (On the other hand, separating modules into *contrib* and *custom* is highly useful, one reason being because of the number of modules a site may install.)

## What kind of files should you expect to find in a theme?

A theme is made up of some combination of the following file types. The number, and existence of any of these files will vary depending on the specifics of the theme.

We use **THEMENAME** to represent the unique name/ID of your theme and use *icecream* as an example machine name for **THEMENAME**.

### Info file (*THEMENAME.info.yml*)

Defines required metadata for a theme and provides additional optional settings used by Drupal's theme layer.

This is the only required file for a theme. The name of this file determines the value of **THEMENAME**.

Example: *themes/icecream/icecream.info.yml*

Learn more about [creating an *.info.yml* file](https://drupalize.me/tutorial/describe-your-theme-info-file).

### Theme logic file (*THEMENAME.theme*)

A PHP file that contains conditional logic, and handles preprocessing of variables before they are output via template files.

Example: *themes/icecream/icecream.theme*

Learn more about [*THEMENAME.theme* files](https://drupalize.me/tutorial/add-logic-themenametheme).

### Template files (*templates/\*.html.twig*)

Template files, written using [Twig](https://twig.symfony.com/) and HTML, provide markup and basic presentation logic. Template files in a theme generally follow a specific naming convention and are used to override the default markup output by Drupal. Template files are **required** to be placed within the *templates/* subdirectory and may be organized into any number of subdirectories from there.

Examples:

- *themes/icecream/templates/node.html.twig*
- *themes/icecream/templates/layout/page--about.html.twig*

Learn more about [overriding template files](https://drupalize.me/tutorial/override-template-file).

### Libraries file (*THEMENAME.libraries.yml*)

Define CSS and JavaScript libraries that can be loaded by your theme. All CSS and JavaScript should be added to the page via [an asset library](https://drupalize.me/tutorial/what-are-asset-libraries).

Example: *themes/icecream/icecream.libraries.yml*

### Breakpoints file (*THEMENAME.breakpoints.yml*)

Defines the responsive design breakpoints used by your theme for Drupal.

Example: *themes/icecream/icecream.breakpoints.yml*

Learn more about the [breakpoints file in Drupal](https://drupalize.me/tutorial/what-breakpoint-yaml-file).

### Theme settings (*config/install/THEMENAME.settings.yml*)

Some themes may provide default configuration or theme settings. To create new default settings, make the changes via the Appearance admin UI in your theme then export your configuration. Move the new *THEMENAME.settings.yml* to your theme's *config/install* directory.

### Theme settings form alterations (*theme-settings.php*)

When you add custom theme settings, you can alter the system theme settings form in a *theme-settings.php* file in the root of your theme. See [Custom Theme Settings](https://drupalize.me/tutorial/customize-theme-settings) to learn more.

### CSS, JS, and image files

Any CSS, JavaScript and image assets that your theme uses. These are not Drupal-specific, though Drupal does define some conventions for best practices regarding use. In most cases it's a good idea to create a subdirectory for *css/*, *js/* and *images/*. You can further organize these directories in whatever way makes sense to you.

Example: *themes/icecream/css/layout.css*

### Post updates (*THEMENAME.post\_update.php*)

Modules and [now themes support post updates](https://www.drupal.org/node/3259199). You may have changes to dependencies in the *THEMENAME.info.yml* or theme settings configuration that need to be applied after a theme has been installed. These type of updates are called *post updates*. They are functions that implement [function hook\_post\_update\_NAME](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Extension%21module.api.php/function/hook_post_update_NAME/). For themes, post-updates should go in a file in the root of your theme named *THEMENAME.post\_update.php*.

### Automated tests

Automated tests for a theme should go in the themes *tests* directory.

### Default configuration and schema

Just like a module, a theme's default configuration should go in its *config/install* or *config/optional* directories, and the configuration schema in its *config/schema* directory.

## Theme directory structure

A single theme directory for a complete theme will contain a some or all of these files. As an example, take a look at how the files within the Olivero theme are organized:

```
/core/themes/olivero
├── config
│   ├── install
│   │   ├── core.date_format.olivero_medium.yml
│   │   └── olivero.settings.yml
│   ├── optional
│   │   ├── block.block.olivero_account_menu.yml
...
│   └── schema
│       └── olivero.schema.yml
├── css
│   ├── base
│   │   ├── base.css
...
│   ├── components
│   │   ├── action-links.css
...
│   │   ├── navigation
│   │   │   ├── menu-sidebar.css
...
│   ├── layout
│   │   ├── grid.css
...
│   └── theme
│       ├── filter.theme.css
...
├── favicon.ico
├── fonts
├── images
├── js
├── logo.svg
├── olivero.breakpoints.yml
├── olivero.info.yml
├── olivero.libraries.yml
├── olivero.post_update.php
├── olivero.theme
├── screenshot.png
├── src
│   └── OliveroPreRender.php
├── templates
│   ├── block
│   │   ├── block--page-title-block.html.twig
...
│   ├── content
│   │   ├── book-node-export-html.html.twig
...
│   ├── dataset
│   │   ├── forum-list.html.twig
...
│   ├── field
│   │   ├── field--comment-body.html.twig
...
│   ├── filter
│   │   ├── filter-guidelines.html.twig
│   ├── form
│   │   ├── details.html.twig
...
│   ├── includes
│   │   ├── get-started.html.twig
│   ├── layout
│   │   ├── html.html.twig
│   │   ├── page.html.twig
│   │   ├── region--breadcrumb.html.twig
...
│   │   └── region.html.twig
...
│   ├── misc
│   │   ├── feed-icon.html.twig
│   │   └── status-messages.html.twig
│   ├── navigation
│   │   ├── book-all-books-block.html.twig
...
│   ├── user
│   │   ├── user--compact.html.twig
...
│   └── views
│       ├── views-mini-pager.html.twig
...
├── tests
│   └── src
│       ├── Functional
│       │   └── Update
│       │       └── OliveroPostUpdateTest.php
│       └── Unit
│           └── OliveroHexToHslTest.php
└── theme-settings.php
```

One of the best ways to learn more about how to keep a theme organized is to look at some examples from popular contributed themes. You can view the [list of themes sorted by most installed](https://www.drupal.org/project/project_theme), browse the source code for the top few, and borrow any organizational schemes that resonate with you.

## Use Starterkit to start a new theme

If you're starting a new theme from scratch the Drupal core Starterkit utility can help setup the necessary structure and files. Learn more in [Start A New Theme with Starterkit](https://drupalize.me/tutorial/start-new-theme-starterkit).

## Recap

In this tutorial we learned that a Drupal theme is made up of a combination of Drupal-specific files, mostly YAML files and Twig template files, that follow specific naming conventions. A theme also typically contains non-Drupal assets like images and CSS files that can be placed anywhere within your theme's code. All of these files are placed into a directory, and this directory of files is called a *theme*. In order for Drupal to discover a theme it needs to exist in one a few locations that Drupal knows to look. The most common of which is the root */themes* directory.

## Further your understanding

- Themes are made up of different types of files; name a few Drupal-specific file types.
- What is the one file required of every theme?
- What is the benefit of placing your custom theme into the */themes/custom* directory instead of just */themes*?
- Other than */themes*, where does Drupal look for non-core themes?

## Additional resources

- [Theme folder structure](https://www.drupal.org/node/2349803) (Drupal.org)
- Change record: [Theme settings default values can not be set in a theme's info.yml files](https://www.drupal.org/node/2382645) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Start a New Theme with Starterkit](/tutorial/start-new-theme-starterkit?p=3267)

Clear History

Ask Drupalize.Me AI

close
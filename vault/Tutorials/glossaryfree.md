---
title: "Glossaryfree"
url: "https://drupalize.me/tutorial/user-guide/glossary?p=2335"
guide: "[[drupal-user-guide]]"
---

# Glossaryfree

## Content

# Glossary

Ajax
:   A web technology used to exchange data with a server to dynamically update parts of a web page (for example, forms) without needing entire page reloads.

Alias
:   A user-friendly name to replace the internal [path](https://drupalize.me/tutorial/user-guide/glossary#glossary-path) that the system assigns to a [URL](https://drupalize.me/tutorial/user-guide/glossary#glossary-url) on the site. For example, you might assign an alias of */about* to the About page on your site, to replace the internal path */node/5*. This would give the page a URL of *<http://example.com/about>* instead of *<http://example.com/node/5>*. See [Section 5.1, “Concept: Paths, Aliases, and URLs”](https://drupalize.me/tutorial/user-guide/content-paths "5.1. Concept: Paths, Aliases, and URLs") for more information.

Anonymous
:   A person ([user](https://drupalize.me/tutorial/user-guide/glossary#glossary-user)) interacting with the site who is not logged in. See [Section 7.1, “Concept: Users, Roles, and Permissions”](https://drupalize.me/tutorial/user-guide/user-concept "7.1. Concept: Users, Roles, and Permissions") for more information.

Authenticated
:   A person ([user](https://drupalize.me/tutorial/user-guide/glossary#glossary-user)) interacting with the site who is logged in. See [Section 7.1, “Concept: Users, Roles, and Permissions”](https://drupalize.me/tutorial/user-guide/user-concept "7.1. Concept: Users, Roles, and Permissions") for more information.

Block
:   A chunk of [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) (text, images, links, etc.) that can be displayed on a page of a site. Blocks are displayed in [regions](https://drupalize.me/tutorial/user-guide/glossary#glossary-region). See [Section 8.1, “Concept: Blocks”](https://drupalize.me/tutorial/user-guide/block-concept "8.1. Concept: Blocks") for more information.

Breakpoint
:   Breakpoints are used to separate the height or width of browser screens, printers, and other media output types into steps. A [responsive](https://drupalize.me/tutorial/user-guide/glossary#glossary-responsive) site adjusts its presentation at these breakpoints. See [Section 6.14, “Concept: Responsive Image Styles”](https://drupalize.me/tutorial/user-guide/structure-image-responsive "6.14. Concept: Responsive Image Styles") for more information.

Bundle
:   Synonym for [Entity subtype](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-subtype).

Cache
:   The site’s internal cache stores the output of time-consuming calculations, such as computing output for an HTML page request, and then retrieves them instead of recalculating the next time they are needed. External caching systems can also be used on the web server to speed up a site’s response. See [Section 12.1, “Concept: Cache”](https://drupalize.me/tutorial/user-guide/prevent-cache "12.1. Concept: Cache") for more information on the internal cache.

Coding standards
:   Coding standards are the rules for programmers that define best practices, formatting, and various other rules, so that everyone uses the same conventions and has the same expectations when they see code. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools") for more information.

Composer
:   The PHP dependency manager used by Drupal, [Drush](https://drupalize.me/tutorial/user-guide/glossary#glossary-drush), the Symfony framework and others. It is the preferred means of installing Drupal projects. See [Section 3.6, “Using Composer to Download and Update Files”](https://drupalize.me/tutorial/user-guide/install-composer "3.6. Using Composer to Download and Update Files") for more information.

CMS
:   Acronym for [Content Management System](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-management-system).

Configuration
:   Information about your site that is not [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content), and is meant to be more permanent than [state](https://drupalize.me/tutorial/user-guide/glossary#glossary-state) information, such as the name of your site, the [content types](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-type) and [views](https://drupalize.me/tutorial/user-guide/glossary#glossary-view) you have defined, etc. See [Section 1.5, “Concept: Types of Data”](https://drupalize.me/tutorial/user-guide/understanding-data "1.5. Concept: Types of Data") for more information.

Content
:   Information meant to be displayed on your site, such as text, images, downloads, etc. See also [Configuration](https://drupalize.me/tutorial/user-guide/glossary#glossary-configuration) and [State](https://drupalize.me/tutorial/user-guide/glossary#glossary-state). See [Section 1.5, “Concept: Types of Data”](https://drupalize.me/tutorial/user-guide/understanding-data "1.5. Concept: Types of Data") for more information.

Content item
:   An item of [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) that is typically meant to be displayed as the main content of a page on your site. This is an [entity type](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-type). See [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields") for more information.

Content Management System (CMS)
:   A collection of tools designed to allow the creation, modification, organization, search, retrieval and removal of information on a website. See [Section 1.1, “Concept: Drupal as a Content Management System”](https://drupalize.me/tutorial/user-guide/understanding-drupal "1.1. Concept: Drupal as a Content Management System") for more information.

Content type
:   An [entity subtype](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-subtype) for the [content item](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-item) [entity type](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-type). Each content type is used for some particular purpose on the site, and each has its own fields. For example, a site for a farmers market might have a content type for simple pages, and another for a vendor listing page. See [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields") for more information.

Contextual Filter (in a View)
:   Limits the data to be output in a [view](https://drupalize.me/tutorial/user-guide/glossary#glossary-view), based on the context of the view [display](https://drupalize.me/tutorial/user-guide/glossary#glossary-display), such as the full URL of the page. See [Section 9.2, “Concept: The Parts of a View”](https://drupalize.me/tutorial/user-guide/views-parts "9.2. Concept: The Parts of a View") for more information.

Contextual link
:   A link to an administrative page for editing or configuring a feature of the site, shown in the context where that feature is displayed. Example: a link to configure a [menu](https://drupalize.me/tutorial/user-guide/glossary#glossary-menu) that is shown when you hover your mouse over the menu. See [Section 4.1, “Concept: Administrative Overview”](https://drupalize.me/tutorial/user-guide/config-overview "4.1. Concept: Administrative Overview") for more information.

Contributed
:   [Modules](https://drupalize.me/tutorial/user-guide/glossary#glossary-module), [themes](https://drupalize.me/tutorial/user-guide/glossary#glossary-theme), and [distributions](https://drupalize.me/tutorial/user-guide/glossary#glossary-distribution) that are not part of the [Drupal core](https://drupalize.me/tutorial/user-guide/glossary#glossary-drupal-core) download, and that can be downloaded separately from the [*Drupal.org*](https://www.drupal.org) website.

Cron
:   On some operating systems, *cron* is a command scheduler application that executes commands or scripts periodically. Your site defines periodic tasks, also known as cron tasks, that need to be triggered either by an operating system cron scheduler, or internally. See [Section 13.1, “Concept: Cron”](https://drupalize.me/tutorial/user-guide/security-cron-concept "13.1. Concept: Cron") for more information.

Cross Site Scripting
:   Security vulnerability typically found in websites. In a site that is not well protected, malicious users can enter script into web pages that are viewed by other users. See [Section 6.15, “Concept: Text Formats and Editors”](https://drupalize.me/tutorial/user-guide/structure-text-formats "6.15. Concept: Text Formats and Editors") for more information.

Devel
:   Module that helps with development tasks such as debugging and inspecting code, analyzing database queries, and generating dummy content. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools") for more information.

Development site
:   Copy of the live website that is used for developing, updating, and testing the website. See [Section 11.7, “Concept: Development Sites”](https://drupalize.me/tutorial/user-guide/install-dev-sites "11.7. Concept: Development Sites") for more information.

Display (in a View)
:   Type of output of a [view](https://drupalize.me/tutorial/user-guide/glossary#glossary-view), for example a page, a [block](https://drupalize.me/tutorial/user-guide/glossary#glossary-block) or a feed. See [Section 9.2, “Concept: The Parts of a View”](https://drupalize.me/tutorial/user-guide/views-parts "9.2. Concept: The Parts of a View") for more information.

Distribution
:   A single download that provides a shortcut for setting up a specific type of site, such as a website for a club or for e-commerce. A distribution contains [Drupal core](https://drupalize.me/tutorial/user-guide/glossary#glossary-drupal-core), along with [contributed](https://drupalize.me/tutorial/user-guide/glossary#glossary-contributed) [modules](https://drupalize.me/tutorial/user-guide/glossary#glossary-module) and/or [themes](https://drupalize.me/tutorial/user-guide/glossary#glossary-theme); many distributions also pre-configure the site or even create sample content upon [installation](https://drupalize.me/tutorial/user-guide/glossary#glossary-installing). See [Section 1.4, “Concept: Distributions”](https://drupalize.me/tutorial/user-guide/understanding-distributions "1.4. Concept: Distributions") for more information.

Drupal Association
:   Non-profit organization dedicated to supporting the Drupal project and community. See [Section 1.6, “Concept: The Drupal Project”](https://drupalize.me/tutorial/user-guide/understanding-project "1.6. Concept: The Drupal Project") for more information.

Drupal core
:   The files, themes, profiles, and modules included with the standard project software download. See [Section 1.1, “Concept: Drupal as a Content Management System”](https://drupalize.me/tutorial/user-guide/understanding-drupal "1.1. Concept: Drupal as a Content Management System") for more information.

Drush
:   Command line shell and scripting interface for Drupal. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools") for more information.

Editorial Workflow
:   Process to create, review, edit, and publish content. Multiple people in different roles (for example content creators and editors) can be part of the process. See [Section 2.6, “Concept: Editorial Workflow”](https://drupalize.me/tutorial/user-guide/planning-workflow "2.6. Concept: Editorial Workflow") for more information.

Entity
:   An item of either [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) or [configuration](https://drupalize.me/tutorial/user-guide/glossary#glossary-configuration) data, although in common usage, the term often refers to content entities. Examples include [content items](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-item), custom [blocks](https://drupalize.me/tutorial/user-guide/glossary#glossary-block), [taxonomy terms](https://drupalize.me/tutorial/user-guide/glossary#glossary-taxonomy-term), and definitions of [content types](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-type); the first three are content entities, and the last is a configuration entity. See also [Entity type](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-type), [Entity subtype](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-subtype), and [Field](https://drupalize.me/tutorial/user-guide/glossary#glossary-field). See [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields") for more information.

Entity subtype
:   Within a [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) [entity type](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-type), a grouping of entities that share the same [fields](https://drupalize.me/tutorial/user-guide/glossary#glossary-field). For example, within the [content item](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-item) entity type, a farmers market site might have subtypes (known as [content types](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-type)) for static pages and vendor pages, each with its own group of fields. You may also see the term *bundle* used (especially in programmer documentation) as a synonym of entity subtype. See [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields") for more information.

Entity type
:   The overall type of an [entity](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity); in common usage, it is only applied to a [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) entity. Examples include [content types](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-type), [taxonomy terms](https://drupalize.me/tutorial/user-guide/glossary#glossary-taxonomy-term), and custom [blocks](https://drupalize.me/tutorial/user-guide/glossary#glossary-block). See [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields") for more information.

Field
:   Data of a certain type that is attached to a [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) [entity](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity). For instance, on a farmers market site’s vendor content type, you might have fields for an image, the vendor description, and a [taxonomy term](https://drupalize.me/tutorial/user-guide/glossary#glossary-taxonomy-term). See [Section 2.3, “Concept: Content Entities and Fields”](https://drupalize.me/tutorial/user-guide/planning-data-types "2.3. Concept: Content Entities and Fields") for more information.

Field bundle
:   Synonym for [Entity subtype](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-subtype).

Field formatter
:   [Configuration](https://drupalize.me/tutorial/user-guide/glossary#glossary-configuration) that defines how the data in a [field](https://drupalize.me/tutorial/user-guide/glossary#glossary-field) is displayed. For example, a text field could be displayed with a prefix and/or suffix, and it could have its HTML tags stripped out or limited. See also [View mode](https://drupalize.me/tutorial/user-guide/glossary#glossary-view-mode) and [Field widget](https://drupalize.me/tutorial/user-guide/glossary#glossary-field-widget). See [Section 6.10, “Concept: View Modes and Formatters”](https://drupalize.me/tutorial/user-guide/structure-view-modes "6.10. Concept: View Modes and Formatters") for more information.

Field widget
:   [Configuration](https://drupalize.me/tutorial/user-guide/glossary#glossary-configuration) that defines how someone can enter or edit data for a [field](https://drupalize.me/tutorial/user-guide/glossary#glossary-field) on a data entry form. For example, a text field could use a single-line or multi-line entry box, and there could be a setting for the size of the box. See also [Field formatter](https://drupalize.me/tutorial/user-guide/glossary#glossary-field-formatter). See [Section 6.8, “Concept: Forms and Widgets”](https://drupalize.me/tutorial/user-guide/structure-widgets "6.8. Concept: Forms and Widgets") for more information.

Filter (in a View)
:   Limits the data to be output in a [view](https://drupalize.me/tutorial/user-guide/glossary#glossary-view), based on criteria such as publication status, type of content, or field value. See [Section 9.2, “Concept: The Parts of a View”](https://drupalize.me/tutorial/user-guide/views-parts "9.2. Concept: The Parts of a View") for more information.

Formatter
:   See [Field formatter](https://drupalize.me/tutorial/user-guide/glossary#glossary-field-formatter).

FOSS
:   Acronym for *Free and Open Source Software*, meaning software that is developed by a community of people and released under a non-commercial license. See also [GPL](https://drupalize.me/tutorial/user-guide/glossary#glossary-gpl). See [Section 1.6, “Concept: The Drupal Project”](https://drupalize.me/tutorial/user-guide/understanding-project "1.6. Concept: The Drupal Project") for more information.

Git
:   [Version control system](https://drupalize.me/tutorial/user-guide/glossary#glossary-vcs) used by Drupal developers to coordinate their individual code changes. Git records everyone’s changes to a given project in a directory tree called a git [repository](https://drupalize.me/tutorial/user-guide/glossary#glossary-repository). See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools") for more information.

GPL
:   Acronym for the *GNU General Public License*, a non-commercial software license. All software downloaded from the [*Drupal.org*](https://www.drupal.org) website is licensed under the ["GNU General Public License, version 2"](http://www.gnu.org/licenses/old-licenses/gpl-2.0.html). See also [FOSS](https://drupalize.me/tutorial/user-guide/glossary#glossary-foss). See [Section 1.7, “Concept: Drupal Licensing”](https://drupalize.me/tutorial/user-guide/understanding-gpl "1.7. Concept: Drupal Licensing") for more information.

Image style
:   A set of processing steps that transform a base image into a new image; typical processing includes scaling and cropping. See [Section 6.12, “Concept: Image Styles”](https://drupalize.me/tutorial/user-guide/structure-image-styles "6.12. Concept: Image Styles") for more information.

Installing
:   Preparing Drupal core or any contributed theme or module for usage. In the case of Drupal core this means downloading the necessary files, creating the database, configuring and running the installation script. See [Section 3.4, “Concept: Methods for Downloading and Installing the Core Software”](https://drupalize.me/tutorial/user-guide/install-decide "3.4. Concept: Methods for Downloading and Installing the Core Software") for more information.

LAMP
:   Acronym for *Linux, Apache, MySQL, and PHP*: the software on the web server that the scripts commonly run on (although it can use other operating systems, web servers, and databases). See [Section 3.2, “Concept: Server Requirements”](https://drupalize.me/tutorial/user-guide/install-requirements "3.2. Concept: Server Requirements") for more information.

Log
:   A list of recorded events on the site, such as usage data, performance data, errors, warnings, and operational information. See [Section 12.4, “Concept: Log”](https://drupalize.me/tutorial/user-guide/prevent-log "12.4. Concept: Log") for more information.

Menu
:   A set of links used for navigation on a site, which may be arranged in a hierarchy. See [Section 5.5, “Concept: Menu”](https://drupalize.me/tutorial/user-guide/menu-concept "5.5. Concept: Menu") for more information.

Module
:   Software (usually PHP, JavaScript, and/or CSS) that extends site features and adds functionality. The Drupal project distinguishes between *[core](https://drupalize.me/tutorial/user-guide/glossary#glossary-drupal-core)* and *[contributed](https://drupalize.me/tutorial/user-guide/glossary#glossary-contributed)* modules. See [Section 1.2, “Concept: Modules”](https://drupalize.me/tutorial/user-guide/understanding-modules "1.2. Concept: Modules") for more information.

Path
:   The unique, last part of the internal [URL](https://drupalize.me/tutorial/user-guide/glossary#glossary-url) that the system assigns to a page on the site, which can be a visitor-facing page or an administrative page. For example, the internal URL for the About page on your site might be *<http://example.com/node/5>*, and in this case, the path is *node/5*. See also [Alias](https://drupalize.me/tutorial/user-guide/glossary#glossary-alias). See [Section 5.1, “Concept: Paths, Aliases, and URLs”](https://drupalize.me/tutorial/user-guide/content-paths "5.1. Concept: Paths, Aliases, and URLs") for more information.

Permission
:   The ability to perform some action on the site, such as editing a particular type of [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content), or viewing user profiles. See also [Role](https://drupalize.me/tutorial/user-guide/glossary#glossary-role). See [Section 7.1, “Concept: Users, Roles, and Permissions”](https://drupalize.me/tutorial/user-guide/user-concept "7.1. Concept: Users, Roles, and Permissions") for more information.

Reference field
:   A [field](https://drupalize.me/tutorial/user-guide/glossary#glossary-field) that represents a relationship between an [entity](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity) and one or more other entities, which may be the same [entity type](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-type) or a different type. For example, on a farmers market site, a recipe content item might have a reference field to the vendor (also a content item) that posted the recipe. [Taxonomy term](https://drupalize.me/tutorial/user-guide/glossary#glossary-taxonomy-term) fields are also reference fields. See [Section 6.4, “Concept: Reference Fields”](https://drupalize.me/tutorial/user-guide/structure-reference-fields "6.4. Concept: Reference Fields") for more information.

Region
:   A defined area of a page where [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) can be placed, such as the header, footer, main content area, left sidebar, etc. Regions are defined by [themes](https://drupalize.me/tutorial/user-guide/glossary#glossary-theme), and the content displayed in each region is contained in [blocks](https://drupalize.me/tutorial/user-guide/glossary#glossary-block). See [Section 2.1, “Concept: Regions in a Theme”](https://drupalize.me/tutorial/user-guide/block-regions "2.1. Concept: Regions in a Theme") for more information.

Relationship (in a View)
:   Expansion of the data that is displayed in a view, by relating the base content to other content entities. See [Section 9.2, “Concept: The Parts of a View”](https://drupalize.me/tutorial/user-guide/views-parts "9.2. Concept: The Parts of a View") for more information.

Repository
:   Location where a version control system stores all the files and directories for a project. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools") for more information.

Responsive
:   A site or [theme](https://drupalize.me/tutorial/user-guide/glossary#glossary-theme) is said to be responsive if it adjusts its presentation in response to the size of the browser screen, printer, or other media output type. See also [Breakpoint](https://drupalize.me/tutorial/user-guide/glossary#glossary-breakpoint). See [Section 6.14, “Concept: Responsive Image Styles”](https://drupalize.me/tutorial/user-guide/structure-image-responsive "6.14. Concept: Responsive Image Styles") for more information.

Revision
:   A record of the past or present state of a [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) [entity](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity), as it is edited over time. See [Section 2.6, “Concept: Editorial Workflow”](https://drupalize.me/tutorial/user-guide/planning-workflow "2.6. Concept: Editorial Workflow") for more information.

Role
:   A named set of [permissions](https://drupalize.me/tutorial/user-guide/glossary#glossary-permission) that can be applied to a [user account](https://drupalize.me/tutorial/user-guide/glossary#glossary-user). See [Section 7.1, “Concept: Users, Roles, and Permissions”](https://drupalize.me/tutorial/user-guide/user-concept "7.1. Concept: Users, Roles, and Permissions") for more information.

Security update
:   An [update](https://drupalize.me/tutorial/user-guide/glossary#glossary-update) that fixes a security-related bug, such as a hacking vulnerability. See [Section 13.3, “Concept: Security and Regular Updates”](https://drupalize.me/tutorial/user-guide/security-concept "13.3. Concept: Security and Regular Updates") for more information.

Session
:   Information about individual site visitors' interactions with the site, such as whether they are logged in and their cookies. See [Section 1.5, “Concept: Types of Data”](https://drupalize.me/tutorial/user-guide/understanding-data "1.5. Concept: Types of Data") for more information.

Staging site
:   Copy of the live website that can be used for testing, or presenting the changes to the client for approval. See [Section 11.7, “Concept: Development Sites”](https://drupalize.me/tutorial/user-guide/install-dev-sites "11.7. Concept: Development Sites") for more information.

State
:   Information of a temporary nature about the current state of your site, such as the time when [cron](https://drupalize.me/tutorial/user-guide/glossary#glossary-cron) was last run, etc. See also [Content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) and [Configuration](https://drupalize.me/tutorial/user-guide/glossary#glossary-configuration). See [Section 1.5, “Concept: Types of Data”](https://drupalize.me/tutorial/user-guide/understanding-data "1.5. Concept: Types of Data") for more information.

Taxonomy
:   The process of classifying [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content). See [Section 6.5, “Concept: Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy "6.5. Concept: Taxonomy") for more information.

Taxonomy term
:   A term used to classify [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content), such as a tag or a category. See also [Vocabulary](https://drupalize.me/tutorial/user-guide/glossary#glossary-vocabulary). See [Section 6.5, “Concept: Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy "6.5. Concept: Taxonomy") for more information.

Text format
:   [Configuration](https://drupalize.me/tutorial/user-guide/glossary#glossary-configuration) that defines the processing that happens to user-entered text before it is shown in the browser. This might include stripping or limiting HTML tags, or turning [URLs](https://drupalize.me/tutorial/user-guide/glossary#glossary-url) into links. See [Section 6.15, “Concept: Text Formats and Editors”](https://drupalize.me/tutorial/user-guide/structure-text-formats "6.15. Concept: Text Formats and Editors") for more information.

Theme
:   Software and asset files (images, CSS, PHP code, and/or templates) that determine the style and layout of the site. The Drupal project distinguishes between *[core](https://drupalize.me/tutorial/user-guide/glossary#glossary-drupal-core)* and *[contributed](https://drupalize.me/tutorial/user-guide/glossary#glossary-contributed)* themes. See [Section 1.3, “Concept: Themes”](https://drupalize.me/tutorial/user-guide/understanding-themes "1.3. Concept: Themes") for more information.

UI
:   Acronym for [*User Interface*](https://drupalize.me/tutorial/user-guide/glossary#glossary-user-interface).

Update
:   A newer version of your site’s software, either [Drupal core](https://drupalize.me/tutorial/user-guide/glossary#glossary-drupal-core) or a [module](https://drupalize.me/tutorial/user-guide/glossary#glossary-module) or [theme](https://drupalize.me/tutorial/user-guide/glossary#glossary-theme). See also [Security update](https://drupalize.me/tutorial/user-guide/glossary#glossary-security-update). See [Section 13.3, “Concept: Security and Regular Updates”](https://drupalize.me/tutorial/user-guide/security-concept "13.3. Concept: Security and Regular Updates") for more information.

URL
:   A web page’s unique address on the web. For example <https://example.com/node/7>. See [Section 5.1, “Concept: Paths, Aliases, and URLs”](https://drupalize.me/tutorial/user-guide/content-paths "5.1. Concept: Paths, Aliases, and URLs") for more information.

User
:   A person interacting with the site, either logged-in or [anonymous](https://drupalize.me/tutorial/user-guide/glossary#glossary-anonymous). See [Section 7.1, “Concept: Users, Roles, and Permissions”](https://drupalize.me/tutorial/user-guide/user-concept "7.1. Concept: Users, Roles, and Permissions") for more information.

User interface
:   The text, styles, and images that are visible on a site, separated logically into the user interface for site visitors and the administrative user interface.

User one (User 1)
:   The initial [user](https://drupalize.me/tutorial/user-guide/glossary#glossary-user) account that is created when you [install](https://drupalize.me/tutorial/user-guide/glossary#glossary-installing) the site (whose ID number is 1). It automatically has all [permissions](https://drupalize.me/tutorial/user-guide/glossary#glossary-permission), even if it is not assigned an administrative [role](https://drupalize.me/tutorial/user-guide/glossary#glossary-role). See [Section 7.2, “Concept: The User 1 Account”](https://drupalize.me/tutorial/user-guide/user-admin-account "7.2. Concept: The User 1 Account") for more information.

Version Control System
:   Software that keeps copies of files and revision history in a [repository](https://drupalize.me/tutorial/user-guide/glossary#glossary-repository), and allows you to add, delete, and update files. See [Section 3.3, “Concept: Additional Tools”](https://drupalize.me/tutorial/user-guide/install-tools "3.3. Concept: Additional Tools") for more information.

View
:   A formatted listing of data; typically, the data comes from [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) [entities](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity). For example, on a farmers market site, you might create a [content item](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-item) for each vendor. You could then make view that generates a listing page that shows a thumbnail image and short description of each vendor, linking to the full-page content item. Using the same data, you could also make a view that generates a new vendors block, which would show information from the most recently added vendors. See [Section 2.4, “Concept: Modular Content”](https://drupalize.me/tutorial/user-guide/planning-modular "2.4. Concept: Modular Content") for more information.

View mode
:   A set of [field formatter](https://drupalize.me/tutorial/user-guide/glossary#glossary-field-formatter) [configuration](https://drupalize.me/tutorial/user-guide/glossary#glossary-configuration) for all of the [fields](https://drupalize.me/tutorial/user-guide/glossary#glossary-field) of a [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) [entity](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity), some of which may be hidden. Each [entity subtype](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-subtype) can have one or more view modes defined; for example, [content types](https://drupalize.me/tutorial/user-guide/glossary#glossary-content-type) typically have *Full* and *Teaser* view modes, where the *Teaser* view mode displays fewer or trimmed-down fields. See [Section 6.10, “Concept: View Modes and Formatters”](https://drupalize.me/tutorial/user-guide/structure-view-modes "6.10. Concept: View Modes and Formatters") for more information.

Vocabulary
:   A group of [taxonomy terms](https://drupalize.me/tutorial/user-guide/glossary#glossary-taxonomy-term) to choose from when classifying [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) in a particular way, such as the list of all of the vendor categories on a farmers market site. Technically, vocabularies are the [entity subtype](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-subtype) for the taxonomy term [entity type](https://drupalize.me/tutorial/user-guide/glossary#glossary-entity-type). See [Section 6.5, “Concept: Taxonomy”](https://drupalize.me/tutorial/user-guide/structure-taxonomy "6.5. Concept: Taxonomy") for more information.

Widget
:   See [Field widget](https://drupalize.me/tutorial/user-guide/glossary#glossary-field-widget).

Wizard
:   A web form that allows you to fill in a few values, and creates something with sensible defaults based on the values you chose. For example, there are wizards for creating [views](https://drupalize.me/tutorial/user-guide/glossary#glossary-view) of different types. See [Section 9.3, “Creating a Content List View”](https://drupalize.me/tutorial/user-guide/views-create "9.3. Creating a Content List View") for more information.

WYSIWYG
:   Acronym for *What You See is What You Get*, meaning a method for editing [content](https://drupalize.me/tutorial/user-guide/glossary#glossary-content) where what you see on the editing screen closely resembles the final product. See [Section 6.16, “Configuring Text Formats and Editors”](https://drupalize.me/tutorial/user-guide/structure-text-format-config "6.16. Configuring Text Formats and Editors") for more information.

Workflow
:   See [Editorial Workflow](https://drupalize.me/tutorial/user-guide/glossary#glossary-editorial-workflow).

XSS
:   Acronym for [Cross Site Scripting](https://drupalize.me/tutorial/user-guide/glossary#glossary-cross-site-scripting).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[A.1. Guide-Wide Attributions](/tutorial/user-guide/attributions?p=2335)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
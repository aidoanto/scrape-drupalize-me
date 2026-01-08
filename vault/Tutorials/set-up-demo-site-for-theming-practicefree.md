---
title: "Set Up Demo Site for Theming Practicefree"
url: "https://drupalize.me/tutorial/set-demo-site-theming-practice?p=3269"
guide: "[[frontend-theming]]"
---

# Set Up Demo Site for Theming Practicefree

## Content

Set up a local development environment to practice Drupal theme development exercises in our course, [Hands-On Theming Exercises for Drupal](https://drupalize.me/course/hands-theming-exercises-drupal).

By the end of this tutorial, you should be able to:

- Install Drupal on your computer, so you can edit files in your theme.
- Generate dummy content, so that you have different kinds of pages to theme.

## Goal

Set up a local development environment with Drupal installed and generate dummy content, so that there are real pages on your site for you to theme.

## Prerequisites

- [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev)

## Exercise: Install Drupal and generate dummy content

### Install DDEV

Follow the steps in [Install Drupal Locally with DDEV](https://drupalize.me/tutorial/install-drupal-locally-ddev) and return to this tutorial to complete setup.

### Install the Devel Generate module

Next, we'll download and install the [Devel Generate module (part of the Devel project)](https://www.drupal.org/project/devel) and use it to generate some sample content. It’s easier to work on developing a Drupal theme if you’ve got some content on your site to look at.

```
ddev composer require drupal/devel
ddev drush en devel_generate
```

Or using the *Manage* administrative menu, navigate to *Extend*, and enable the Devel Generate module along with any required dependencies.

You are now ready to generate some content, which will make it easier to identify and theme different types of pages and components.

### Generate users, tags, and content

Devel Generate comes with custom Drush commands that we can use to generate users, tags, and content. We recommend you run the commands in the order that follows so that the content you generate is assigned to random users to simulate a more realistic experience.

```
ddev drush devel-generate-users 10
ddev drush devel-generate-terms 20 --bundles tags --max-depth 1
ddev drush devel-generate-content 25
```

#### Using the UI

Alternatively, if you didn't install Drush, use the administrative UI to generate users, tags, and content. You can find this UI on the *Configuration* page in the Development section (after enabling Devel Generate on the *Extend* (*admin/modules*) page).

1. Generate users (10).
2. Generate terms. (Vocabularies: Tags. Number of terms: 20. (Optional) Maximum depth for new terms in the vocabulary hierarchy: 1.
3. Generate content. (Check both Article and Basic Page content types. 25 nodes.)

You can verify that the commands worked by visiting the following administrative pages:

- Verify generated **users** at *People* (*admin/people*).
- Verify generated **terms** at *Structure* > *Taxonomy* > *Tags* (select List terms) (*admin/structure/taxonomy/manage/tags/overview*).
- Verify generated **content** at *Content* (*admin/content*).

You now have some dummy content to theme!

## Recap

After completing this exercise you should have a working copy of Drupal that you can access on your local development environment. It should contain either real or dummy content that you can use when previewing your theme during development.

## Further your understanding

- Execute the `ddev help` command in your terminal and browse the additional ddev commands
- Can you figure out how you might share this new local development configuration with others on your team so that you can all work on similarly configured environments?

## Additional resources

- [Development Environments](https://drupalize.me/topic/development-environments) (Drupalize.Me)
- [Drush](https://drupalize.me/topic/drush) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Exercise: Create a New Theme](/tutorial/exercise-create-new-theme?p=3269)

Clear History

Ask Drupalize.Me AI

close
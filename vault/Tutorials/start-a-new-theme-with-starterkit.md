---
title: "Start a New Theme with Starterkit"
url: "https://drupalize.me/tutorial/start-new-theme-starterkit?p=3267"
guide: "[[frontend-theming]]"
order: 36
---

# Start a New Theme with Starterkit

## Content

When it's time to start a custom Drupal theme from scratch (especially if you're new to Drupal theming), we recommend using Starterkit. Starterkit helps you get a new theme up and running by scaffolding a set of theme files with sensible defaults, saving you from a bunch of repetitive work.

In this tutorial we'll:

- Learn what Starterkit is
- Discuss when you should--and should not--use Starterkit
- Walk through how to use Starterkit to generate a new Drupal theme

By the end of this tutorial you should be able to explain the use case for Starterkit and understand how to use it to start a new custom theme.

## Goal

Start a new custom theme using the Drupal core utility, Starterkit.

## Prerequisites

- You'll need a [local Drupal development environment](https://drupalize.me/topic/development-environments) and Drupal installed. **Note:** Starterkit requires Drupal 9.3 or greater
- [What Is a Theme?](https://drupalize.me/tutorial/what-theme)
- [Moving Around the Command Line](https://drupalize.me/tutorial/moving-around-command-line?p=880)

## Generate a new theme with Starterkit

Ready to start a new Drupal theme?

From the root of your Drupal project (where the *core* directory lives), run the following command, replacing `{MY_THEME}` with the machine name you want for your new theme.

```
php core/scripts/drupal generate-theme {MY_THEME}
```

The machine name you choose should be a unique name within your Drupal site, not shared by any other theme, module, or profile. By default, the Starterkit utility will generate a set of theme files using that name based on Drupal core's *starterkit\_theme*.

## What is Starterkit?

Starterkit comprises a file scaffolding script and an API. Starterkit's PHP script, when executed by running the `drupal generate-theme` command, will create a new directory for a custom theme and populate it with a bunch of files. The files inside the core theme, *starterkit\_theme*, serve as a template that the script uses to scaffold a new theme. The core *starterkit\_theme* also provides an API for post-processing tasks that Starterkit template themes can use to customize how a new theme is scaffolded.

When you run the `drupal generate-theme` command, it copies the contents of *core/themes/starterkit\_theme*, executes any code that implements its API, and renames everything based on the provided machine name (as appropriate) to create a new theme.

We think Starterkit is a fantastic way to learn how to create Drupal themes. The Starterkit-generated info files, templates, and asset libraries work just as they would in any other Drupal theme. The difference is you get to start from a working theme full of code examples you can copy or modify instead of a blank slate.

Starterkit creates a lot of template files (see the *templates* directory), and overrides a bunch of core CSS asset libraries (see the *info* and *libraries* YAML files). The reason for this is to make it clear which files compose your custom theme.

If you've created a Drupal theme prior to the introduction of Starterkit you may have started by creating an info file, and using [Classy](https://drupalize.me/tutorial/drupal-base-themes-stable-and-classy) as a [base theme](https://drupalize.me/tutorial/theme-inheritance-base-themes). By extending Classy your custom theme is implicitly dependent on all the template files in that theme, which makes your custom theme dependent on Classy. But that's not always obvious. With Starterkit, you effectively get the same result, but without the need to extend Classy--or be dependent on its code. **Instead, all the files used by your theme are located in your custom theme**.

If you're curious about how Starterkit evolved, and the transition away from using Classy as a base theme, read this blog post: [New starterkit will change how you create themes in Drupal 10](https://www.drupal.org/about/core/blog/new-starterkit-will-change-how-you-create-themes-in-drupal-10) (Drupal.org).

## What does Starterkit do?

The goal of Starterkit is to provide a quick way to scaffold a new theme and make it explicit what markup your theme is producing. To accomplish this, the utility will create a new directory, and populate it with files copied from the specified Starterkit template (by default, the core *starterkit\_theme*).

Example:

```
/themes/my_awesome_theme
├── README.md
├── css
│   ├── components
├── images
│   └── icons
├── js
│   └── bootstrap
├── logo.svg
├── reboot.info.yml
├── reboot.libraries.yml
├── reboot.theme
├── screenshot.png
├── src
│   └── StarterKit.php
└── templates
    ├── block
    ├── content
    ├── content-edit
    ├── dataset
    ├── field
    ├── form
    ├── layout
    ├── misc
    ├── navigation
    ├── user
    └── views
```

The main benefit of using this approach is that a lot of the boilerplate code that goes into a theme's *.info.yml* file, its *.libraries.yml* file, and ensuring that template files are placed into a *templates/* subdirectory is done already. Fewer steps, and less naming conventions you have to memorize.

## How does Starterkit work?

From an end-user perspective, Starterkit is used via the `drupal generate-theme` command. Use the `--help` flag for a complete list of options.

### Example: Explore Starterkit's options with `--help`

```
php core/scripts/drupal generate-theme --help
```

### Specify a location for your theme

Use the `--path` option to specify a location for the new code to be placed other than the root */themes* directory. For example: `--path=themes/custom/` to generate the new theme in *themes/custom/*.

### Specify a Starterkit template theme

You can use the optional `--starterkit` flag to use a theme other than the default *starterkit\_theme* as the theme to copy from. **The target theme must have `starterkit: true` in its *.info.yml* file.** You can use this feature to create your own custom starting points, or in conjunction with some contributed themes downloaded from Drupal.org.

### Inside Starterkit's generate-theme command

Behind the scenes, the command executes the code in [`\Drupal\Core\Command\GenerateTheme`](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Command!GenerateTheme.php/class/GenerateTheme). Which recursively copies the files from the target Starterkit theme, performs a search-and-replace operation on file names and asset library names, and generates an updated *.info.yml* file. The command also inserts a line like `generator: 'starterkit_theme:10.1.1'` into the new *.info.yml* file. This line tells you which theme was used as a Starterkit template (from which Starterkit copied theme files), and which version of the Starterkit template theme was used. This can be used later to check for differences when updates to the Starterkit template theme are made, if you want to incorporate those into your custom theme.

Themes that are used as a Starterkit (`starterkit: true`) can provide additional post-processing logic that is executed after all the files are copied. Starterkit themes can implement `\Drupal\Core\Theme\StarterKitInterface` as a class named `StarterKit` in the theme's namespace. For example, if you had a custom theme named `icecream`:

Create the file *icecream/src/StarterKit.php*, and add your code to it:

```
<?php
namespace Drupal\icecream;

use Drupal\Core\Theme\StarterKitInterface;

final class StarterKit implements StarterKitInterface {

  /**
   * {@inheritdoc}
   */
  public static function postProcess(string $working_dir, string $machine_name, string $theme_name): void {
    // Do your custom post-processing here ...
  }

}
```

## Recap

In this tutorial we learned how to start a new custom theme using the Drupal core Starterkit utility. We talked about why we recommend using Starterkit, especially if you're new to theming. We provided some details about why Starterkit was created and how it works.

## Further your understanding

- Why is Classy being replaced with Starterkit? And what are the benefits of copying all the default template files into your custom theme versus inheriting them from a base theme?
- Learn more about [what is in the *.info.yml* file](https://drupalize.me/tutorial/describe-your-theme-info-file) that Starterkit generated for you.
- Learn to [Override a Template File](https://drupalize.me/tutorial/what-are-template-files).

## Additional resources

- [New starterkit will change how you create themes in Drupal 10](https://www.drupal.org/about/core/blog/new-starterkit-will-change-how-you-create-themes-in-drupal-10) (Drupal.org)
- [The Drupal Theme StarterKit (Podcast)](https://www.lullabot.com/podcasts/lullabot-podcast/drupal-theme-starterkit) (lullabot.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Structure of a Theme](/tutorial/structure-theme?p=3267)

Next
[Describe Your Theme with an Info File](/tutorial/describe-your-theme-info-file?p=3267)

Clear History

Ask Drupalize.Me AI

close
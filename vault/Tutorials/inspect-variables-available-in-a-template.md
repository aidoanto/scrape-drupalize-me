---
title: "Inspect Variables Available in a Template"
url: "https://drupalize.me/tutorial/inspect-variables-available-template?p=2879"
guide: "[[frontend-theming]]"
---

# Inspect Variables Available in a Template

## Content

Knowing how to inspect the variables available within a template file enables you to discover all of the dynamic content in a Twig file, not just that which is already being used.

In this tutorial, we'll learn how to use `{{ dump() }}`, `kint()`, `vardumper()`, and Xdebug to inspect variables in a template file.

## Goal

Discover and inspect variables available in any template file.

## Prerequisites

- [What Is a Theme?](https://drupalize.me/tutorial/what-theme)
- [Describe Your Theme with an Info File](https://drupalize.me/tutorial/describe-your-theme-info-file)
- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development)
- [What Are Template Files?](https://drupalize.me/tutorial/what-are-template-files)
- [Override a Template File](https://drupalize.me/tutorial/override-template-file)
- [Downloading and Installing a Module from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install?p=3072)
- [Using Composer to Download and Update Files](https://drupalize.me/tutorial/user-guide/install-composer?p=3074)
- [Concept: Additional Tools](https://drupalize.me/tutorial/user-guide/install-tools?p=3074)

## Find variable information in the base template

The first place to look for information about the variables available in a template file is in the file itself, or the base version of the template. Each core template contains documentation near the top of the file that explains the most commonly used variables in that template. Not sure how to find the base template? See [Determine the Base Name of a Template](https://drupalize.me/tutorial/determine-base-name-template).

## Discovering all variables in a template

This documentation, though useful, doesn't cover all of the variables available in a template. As you start adding new fields to entities or installing new modules, you can introduce new variables to template files. The next best way to discover the variables available in a template file is to use Twig's `dump()` function to run `{{ dump(_context|keys) }}` and then inspect the variable with `dump(variable_key_name)`.

Sprout Video

## Using Twig's `dump()` function

### Enable Twig debug mode

Ensure your site is configured for Twig debugging. See [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development).

### Locate a file to inspect

Locate the file for which you would like to get a list of available variables and open it in your editor.

### Discover the variable key names

Add the code `{{ dump(_context|keys) }}` at the bottom of the file and refresh the page. This will produce a list of all of the variable key names available to inspect in this template file.

### Choose a variable key and inspect it

Select one of the variable key names from the output of `{{ dump(_context|keys) }}`. Inspect that variable by passing in the key name to Twig's `dump()` function. For example:

```
dump(variable_key_name)
```

This will provide PHP `var_dump()`-style output for all of the variables available in the scope of the template file where you put this code.

## Interpreting variable inspection output

The key of each array is the name that you would use to access a variable within Twig. Consider the following output:

```
'is_admin' => boolean true
  'logged_in' => boolean true
  'user' =>
    object(Drupal\Core\Session\AccountProxy)[517]
      protected 'account' =>
        object(Drupal\Core\Session\UserSession)[100]
          protected 'uid' => string '1' (length=1)
          protected 'roles' =>
            array (size=2)
              ...
          protected 'access' => string '1440187417' (length=10)
          public 'name' => string 'admin' (length=5)
          protected 'preferred_langcode' => string 'en' (length=2)
          protected 'preferred_admin_langcode' => null
          protected 'mail' => string '[email protected]' (length=17)
          protected 'timezone' => string 'America/New_York' (length=16)
          public 'langcode' => string 'en' (length=2)
          public 'pass' => string '$S$EA9QMFCiUeM9.aF0Zxyg7hp7kXGj4acPcK43c8XDQScyGrAxlcL1' (length=55)
          public 'status' => string '1' (length=1)
          public 'created' => string '1439482566' (length=10)
          public 'changed' => string '1439483491' (length=10)
          public 'login' => string '1439483491' (length=10)
          public 'init' => string '[email protected]' (length=17)
          public 'default_langcode' => string '1' (length=1)
      protected 'initialAccountId' => null
      public '_serviceId' => string 'current_user' (length=12)
```

In this example, each of the top level keys is available as a variable that can be accessed directly, such as `{{ is_admin }}`, and the nested keys can be accessed like so: `{{ user.name }}`.

Note: For easier to read output, either install the [PHP Xdebug extension](http://xdebug.org/docs/display) and enable [html\_errors](https://www.php.net/manual/en/errorfunc.configuration.php#ini.html-errors), or wrap the output in

`<pre>` tags like so:

```
<pre>{{ dump() }}</pre>
```

## Prettier output with contributed modules

Using Kint and the Devel module or Twig Vardumper for prettier output

## Kint

[Kint](https://github.com/kint-php/kint) is a handy tool for inspecting variables. It functions almost identically to Twig's built in `dump()` function, but has much easier to read output. Kint used to be included with the Devel project but that is no longer the case. To use Kint for inspecting variables in your template files, you will need to download Kint using Composer and then use Devel to configure Kint as your debugger of choice.

### Install and enable Devel module

Install the [Devel module](https://www.drupal.org/project/devel) and enable it on the Extend page. You'll use Devel to configure your debugger of choice (Kint, in this instance).

See also [Downloading and Installing a Module from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install?p=3072).

### Download the Kint library using Composer

Assuming you are [managing your site's dependencies with Composer](https://drupalize.me/tutorial/use-composer-your-drupal-project), from the root of your project (where your site's *composer.json* is located) run the following command:

```
composer require kint-php/kint --dev
```

This will download the Kint library to your site's *vendor* directory and add `kint-php/kint` to your site's *composer.json* in the `require-dev` section.

### Clear the cache

Before Devel's configuration page can recognize Kint as an option, you'll need to clear the cache. If you're using Drush, run `drush cr`. Otherwise, using the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Performance* (*admin/config/development/performance*) and select *Clear all caches*.

### Configure Kint as your debugger of choice

Using the *Manage* administrative menu, navigate to *Configuration* > *Development* > *Devel settings* (*admin/config/development/devel*) and under the heading, *Variables Dumper*, select *Kint*, then *Save configuration*. (You'll notice that you can also try out other libraries here as well.)

### Using `kint()` as your variables dumper

In your template files instead of `{{ dump() }}` you can use `{{ kint() }}` which will provide the output in an easier to read and navigate format.

Image

![Kint output example](/sites/default/files/styles/max_800w/public/tutorials/images/kint-output-example.jpg?itok=khVXjroJ)

## Twig Vardumper module

An alternative to Kint is Twig Vardumper. It provides a responsive and, in many cases, more performant output of variables than Kint.

### Download Twig Vardumper

See the [Twig Vardumper project page](https://www.drupal.org/project/twig_vardumper) on Drupal.org for the latest release. Download it to your *modules/contrib* directory.

See also [Downloading and Installing a Module from Drupal.org](https://drupalize.me/tutorial/user-guide/extend-module-install?p=3072).

### Enable Twig Vardumper

Go to the *Extend* page (*admin/modules*) and enable Twig Vardumper.

## Use `vardumper()`

In your template files instead of `{{ dump() }}` you can use `{{ vardumper() }}` which will provide the output in an easier to read and navigate format.

## Using a debugger like Xdebug

You can also use a PHP debugger like [Xdebug](https://xdebug.org/) to inspect variables. And we highly recommend learning how to do so as it's an important skill for any developer.

Check out these resources on debugging in PhpStorm to get started. [If you've installed Drupal on DDEV locally](https://drupalize.me/tutorial/install-drupal-locally-ddev), Xdebug is included.

- [DDEV: Step Debugging with Xdebug](https://ddev.readthedocs.io/en/stable/users/debugging-profiling/step-debugging/) (ddev.readthedocs.io)
- [Xdebug tutorials and external resources](https://drupalize.me/topic/xdebug) (Drupalize.Me)

Since template files are Twig, and not PHP, and since they're actually compiled to PHP and then later cached, using a debugger on a template file can be a bit tricky. We find the best way to do so is to implement a preprocess function for the template in question, and set a breakpoint inside that preprocess function. From there, you can use all the tools in your debugger to inspect the `$variables` array.

Add a [preprocess function](https://drupalize.me/tutorial/what-are-preprocess-functions) like the following to your *.theme* file, and change the `$hook == 'node'` line to whatever template for which you're inspecting variables.

```
function icecream_preprocess(&$variables, $hook) {
  if ($hook == 'node') {
    xdebug_break();
  }
}
```

Then start a debug session, view any page with that template, and you should see the output in your debugger.

Image

![PHPStorm xdebug variable inspector](/sites/default/files/styles/max_800w/public/tutorials/images/inspecting-variables-debugger.png?itok=AM2SpYdz)

## Preprocess functions

Variables are provided to Twig templates via preprocess functions and you can always read the code for those functions to get more insight into where the variables in a template are generated as well as the logic that created them. Learn about preprocess functions in [What Are Preprocess Functions?](https://drupalize.me/tutorial/what-are-preprocess-functions)

## Recap

In this tutorial, you learned how to inspect variables using several different methods and tools. If you're running into PHP errors during the process, be sure to revisit the tutorial [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development), especially the section on setting PHP variables in your local environment.

## Further your understanding

- Enable Twig debug mode and use the new `dump()` function in a template in your theme.
- If you use `dump()` in two different templates what variables are the same for both?
- Many of the variables you'll see inside of a template file are deeply nested arrays. Do you know what these arrays are used for?

## Additional resources

- [Configure Your Environment for Theme Development](https://drupalize.me/tutorial/configure-your-environment-theme-development) (Drupalize.Me)
- [DDEV: Step Debugging with Xdebug](https://ddev.readthedocs.io/en/stable/users/debugging-profiling/step-debugging/) (ddev.readthedocs.io)
- [PHP Xdebug extension](http://xdebug.org/docs/display) (xdebug.com)
- [Xdebug tutorials and external resources](https://drupalize.me/topic/xdebug) (Drupalize.Me)
- [html\_errors](https://www.php.net/manual/en/errorfunc.configuration.php#ini.html-errors) (PHP manual)
- [Devel project (includes Kint)](https://www.drupal.org/project/devel) (Drupal.org)
- [Kint PHP library](https://github.com/kint-php/kint) (github.com)
- [Twig Vardumper](https://www.drupal.org/project/twig_vardumper) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Determine the Base Name of a Template](/tutorial/determine-base-name-template?p=2879)

Next
[Overview: Theming Views](/tutorial/overview-theming-views?p=2879)

Clear History

Ask Drupalize.Me AI

close
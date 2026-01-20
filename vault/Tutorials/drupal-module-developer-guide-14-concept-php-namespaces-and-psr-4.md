---
title: "Concept: PHP Namespaces and PSR-4free"
url: "https://drupalize.me/tutorial/concept-php-namespaces-and-psr-4?p=3236"
guide: "[[drupal-module-developer-guide]]"
order: 14
---

# Concept: PHP Namespaces and PSR-4free

## Content

Drupal uses PSR-4 namespaces to autoload the correct PHP class from a file, accommodating variations in site structures. As a module developer, it's important to understand PSR-4, as it dictates the location within your module directory for most of your custom code.

In this tutorial, we'll:

- Define the PSR-4 namespace standard.
- Explore its use in Drupal.
- Learn to read a namespace and locate the corresponding PHP file.

By the end of this tutorial, you should be able to recognize a PSR-4 namespace, determine the related fully-qualified class name, and the location of the corresponding PHP file.

## Goal

Identify and use PSR-4 namespaces for PHP classes inside custom Drupal modules.

## Prerequisites

- None.

## Understanding PSR-4 namespaces in Drupal

[PHP namespaces](https://www.php.net/manual/en/language.namespaces.php) and the [PSR-4 autoloading standard](https://www.php-fig.org/psr/psr-4/) allow Drupal to manage and autoload PHP classes efficiently. Namespaces serve as a method for ensuring unique names for items like classes. PSR-4, defined by [PHP-FIG](https://www.php-fig.org/), specifies the naming and organization of files for autoloading.

This approach helps avoid name conflicts and enables Drupal to automatically discover and execute code provided by custom modules.

## Implementing namespaces in your module

When creating a PHP class in a Drupal module, you need to define a namespace for it. Each module has a namespace corresponding to its name. For example, the namespace for a module named *anytown* is:

```
Drupal\anytown
```

The module's namespace maps to its *src/* directory:

| PSR-4 namespace | Corresponding directory |
| --- | --- |
| `Drupal\anytown` | *modules/anytown/src/* |

Subsequent parts of the namespace map directly to the file structure:

| PSR-4 namespace | Corresponding directory |
| --- | --- |
| `Drupal\anytown\Ingredients\Carrots` | *modules/anytown/src/Ingredients/Carrots.php* |

In the *Carrots.php* file, the namespace is at the top, and the PHP class name derives from the file name without the *.php* extension.

For example, *modules/anytown/src/Ingredients/Carrots.php*:

```
<?php
namespace Drupal\anytown\Ingredients;

class Carrots {

}
?>
```

To use the `Carrots` class, instantiate it with its fully qualified namespace, and Drupal will locate and include the file:

```
use Drupal\anytown\Ingredients\Carrots;

$carrots = new Carrots();
$carrots->eat();
```

Always reference a class in a Drupal module using its full namespace. For example, Drupal's Plugin API searches for code within a sub-namespace like `Drupal\*\Plugins\Block\**.php`, where the first `*` is any **enabled** module, and `**.php` is any class in the corresponding PSR-4 subdirectory.

## Finding files based on namespaces

You will need to know how to read a namespace and find the associated file. The key is understanding the relationship between the namespace and the module's directory structure. For example, the namespace `Drupal\anytown\Ingredients\Carrots` corresponds to *modules/custom/anytown/src/Ingredients/Carrots.php*.

## Why PSR-4?

Drupal adopted the PSR-4 standard for namespaces and autoloading to align with the broader PHP community, which uses it to efficiently organize classes. PSR-4's compatibility with Composer enhances Drupal's dependency management.

## Recap

In this tutorial, we explored PHP namespaces and PSR-4 in Drupal. We looked at an example of how PSR-4 infers the location of a *.php* file, explaining why understanding this pattern is essential for Drupal module developers.

## Further your understanding

- Try creating a new PHP class in a module. Can you define the correct namespace and file path?
- How do namespaces prevent class name conflicts in Drupal projects?

## Additional resources

- [PHP Namespaces in Under 5 Minutes](https://symfonycasts.com/screencast/php-namespaces/namespaces) (symfonycasts.com)
- [Namespaces Overview](https://www.php.net/manual/en/language.namespaces.php) (php.net)
- [PSR-4: Autoloader](https://www.php-fig.org/psr/psr-4/) (php-fig.org)
- [PSR-4 Namespaces and Autoloading in Drupal](https://www.drupal.org/docs/develop/standards/php/psr-4-namespaces-and-autoloading-in-drupal-8) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Routes](/tutorial/concept-routes?p=3236)

Next
[Concept: Controllers](/tutorial/concept-controllers?p=3236)

Clear History

Ask Drupalize.Me AI

close
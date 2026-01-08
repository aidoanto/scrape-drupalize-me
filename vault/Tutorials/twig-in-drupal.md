---
title: "Twig in Drupal"
url: "https://drupalize.me/tutorial/twig-drupal?p=2464"
guide: "[[frontend-theming]]"
---

# Twig in Drupal

## Content

Twig is the default template engine for Drupal. If you want to make changes to the markup that Drupal outputs you're going to need to know at least some Twig. In this tutorial, we will outline the role that Twig now plays in Drupal, how Twig impacts the theming experience, and where to find additional resources for learning Twig.

At the end of this lesson, you'll be able to:

- Describe the role that Twig plays in creating Drupal themes
- Explain how Twig impacts the theming experience in Drupal
- Locate additional resources for learning Twig

## Goal

Get a high-level overview of how Twig works in Drupal.

## Prerequisites

- None.

## Video

Sprout Video

**Note:** Documentation for Twig has been moved to [twig.symfony.com](https://twig.symfony.com/doc/3.x/). Drupal currently uses Twig 3.x. See the topic [Template Design with Twig](https://drupalize.me/topic/template-design-twig) for more information.

## What is Twig?

Twig is a template engine for PHP. A template engine allows an application or system like Drupal to separate the concerns of functional "business" logic and the presentation or markup of the resulting data.

## Twig's syntax

With Twig, there are 3 syntax delimeters:

```
{{ say something }}
{% do something %}
{# comment on something #}
```

Learn more in [Twig Syntax Delimiters](https://drupalize.me/tutorial/twig-syntax-delimiters).

## Template inheritance in Twig

- The `extends` keyword lets you "dress" a template in another template's markup.
- The `block` keyword defines the customizable area where another template's code will be dropped in.
- When a template uses `extends`, all markup is surrounded by `block` tags to define the custom markup.

Learn more in [Twig Template Inheritance](https://drupalize.me/tutorial/twig-template-inheritance).

## Why Twig in Drupal?

Twig was adopted in Drupal as a replacement for PHP template for a number of reasons including:

### Improved security

- Twig introduces autoescaping and sanitizes all HTML to prevent XSRF attacks.
- PHP will not be executed in a Twig file and will display instead as plain text.
- Previous major versions of Drupal executed any PHP and made it hard to know what user input was escaped.

### Simpler, cleaner templates

- Syntax for printing values inside an array or object is the same
- More streamlined, consistent syntax for printing variables
- Elimination of `print` and `render` keywords clears up confusion and results in cleaner templates.

### Language intended for templates

- Twig is specifically a templating language
- The language is designed for template authors who are markup experts, not necessarily PHP experts
- All Twig functionality is meant for use in template files
- PHP functionality goes way beyond what is needed for a template
- Twig empowers themers with an easy-to-learn syntax

### Community benefits

- Wide adoption outside the Drupal community
- Broad support within the Drupal community

## Challenges with Twig

- If you don't already know Twig, you'll need to learn it in order to be an effective Drupal themer.
- To use preprocess functions to add or change variables available in a template or to add theme hook suggestions, you'll still need to use PHP.

## Why learn Twig?

- If you want to output markup in a module or theme, you'll need to use templates and the Twig templating language to do so.
- If you're upgrading your site to Drupal from Drupal 7 or prior version, you'll need to convert your *tpl.php* PHP template files into Twig.

Who needs to learn Twig? If you're responsible for the markup output for a Drupal site, you'll need to learn Twig. Your role might be a front-end developer, themer, or module developer.

## Recap

This tutorial provided a basic high-level overview of Twig in Drupal.

## Further your understanding

- What is a template engine?
- What are the benefits of using Twig instead of vanilla PHP for templates?
- Can you list any other projects using Twig, or a template language with Twig like syntax?

## Additional resources

- Topic: [Template Design with Twig](https://drupalize.me/topic/template-design-twig) (Drupalize.Me)
- Course: [Using Twig in Drupal Templates](https://drupalize.me/course/using-twig-drupal-templates) (Drupalize.Me)
- [Twig in Drupal](https://www.drupal.org/docs/theming-drupal/twig-in-drupal) (Drupal.org)
- [Twig 3.x Documentation](https://twig.symfony.com/doc/3.x/) (twig.symfony.com)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Twig Syntax Delimiters](/tutorial/twig-syntax-delimiters?p=2464)

Clear History

Ask Drupalize.Me AI

close
---
title: "An Introduction to YAMLfree"
url: "https://drupalize.me/tutorial/introduction-yaml?p=3292"
guide: "[[develop-drupal-sites]]"
order: 2
---

# An Introduction to YAMLfree

## Content

Sprout Video

YAML, which stands for YAML Ain't Markup Language, is a human-readable data serialization format that's been widely adopted in a variety of use cases in Drupal. Anyone wanting to write modules, or themes, for Drupal will need to understand YAML syntax. Even site builders are likely to encounter YAML at least in passing as YAML is the data-serialization format of choice for Drupal's configuration management system. Good thing it's pretty easy to learn even with the most basic of programming backgrounds.

This tutorial will look at the YAML data format and provide examples of how to write and read YAML. Starting with an introduction to the language's syntax and some of the strengths of YAML. Then looking at the difference between scalar data types like strings and integers, and collection data types like lists and associative arrays.

Since YAML in the Drupal world is read into PHP and ultimately becomes a PHP data structure that we can use in our own code we'll also look at how the YAML we write in a *.yml* file is represented in PHP data types. To do this we'll use the YAML Sandbox module that provides a handy textarea into which we can type YAML and have it parsed into PHP data structures.

#### Learning objectives

- Explain what YAML is and its strengths as a data serialization format
- Create scalar key/value pairs in YAML
- Create lists, and associative arrays using YAML collections
- Understand how the YAML you write is represented in PHP

#### Tips

- In Drupal, use the *.yml* extension and **not** *.yaml*
- Ensure your code editing application is configured to use spaces (preferably 2 spaces, as per Drupal coding standards), **not the tab character** when the TAB key is pressed. If you have tab characters in a YAML file within a Drupal environment, a fatal PHP error will be thrown and you'll see a White Screen of Death (WSOD).
- Copy and paste from an existing YAML file to ensure the formatting is correct, and edit from there.

### Additional resources

- <http://www.yaml.org>
- [YAML Sandbox module](https://www.drupal.org/project/yaml_sandbox)
- Find other tutorials and external resources related to YAML on our [YAML topic page](https://drupalize.me/topic/yaml) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Info Files for Drupal Modules](/tutorial/overview-info-files-drupal-modules?p=3292)

Next
[PHP Attributes](/tutorial/php-attributes?p=3292)

Clear History

Ask Drupalize.Me AI

close
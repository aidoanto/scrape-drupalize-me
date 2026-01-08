---
title: "Dynamic Layout Plugins in Drupal's Layout Builder"
url: "https://drupalize.me/tutorial/dynamic-layout-plugins-drupals-layout-builder?p=3271"
guide: "[[layout-builder]]"
---

# Dynamic Layout Plugins in Drupal's Layout Builder

## Content

In their simplest form layout plugins in Drupal Layout Builder define the part of the content output that can't be changed. For example a three column layout will consist of three equal columns every time an editor decides to use it as the layout section. The editor can place whatever they want into the three columns. But they can not change the overall layout. This restricts editorial capabilities of using layout plugins since in real life a three column layout may need to consist of a wider middle column and narrower side columns, allow for column headings, or other customizations.

This flexibility is accomplished by creating, and exposing, configuration options for layout plugins in Drupal's Layout Builder. In more advanced cases, we can take this flexibility further by exposing an interface editors to dynamically define layout plugins.

In this tutorial we'll:

- Learn how to use custom PHP classes in the layout plugin annotation
- Learn what annotations properties can be used for custom layout declaration
- Define the concept of derivatives and outline scenarios for using them
- How to declare static single layouts using YAML format

By the end of this tutorial you'll learn advanced ways of declaring configurable custom layout plugins.

## Goal

Introduce advanced methods and terms related to declaring layout plugins in Drupal.

## Prerequisites

- [Introduction to Layout Builder](https://drupalize.me/tutorial/introduction-layout-builder)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [Plugin Derivatives](https://drupalize.me/tutorial/plugin-derivatives)

## What is a flexible layout?

Layout plugins that have a settings form, allowing an editor to control certain aspects of the layout, are called flexible layouts.

For example, if your site uses a 3-column layout, and you want to allow editors to choose variations like equal column widths, 25% | 50% | 25%, or 50% | 25% | 25%, etc. You could either define a new layout plugin for each variation, or a single layout plugin that presents the user with the choice of which variant to use. In most cases the latter is easier to maintain.

## How to define a flexible layout

While defining a layout plugin can be done in a theme, the PHP required to make them flexible has to be in a module, so we recommend keeping them together. Declare your layouts in the module as well.

Flexible layout definitions can be declared in the *[your\_module].layouts.yml*. In addition to the standard properties it must have a `class` property that will contain a path to a PHP class.

If this property is omitted, the default layout class provided by core is used. When a custom class is defined, it can extend the default core class and allow developers to alter the base functionality.

For the example use case described above, you need to define the alternate class, extend *\Drupal\Core\Layout\LayoutDefault*, and implement the *buildConfigurationForm*, *validateConfigurationForm*, *submitConfigurationForm* methods. *Note*: your custom class also has to implement *PluginFormInterface*.

This works similar to [defining a new form controller](https://drupalize.me/tutorial/define-new-form-controller-and-route). The defined form is presented to the user when the layout is placed within the Layout Builder UI.

Settings saved during the form submission need to be saved into the configuration object. That is then exposed to the layout's Twig template inside the `{{ settings }}` variable and can be used to alter the template's output.

## Declare custom layouts using PHP attributes

It's also possible to declare custom layouts using PHP attributes. For situations where you have just one custom layout override, or you have to have different settings forms for every layout, we recommend declaring layout plugins in PHP using attributes.

This approach can only be taken in a module and not a theme since custom themes cannot provide autoloaded class files.

When using this approach you do not need a *{MODULE\_NAME}.layouts.yml* file; all layouts will be single PHP classes in the *{MODULE\_NAME}/src/Plugin/Layout* directory and extending the *Drupal\Core\Layout\LayoutDefault* class.

The class declaration should include an `\Drupal\Core\Layout\Attribute\Layout` attribute and contain the same properties as a *{MODULE\_NAME}.layouts.yml* file would. You can find the [full annotation reference](https://www.drupal.org/docs/drupal-apis/layout-api/how-to-register-layouts#full-annotation-reference) on drupal.org. To learn more about creating annotation-based plugins see [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes).

## Declaring dynamic layouts

When you don't want to limit editors to a set of layouts pre-declared for them and your design requires the ability to create layout sections on the fly, you may want to declare dynamic layouts instead of the static ones.

This can be accomplished using derivatives -- a set of plugins declared dynamically based on user-provided data.

In this case you would need to implement a 2-step process:

1. Provide an editor with the configuration form that would store new layout configuration and meta-data as a configuration entity
2. The configuration entity can then be used within a deriver in the custom layout class to dynamically declare the layout plugin for each of the saved configuration entities.

When using a deriver, the annotation of the dynamic layout plugin will not have the standard properties we have seen previously. Instead, it will contain an id and point to a deriver class. The deriver class then fetches all the configuration entities and uses them to provide the missing annotation properties dynamically.

Since the layout is flexible it may be challenging to point to a single template. To resolve this challenge, you can override the `build` method within your dynamic layout class and render the layout properly based on the provided data from the configuration entity.

Refer to this tutorial if you need a [refresher on plugin derivatives](https://drupalize.me/tutorial/plugin-derivatives).

## Keep it clean and manageable

While working with flexible custom layouts things can get out of hand with the amount of layout classes and layout declarations spread between themes and modules.

We recommend following these best practice guidelines:

- Choose one place to declare and store your layout files: either a module or a theme -- not both.
- If you are only going to use basic layouts, declare them in the theme. This keeps all of your templates used for layouts and other parts of the site in one place.
- If you only have a single one-off flexible layout, declare it using PHP attributes in a module as opposed to using a *{MODULE\_NAME}.layouts.yml* file.
- Be consistent in how you declare layouts. Declare them all either in PHP or in YAML -- not both.

## Recap

In this tutorial, we learned that you can declare static single layouts using YAML format. Layout plugins can contain plugin-specific settings if you override the default plugin class and provide a settings form. For more complex scenarios you can dynamically define layouts using plugin derivatives.

## Further your understanding

- What settings other than CSS classes can be exposed in the custom layout settings form?
- What challenges may exist when rendering custom dynamic layouts?

## Additional resources

- [Layout Builder documentation](https://www.drupal.org/docs/8/core/modules/layout-builder) (Drupal.org)
- [Layout API](https://www.drupal.org/docs/8/api/layout-api) (Drupal.org)
- [Layout builder base contributed module that implements layout plugins](https://www.drupal.org/project/layout_builder_base) (Drupal.org)
- [Layout components contributed module that implements layout plugins](https://www.drupal.org/project/layoutcomponents) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[How to Create a Layout with Configurable Settings in Drupal's Layout Builder](/tutorial/how-create-layout-configurable-settings-drupals-layout-builder?p=3271)

Clear History

Ask Drupalize.Me AI

close
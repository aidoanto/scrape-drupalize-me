---
title: "Scaffold a Custom Content Entity Type with Drush Generators"
url: "https://drupalize.me/tutorial/scaffold-custom-content-entity-type-drush-generators?p=2607"
guide: "[[work-data-modules]]"
order: 5
---

# Scaffold a Custom Content Entity Type with Drush Generators

## Content

Code generators are great productivity boosters that allow generating scaffolds for common development tasks in Drupal. One of the most common use cases for generators is scaffolding the code required for a [custom entity type](https://drupalize.me/tutorial/create-custom-content-entity). Custom entities require many files and complicated annotations in order to function properly. There is a lot of boilerplate code that is more-or-less the same for every entity type. Creating all the files is repetitive, time-consuming, and prone to human error. Generators can help automate this task and make creating your own custom entity types quicker.

In this tutorial we'll:

- Learn how to generate the code for a custom entity with Drush
- Learn about the options that generators provide for custom entities

By the end of this tutorial you should know how to generate custom entities with Drush.

## Goal

Generate a custom *News* content entity and understand how the generator-provided options influence the final result.

## Prerequisites

- [Command Line Basics](https://drupalize.me/series/command-line-basics-series)
- [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity)
- [Develop Drupal Modules Faster with Drush Code Generators](https://drupalize.me/tutorial/develop-drupal-modules-faster-drush-code-generators)

## Generate a content entity type

The steps outlined below walk through the Drush generate command that helps scaffold some common code of a content entity. If you are not already familiar with the Entity API and the code required for creating a custom entity type, we recommend reading [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity) first. It's important to understand what the code generated here is doing, and not just blindly rely on the generator.

### Locate the appropriate generator

To see all the available generators for your Drupal installation, navigate to the root of your Drupal project through the command line and run `drush generate`. You'll see the list of generators like below:

```
drush generate

…
entity:                                                                                                  
  entity:bundle-class (bundle-class)                     Generate a bundle class for a content entity.   
  entity:configuration (config-entity)                   Generates configuration entity                  
  entity:content (content-entity)                        Generates content entity                        
form:                                                                                                    
  form:config (config-form)                              Generates a configuration form                  
  form:confirm (confirm-form)                            Generates a confirmation form                   
  form:simple (form)                                     Generates simple form  
…
```

For this tutorial, we'll use entity generators. Drush provides 3 entity type generators: bundle class, configuration entity, and content entity. We'll be generating a content entity in this tutorial (`drush generate entity:content`).

### Generate News content entity

We need to generate a *News* content entity. We'll use the `entity:content` generator. This generator asks for an existing module to encapsulate the content entity and creates the files required for a custom content entity based on the answers given to the generator's questions inside the specified module directory. If you don't already have a module created, try using the module generator first (`drush generate module`), and then run the `entity:content` generator.

In the command line, run `drush generate entity:content` and answer the questions. Your output may look something like the following. (Note: In this example, we had already created a module named `content_entity_example` and used it as the "Module machine name".)

**Tip:** Use a singular noun for the name of your content entity.

```
drush generate entity:content

 Welcome to content-entity generator!
––––––––––––––––––––––––––––––––––––––

 Module machine name [web]:
 ➤ content_entity_example

 Entity type label [Content Entity Example]:
 ➤ News

 Entity type ID [news_entity]:
 ➤ news

 Entity base path [/news]:
 ➤ /admin/content/news

 Make the entity type fieldable? [Yes]:
 ➤ 

 Make the entity type revisionable? [No]:
 ➤ Yes

 Make the entity type translatable? [No]:
 ➤ Yes

 The entity type has bundle? [No]:
 ➤ 

 Create canonical page? [Yes]:
 ➤ 

 Create entity template? [Yes]:
 ➤ 

 Create CRUD permissions? [No]:
 ➤ 

 Add "label" base field? [Yes]:
 ➤ 

 Add "status" base field? [Yes]:
 ➤ 

 Add "created" base field? [Yes]:
 ➤ 

 Add "changed" base field? [Yes]:
 ➤ 

 Add "author" base field? [Yes]:
 ➤ 

 Add "description" base field? [Yes]:
 ➤ No

 Create REST configuration for the entity? [No]:
 ➤ No

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • /var/www/html/web/modules/custom/content_entity_example/content_entity_example.links.action.yml
 • /var/www/html/web/modules/custom/content_entity_example/content_entity_example.links.contextual.yml
 • /var/www/html/web/modules/custom/content_entity_example/content_entity_example.links.menu.yml
 • /var/www/html/web/modules/custom/content_entity_example/content_entity_example.links.task.yml
 • /var/www/html/web/modules/custom/content_entity_example/content_entity_example.module
 • /var/www/html/web/modules/custom/content_entity_example/content_entity_example.permissions.yml
 • /var/www/html/web/modules/custom/content_entity_example/content_entity_example.routing.yml
 • /var/www/html/web/modules/custom/content_entity_example/src/NewsInterface.php
 • /var/www/html/web/modules/custom/content_entity_example/src/NewsListBuilder.php
 • /var/www/html/web/modules/custom/content_entity_example/src/Entity/News.php
 • /var/www/html/web/modules/custom/content_entity_example/src/Form/NewsForm.php
 • /var/www/html/web/modules/custom/content_entity_example/src/Form/NewsSettingsForm.php
 • /var/www/html/web/modules/custom/content_entity_example/templates/news.html.twig
```

### Explore the commands options

The generate command collects answers to questions that help determine if the entity should have bundles, should be revisionable, translatable, and fieldable. And thus, what code should be generated. In most cases your answers here will cause the generator to use different values in the annotations, different base classes, and in some cases even populate class methods with code.

#### Bundles

Bundles allow defining different entity subtypes with their own fields. It's similar to the *Node* entity content types or *Media* entity and its types. *Node*, *Media*, and *Taxonomy Term* are examples of bundleable entities in Drupal core. *User* is an example of a non-bundleable entity in Drupal since you cannot create different types of users and a concept of "roles" is used instead.

To determine whether to use bundles, ask yourself this question: Do I want administrators to be able to define new bundles of this entity type via the UI so that they can specify different fields per bundle but share other entity properties?

In our case, we don't need different types of *News*, so we answered *No* to the bundle question.

#### Translations and revisions

Questions that relate to entities being translatable and revisionable allow entities to support Drupal core's multilingual setup and utilize Drupal core revisions mechanisms that allow content editors to save, revert, and review different revisions (content states) of the entity. Ask yourself these questions: Do I want admins to be able to revert, save and view revisions of the entity content; is my site multilingual - needs to support multiple languages? We answered *Yes* to both of these questions.

Note: Unless you can articulate a good reason to *not* do, so we recommend making your custom content types translatable. You never know when you might need to translate content, and until you enable the content-translation-related features on your site, allowing your content types to be translatable will have little impact on the experience of editing your custom entity content.

#### Fieldable entities

Declaring an entity to be fieldable is a very important question and needs to be carefully considered before the entity is created. One of the advantages of a custom entity is the ability to declare all fields in one database table. By default, Drupal core creates at least one table per field, and two tables if the entity is revisionable. Declaring an entity non-fieldable allows it to store all of its fields data in one database table. This can be a significant win for performance, especially if you are planning to store a large amount of data for these entities.

However, it has its drawbacks. If an entity is not fieldable, then you won't be able to add fields through the normal Drupal *Manage fields* UI. All the fields will need to be declared in the entity definition class in code prior to installing the custom module. If any changes are needed, then the code needs to be updated and the module reinstalled, or an update hook needs to be declared.

Tip: If there are data points (fields) that your entity type requires be present on **all** entities of this type, or if the logic in your code expects the property to always exist, you'll likely want to add them as base fields. More below.

Alternatively, if the entity is fieldable then it has access to the same Drupal Field UI as *Node* or *Media* entities. This will allow you to create and manipulate fields through UI, but, as a downside, all the fields created through the UI will be created as separate database tables -- just like default Drupal core behavior for content types. This mitigates performance gains and essentially makes a custom entity very similar to *Node*.

Ask yourself these questions: Do I want administrators to be able to add and configure fields through the Drupal UI? Do I plan to store and display a list of thousands of custom entities on the website -- and performance is my biggest concern?

For this tutorial, we made the entity fieldable but also declared a few base fields in code to gain the benefits of the 2 described approaches. All base fields will be in 1 table, while all the fields that are added through the UI will have their own tables.

#### Base fields

The generator allows us to generate the schema for a fixed set of common base fields (fields that will be defined in the entity database table and will not be available through the *Managed fields* interface): title, author, created date, and changed date. It also allows you to create a *description* field similar to the taxonomy's *description* field.

Base fields settings can be adjusted through the *Manage form display* tab and *Manage display* tab for the entity. Unlike user-generated fields they cannot be removed from the entity type.

#### Advanced settings

The *CRUD permissions* question allows you to generate create, edit, view and delete permissions for the entity. If *No* is answered for this question, only a base *admin* permission will be generated. The generator also can help to generate a starting Twig template file for an entity, and REST configuration.

### Enable the module and verify it's working

Let's enable the module and check the entity in Drupal. In the command line, run `drush en content_entity_example` or replace *content\_entity\_example* with the machine name for the module you used. Then clear Drupal's cache using `drush cr -y`.

In your browser, navigate to the *Structure* admin menu item (*/admin/structure*). You should see a new item called *News*. Navigate there, and you should see settings for the *News* entity. Since we didn't specify any settings, the page should be empty. Choose *Manage fields* tab. You should see that we currently don't have any fields since the fields we defined were base fields and therefore aren't available through this UI. Since we made our entity fieldable we should see the *Add field* button available to us.

Choose *Manage form display* tab. You should see all the base fields we defined above in there. We can configure their form widget settings, visibility and order of appearance on this tab, just like we would be able to for *Node* content types.

Image

![Screenshot of News entity form display](../assets/images/news_entity_form_display.png)

Similarly, we can see the base fields on the *Manage display* tab and manipulate their settings.

## Recap

In this tutorial, we used the `drush generate entity:content` command to help speed up the process of authoring a custom content entity type. The command asks a set of questions related to common Entity API features, and then scaffolds the necessary code. In our case, we generated a new *News* content entity type.

## Further your understanding

- Take the time to review and understand the code that Drush generated for you.
- We generated a new module for the entity. Is it possible to generate a content entity in an existing module? How?
- Generate a configuration entity and explore the options of the generator.

## Additional resources

- [Drush official documentation](https://www.drush.org) (drush.org)
- [Drush Git repository](https://github.com/drush-ops/drush) (github.com)
- [Drupal Code Generator repository](https://github.com/Chi-teck/drupal-code-generator) (github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[ContentEntityType Attribute: Properties Reference](/tutorial/contententitytype-attribute-properties-reference?p=2607)

Next
[Working with Entity CRUD](/tutorial/working-entity-crud?p=2607)

Clear History

Ask Drupalize.Me AI

close
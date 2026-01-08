---
title: "Expose Custom Entities to Views"
url: "https://drupalize.me/tutorial/expose-custom-entities-views?p=2939"
guide: "[[views-drupal]]"
---

# Expose Custom Entities to Views

## Content

Drupal's Entity API allows developers to expose custom entities to the Views module, and takes care of many common features. It can handle exposing the fields associated with fieldable entity types for use as fields, filters, sorts, and arguments. It provides a way to customize any aspect of the Views integration, and makes it possible to create *explicit relationships* between 2 different entity types.

In this tutorial we'll:

- Expose a custom *Subscriber* content entity type and all of its data to Views.
- Create an explicit relationship between the custom content entity and Drupal core User entities.
- Build a view of *Subscriber* entities.

By the end of this tutorial you should know how to expose custom entities to Views.

## Goal

Expose a custom *Subscriber* entity type (generated with the help of Drush) to Views so that an administrator can create a view of all subscribers.

## Prerequisites

- [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity)
- [Annotations](https://drupalize.me/tutorial/annotations)

## Create a custom Subscriber entity type

For this tutorial we'll be using [Drush](https://drupalize.me/tutorial/install-drush-using-composer) to help generate code for our custom entity type. This creates the directory and file structure, and scaffolds some of the code.

The tutorial is split into 2 parts -- if you're looking to add Views integration to an existing entity type's code, you can skip ahead.

### Generate a module

We need a module to encapsulate our content entity code. We'll use Drush to scaffold a new module. In the terminal, navigate to the folder with your Drupal installation, run the following command, and answer the questions when prompted.

```
drush generate module
```

```
 Welcome to module generator!
––––––––––––––––––––––––––––––

 Module name [Web]:
 ➤ Subscriber

 Module machine name [subscriber]:
 ➤ 

 Module description [Provides additional functionality for the site.]:
 ➤ An example module                   

 Package [Custom]:
 ➤ 

 Dependencies (comma separated):
 ➤ 

 Would you like to create module file? [No]:
 ➤ 

 Would you like to create install file? [No]:
 ➤ 

 Would you like to create libraries.yml file? [No]:
 ➤ 

 Would you like to create permissions.yml file? [No]:
 ➤ 

 Would you like to create event subscriber? [No]:
 ➤ 

 Would you like to create block plugin? [No]:
 ➤ 

 Would you like to create a controller? [No]:
 ➤ 

 Would you like to create settings form? [No]:
 ➤ 

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • modules/custom/subscriber/subscriber.info.yml
```

**Result:** We created a new module called *Subscriber* (`subscriber`) and placed it inside the */modules/custom* folder.

### Generate an entity type

In the terminal, navigate to the folder with your Drupal installation, run the following command, and answer the questions when prompted.

```
drush generate entity:content
```

**Note:** This command requires Drush 10 and up.

```
Welcome to content-entity generator!
–––––––––––––––––––––––––––––––––––––––––––––

 Module machine name:
 ➤ subscriber

 Module name [Subscriber]:
 ➤

 Entity type label [subscriber]:
 ➤ Subscriber

 Entity type ID [subscriber]:
 ➤

 Entity class [Subscriber]:
 ➤

 Entity base path [/admin/content/subscriber]:
 ➤ 

 Make the entity type fieldable? [Yes]:
 ➤ 

 Make the entity type revisionable? [No]:
 ➤ 

 Make the entity type translatable? [No]:
 ➤ 
 
 The entity type has bundle? [No]:
 ➤ 
 
 Create canonical page? [Yes]:
 ➤ 

 Create entity template? [Yes]:
 ➤ No

 Create CRUD permissions? [No]:
 ➤ 

 Add "label" base field? [Yes]:
 ➤ No

 Add "status" base field? [Yes]:
 ➤ No

 Add "created" base field? [Yes]:
 ➤ No

 Add "changed" base field? [Yes]:
 ➤ No

 Add "author" base field? [Yes]:
 ➤ No

 Add "description" base field? [Yes]:
 ➤ No

 Create REST configuration for the entity? [No]:
 ➤ 

 The following directories and files have been created or updated:
–––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––––
 • modules/custom/subscriber/subscriber.links.action.yml
 • modules/custom/subscriber/subscriber.links.menu.yml
 • modules/custom/subscriber/subscriber.links.task.yml
 • modules/custom/subscriber/subscriber.permissions.yml
 • modules/custom/subscriber/subscriber.routing.yml
 • modules/custom/subscriber/config/install/system.action.subscriber_delete_action.yml
 • modules/custom/subscriber/src/SubscriberInterface.php
 • modules/custom/subscriber/src/SubscriberListBuilder.php
 • modules/custom/subscriber/src/Entity/Subscriber.php
 • modules/custom/subscriber/src/Form/SubscriberForm.php
 • modules/custom/subscriber/src/Form/SubscriberSettingsForm.php
```

**Result:** We generated a `Subscriber` content entity type with some boilerplate code.

We opted to skip things like making the entities revisionable, or translatable since we don't need that feature for this example. However, if you need those features go ahead and enable them. The Views integration works the same regardless, and is even smart about doing things like handling revisions automatically.

Learn more about creating content entity types in [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity).

### Modify the generated code

For this tutorial we'll assume that *Subscribers* need to be related to Drupal user accounts so that administrators are able to see which users are subscribed to the newsletter.

To connect users and subscribers we need to have matching fields in the base tables for both entities. In SQL terms this is your foreign key. Since every subscriber will have to have an email address filled in, we'll connect the Subscriber *email* field and the User *mail* fields.

By default, *email* isn't a base field option provided by the Drush generator. We need to manually add it to our *Subscriber* entity class.

Example *subscriber/src/Entity/Subscriber.php*:

```
class Subscriber extends ContentEntityBase implements SubscriberInterface {

  /**
   * {@inheritdoc}
   */
  public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {
    $fields = parent::baseFieldDefinitions($entity_type);

    // Add an email base field to the subscriber entity type.
    $fields['email'] = BaseFieldDefinition::create('email')
      ->setLabel(t('Email'))
      ->setDescription(t('The email of the subsciber.'))
      ->setDefaultValue('')
      ->setDisplayConfigurable('form', TRUE)
      ->setDisplayConfigurable('view', TRUE)
      ->setRequired(TRUE)
      ->addConstraint('UserMailRequired')
      ->addConstraint('UserMailUnique');

    return $fields;
  }

}
```

We also need to add 2 `use` statements, `use Drupal\Core\Field\BaseFieldDefinition;` and `use Drupal\Core\Entity\EntityTypeInterface;`. The `use` statement section should look like this:

```
use Drupal\Core\Field\BaseFieldDefinition;
use Drupal\Core\Entity\ContentEntityBase;
use Drupal\subscriber\SubscriberInterface;
use Drupal\Core\Entity\EntityTypeInterface;
```

In the snippet above we create a definition for the *Email* field. We set its label, description, and default value. We expose it to the *Manage form display* section via the `setDisplayConfigurable('form', TRUE)` line. Then the `setDisplayConfigurable('view', TRUE)` line exposes the *Email* field to the *Manage display* section of Drupal's UI. Finally, we add some validation constraints for the field to make sure the value is required and unique. This is like if someone added a new email field to the entity type via the UI, but base fields are mandatory and cannot be removed from an entity type.

### Enable the module and add some fields

Enable the new *Subscriber* module:

```
drush en subscriber
```

Then in the *Manage* administration menu, navigate to *Structure* > *Subscriber* (*admin/structure/subscriber*). Choose the *Manage fields* tab. Add plain text fields for *First name* and *Last name*. Switch to the *Manage form display* tab and drag *Email* field out of the *Disabled* section and adjust other settings for all the fields as required.

**Note:** Adding fields through the UI creates a table for every field and will remove the benefit of a flat table structure without joins, which is one of the advantages of custom entities. In real life, you may want to define all fields like the email field above. For this tutorial we'll use the UI.

Your field structure may look something like the following:

Image

![Screenshot of fields for the subscriber entity.](/sites/default/files/styles/max_800w/public/tutorials/images/subscriber_fields.png?itok=Q3e2h-Kr)

### Add some example content

1. Using the *Manage* administration menu, navigate to *Content* > *Subscriber* (*/admin/content/subscriber*).
2. Press the *Add subscriber* button.
3. Create 2 to 3 entries to have some content for the View.

Example:

Image

![Screenshot of fields for the subscriber entity.](/sites/default/files/styles/max_800w/public/tutorials/images/subscribers.png?itok=rLweXAE7)

## Integrate a custom entity type with Views

Next we need to expose the data from our custom content entity type to Views so that administrators can build views that display subscriber data.

In your entity types annotation, you define a `"views_data"` handler, which points to the class responsible for integrating your entity type with Views.

Example annotation:

```
/**
 * Defines the subscriber entity class.
 *
 * @ContentEntityType(
 *   id = "subscriber",
 *   label = @Translation("Subscriber"),
 *   label_collection = @Translation("Subscribers"),
 *   handlers = {
 *     "view_builder" = "Drupal\subscriber\SubscriberViewBuilder",
 *     "list_builder" = "Drupal\subscriber\SubscriberListBuilder",
 *     "views_data" = "Drupal\views\EntityViewsData",
 *     "form" = {
 *       "add" = "Drupal\subscriber\Form\SubscriberForm",
 *       "edit" = "Drupal\subscriber\Form\SubscriberForm",
 *       "delete" = "Drupal\Core\Entity\ContentEntityDeleteForm"
 *     },
 *     "route_provider" = {
 *       "html" = "Drupal\Core\Entity\Routing\AdminHtmlRouteProvider",
 *     }
 *   },
 *   base_table = "subscriber",
 *   revision_table = "subscriber_revision",
 *   show_revision_ui = TRUE,
 *   admin_permission = "administer subscriber",
 *   entity_keys = {
 *     "id" = "id",
 *     "revision" = "revision_id",
 *     "label" = "id",
 *     "uuid" = "uuid"
 *   },
 *   revision_metadata_keys = {
 *     "revision_log_message" = "revision_log"
 *   },
 *   links = {
 *     "add-form" = "/admin/content/subscriber/add",
 *     "canonical" = "/subscriber/{subscriber}",
 *     "edit-form" = "/admin/content/subscriber/{subscriber}/edit",
 *     "delete-form" = "/admin/content/subscriber/{subscriber}/delete",
 *     "collection" = "/admin/content/subscriber"
 *   },
 *   field_ui_base_route = "entity.subscriber.settings"
 * )
 */
```

In this example, the line `* "views_data" = "Drupal\views\EntityViewsData",` tells the Entity API to use the core `Drupal\views\EntityViewsData` class to handle integration with Views. This class will take care of making sure that Views knows about any fields you attach to your entity type via the UI, any base fields defined in code, revisions, translations, CRUD links, and more. It's quite robust, and often the integration it provides is enough.

When it's not, you can create a new class that extends `Drupal\views\EntityViewsData`, and update the annotation to point to your custom class. Then within that class you can perform any logic required. We're going to do that to define an explicit relationship between our *Subscriber* entity type and Drupal core *User* entities.

### Define a `ViewsData` class

In the *subscriber* module's directory create a new file named *src/SubscriberEntityViewsData.php* with the following content:

```
<?php
/**
 * @file
 */

namespace Drupal\subscriber;

use Drupal\views\EntityViewsData;

class SubscriberEntityViewsData extends EntityViewsData {

  /**
   * {@inheritdoc}
   */
  public function getViewsData() {
    $data = parent::getViewsData();

    // Add your custom data descriptions here.

    return $data;
  }

}
```

Custom *ViewsData* classes should extend the core `EntityViewsData` class. At a minimum they need to implement `\Drupal\views\EntityViewsDataInterface`. In our class we override the `getViewsData()` method, and will use this as the place to make changes to the description of our data that Views sees. This works like `hook_views_data()`.

### Add relationship to User entities

To add a relationship pointing to Drupal *User* entities we'll need to modify the `getViewsData()` method.

The return value of `getViewsData()` is the same as *hook\_views\_data()*, an associative array that describes the different fields, and their associated handlers, to Views. You can learn more about the structure of this array in [Expose a Custom Database Table to Views](https://drupalize.me/tutorial/expose-custom-database-table-views).

The `\Drupal\views\EntityViewsData` base class will take care of adding both the base fields and the fields configured via the UI for *Subscriber* entities, as long as you remember to call `$data = parent::getViewsData()`.

Let's modify the array to add a relationship to User entities. Your code may look like the below:

```
  /**
   * {@inheritdoc}
   */
  public function getViewsData() {
    $data = parent::getViewsData();

    // Note that $data['subscriber']['email'] was already defined when the base
    // class added data about base fields. We're extending that definition here.
    // Though you could also override it completely. Or add entirely new fields
    // here as well.
    $data['subscriber']['email']['relationship'] = [
      'title' => $this->t('Related users'),
      'help' => $this->t('Relate users to subscribers.'),
      'base' => 'users_field_data',
      'base field' => 'mail',
      // ID of relationship handler plugin to use.
      'id' => 'standard',
      // Default label for relationship in the UI.
      'label' => $this->t('Related users'),
    ];

    return $data;
  }
```

In the code above we're connecting 2 tables: the `subscriber` table and the `users_field_data` table via the *email* and *mail* fields respectively. We add `title` and `help` properties that show up in the *Relationship* section of the Views UI. The data structure `$data[‘subscriber’][‘email’]` defines the entity table for which the relationship will be available when this table is used as a base in Views.

Under the `relationship` key we have a `base` key that defines a table to join to. In our case we are joining to the `users_field_data` table. The `base field` defines the field on which join will be executed in the base table. We join by `email`, so we used the corresponding `mail` field in the `users_field_data` table. `id` key defines the relationship plugin. In our case we are using *standard* join. We also specified a label that will show up when the relationship is in use.

### Edit the `@ContentEntity` annotation

We need to point to our new class in the annotation for the Subscriber entity type. In *src/Entity/Subscriber.php* change the `views_data` handler from:

```
"views_data" = "Drupal\views\EntityViewsData",
```

To:

```
"views_data" = "Drupal\subscriber\SubscriberEntityViewsData",
```

Then [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) and it's time to build a View.

## Build a view to test

To test that it's working, let's create a View of subscribers. Navigate to *Structure* > *Views* > *Add view* (*/admin/structure/views/add*). Fill in the View name and then in the *View settings* section select *Subscriber* in the *show* area. Create a page display and choose to render subscribers as entities (*Format* > *Show*, select *Subscriber*). Your views settings may look something like the following:

Image

![Screenshot of settings of the Views wizard for Subscribers view](/sites/default/files/styles/max_800w/public/tutorials/images/subscribers_add_view.png?itok=U7nqI9bQ)

Press *Save and edit*. On the next page, scroll down to the preview area and you should see all the subscribers rendered in the default view mode.

Let's make this view more functional by adding operations links. Switch the display format to fields (*Format* > *Show*, select *Fields*) and set them to be displayed as a table (*Format*, select *Table*). You may add other fields from the entity as you'd like. In our case we will add *First Name* and *Last Name*. Add those fields, and also add *Operations links* as a field.

The preview of your view should look something like the following:

Image

![Screenshot of subscribers view preview](/sites/default/files/styles/max_800w/public/tutorials/images/subscribers_view_preview.png?itok=EKTbEZGD)

Our view now resembles the content administration view with operations links and fields.

### Test the relationship

It's good to have a subscribers management view, but it would be valuable to show subscribers in relation to user accounts.

Let's add a relationship to the view. Expand the *Advanced* section of the view's editing form and select *Add* under *Relationships* . Then search for *Related users*, select it, and press *Add and configure relationships*.

Image

![Screenshot of related users relationship](/sites/default/files/styles/max_800w/public/tutorials/images/rel_subs.png?itok=JbuoSkGv)

Now fields from User entities should be available in Views. Press *Add* in the *Fields* section and add the *Email* field in the *User* category. Now administrators can see user emails and which users on the site are subscribers. Rearrange the fields by selecting the dropdown arrow next to *Add* in the *Fields* section, and select *Rearrange*. Drag the Operations links field to the end of the list.

A preview of the results may look something like the following:

Image

![Screenshot of the final results preview for subscribers view](/sites/default/files/styles/max_800w/public/tutorials/images/subs_preview.png?itok=SJOG_FrC)

This works because of the custom relationship definition we added.

## Recap

In this tutorial we learned how to expose custom entities to Views. We learned about the `Drupal\views\EntityViewsData` handler provided by core, and that it can do a lot of the hard work of exposing the fields associated with an entity. Then we explored how to specify an explicit relationship between custom entities and the base tables of other entities, allowing an administrator to connect them through the Views UI. We accomplished this by defining our own *ViewsData* class, editing the entity annotation to use the new class, and the implementing the `getViewsData()` method to expand the default definition of our entity type.

When these pieces of code are in place, you can create views of your custom entities through the Views UI.

## Further your understanding

- When building a view of subscribers, how did Views know about the operations fields and other data it could access?
- Using a debugger, compare the `$data` array in the `getViewsData()` method and `hook_views_data()`. How is it similar? What is different?
- We specified the relationship between subscriber entities and user entities that exposed users to the subscribers view. How would you expose subscriber entities to views of user entities?

## Additional resources

- [Documentation on the hook\_views\_data()](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_data) (api.drupal.org)
- [Documentation on Entity API](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Entity!entity.api.php/group/entity_api) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Relationships Between 2 Tables in Views](/tutorial/add-relationships-between-2-tables-views?p=2939)

Next
[Overview: Views Plugins](/tutorial/overview-views-plugins?p=2939)

Clear History

Ask Drupalize.Me AI

close
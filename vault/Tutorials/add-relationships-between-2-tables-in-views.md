---
title: "Add Relationships Between 2 Tables in Views"
url: "https://drupalize.me/tutorial/add-relationships-between-2-tables-views?p=2939"
guide: "[[views-drupal]]"
---

# Add Relationships Between 2 Tables in Views

## Content

In [Expose a Custom Database Table to Views](https://drupalize.me/tutorial/expose-custom-database-table-views) we learned how to let Views know about custom tables created by a Drupal module. In that example, the custom table was a stand-alone one, without any connections to the other tables in the database. However, it's common for data in one table to relate to data in another.

For example, you might have `TableA` with the columns `first_name, last_name, email` and `TableB` with the columns `email, score`. `TableA.email` and `TableB.email` can be used to join the two tables together.

It's useful to define these relationships for Views so that when `TableA` is used as the base table the fields from `TableB` are also available in the view. When the fields from a related table are automatically loaded, this is known as an *implicit relationship*. Our earlier example could benefit from the relationship with the *users\_field\_data*. This relationship will allow us to associate *First Name* and *Last Name* fields from the subscriptions table with the users on the site.

In this tutorial we'll:

- Define the difference between *implicit* and *explicit* relationships in Views.
- Learn how to create an implicit relationship between 2 tables using `hook_views_data`.

By the end of this tutorial you should know how to describe custom implicit relationships in a view, making data from one or more secondary tables available to the Views query builder.

## Goal

Use `hook_views_data()` to expose the relationship between a custom `subscribers` table and the Drupal core `users` table in a view.

## Prerequisites

- [Overview: Build and Render Cycles in Views](https://drupalize.me/tutorial/overview-build-and-render-cycles-views)
- [Expose a Custom Database Table to Views](https://drupalize.me/tutorial/expose-custom-database-table-views)

## Initial setup

This tutorial assumes you've already completed [Expose a Custom Database Table to Views](https://drupalize.me/tutorial/expose-custom-database-table-views). In that tutorial we implemented `hook_views_data()` to expose a table that stores newsletter subscriptions. Then we created a view of the data in that table. This current set up doesn't allow us to use Views to see how many users are also newsletter subscribers. So we are going to add a relationship between the custom *news\_subs* table and the Drupal core *users\_field\_data* table. Then we can expose newsletter subscriber data in things like the *People* administration view.

Views supports two types of relationships:

- *Implicit relationships* connect a custom table to another base table, usually an entity type. When the related table is used as a base for a view, the fields of the custom table will be loaded and available to add in the *Fields* section without the need to add the relationship handler in the *Relationship* section of the view.
- *Explicit relationships* use a specified relationship handler and work similar to entity reference fields. A common use case would be to relate a `custom_table.uid` field to a User entity. These relationships need to be explicitly added in the *Views UI* to make use of them. Learn more about creating explicit relationships in [Expose Custom Entities to Views](https://drupalize.me/tutorial/expose-custom-entities-views).

### Add the relationship

To add an implicit relationship we need to know a few parameters:

- The machine name of the table we want to relate our table to. In this example it's *users\_field\_data*.
- Which field in our custom table we'll use as the *key* field. This field should contain data that is present in both tables. Essentially this is our foreign key from the other table.

In our example the *email* field in the *news\_subs* table can act as a foreign key from the *users\_field\_data* table. In the *users\_field\_data* table the corresponding field is *mail*. Now that we know the machine name of the other table, and names of the two fields that we'll use to construct the relationship between tables, we can modify the code in our `hook_views_data()` implementation like below:

```
/**
 * Implements hook_views_data().
 */
function news_views_data() {
  $data = [];
  $data['news_subs'] = [];
  // Table.
  $data['news_subs']['table'] = [
    'group' => t('News Subscriptions'),
    'provider' => 'news',
    'base' =>  [
      'field' => 'email',
      // Label in the UI.
      'title' => t('News Subscriptions'),
      'help' => t('News subscriptions custom table'),
    ]
  ];

  // This table references the {users_field_data} table.
  // The declaration below creates an
  // 'implicit' relationship to the table, so that when it is the base
  // table, the fields are automatically available.
  $data['news_subs']['table']['join'] = [
    // The key of this inner array is the name of the table to join to.
    'users_field_data' => [
      // The primary key in the referenced table e.g.) user_field_data.mail.
      'left_field' => 'mail',
      // The foreign key in this table e.g.) news_subs.email.
      'field' => 'email',
    ],
  ];

  // Fields.
  $data['news_subs']['email'] = [
    'title' => t('Email'),
    'help' => t('Subscription email.'),
    'field' => [
      'id' => 'standard',
    ],
    'sort' => [
      'id' => 'standard',
    ],
    'filter' => [
      'id' => 'string',
    ],
    'argument' => [
      'id' => 'string',
    ],
  ];

  $data['news_subs']['first_name'] = [
    'title' => t('First name'),
    'help' => t('Subscriber\'s first name.'),
    'field' => [
      'id' => 'standard',
    ],
    'sort' => [
      'id' => 'standard',
    ],
    'filter' => [
      'id' => 'string',
    ],
    'argument' => [
      'id' => 'string',
    ],
  ];

  $data['news_subs']['last_name'] = [
    'title' => t('Last name'),
    'help' => t('Subscriber\'s last name.'),
    'field' => [
      'id' => 'standard',
    ],
    'sort' => [
      'id' => 'standard',
    ],
    'filter' => [
      'id' => 'string',
    ],
    'argument' => [
      'id' => 'string',
    ],
  ];

   return $data;
}
```

The important part of this updated code is the new `$data['news_subs']['table']['join']` array element. It declares the name of the table we want to join to, and the names of the fields to use on the left and right sides of the join. We only added one join here, but you could join to more tables by adding them to the `'join'` array.

### Edit the *People* administration view

In the *Manage* administration menu, navigate to *Structure* > *Views* (*admin/structure/views*), then press the *Edit* button for the *People* view.

Next, press the *Add* button in the *Fields* section of the view. Start entering **First Name** in the search field and you should see the *First Name* field from the custom subscriptions table.

Example:

Image

![Screenshot of addition of the first name field from subscribers table to the people view.](/sites/default/files/styles/max_800w/public/tutorials/images/add_first_name_to_view.png?itok=yEzzcbkW)

In the screenshot you can see that we have the *First Name* field with the *News Subscriptions* category available in the list of fields. Add it to the view along with the *Last Name* field from the *News Subscriptions* table and drag them to the top of the list to be displayed right after the *Username* field.

Scroll the page to the preview area of the view and you should see the new fields displayed.

Image

![Screenshot of addition of the first name field from subscribers table to the people view.](/sites/default/files/styles/max_800w/public/tutorials/images/views_preview_relationship.png?itok=gjqFmr7z)

You may notice that we have two users in the screenshot above: *sitesuper*, an administrator, and *john*. In this example, John Doe is subscribed to our newsletter. This modification already provides a way for administrators to see which users are also subscribers. But we can make this clearer.

### Make it easier to differentiate subscribed users

Let's make the subscription status a little more visible to the administrators. We have a few ways to do it: modify subscriptions table to store subscription status or update the view.

Since our custom table only stores active subscribers and *Email* field is required for all subscribers, let's utilize this condition to override the value and show *Yes* instead of the email address in our view if the user has an entry in the subscriptions table.

Press the *Add* button in the *Fields* section of the *People* view and enter *Email* in the field search. Some of the results may be coming from the *User* category. We need to select the one that is coming from the *Newsletter Subscriptions* category as that's the one from our custom subscriptions table.

Image

![Screenshot of addition of the first name field from subscribers table to the people view.](/sites/default/files/styles/max_800w/public/tutorials/images/subscriptions_email_field.png?itok=ieRvR1Vz)

Press the *Add and configure fields* button. In the field settings dialogue, open the *Rewrite results* accordion and select the option *Override the output of this field with custom text*. In the *Text* field enter *Yes*.

Change the field label above to say *Subscriber?*. Then press *Apply*. Rearrange the fields so that the new one appears right after the original *Email* field in the fields section of the view. Scroll to the preview area and you should see the text "Yes" display next to each user subscribed to the newsletter.

Image

![Screenshot of addition of the first name field from subscribers table to the people view.](/sites/default/files/styles/max_800w/public/tutorials/images/subscriber_status.png?itok=NLH-iiOg)

Make sure to save the view to preserve your changes.

## Recap

In this tutorial we learned how to add an implicit relationship between custom tables described in a `hook_views_data()` implementation. This allows us to expose fields stored in a custom table to other base tables inside of Views without the need to add relationships through the Views UI. To add an implicit relationship, both tables need to be connected via *key* fields which contain the same data in both tables. To describe the relationships you'll need to know the machine names of the *key* fields, and a machine name of the joined table. Then you need to add a new *join* index to the *table* array in `hook_views_data()` that describes the relationship.

## Further your understanding

- Can you add an *Is Subscriber* column to the custom table and expose it to Views?
- In MySQL terms is this a `LEFT JOIN` or an `INNER JOIN`? Why does that matter?

## Additional resources

- [`hook_views_data()` documentation](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_data/) (api.drupal.org)
- [List of views hooks](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/11.x) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Expose a Custom Database Table to Views](/tutorial/expose-custom-database-table-views?p=2939)

Next
[Expose Custom Entities to Views](/tutorial/expose-custom-entities-views?p=2939)

Clear History

Ask Drupalize.Me AI

close
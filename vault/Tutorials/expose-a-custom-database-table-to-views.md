---
title: "Expose a Custom Database Table to Views"
url: "https://drupalize.me/tutorial/expose-custom-database-table-views?p=2939"
guide: "[[views-drupal]]"
---

# Expose a Custom Database Table to Views

## Content

Any Drupal module that provides custom database tables should implement `hook_views_data()` to describe the schema of those tables to Views. This hook is used to provide information to Views about the fields in a table, their human-readable names, and the types of data (string, integer, date, etc.) stored in each column. You can also tell Views how it should handle sorting, filtering, and formatting the data. Implementations of `hook_views_data()` can also be used to describe relationships between tables.

If you're creating a module that implements `hook_schema()` and adds new tables to the database it's a good idea to also add support for Views. Among other things, it'll allow administrators to create any user-facing displays of data from your table using Views. Then, they can be edited without having to write code. Once you've described your table to Views via `hook_views_data()` Views will be able to provide a way for administrators to construct queries against your data via the UI.

In this tutorial we'll:

- Use `hook_views_data()` to expose a custom table defined in a Drupal module to Views.
- Learn how to describe different types of data to Views.
- Demonstrate the relationship between `hook_views_data()` and what a site administrator has access to in the Views UI.

By the end of this tutorial you should know how to describe custom database tables and their fields to the Views module.

## Goal

Use `hook_views_data()` to expose a custom table of newsletter subscribers to the Views module.

## Prerequisites

- [Overview: Build and Render Cycles in Views](https://drupalize.me/tutorial/overview-build-and-render-cycles-views)
- [Implement Any Hook](https://drupalize.me/tutorial/implement-any-hook)

## Setup demo module

For this tutorial we're going to create a custom module named *news* with a custom database table named *news\_subs* that stores subscriptions to our newsletter. We'll collect a subscriber's first and last name, email address, and a flag indicating if their subscription is active or not.

This is for demonstration purposes. If you've already got a module with a custom database table, use that; the process for describing it to Views is the same. Feel free to skip this set-up step.

Our *news* module has the following in the *news/news.install* file:

```
/**
 * Implements hook_schema().
 */
function news_schema() {
  $schema['news_subs'] = [
    'description' => 'Newsletter subscriptions',
    'fields' => [
      'first_name' => [
        'description' => 'First Name',
        'type' => 'varchar',
        'length' => 32,
        'not null' => TRUE,
        'default' => '',
      ],
      'last_name' => [
        'description' => 'Last Name',
        'type' => 'varchar',
        'length' => 32,
        'not null' => TRUE,
        'default' => '',
      ],
      'email' => [
        'description' => 'Email',
        'type' => 'varchar',
        'length' => 32,
        'not null' => TRUE,
        'default' => '',
      ],
      'created' => [
        'description' => 'Created',
        'type' => 'int',
        'length' => 11,
        'not null' => TRUE,
        'default' => 0,
      ],
      'is_active' => [
        'description' => 'Is Active?',
        'type' => 'int',
        'size' => 'tiny',
        'default' => 0,
        'not null' => TRUE,
      ],
    ],
  ];

  return $schema;
}
```

This describes our custom database table. When the module is installed Drupal will create the *news\_subs* table for us. If you'd like a refresher on `hook_install()` or schema definitions, check out [the documentation](https://api.drupal.org/api/drupal/core!lib!Drupal!Core!Extension!module.api.php/function/hook_install).

Ensure the module is enabled, and the table exists:

```
drush en -y news
drush cr -y
```

If you have database management software, connect to your Drupal site's database and search for the *news\_subs* table in the tables list. You should have a table that looks something like the following:

Image

![Screenshot of the database news_subs table](/sites/default/files/styles/max_800w/public/tutorials/images/news_subs_db.png?itok=Oqh1T8EF)

### Populate the table with some data

In a real life scenario, your table will probably be populated by the submit handler of a subscription form. For this demonstration we'll manually populate the table with some mock data, so we can see real results in Views while testing.

Using your database management tool of choice, run a couple of direct `INSERT` queries like the following:

```
INSERT INTO news_subs (first_name, last_name, email, created, is_active) VALUES ('John', 'Doe', '[email protected]', UNIX_TIMESTAMP(), 1);
```

Update values in the query and run it a couple of times to populate the table with some records. At the end your table should look something like the one below:

```
MariaDB [db]> select * from news_subs;
+------------+-----------+------------------------+------------+-----------+
| first_name | last_name | email                  | created    | is_active |
+------------+-----------+------------------------+------------+-----------+
| John       | Doe       | [email protected]   | 1612890298 |         1 |
| Jane       | Doe       | [email protected]   | 1612890308 |         1 |
| Justa      | Fish      | [email protected] | 1612890377 |         0 |
+------------+-----------+------------------------+------------+-----------+
```

## Describe your custom database table to Views

### Make a list of fields

Start by making a list of the fields you want to expose to Views. You can get the field names by looking at the module's `hook_schema()` implementation, or at the database itself. Make note of the *type* of data the field stores, such as numbers, strings, references to other tables, etc.

In our example this is:

| field | data type |
| --- | --- |
| first\_name | string |
| last\_name | string |
| email address | string |
| created | date |
| is\_active | boolean |

### Define `hook_views_data()`

Implement `hook_views_data()` to describe your custom table to Views.

Add a `hook_views_data()` function to the *news.module* file with the following content:

```
/**
 * Implements hook_views_data().
 */
function news_views_data() {
  $data = [];
  $data['news_subs'] = [];

  // Describe a single database table named news_subs.
  $data['news_subs']['table'] = [
    // Human-readable name of this table used in the Views UI to prefix fields,
    // filters, etc. Example: "News subscriptions: Email". This string should
    // be translatable.
    'group' => t('News subscriptions'),
    
    // Name of the module that provides the table schema.
    'provider' => 'news',
    
    // A table can be a "base" table, meaning that in Views you can use it as
    // base for a View. Non-base tables can be associated to a base table via
    // a relationship. The primary table for your custom data should be a base
    // table. Add the "base" key with the following properties:
    'base' =>  [
      // Identifier (primary) field in this table for Views.
      'field' => 'email',
      // Label in the UI.
      'title' => t('News subscriptions'),
      // Longer description in the UI. Required.
      'help' => t('News subscriptions custom table'),
    ]
  ];

  // Other top level elements of the news_subs array define the individual
  // columns of the table that you want to make available to Views. The key is
  // the name (and must be unique) used by Views. It's usually the same as the
  // name of the database column it describes. But doesn't have to be. It's
  // possible to created computed fields that are not a one-to-one relationship
  // to a column in the database. For example, a field that contains a link to
  // edit a record from the table.
  //
  // The 'title' and 'help' elements are required.
  //
  // Each field definition needs to describe the views plugins (frequently
  // called "handlers") that are responsible for handling the fields data in
  // different scenarios including: field, filter, sort, argument, area, and
  // relationship. All of which are optional.
  $data['news_subs']['email'] = [
    // Human-readable name of the field that will be displayed in the UI.
    'title' => t('Email'),
    // Required help text that describes the content of the field.
    'help' => t('Subscription email.'),
    // Optional handler to use when displaying a field. This maps to what a user
    // will see in the "Fields" section of the Views configuration UI. Specify
    // this if you want a user to be able to display the content of this field.
    'field' => [
      // ID of field handler plugin to use. More information about this below.
      'id' => 'standard',
    ],
    // Optional handler to use when sorting field data. This maps to what a user
    // will see in the "Sort criteria" section of the Views configuration UI.
    // Specify this if you want a user to be able to sort a Views results based
    // on the content of this field.
    'sort' => [
      'id' => 'standard',
    ],
    // Optional handler to use when filtering results based on a field. This
    // maps to what a user will see in the "Filter criteria" section of the
    // Views configuration UI. Specify this if you want a user to be able to
    // filter a Views results based on the content of this field.
    'filter' => [
      'id' => 'string',
    ],
    // Optional handler to use when making this field available as an argument.
    // This maps to what a user will see in the "Contextual filters" section of
    // the Views configuration UI. Specify this if you want a user to be able to
    // use this field in contextual filters.
    'argument' => [
      'id' => 'string',
    ],
  ];

  // More examples of field descriptions.
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

  $data['news_subs']['created'] = [
    'title' => t('Created'),
    'help' => t('Subscription date'),
    'field' => [
      'id' => 'date',
    ],
    'sort' => [
      'id' => 'date',
    ],
    'filter' => [
      'id' => 'date',
    ],
    'argument' => [
      'id' => 'date',
    ],
  ];

  $data['news_subs']['is_active'] = [
    'title' => t('Is Active?'),
    'help' => t('Is it an active subscriber?'),
    'field' => [
      'id' => 'boolean',
    ],
    'sort' => [
      'id' => 'numeric',
    ],
    'filter' => [
      'id' => 'boolean',
    ],
    'argument' => [
      'id' => 'standard',
    ],
  ];

   return $data;
}
```

This hook doesn't take any arguments, and it needs to return an associative array describing the structure of your custom table. We added some inline comments to the example code above to help you get started. The documentation for `hook_views_data()` contains some good example code as well.

A lot of what you're doing in this array is telling Views what string(s) to use in the UI when an administrator is working with a field, and which plugin(s) to use when handling a field's data in different scenarios. This is accomplished by including the *ID* of the plugin you want to use. It's helpful to be familiar with the concept of plugins; you can learn more in [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins) In this case you can think of the *ID* you enter in the `$data` array as the indicator of what PHP class to use for the operation. When Views needs to know how to filter on a field's data, for example, it'll instantiate an instance of the required plugin and populate it with the data from the database.

The tricky part is figuring out what plugins are available, and what their *IDs* are. The best place to look right now is [api.drupal.org](https://api.drupal.org/api/drupal), but note that this only lists the plugins provided by Drupal core; contributed modules may provide additional plugins.

| Plugin type | Description |
| --- | --- |
| [Field handler plugins](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!views!field!FieldPluginBase.php/group/views_field_handlers/) | These plugins are responsible for both querying the database and displaying the content of a field. |
| [Filter handler plugins](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!views!filter!FilterPluginBase.php/group/views_filter_handlers/) | These plugins are responsible for handling filtering a Views results and can do things like indicate that a column which looks like an integer is actually a timestamp and for filtering purposes you might want to filter a date range. |
| [Sort handler plugins](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!views!sort!SortPluginBase.php/group/views_sort_handlers/) | These plugins are responsible for understanding how to sort based on a field's data. For example, knowing that an integer represents a timestamp and how that influences sorting. |
| [Argument handler plugins](https://api.drupal.org/api/drupal/core!modules!views!src!Plugin!views!argument!ArgumentPluginBase.php/group/views_argument_handlers/) | Deal with processing contextual data and assist in building the query for a View. |
| [Additional Views related plugin types](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/group/views_plugins/) | This page lists all available Views plugin types. |

To find the *ID* of a plugin, check its attribute. For example, the *StringFilter* plugin attribute looks like the following:

```
/**
 * Basic textfield filter to handle string filtering commands.
 *
 * Including equality, like, not like, etc.
 *
 * @ingroup views_filter_handlers
 */
#[ViewsFilter("string")]
class StringFilter extends FilterPluginBase implements FilterOperatorsInterface {
```

The *ID* is defined in the `#[ViewsFilter("string")]` attribute, and in this case, it's *string*. This is the value you'll use in the `$data` array in your `hook_views_data()` implementation.

After defining or editing your `hook_views_data()` code, you'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).

### Build a test view

1. Using the *Manage* administrative menu, navigate to *Structure* > *Views* (*admin/structure/views*).
2. Press the *+ Add view* button.
3. Create a view using the new type *News subscriptions* option and then select *Add page*. Note that this new option relates to the "base" table defined above in our implementation of `hook_views_data`.

Image

![Screenshot of the view wizard](/sites/default/files/styles/max_800w/public/tutorials/images/subs_view_wizard.png?itok=gPlrff2j)

1. Press *Save and edit*.
2. On the next screen add the *First name*, *Last name*, *Email*, *Is active*, and *Created* fields to the View.

Example:

Image

![Screenshot of the news subscribers view edit screen](/sites/default/files/styles/max_800w/public/tutorials/images/news_subscribers_view.png?itok=bSFJb1m0)

1. Scroll to the preview area and you can see the results:

Image

![Screenshot of the news subscribers view preview](/sites/default/files/styles/max_800w/public/tutorials/images/news_subs_preview.png?itok=KNamZDz2)

The results can also be viewed on the front-end at the path defined for this page display.

## Recap

In this tutorial, we learned how to expose a custom database table to Views using `hook_views_data()`. This makes the fields, and everything we know about the data they contain, visible to administrators using the Views UI. Then it allows them to display, filter, sort, and more using these fields.

## Further your understanding

- How would you define the relationship to the *Users* table in this example? Hint: use the `join` key for a table.
- Try using the fields we exposed in the View as filters, sorts or inside header or footer areas to get a sense for how the different plugins work.

## Additional resources

- [List of views hooks](https://api.drupal.org/api/drupal/core%21modules%21views%21views.api.php/11.x) (api.drupal.org)
- [Hook\_views\_data documentation](https://api.drupal.org/api/drupal/core!modules!views!views.api.php/function/hook_views_data/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Alter the Query Used for a View](/tutorial/alter-query-used-view?p=2939)

Next
[Add Relationships Between 2 Tables in Views](/tutorial/add-relationships-between-2-tables-views?p=2939)

Clear History

Ask Drupalize.Me AI

close
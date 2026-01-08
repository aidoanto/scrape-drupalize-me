---
title: "Index Reference Fields"
url: "https://drupalize.me/tutorial/index-reference-fields?p=2815"
guide: "[[drupal-site-administration]]"
---

# Index Reference Fields

## Content

Reference field types, such as taxonomy term fields, paragraph fields, or plain entity reference fields, refer to a completely separate entity within the site. This makes search configuration complicated as the typical scope of a search crawl is on a per-node (really a per-entity) basis. Fortunately there are known strategies to index these fields with ease.

In this tutorial, we'll:

- Describe why reference types pose a particular challenge to indexing
- Discuss the importance of display modes in indexing
- Highlight how the **Rendered HTML Output** field can be used to index paragraphs

By the end of this tutorial you should be able to add reference fields to your Search API Index and allow users to search their contents in the correct context.

## Goal

Modify an existing Search API index to crawl a complex field type, such as a taxonomy reference field.

## Prerequisites

- [Create Search API Indexes](https://drupalize.me/tutorial/create-search-api-indexes)
- [Populate Search API Indexes](https://drupalize.me/tutorial/index-reference-fields)

## Taxonomy term fields

Tag fields are the most common kind of reference field types that need to be included in a search index. Tag names often correspond to search query keywords, and should be given special attention. In the database, a tag field value is stored as a row in a table. The key column in that table refers to the term entity ID number.

While we could index the entity ID number, it wouldn't be particularly useful in search results. Instead, we should index the **name** field on the underlying term entity. Thankfully, Search API understands term reference fields out of the box.

### Add the term reference field to the Search API index

In the web UI, reference fields appear as hierarchical components below the field name. We can traverse the reference and select components on the target entity to add to the Search API index.

When adding tags to a Search API index, we want to take special care in selecting the field **type**. The default type, **string**, treats tag names as complete values. While this is a good assumption for tags in general, it also makes it unavailable for fulltext searches. As a result, we want to choose a different field type.

The **fulltext unstemmed** type removes some additional processing -- stemming -- which attempts to find the roots of plurals and conjugated verbs. Since tags are more like keywords, we want to disable this additional processing.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Locate the index you created earlier and open it for editing.
4. Open the *Fields* tab.
5. Click *Add fields*.
6. The *Add field to index...* modal dialog appears. Scroll through the list and locate the *Tags* field.
7. Click the `(+)` link next to the *Tags* field to expand it.
8. Expand the *Taxonomy Term* item that appears by clicking the `(+)` next to it.
9. Scroll through the list of Term entity fields that appear. Click *Add* next to the *name* field.
10. Click *Done* to dismiss the modal dialog.
11. Select the *Type* for the new field as *Fulltext unstemmed*.
12. Select the *Boost* value as appropriate.
13. Click *Save changes* to finish adding the field to the index.

### Force a reindex of the site content

Once we add a new field, we need to force a reindexing of site content for the new field to be crawled.

```
drush sapi-i
```

See [Populate Search API Indexes](https://drupalize.me/tutorial/populate-search-api-indexes) for more on reindexing.

### Export the configuration

Export the configuration using Drush. Add and commit the changes to the repository.

## Paragraphs and other reference fields

Tag fields are a common and relatively straightforward reference type to add to a Search API index. The Term entity's **name** field contains everything most sites need to leverage the field in searches. Other reference fields can be more difficult. Any plain entity reference field has the ability to reference multiple bundles of the same entity type. An entity reference field targeting nodes can reference Articles, Basic Pages, and any other node type created on the page. Paragraph fields also share this ability, although it's limited to paragraph-type entities.

Since each entity bundle can have different fields, there is often no one field to add to the Search API index. We could add each relevant field from each bundle to the Search API index, but this would be cumbersome.

A better solution is to use a special virtual field provided by Search API: **Rendered HTML output**.

## Using the Rendered HTML output field

Instead of crawling raw field data, the **Rendered HTML output** field renders the crawled node or entity as it would be displayed to the end-user. The resulting HTML content is then sent to Solr for further processing. Using this field makes it easy to consume any reference field by converting it all to text.

To do this we recommend:

1. Creating a new [entity view mode](https://drupalize.me/tutorial/user-guide/structure-view-modes) to use for the Search Index.
2. Configuring the view mode to display the fields you want indexed.
3. Add the Rendered HTML output to the Search API Index.

### Create a Search Index view mode

The **Rendered HTML output** field renders content using the same process as Drupal does before displaying it to the end user. However, we don't usually want to submit the same exact display to Solr. We may wish to exclude key fields, use different field widgets, or even use completely different theme templates.

So, it's good practice to create a new display mode specifically for rendering content to submit to Solr. Search API automatically adds a view mode named **Search index**.

We can use this display mode, or create our own:

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Structure* > *Display modes* > *View modes*.
3. A list of view modes appears. Click *Add view mode*.
4. Select the entity type for which to create the new display mode, typically *Content*.
5. Enter a display mode *Name* of your choosing. Make it brief--but obvious--that this mode is used for search indexing.
6. Click *Save*.

### Configure the view mode

Creating the view mode is only the first part of a lengthier process. After creation, we need to go through each content type, and each field on those types, to configure whether and how they are displayed.

For regular content (node) types, this can be accomplished via the web UI:

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Structure* > *Content types*.
3. Under *Operations*, select *Manage display* for the target content types.
4. Expand the *Custom display settings* fieldset at the bottom of the *Manage display* page.
5. Select the checkbox next to the view mode you created earlier.
6. Click *Save*.
7. A new sub-tab appears for your display mode: open it.
8. Configure the field display as necessary, taking special care to set the *Format* of reference fields as *Rendered entity* and to remove image fields.
9. When finished, click *Save*.
10. Repeat the process for all remaining content types to add to the index.

### Add the field to the Search API index

Once we have the view mode created and configured, we can finally leverage it for the Search API index.

1. Open the target Search API index for editing.
2. Open the *Fields* tab, and click *Add field*.
3. The *Add fields to index...* modal dialog appears.
4. At the top of the modal dialog, locate *Rendered HTML output* and click *Add*.
5. A new modal dialog appears, allowing you to edit the details of the *Rendered HTML output* field.
6. Select the *User roles* with which to render the content. Different user roles have different permissions, and thus content will render differently. Typically, the anonymous role is used.
7. For each content type, select the view mode you created earlier.
8. When finished, click *Save*.
9. Click *Done* to dismiss the modal dialog, then *Save changes*.

### Export and reindex

Using Drush, export your site configuration (`drush cex`), add, and commit it to your repository.

Using either the web UI or Drush, force and reindex the site content as you did earlier.

## Recap

Reference fields can complicate the development of a search feature. Thankfully, Search API has the ability to traverse reference fields and index fields on the referenced content. This works well for tag fields. For paragraphs or generic reference fields, we can leverage the **Rendered HTML output** virtual field can be used to pass content as text to the Solr server. This feature leverages Drupal features such as display modes and theme templates.

## Further your understanding

- Would you need to add other fields to the index if using **Rendered HTML output**?
- Why would you create multiple search-dedicated display modes?

## Additional resources

- [Search API project](https://www.drupal.org/project/search_api) (Drupal.org)
- [Adding an index](https://www.drupal.org/docs/8/modules/search-api/getting-started/adding-an-index) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Populate Search API Indexes](/tutorial/populate-search-api-indexes?p=2815)

Next
[Create Search Pages and Blocks with Views](/tutorial/create-search-pages-and-blocks-views?p=2815)

Clear History

Ask Drupalize.Me AI

close
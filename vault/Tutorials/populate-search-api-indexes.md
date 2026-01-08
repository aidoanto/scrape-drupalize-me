---
title: "Populate Search API Indexes"
url: "https://drupalize.me/tutorial/populate-search-api-indexes?p=2815"
guide: "[[drupal-site-administration]]"
---

# Populate Search API Indexes

## Content

Creating an index alone is not enough. To populate the index, we need to specify the fields necessary to populate the index. Selecting the fields is accomplished in the Search API admin UI.

In this tutorial, we'll:

- Explain how to select what populates a search index
- Describe a field boost, and how it is used to customize results

By the end of this tutorial you should be able to add fields to a Search API Index so their content is available for searching, and then instruct Search API to index the content of your site.

## Goal

Customize an existing Search API index by specifying which fields to process.

## Prerequisites

- [Create Search API Indexes](https://drupalize.me/tutorial/create-search-api-indexes)

## Table of contents

This tutorial contains the following sections:

- [Add fields to the index](#add-fields-to-the-index)
- [Search API field types](#search-api-field-types)
- [Generate the search index](#generate-the-search-index)
- [Force all content to be reindexed](#force-all-content-to-be-reindexed)

## Add fields to the index

When you created a Search API index in the previous tutorial, you selected the content types, languages, and the Search API server to which to send data. Now we need to select the data within the content to send to the index.

### Add a simple field to the index

Many fields within a node are considered *simple* fields. They have scalar data such as a string or a number. One such field is the node's title field. Let's add that to our Search API index.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Locate the index you created earlier and open it for editing.
4. Open the *Fields* tab.
5. Click *Add fields*.
6. The *Add fields to index...* modal dialog appears. Scroll through the list and select *Title* by pressing the *Add* button for the field.
7. Click *Done*.
8. Notice that a new row appears in the *Content* table. Click *Save changes*.

### Add a complex field to the index

The title field is straightforward to add to the index: select it in the UI and move on to the next field. But some fields are *complex*, and made of multiple components. The default body field of nodes is one such complex field. It contains the body text, a summary, and information about what text format to use when displaying the text. For search purposes we only care about the text the people actually read.

Solr doesn't understand complex fields, so we need to select the component of the complex field to add to the index.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Locate the index you created earlier and open it for editing.
4. Open the *Fields* tab.
5. Click *Add fields*.
6. The *Add fields to index...* modal dialog appears. Scroll through the list and locate the *Body* field.
7. To the left the field name, notice there's a `(+)` link. Click it to expand the complex field.
8. Next to *Processed text*, click *Add*.
9. Click *Done* to dismiss the modal dialog.
10. Notice that a new row appears in the *Content* table for the field, and *Property Path* displays *body:processed*.
11. Click *Save changes*.

### Export the configuration

1. Use the Drush command to export the configuration.

   ```
   drush cex -y
   ```
2. Add and commit the new site configurations to the repository.

## Search API field types

Each field selected for indexing in Search API also has a field *type*. The type instructs Search API how to process and send the data to Solr for further processing. There are many field types, but there are several we will use in nearly all Solr search implementations:

- **string**, the default type, submits the field value as a complete string. Search strings will need to match the entire field value, rather than parts of it.
- **fulltext** breaks up the field data into tokenized words, each considered for matches during a search.
- **integer** and **decimal** work like strings, but for numeric data.

The **fulltext** type also has a special **boost** parameter. This parameter, a number greater than 0, instructs Search API to let it act as a scaling factor for search matches against the field value. A boost greater than 1 will increase the match relevancy for the field. A boost between 0 and 1 will decrease it.

### Configure the field types

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Locate the index you created earlier and open it for editing.
4. Open the *Fields* tab.
5. Locate the target field and select the *Type*. For the *Title* and *Body* fields, select *Fulltext*.
6. Click *Save changes*.

### Select the boost for fulltext field types

For **fulltext**-type fields, a special **boost** parameter appears adjacent to the type selector. We want the **title** field to be more heavily matched against search queries compared to the **body** field.

Change the **boost** parameter for the **title** field to a number greater than **1.0**.

1. Open the Search API index for editing.
2. Locate the target fulltext field in the table.
3. The *Boost* parameter appears. Select the value as needed.
4. Click *Save changes*.

### Export the configuration

Use Drush to export the configuration (`drush cex`). Then add and commit the site configuration to the repository.

## Generate the search index

Once we configure the Search API index, everything is ready to generate the search index. As new content is posted to the site, the default behavior of an index is to process the content and send it to Solr for indexing. For a site with existing content, we need to index it *en masse*. Fortunately, Search API provides us two methods to reindex an entire site.

### Use the web UI to reindex the site

The web UI can be used to reindex a site's content. This method is easy and accessible, but it can result in timeouts for sites with lots of content.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Under the *Name* column, click the link for the Search API index you need to reindex.
4. A new page appears. Notice the progress bar at the top; this indicates how many nodes have been indexed, and how many remain to be indexed.

   Image

   ![Screenshot of Search API Index status page](/sites/default/files/styles/max_800w/public/tutorials/images/search-api-index-status.png?itok=DVV6VVwj)
5. Click *Index now*.

### Use Drush to reindex the site

An alternative method is to use the Drush utility to instruct Search API to reindex the site from the command line. This method relieves the web server of any load while performing the index operation, avoiding any timeouts. Furthermore, running PHP from the command line tends to have less memory restrictions than the web server, avoiding out of memory problems.

Use the Drush command to reindex the site:

```
drush sapi-i
```

The site's content will now be reindexed.

## Force all content to be reindexed

Sometimes an index operation does not perform as expected. Old content does not get reindexed unless forced. Instead of troubleshooting individual items, it is often better to force all content to be reindexed.

Forcing a reindex doesn't occur at the Search API index level, but on the level of each individual node in the search index. In order to force a node to be reindexed, you must choose to do one of two operations:

- Mark the node as needing reindexing. This preserves existing search data, but it will be overwritten on the next index operation.
- Erase ("clear") the search index record for the node. This creates a completely new entry, but results in the content disappearing from search results until reindexed.

You can force a reindex either in the web UI or via Drush.

### Use the web UI to force a reindex

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API*.
3. Under the *Name* column, click the link for the Search API index you need to reindex.
4. Click *Queue all items for reindexing* to mark all items for reindexing, or *Clear all indexed data* to delete all search index data.
5. Use the *Confirm* button on the next page to confirm the request.
6. Reindex the site by clicking *Index now*.

### Use Drush to force a reindex

Use the Drush command to mark all content as needing indexing:

```
drush sapi-r
```

Or to erase all data from the index:

```
drush sapi-c
```

Use Drush to reindex the content:

```
drush sapi-i
```

The site's content will now be reindexed.

## Recap

The bulk of Search API configuration is selecting the fields and field types necessary to send to the search index. Adding fields is performed in the Drupal web UI. Each field has a type, which has significance in how data is processed and considered against search queries. Once added to the Search API index, you can use the web UI or Drush to index content on the site, or force a reindex.

## Further your understanding

- When would you erase all content from the search index instead of just marking all content as needing reindexing?
- On what sort of data would you use a boost below 1?
- What other Search API field types are available?

## Additional resources

- [Search API project](https://www.drupal.org/project/search_api) (Drupal.org)
- [Adding an index](https://www.drupal.org/docs/8/modules/search-api/getting-started/adding-an-index) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create Search API Indexes](/tutorial/create-search-api-indexes?p=2815)

Next
[Index Reference Fields](/tutorial/index-reference-fields?p=2815)

Clear History

Ask Drupalize.Me AI

close
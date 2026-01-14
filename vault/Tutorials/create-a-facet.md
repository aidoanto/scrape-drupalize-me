---
title: "Create a Facet"
url: "https://drupalize.me/tutorial/create-facet?p=2815"
guide: "[[drupal-site-administration]]"
---

# Create a Facet

## Content

Creating a facet in Drupal is rather different from using Facets API in Drupal 7. In the new module, we first create a search view, and then configure facets against target fields in the index. Once created, we must configure the facet UI to appear on target pages using the Blocks UI.

In this tutorial, we'll:

- List the steps necessary to create a facet using a non-reference field (i.e. boolean, or text list)
- Explain why facets are displayed using blocks
- Describe the various facet display modes and uses for each

By the end of this tutorial you should be able to add a facet based on a *text list* field and allow users to filter search results using the values in the list field.

## Goal

Install the Facets module and create a Facet on an existing crawled field.

## Prerequisites

- [Create Search Pages and Blocks with Views](https://drupalize.me/tutorial/create-search-pages-and-blocks-views)
- [Facets](https://drupalize.me/tutorial/facets-search)

## Download and enable Facets

Before we can create a new facet, we need to download the Facets module. This can be done in several ways, but we prefer using Composer.

```
cd path/to/my_project
composer require drupal/facets
```

Once downloaded, we can enable the module either via the web UI (Extend), or via Drush:

```
drush en -y facets
```

## Field types for Facets

A facet can be thought of as a "predefined search axis". Instead of a text entry field with which to do a fulltext search, Facets provides a selection based on the values available in the search result. For this reason, not all field types are recommended for use as a facet.

Good facet fields:

- Text list fields
- Taxonomy reference fields
- Bounded integer fields

Fields that may be acceptable, depending on implementation:

- Bounded decimal fields
- Plain text fields with the *String* Search API index field type
- General entity reference fields

Avoid:

- Unbounded numeric fields
- Any text field indexed as fulltext
- Search API's Rendered HTML Output field

Fields which provide a set number of values tend to be the best for use as a facet. Text list fields and some entity reference fields (such as a taxonomy term field) yield the best results when creating a facet. These fields have a *predefined number of values*, making them excellent candidates. Fields that are configured in the Search API index as the *String* type also make good candidates for facets, but special care must be taken to ensure content creators do not abuse the field. Numeric types such as integer or decimal values can be good candidates for faceting, depending on the application. Unbounded numeric fields can be problematic for facets. Any fulltext field should be avoided for use as a facet. This includes fields like the body field, or Search API's rendered HTML output field.

## Creating a list-item facet

Aside from taxonomy reference fields, text list fields are the most popular type on which to base a facet. These fields provide a set number of human-readable values. Content creators must select one or more pre-configured values, and cannot enter alternatives without modifying the field.

### Create the text list field

Text list fields create a text field that has a set number of possible values configured at the time of field creation. They are useful for creating a field with values that seldom (if ever) change.

While you can create any text list field you like, this tutorial will create a list field of rainbow colors (red, orange, yellow, green, blue, indigo, and violet).

1. Log in to your Drupal site with administrator privilege.
2. In the *Manage* administrative menu, navigate to *Structure* > *Content types* (*admin/structure/types*).
3. Open the target content type for editing.
4. Under the *Managed Fields* tab, click *Add field*.
5. Using the *Add a new field* dropdown, select *List (text)*.
6. Enter a *Label* of your choice.
7. Click *Save and continue*.
8. In the *Allowed value list* enter key-value pairs in the following format. Ideally, avoid uppercase and special characters for the *key\_name* (however, the underscore (`_`) character is fine to use).

   ```
   key_name|Display name
   ```
9. Use the *Allowed number of values* field to select if this field can only have a single, set number, or unlimited number of values.
10. When finished, click *Save field settings*.

### Update content

Once the field has been created, update your content to make use of the field. If you are using the Devel module to autogenerate content, you may wish to simply generate additional nodes.

### Add the field to the Search API index

Next, we make Search API and Solr aware of the new field by adding it to the index.

1. In the *Manage* administrative menu, navigate to *Configuration* > *Search and metadata* > *Search API*, and open the target Search API index for editing.
2. Open the *Fields* tab and click *Add fields*.
3. The *Add field to index...* modal dialog appears. Scroll through the list and click the *Add* button next to your field.
4. Click *Done* to dismiss the modal dialog.
5. A new field appears in the *Content* table. Ensure the *type* is *String*.
6. Click *Save changes*.

### Rebuild the search index

Since we added a new field to the Search API index, we need to reindex.

```
drush sapi-c
drush sapi-i
```

Learn more about reindexing, and how to do it via the UI, in [Populate Search API Indexes](https://drupalize.me/tutorial/populate-search-api-indexes).

### Update the search view

Facets module does not pull fields from the Search API index directly, but relies on the search view. Thus, we need to add the field to the search view before we can create the facet. The field, however, does not need to be displayed in the search results. We can suppress the display of the field in the view, while still relying on it for our facet.

1. In the *Manage* administrative menu, navigate to *Configuration* > *Structure* > *Views* (*admin/structure/views*) and open your search view for editing.
2. Under *Fields*, click *Add*.
3. The *Add fields* modal dialog appears. Select your field from the list. Be sure that it's shown as *(indexed field)* so the field value is pulled from Solr.
4. Click *Add and configure fields*.
5. Select *Exclude from display*.
6. Click *Apply*.

### Create the facet

With all the setup done, we can now create the facet for our new field.

1. In the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Facets* (*admin/config/search/facets*).
2. Notice that your view appears in the table as a *Facet source*.
3. Click *Add facet*.
4. Select your view as the *Facet source*.
5. Select the *Field* you just created. If it does not appear, go back and update the view.
6. Enter a *Name* of your choice.
7. Click *Save*.
8. Select the *Widget* for the facet display. This tutorial uses *List of links*.
9. Click *Save*.

### Showing text-list display values rather than keys

One important option for text-list fields is whether you want to display the key name or the display name of the field value. By default, only the key name is shown, as that is what is contained in the search index. Fortunately, Facets offers us the option to use the display name instead when configuring the facet.

1. In the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Facets* (*admin/config/search/facets*) and open your facet for editing.
2. Under *Facet settings* select *List item label*. This will instruct Facets to display the display name of the text list value, rather than the key.
3. When finished, click *Save*.

### Showing the number of results

The advantage of Facets is that the values shown correspond to what is in the search results, rather than all possible values for the field. To this end, Facets provides us a *Show the amount of results* option to show the number of items the facet matches within the search results.

1. In the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Facets* and open your facet for editing.
2. Select *Show the amount of results*.
3. When finished, click *Save*.

### Configuring the facet display order

A facet can be configured to sort the items it displays by several criteria. By default, items are sorted by:

- Whether they are selected (active) or not selected (inactive)
- The number of search results match the facet
- The display value of the underlying field

The display value may not always be desirable, as it might not be the preferred order. For text list fields, you can choose to configure the field by prefixing the key name with a number (as in `01_red`, `02_orange`, etc.). Then, you can configure the field to sort by *raw value* instead.

1. In the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Facets* (*admin/config/search/facets*) and open your facet for editing.
2. Under *Facet sorting* at the bottom of the page, configure sorting options as desired.
3. When finished, click *Save*.

### Place the facets block

Each facet is made available for display as an independent block. This differs from Views' exposed filters where all the filters for a view are provided as a single block. We can place the facet block on our search page using the Block UI.

1. In the *Manage* administrative menu, navigate to *Structure* > *Block layout* (*admin/structure/block*).
2. Use a *Place block* button to place the block in a target region. While this can be anywhere, typical placement for facet blocks is either above the *Content* or in a sidebar region.
3. The *Place block* modal dialog appears. Scroll through the list and locate the block for your facet. If you are having difficulty finding it, look for any items with the *Category* of *Facets*.
4. Click *Place block*.
5. Under *Visibility*, open the *Pages* vertical tab. Configure the facet block to only appear on the page provided by your search view.
6. Click *Save block*.
7. Click *Save blocks*.

### Validate the configuration

1. Navigate to the page provided by your search view.
2. Perform a search. If you are using autogenerated content from the Devel Generate module, take special care in selecting the search term.
3. Note that your facet block now appears on the page, and the values shown correspond to what is in existing search results.

   Image

   ![A screenshot showing search results with the facets block in a sidebar](../assets/images/facetBlock.png)
4. Use the facet to drill down in your search results.
5. Notice that you have the option to deselect a previously selected facet. For the *List of links* facet type, selected facets are prefixed with `(-)`.

   Image

   ![A screenshot closeup of the facet block, showing a selected facet](../assets/images/facetSelected.png)
6. Deselect a previously selected facet. Notice now that the search results and the facet results now show a wider list of results.

## Recap

Facets rely on fields configured in a Search API-powered view. Once you add the field to your Search API index and view, you can create a new facet that relies on the field. Facets are provided as highly configurable blocks, one block per facet.

## Further your understanding

- When would you use the facet *Widget* type: *Array with raw results*?

## Additional resources

- [Facets project](https://www.drupal.org/project/facets) (Drupal.org)
- [Devel](https://drupalize.me/topic/devel) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Facets in Search](/tutorial/facets-search?p=2815)

Next
[Create a Facet using Taxonomy](/tutorial/create-facet-using-taxonomy?p=2815)

Clear History

Ask Drupalize.Me AI

close
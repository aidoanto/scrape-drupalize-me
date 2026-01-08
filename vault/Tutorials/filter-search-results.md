---
title: "Filter Search Results"
url: "https://drupalize.me/tutorial/filter-search-results?p=2815"
guide: "[[drupal-site-administration]]"
---

# Filter Search Results

## Content

One of the key advantages of custom search is to do more than provide a single, global search box. Filtering allows you to divide results to a subset.

In this tutorial, we'll:

- Describe how to configure filtering through use of a taxonomy field
- Explain the disadvantages of this approach, including how it relies on Views to reduce results rather than Solr

## Goal

Learn to use Views exposed filters in a Search API view.

## Prerequisites

- [Create Search Pages and Blocks with Views](https://drupalize.me/tutorial/create-search-pages-and-blocks-views)

## Filtering results

When we use a public search engine, we often only have the option to search using a phrase or keyword. We enter in the text we expect to see on the pages we hope to find. If we need to narrow our results, we often add more search terms.

Public search engines conceptualize sites as little more than an interlinked set of pages. Without deeper knowledge of a site's content structure, a fulltext search field provides a "one size fits all" approach.

Fortunately for us, we do have additional understanding of our site's content structure. Combined with our Search API-powered view, we can design our search feature to suit our content.

## Create a search filter

In many ways, a Search API-powered view is the same as any view. You can apply sorting, filters, exposed filters, and even contextual filters as you would for a content-powered view. This capacity makes it easy to create customized search experiences using Solr and your existing Drupal knowledge.

### Update the Search API index

When creating a content view, we often will provide an exposed filter that allows you to filter results by taxonomy terms. We can do the same thing in a Search API-powered view.

The first step is to add this field to our Search API index. Follow the steps in [Index Reference Fields](https://drupalize.me/tutorial/index-reference-fields) to accomplish this.

### Add a tag filter to the search view

Once our Search API Index is updated, we can modify our search view to leverage the field. If you haven't created the view yet, follow the steps in [Create Search Pages and Blocks with Views](https://drupalize.me/tutorial/create-search-pages-and-blocks-views) first.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Structure* > *Views* (*admin/structure/views*).
3. Open your Search API-powered view for editing.
4. Under *Filter criteria* click *Add*.
5. The *Add filter criteria* modal dialog appears. Select the taxonomy term field you added earlier. Since the term is a reference field, the field name will be the component path, such as *Tags » Taxonomy term » Name*.
6. Click *Add and configure filter criteria*.
7. Click the *Expose this filter...* checkbox.
8. Change the *Label* and other settings as you see fit.
9. When finished click *Apply*.
10. Click *Save*.

### Clear the site cache

When updating views with exposed filters as blocks, the blocks may not update when the view is saved. To ensure the page displays the most current configuration of the block, clear the site cache.

Learn how to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache).

### Validate your changes

Now that the filter is set up, we can put it to use.

1. Navigate to the search page provided by your Search API-powered view.
2. Locate your search form. This should either be above the view content, or in an exposed form block elsewhere on the page.
3. Notice that in addition to our existing fulltext search field, we also now have a new text entry field for the filter.

## Reference types and filters

When we configured the above filter, the results weren't what we expected. If we were to build the same filter in a content-powered view (rather than Search API), the taxonomy term field could be presented as an autocomplete field or a dropdown menu. This time, however, the *Tags » Taxonomy term » Name* was shown as a plain text entry field. This isn't very useful as a filter since we need to know what tag names we have first.

Why can't views render the filter as an autocomplete or a dropdown? Why doesn't it work like a normal content view? The answer is how we configured the Search API index.

When we added the taxonomy term field in [Index Reference Fields](https://drupalize.me/tutorial/index-reference-fields), we selected the *Name* component under the referenced entity. This works great for Solr, since it doesn't understand Drupal entities -- but Views *does* understand entities. By only including the *Name* component, we've removed all the other information Views needs in order to render the filter more intelligently.

In order to get that information back, we need to add a new index field that retains all the entity information.

### Update the Search API index

Instead of replacing the taxonomy term field we added to the Search API index, we're going to add a field containing full tag information. The plan is to continue to use the *Name* component for text search results as before, while adding the ability to create better views filtering. Search API allows you to add multiple instances of the same field to the index.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and metadata* > *Search API* (*admin/config/search/search-api*).
3. Locate the index you created earlier and open it for editing.
4. Open the *Fields* tab.
5. Click *Add fields*.
6. The *Add fields to index...* modal dialog appears. Scroll through the list, locating the target taxonomy field.
7. Click the *Add* button next to the field. Do not expand the field to select a component.
8. Notice that a new field appears in the *Content* table. This time, the Search API field *machine name* matches the field name. Furthermore, notice that the *Type* is *integer* rather than *string*.
9. Click *Save changes*.

### Rebuild the search index

Since we added a new field to the Search API index, we need to reindex.

```
drush sapi-c
drush sapi-i
```

Learn more about reindexing, and how to do it via the UI, in [Populate Search API Indexes](https://drupalize.me/tutorial/populate-search-api-indexes).

### Update the search view

Finally, we need to swap out our earlier filter field with a new one based on our new Search API index field.

1. Open your search view for editing.
2. Click the filter we created earlier.
3. In the *Configure filter criterion...* modal dialog, click *Remove*.
4. On the view edit page, under *Filter criteria*, click *Add*.
5. Select the *Tags* field. It should have the type: *Content datasource*.
6. Click *Add and configure filter criteria*.
7. This time, a new option appears for the *Selection type*. Select *Dropdown*.
8. Expose the filter as you did before.
9. Configure the remaining filter options as necessary. When finished, click *Apply*.
10. *Save* the view.

### Clear the cache again

If your view's exposed filters are displayed as a block, you'll need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) for your changes to take immediate effect.

### Validate the configuration

1. Navigate to the search page provided by your Search API-powered view.
2. Perform a search. If you are using autogenerated content from the Devel module, take special care to select existing placeholder text.
3. Constrain the results using your new filter.

## Recap

Applying a filter to your Search API-powered view isn't difficult. Since Search API relies on views to create search pages, conventional methods of adding exposed filters work even for Solr search results. If you plan to filter using a reference field, selecting the entire field (rather than a subcomponent such as *Name*) is essential to allow Views to bring in additional entity information.

## Further your understanding

- Could we apply multiple filters using the same method?
- Is this filter behavior "drill-down"?

## Additional resources

- [Facets in Search](https://drupalize.me/tutorial/facets-search) (Drupalize.Me)
- [Devel](https://drupalize.me/topic/devel) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Autocomplete to Search](/tutorial/add-autocomplete-search?p=2815)

Next
[Facets in Search](/tutorial/facets-search?p=2815)

Clear History

Ask Drupalize.Me AI

close
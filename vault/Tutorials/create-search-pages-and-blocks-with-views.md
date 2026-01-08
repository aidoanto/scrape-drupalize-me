---
title: "Create Search Pages and Blocks with Views"
url: "https://drupalize.me/tutorial/create-search-pages-and-blocks-views?p=2815"
guide: "[[drupal-site-administration]]"
---

# Create Search Pages and Blocks with Views

## Content

One of Search API’s key advantages is that custom search pages can be created using Views. This allows a high degree of customization, while relying on a familiar toolset.

In this tutorial, we'll:

- Describe how to use Views to create a search page
- Explain search page best practices, including requiring input and no-results text

By the end of this tutorial you should be able to create a page that users can use to search your site's content using the Solr search backend.

## Goal

Use the Views UI to create a Search API-powered search view that relies on our Solr core.

## Prerequisites

- General understanding of the Views module and how to create a view. See Chapter 9 of the Drupal User Guide: [Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter).
- [Create Search API Indexes](https://drupalize.me/tutorial/create-search-api-indexes)

## Table of contents

This tutorial contains the following sections:

- [Search views](#search-views)
- [Search blocks](#search-blocks)

## Search views

Throughout this series, we've built and configured a Search API index suitable to send data to Solr. Search API, however, does not provide us a search page out of the box. Instead, Search API assumes we will create a search page using views. This allows us to tailor our search to our specific needs.

### Create a search view

Creating a Search API-powered view is similar to creating a view for regular content. The key difference is the data source of the view. Instead of *content*, we use a *Search API index* for the data source.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Structure* > *Views* (*admin/structure/views*).
3. Select *Add view*.
4. Enter a *View name* of your choosing.
5. Under *View content*, select *Show* as *Index your\_index\_name*, where *your\_index\_name* is the name of the Search API index you created earlier.
6. Select *Create a page*, and configure it as desired.
7. When finished, select *Save and exit*.

### Add a fulltext search filter

A Search API-powered view will start by displaying all data found in the search index. This seems confusing at first, until we realize that performing a search is like running a filtering operation against the search index. As such, we need to add a fulltext search filter to the view, and expose that filter so it can be entered by the end user.

1. Open the Search API-powered view you created earlier for editing.
2. Under *Filter criteria*, click *Add*.
3. The *Add filter criteria* modal dialog appears. Notice that unlike a content-powered view, only fields selected for indexing appear in the list.
4. Select *Fulltext search*, and click *Add and configure filter criteria*.
5. Select *Expose this filter to visitors...*.
6. For the *Filter type to expose*, select *Single filter*.
7. Change the *Label* as you see fit.
8. Select the *Operator*. For most general search views, select *Contains any of these words*
9. Under *Searched fields*, select the Search API index fields in which to search against. If you've been following along, select the *Title*, *Body*, and tag *Name*.
10. When finished, click *Apply*

### Make the search box entry mandatory

Even after adding the exposed, fulltext search box, the view will still display all data in the index prior to entering a query. Again, this makes sense for views, as exposed filters by default do not need a value selected.

In order to make the Search API-powered view act like a search page, we need to configure the fulltext search box to be required. This will prevent the search page from displaying anything until an entry is made.

1. Open the Search API-powered view you created earlier for editing.
2. Under *Filter criteria*, click on the fulltext search box you created earlier.
3. In the *Configure filter criterion...* modal dialog, select the *Required* checkbox.
4. Select *Apply*.
5. Select *Update preview* on the view edit page. Note that no results are displayed as long as the search box is empty.
6. Select *Save*.

### Configure the "no results" page

A blank page is the last thing an end user wants to see after submitting a search query. This leaves the user wondering if a search was performed at all. In a Search API view, the solution is the same as for a normal content view -- configure the *No results behavior*.

1. Open the Search API-powered view you created earlier for editing.
2. Under *No results behavior*, click *Add*.
3. There are several options to choose from depending on your needs. For this tutorial, select *Text area*.
4. Select *Add and configure no results behavior*.
5. In *Content*, enter some no-results text of your choosing.
6. Select *Save*.

### Validating the view configuration

Now that the view is created, we can visit the resulting page on the site and test its function.

1. Login to your Drupal site with administrator privileges.
2. Examine the content on your site briefly for a suitable test keyword. This is especially important if you are using generated content from the Devel module.
3. Navigate to your Search API-powered view, using the *Path* you entered when creating it.
4. Note that the no-results text is displayed when no search query is submitted.
5. Enter the search keyword you chose earlier in the fulltext search box, and click *Apply*.
6. Examine the results, if any.

If no results appear, manually re-examine your content and select another keyword. If this keyword also returns no results, force a reindex. Then try your search again.

## Search blocks

We don't usually want to visit a dedicated search page prior to submitting a search query. Many sites have a search icon or box at the top of every page, making it easy to search no matter where in the site you are. This too can be accomplished using a Search API-powered view by providing the exposed, fulltext filter as a separate block.

### Configure the exposed form as a block

1. Open the Search API-powered view you created earlier for editing.
2. Under *Advanced*, click the link next to *Exposed form in block*.
3. A modal dialog appears. Select *Yes*, and click *Apply*.
4. Save the view.

### Place the exposed form block

1. Using the *Manage* administrative menu, navigate to *Structure* > *Block layout* (*admin/structure/block*).
2. Use a *Place block* button to place the block in a target region, typically the *Header*.
3. The *Place block* modal dialog appears. Scroll through the list and locate the *Exposed form...* block for your view, and click *Place block*.
4. Configure the block as desired, then click *Save block*.
5. Select *Save blocks*.

### Validate the block configuration

Return to your site's main page. The search block should now appear in the header. Submit a search query, noting how you are redirected to your search page.

### Export the configuration

Export the configuration using Drush (`drush cex`). Add and commit the changes to the repository.

In [Add Excerpts for Search Results](https://drupalize.me/tutorial/add-excerpts-search-results) we'll cover how to add snippets of text that highlight search terms (similar to Google.com search results) to Search API's results.

## Recap

Search API relies on views to provide search pages. While this can seem counterintuitive, it relies on a standard and versatile toolset within any Drupal site. This allows you to customize your search experience as you see fit.

## Further your understanding

- Could other views filters be used on a Search API-powered view?

## Additional resources

- [Add Autocomplete to Search](https://drupalize.me/tutorial/add-autocomplete-search) (Drupalize.Me)
- [Filter Search Results](https://drupalize.me/tutorial/filter-search-results) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Index Reference Fields](/tutorial/index-reference-fields?p=2815)

Next
[Multiple Search API Indexes](/tutorial/multiple-search-api-indexes?p=2815)

Clear History

Ask Drupalize.Me AI

close
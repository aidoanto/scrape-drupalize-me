---
title: "Add Excerpts for Search Results"
url: "https://drupalize.me/tutorial/add-excerpts-search-results?p=2815"
guide: "[[drupal-site-administration]]"
---

# Add Excerpts for Search Results

## Content

Excerpts are brief snippets of text displayed in search results. They give context to how the search terms relate to the result. Search API provides support for excerpts out of the box.

In this tutorial, we'll:

- Identify how to apply excerpts to a search index
- Describe how to add excerpt display to the search view

By the end of this tutorial you should be able to use the *Highlight* search processor to add excerpts to search results.

## Goal

Add excerpting, or "snippets", to search results without the need for custom code.

## Prerequisites

- [Processors in Search](https://drupalize.me/tutorial/processors-search)

## The Highlight processor

Excerpting is provided by the *Highlight* processor. Highlight is run on results as they are received from the Solr server. The processor displays portions of the search result with the search keyword highlighted using a given tag.

Adding the Highlight processor can be done in the Search API UI.

### Add Highlight to the Search API index

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Config* > *Search and Metadata* > *Search API* (*admin/config/search/search-api*).
3. Open the target index for editing.
4. Open the *Processors* tab.
5. Scroll through the list of processors and select *Highlight*.
6. Notice that under *Processor order* the processor has already been added to the *Postprocess query* phase of the pipeline.

### Configure the Highlight processor

In a search result page, it isn't practical to display an entire node or entity. That would make it difficult to scan results and select the page you're looking for. Instead, Highlight enforces a character limit so that an excerpt is never longer than expected. If multiple instances of a search term are found in the node, the content between the keywords is replaced with an ellipsis.

Another key setting is a prefix and suffix to apply around any matched keywords. Typically, this is used to surround the matched keyword with an HTML tag. By default, it uses the `<strong>` tag. You can add a custom class, use a different tag, or even add custom display text.

1. Open the *Processors* tab for the target index.
2. Scroll down to *Processor settings* and open the vertical tab for *Highlight*.
3. Select *Create excerpt*.
4. Enter an *Excerpt length* of your choosing.
5. Using *Exclude fields from excerpt*, select which fields not to display in the excerpt. Typically, the *Title* field is excluded.
6. Enter the *Highlight prefix* and *suffix*.
7. Click *Save*.

### Export the configuration

Using Drush, export your site configuration (`drush cex`). Then, add and commit the configuration changes to your repository.

## Display excerpts

Since excerpts are derived from one or more fields configured on the Search API Index, you might think the processor would modify the display of those fields and show them as excerpts instead. This would be limiting since there are some search applications where you **do** want to render an entire field in addition to an excerpt. Furthermore, since Highlight can work over multiple fields in the Search API index, the display can become unpredictable.

Highlight instead provides a new field to display the excerpt. This must be added to the fields displayed in the search view.

### Add the excerpt to the view

While the processor is named *Highlight*, the field it provides within the view is called *Excerpt*. Keep this in mind as you update your view.

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Structure* > *Views* (*admin/structure/views*).
3. Open your Search API-powered view for editing. See [Create Search Pages and Blocks with Views](https://drupalize.me/tutorial/create-search-pages-and-blocks-views) if you haven't created one yet.
4. Under *Fields* click *Add*.
5. The *Add fields* modal dialog appears. Scroll through the list and select *Excerpt*.
6. Click *Add and configure fields*.
7. The *Configure field: Search: Excerpt* modal dialog appears. If you want to highlight matched search words, check *Use highlighted field data*.
8. Configure the field as necessary. When finished, click *Apply*.
9. Click *Save* to save the view.

### Remove other fields

If you followed [Create Search Pages and Blocks with Views](https://drupalize.me/tutorial/create-search-pages-and-blocks-views), you already have a Search API-powered view that displays one or more fields, including the body field. This field can get quite long in a search result page. The excerpt already takes the place of this field, so we can now remove it from our view.

1. Open your Search API-powered view for editing.
2. Under *Fields* locate a field -- like the body field -- that is no longer necessary now that we have the excerpt.
3. Click the field name to edit it.
4. In the modal dialog, click *Remove*.
5. Repeat the process for any remaining fields.
6. Click *Save* to save the view.

### Check functionality

Now that are search view is updated, we can check to see if the excerpt appears in the search page.

1. Navigate to your search page provided by your Search API-powered view.
2. Perform a search. Remember, if you are using auto-generated content from Devel, you may need to first find a suitable search term that would match the placeholder text.
3. The search results should now display the excerpt, surrounding matched terms with the prefix and suffix of your choice:

Image

![Screenshot of search results showing excerpts](../assets/images/Excerpts.png)

If the excerpts do not appear as expected, try a different search term, or force a reindex.

### Export the site configuration

Using Drush, export your site configuration (`drush cex`). Add and commit it to your repository.

## Search API excerpts vs. Solr excerpts

The above instructs you how to create excerpts that are generated via Search API. Apache Solr also provides its own excerpting mechanism, but it requires a custom schema configuration.

Search API's excerpting is more natural for Drupal sites. The consequence is that all the processing to generate and render the excerpt occurs on the web server, rather than the Solr server. Keep this in mind when developing your site, as you may require additional web server resources to support the feature.

## Recap

Excerpting provides context to the end user where their search terms can be found in matched content. For Search API, this feature is provided by the *Highlight* processor, which acts as a postprocess query processor. Once added to the Search API index, excerpts can be added to the display by adding an excerpt field to the view.

## Further your understanding

- Why would you use the HTML filter processor and the Highlight processor together?
- Can you think of other content fields you would display in search results in addition to the excerpt?

## Additional resources

- [Search API project](https://www.drupal.org/project/search_api) (Drupal.org)
- [Devel](https://drupalize.me/topic/devel) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Processors in Search](/tutorial/processors-search?p=2815)

Next
[Add Autocomplete to Search](/tutorial/add-autocomplete-search?p=2815)

Clear History

Ask Drupalize.Me AI

close
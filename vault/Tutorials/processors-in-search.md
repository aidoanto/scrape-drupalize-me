---
title: "Processors in Search"
url: "https://drupalize.me/tutorial/processors-search?p=2815"
guide: "[[drupal-site-administration]]"
---

# Processors in Search

## Content

Processors allow you to augment your search indexes by performing additional operations before or after the index operation. This can make your search more flexible.

In this tutorial, we'll:

- Identify what a processor is, and when it can be employed in the search pipeline.
- List useful processors provided by Search API.
- Describe how to apply a processor to an index, and why reindexing is necessary.

## Goal

Introduce *processors* in search applications, which allow you to modify the search crawl and search results in various ways.

## Prerequisites

- [Populate Search API Indexes](https://drupalize.me/tutorial/populate-search-api-indexes)

## Normalizing search data

When developing a search feature, we often need to modify the data sent to the index. This can be as simple as transforming the case of all data to lower case, stripping out HTML tags, or other such manipulation. Modifying the data before sending it to the search index allows us to *normalize* it.

Normalizing data prior to sending it to the search server for indexing allows broader matches, which can make the search feature more effective. It also introduces a problem. Imagine that we converted all data to lowercase prior to sending it to the index. Now, when someone submits a search query that includes capitalization, they will receive *fewer* hits as a result. For this reason, we need to normalize the search query as well. This will allow the query -- no matter the input -- to correspond to the normalized data in the search index.

## Value-added results

Like normalizing search data and queries, we often also want to modify our search results prior to display. Here too, we want to normalize data. If our search results contain unexpected HTML, for example, our search page may display bizarrely.

Modifying search results, however, have motivations beyond data normalization. Sometimes we want to add value to the results for a better user experience. A common modification to search results is to display *excerpts*. Instead of displaying an entire node or entity, we only want to see a truncated snippet of the content relevant to our search. The search keywords are often highlighted in the snippet for added effect.

Another example of modifying search results is to respond to access control. If a user doesn't have access to the content matched in a search, we can modify the results prior to display to remove restricted content.

## The preprocess pipeline

In Search API, there are three points at which processors may be employed:

- Preprocess index
- Preprocess query
- Postprocess query

The **preprocess index** phase allows processors to act on data prior to sending it to the backend for indexing. This makes the preprocess index phase the most commonly used phase in any Search API implementation, as you can process text, remove HTML, and perform many other forms of data manipulation.

The **preprocess query** phase acts not on the data to be indexed, but on the search query text. In this case, the preprocess query acts on the search query prior to sending it to the backend. This sounds unusual, but it is commonly used to manipulate search terms such as transforming the case, correct spelling, use stemmers, and so on.

The **postprocess query** phase is often the least-used phase by processors. It acts on the search results after performing the search operation. As we'll see later in the series, we'll use a postprocess query processor to display excerpts.

## Using processors

Processors are a configuration on the Search API index. This has a few implications. The kinds of processors available depends largely on the backend used to power the Search API index.

Solr has its own mechanisms for ignoring case, applying stop words, and other features that can be supplied by a Search API processor. Likewise, The Search API Solr module provides some of its own processors specifically geared toward Solr-powered search. As a result, the kinds of processors available in the UI differ if relying on different search backends.

### Add a processor to the Search API index

1. Login to your Drupal site with administrator privileges.
2. Using the *Manage* administrative menu, navigate to *Configuration* > *Search and Metadata* > *Search API* (*admin/config/search/search-api*).
3. Edit the index to which to add the processor.
4. Open the *Processors* tab.
5. Read through the list of processors, selecting one or more for use. For example, *HTML filter*.

### Select when the processor will run

Recall that processors can run at 3 points, before indexing, before querying, and after querying. Selecting at which points the processor runs is done under the Search API index's *Processors* tab. Many processors automatically add themselves to the points in the pipeline where they are most commonly used.

1. Open the *Processors* tab for the target index.
2. Scroll down to the bottom of the page to the *Processor order* section.
3. Notice there are 3 boxes, 1 for each point in the pipeline at which a processor may run.
4. Using the cross-hairs icon, drag the processors within each box to the desired execution order.

### Configure the processor

Each processor may have some configuration allowing you to customize its function. Configuring a processor is done in the *Processors* tab of the target Search API index.

1. Open the "processor" tab for the target index.
2. Scroll down to the bottom of the page to the *Processor settings* section.
3. Within the box, select the vertical tab for the processor to configure.
4. Select the fields on the index to which to apply the processor.
5. Configure the remaining options as necessary.
6. Repeat the process for every additional processor to configure.
7. When finished, click *Save*.

### Export the site configuration

Since we've made changes to the Search API index, we need to export the site configuration.

```
drush cex -y
```

Then, add and commit the new site configuration to the repository.

### Force a reindex

Adding processors to the Search API index means that the data within the search index is now out of sync with the configuration. In order to use the new processors, we need to force a new reindexing of the site.

By default, adding any processor will mark the entire Search API index as needing reindexing. Often, however, we should completely delete the search index ("clear") and build a fresh one.

#### To reindex using the web UI

Clear the Search API index, and then reindex, using Drush:

```
drush sapi-c
drush sapi-i
```

Learn more about reindexing, and how to do it via the UI, in [Populate Search API Indexes](https://drupalize.me/tutorial/populate-search-api-indexes).

## Recap

Processors allow you to customize the data sent to the search index, as well as modify the search query and results. The motivation is to normalize search data to make results more effective. Furthermore, value-added modifications can be done on search results for a better user experience. Processors are configured as part of the Search API index.

## Further your understanding

- Under what circumstances would you want to write a custom processor?

## Additional resources

- [Search API project](https://www.drupal.org/project/search_api) (Drupal.org)
- [Processors](https://www.drupal.org/docs/8/modules/search-api/getting-started/processors) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Multiple Search API Indexes](/tutorial/multiple-search-api-indexes?p=2815)

Next
[Add Excerpts for Search Results](/tutorial/add-excerpts-search-results?p=2815)

Clear History

Ask Drupalize.Me AI

close
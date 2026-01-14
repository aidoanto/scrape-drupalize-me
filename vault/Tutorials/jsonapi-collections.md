---
title: "JSON:API Collections"
url: "https://drupalize.me/tutorial/jsonapi-collections?p=3277"
guide: "[[decoupled-headless-drupal]]"
order: 14
---

# JSON:API Collections

## Content

JSON:API includes a way to request a list of entities of a given resource from the server. Collections are the best way to find content based on filters, and to build listings into the consumers. Moreover, collections can be combined with all the options you can apply to a single resource, like [sparse fieldsets](https://drupalize.me/tutorial/jsonapi-sparse-fieldsets) and [includes](https://drupalize.me/tutorial/jsonapi-includes).

In this tutorial we'll:

- Learn about what collections are in JSON:API
- Learn how to request, sort, and paginate lists of content

By the end of this tutorial you should know how to retrieve a list of resources from the JSON:API server, and how to optionally sort and paginate the items in the list.

## Goal

Request a list of articles from the JSON:API server in the form of a collection.

## Prerequisites

- [Modern Web Services with JSON:API and GraphQL](https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql)
- [Install JSON:API Module](https://drupalize.me/tutorial/install-jsonapi-module)

Sprout Video

## Fetching a collection of articles

Previously, one of the biggest issues when working with the REST module in Drupal core is that it can't produce collections of entities. You can use the Views module to mitigate that issue. However, when you configure a view and save it to the server you are making the server aware of the presentation of a particular consumer (think of the fields on each row). That goes directly against the mantra we talked about [in a previous tutorial](https://drupalize.me/tutorial/separation-concerns-content-vs-presentation). In fact, the name *Views* already hints at the concept of presentation.

Now, Drupal core includes JSON:API and with it [a feature](http://jsonapi.org/format/#fetching) called *collections*. It is a similar concept to what Views does, but instead of storing the configuration in the server the consumer will specify all the conditions for the lists.

In this tutorial, we will learn how to sort and paginate our collections. We will [learn about filters on collections in a separate tutorial](https://drupalize.me/tutorial/jsonapi-filtering-collections).

## Collection of articles

In its most basic form, a collection is just a request to a resource without specifying an ID. Hence we are requesting information from our */jsonapi/node/article* but we are not specifying the particular article we are interested in. The effect is that we get from the server the list of all the available articles.

Make the following request:

```
# Make a request to the articles resource but do not specify an ID.
http https://example.org/jsonapi/node/article
```

In the response, note how the property `"data"` is no longer holding an object for a particular article but an array of objects instead. Each object in the array represents an individual article.

```
{
  "data" : [
    {
      "type" : "node--article",
      "id" : "3357524f-ebbe-4c12-808d-1783081fc5cb",
      "links" : {
        "self" : "https://example.org/jsonapi/node/article/3357524f-ebbe-4c12-808d-1783081fc5cb"
      },
      "relationships" : {
        "uid" : {
        "data" : {
          "id" : "694d41c7-1890-4597-b899-0bc32ea265e3",
          "type" : "user--user"
        }
  …
```

If we look closely at the results above we can also notice that each one of the articles in the collection comes with a `link.self` property to request that particular article.

Using this procedure we can produce a collection for each resource in our server without any configuration needed. If a new resource gets added, the collection is instantly available.

## Sorted collection

Sorting collections is easy in JSON:API. We can sort any collection based on any attribute in the response. In order to do so we only need to use the `sort` parameter in the URL.

Modify the previous request and append the parameter to sort the list by the article title.

```
# List of articles sorted by title.
http https://example.org/jsonapi/node/article?sort=title
```

We can sort a collection in descending order very easily by adding a `-` in front of the name of the attribute to sort by. Let's sort a list of articles to get the most recent ones first. That request looks like:

```
# List of articles sorted by title.
http https://example.org/jsonapi/node/article?sort=-created
```

We can also sort by multiple properties at the same time. The following request will sort the list of articles by title. When two articles have the same title those will be ordered by most recent first.

```
# List of articles sorted by title and then by creation date.
http https://example.org/jsonapi/node/article?sort=title,-created
```

## Paginated collection

When there are lots and lots of results to return, a collection can grow very big. It can even become a big performance issue when Drupal needs to generate a response for 20,000 articles in one request. Even worse, imagine an attacker that knows there are so many articles and keeps requesting all the 20,000 articles until the Drupal server comes down.

This is why the JSON:API module comes with pagination by default. Using pagination you can limit the number of results returned. To make a collection paginated we will use the `page[limit]` and `page[offset]` parameters.

Make the following request to return *at most* 6 articles in the response.

```
# List articles in pages of 6.
http https://example.org/jsonapi/node/article?page[limit]=6
```

Notice in the response that there are some new links. The link in `links.next` contains the URL to request the next batch (aka page) of articles. Mind that some of the characters in the links have been encoded to be URL friendly.

```
{
    "data": [ {…}, {…} , {…} , {…} , {…} , {…} ],
    "links": {
        "self": "https://example.org/jsonapi/node/article?page%5Blimit%5D=6",
        "next": "https://example.org/jsonapi/node/article?page%5Boffset%5D=3&page%5Blimit%5D=3",
        "first": "https://example.org/jsonapi/node/article?page%5Boffset%5D=0&page%5Blimit%5D=3"
    }
}
```

Let's access the next 6 articles by using the `page[offset]` parameter. That will tell our server to skip as many articles from the list as the number in that parameter. Since we already got the first 6 articles, we need to skip 6 items in order to get the next batch of items. After that, we will need to skip 12 items to get the next batch of items. And so on.

The following request will return the 30th, 31st and 32nd articles.

```
# Return 3 articles, skip the first 29.
http https://example.org/jsonapi/node/article?page[limit]=3&page[offset]=29
```

Pagination is often combined with sort. Imagine that the design for your website consumer shows a *card* at the end of each article showing a teaser to the three most recent articles. The consumer can combine sort and pagination to get a list of articles sorted by creation date in descending order, and then limit the response to 3 items.

```
# The 3 most recent article titles in the content store.
http https://example.org/jsonapi/node/article?page[limit]=3&sort=-created&fields[node--article]=title
```

## Recap

Collections are one of the most powerful tools that the JSON:API implementation for Drupal can offer. It will allow us to interact with the content store without having to find the UUID for the content first. Collections also allow us to request multiple items at the same time.

We have learned that by using the `sort` and `page` query string paramenters we can control how the server creates the collection, from the consumer perspective.

## Further your understanding

- [Explore more sorting and pagination examples in the community documentation for JSON:API](https://www.drupal.org/docs/8/modules/json-api/collections-filtering-sorting-and-paginating).
- Try to request more than 50 items in a single page. What happens? See [this thread in the issue queue](https://www.drupal.org/node/2793233) to understand the security protections the JSON:API module includes.

## Additional resources

- [Fetching Data](https://jsonapi.org/format/#fetching) (jsonapi.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API Relationships](/tutorial/jsonapi-relationships?p=3277)

Next
[JSON:API Includes](/tutorial/jsonapi-includes?p=3277)

Clear History

Ask Drupalize.Me AI

close
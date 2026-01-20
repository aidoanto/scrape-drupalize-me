---
title: "JSON:API Sparse Fieldsets"
url: "https://drupalize.me/tutorial/jsonapi-sparse-fieldsets?p=3277"
guide: "[[decoupled-headless-drupal]]"
order: 16
---

# JSON:API Sparse Fieldsets

## Content

By default, the JSON:API returns all the available data for an object in its response. Using JSON:API *sparse fieldsets* you can increase the performance of your consumer application by reducing the fields in the returned response object to just those that you need.

In this tutorial, we will learn how to reduce the output to get *exactly* the information that we need from the API.

This is one of the most important features of modern APIs like JSON:API.

By the end of this tutorial, you'll know what sparse fieldsets are, the role they fulfill, and how to use them when requesting data from a JSON:API server.

## Goal

Request an article resource using sparse fieldsets so that only the fields we plan to use are included in the response.

## Prerequisites

- [Modern Web Services with JSON:API and GraphQL](https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql)
- [Install JSON:API Module](https://drupalize.me/tutorial/install-jsonapi-module)
- [JSON:API Resource Requests](https://drupalize.me/tutorial/jsonapi-resource-requests)
- [JSON:API Includes](https://drupalize.me/tutorial/jsonapi-includes)

Sprout Video

## Sparse fieldsets

[In previous tutorials](https://drupalize.me/tutorial/jsonapi-resource-requests) we have seen how to request data from the JSON:API server. Each time we requested information about a resource, the response was the full list of the entity's fields. To improve performance in our consumer applications we can reduce the fields in the output. We can do that by providing the full list of fields the consumer cares about.

JSON:API calls this feature *sparse fieldsets*. In order to communicate to our Drupal JSON:API server the fields we want, we have to use the `fields` query string parameter.

Imagine that we want to request the title of an article, the publication date, and the name of the author. We learned in [a previous tutorial](https://drupalize.me/tutorial/jsonapi-includes) that we can get both the article and the author by using the `include` parameter. We can do so by issuing the following request:

```
http https://example.org/node/article/caa01880-46b9-4617-be11-3e020db1b911?include=uid
```

That means that we will get all the fields available for the article and all the fields available for the related user (the author). We can provide the `fields` parameter and specify which fields should be returned for each resource type. To do so, make the following request:

```
http https://example.org/node/article/caa01880-46b9-4617-be11-3e020db1b911?include=uid&fields[node--article]=title,created,uid&fields[user--user]=display_name
```

That will result in:

```
{
  "data": {
    "type": "node--article",
    "id": "caa01880-46b9-4617-be11-3e020db1b911",
    "attributes": {
      "title": "The Best Title Available",
      "created": 1499146003,
    }
  },
  "included": [
    {
      "type": "user--user",
      "id": "893ac8d7-ce93-472a-8641-5122e8b01586",
      "attributes": {
        "display_name": "Wesley"
      }
    }
  ],
  "links": {
    "self": "https://example.org/api/node/article/caa01880-46b9-4617-be11-3e020db1b911"
  }
}
```

In the previous request, we can observe that we added `fields[node--article]=title,created,uid&fields[user--user]=display_name` to the existing request. That indicates that the objects of type `node--article` will only have attributes or relationships with the name `title`, `created`, and `uid`. Note that when using `include=uid` we also need to specify the `uid` field in the sparse fieldset or the include will not work.

In this example, the included `user--user` objects will only contain `display_name`. It's important to note that the `fields` parameter is keyed by the value of the `type` property. Thus doing something like `fields[node/article]=title,created` will not work.

Unlike the other interactions with the API, the `fields` parameter targets its effects to all the objects of a certain type.

When a consumer is requesting data from the API, it's always a good idea to request the fields that the consumer needs to output. If we do that, we will observe a significant decrease in the size of the response. That will lead to a faster transport time from the server to the consumer, making the consumer application faster.

## Recap

In this tutorial, we learned how to get *only* the information that we care about. We used the `fields` parameter keyed by the resource type. In that parameter we provided the names of the attributes or relationships that our consumer wants in the response.

## Further your understanding

- Experiment with the reduction in response size caused by sparse fieldsets:
  - Try to make a request that returns more than 20 results without specifying sparse fieldsets.
  - Write down the number of characters in the response.
  - Then limit the output of those results to one field.
  - Compare the number of characters in this response with the number you wrote down.

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API Includes](/tutorial/jsonapi-includes?p=3277)

Next
[JSON:API Filtering Collections](/tutorial/jsonapi-filtering-collections?p=3277)

Clear History

Ask Drupalize.Me AI

close
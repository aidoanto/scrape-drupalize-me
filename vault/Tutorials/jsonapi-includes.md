---
title: "JSON:API Includes"
url: "https://drupalize.me/tutorial/jsonapi-includes?p=3277"
guide: "[[decoupled-headless-drupal]]"
---

# JSON:API Includes

## Content

Embedding resources at the consumer's demand is one of the crucial features of a modern API. We mentioned in [Modern Web Services with JSON:API and GraphQL](https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql) that multiple round trips to the server is harmful for performance. This issue can be overcome by making a request that embeds any required related resources into the response for the resource we're retrieving.

In this tutorial, we'll learn how to use JSON:API's `include` parameter to embed resources in a response.

By the end of this tutorial, you should be able to make a single request that retrieves multiple embeded resources in order to improve the performance of your application when interacting with a JSON:API server.

## Goal

Request a Drupal entity via JSON:API and included content from related entities in the response object.

## Prerequisites

- [Modern Web Services with JSON:API and GraphQL](https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql)
- [Install JSON:API Module](https://drupalize.me/tutorial/install-jsonapi-module)
- [JSON:API Resource Requests](https://drupalize.me/tutorial/jsonapi-resource-requests)
- [JSON:API Relationships](https://drupalize.me/tutorial/jsonapi-relationships)

Sprout Video

## Using the "include" parameter

The JSON:API specification defines [compound documents](http://jsonapi.org/format/#document-compound-documents) as follows:

> To reduce the number of HTTP requests, servers MAY allow responses that include related resources along with the requested primary resources. Such responses are called “compound documents.”

We can use embedded resources (or compound documents) by specifying the relationships to traverse inside of the `"include"` parameter. We can even provide multiple relationships to traverse. To do so, we specify those relationship names separated by commas. In addition to that, using dot notation we can provide relationship paths that go as deep as necessary.

Every relationship that you go through will be included in the output (this is called *full linkage* in the specification).

**Note:** If the user making the request does not have permission to view the included entity it will not be included and instead an error will be included along with the response. See [API Authentication and Authorization](https://drupalize.me/tutorial/api-authentication-and-authorization) for more information about making authenticated requests and how they relate to Drupal's permissions.

## Request a single embed

Imagine that we want to request from our article resource a list of articles and the authors of each article. Since we know that the author relationship is stored in the `uid` field, we could do something like:

```
http https://example.org/jsonapi/node/article?include=uid
```

That will return a collection of articles (since we didn't provide a specific article ID) along with all the possible authors. Note that even if there are fifty articles returned, we may get only three author objects in the response. That can happen if those fifty articles were written by the same three people. Hence, multiple articles can point to the same author object, without having to embed duplicate copies of each author.

The included entities in JSON:API are moved to a top level member in the response called `"included"`. In order to build the data tree it's the consumer's responsibility to cross reference the relationship type and ID with the entities in the `"included"` section.

This example shows a *recipe* content type with an associated vocabulary named *category*.

Assuming the request `https://example.com/jsonapi/recipes`:

With no `?include=` specified, the data returned contains a reference to any associated category entities via the `data.relationships.category` element. However, this contains limited information about the category: only its ID and information in the `links` section about where to find more details.

```
{
  "data": [
    {
      "type": "recipes",
      "id": "a542e833-edfe-44a3-a6f1-7358b115af4b",
      "attributes": {...},
      "relationships": {
        "contentType": {...},,
        "category": {
          "data": {
            "type": "categories",
            "id": "529406be-17fa-4080-b98d-19d23eaabb7b"
          },
          "links": {
            "self": "https://example.com/jsonapi/recipes/a542e833-edfe-44a3-a6f1-7358b115af4b/relationships/category",
            "related": "https://example.com/jsonapi/recipes/a542e833-edfe-44a3-a6f1-7358b115af4b/category"
          }
        },
      },
      ...
    }
  ],
  "jsonapi": {...},
  "links": {...},
}
```

If we change the query to `https://example.com/jsonapi/recipes?include=category` the backend will perform some additional lookups and include additional category information in the response. This information is entered into the `included` top-level element of the response. There will be one entry in here for each unique category encountered when looking up the list of recipes. This keeps the size of the response down by removing possible duplicate content.

Note that the `data.relationships.category` element in the main `data` of the response doesn't change. In order to make use of the additional included data your code will need to use the `data.relationships.category.data.id` property to find the relevant details in the `included[]` list.

```
{
  "data": [
    {
      "type": "recipes",
      "id": "a542e833-edfe-44a3-a6f1-7358b115af4b",
      "attributes": {...},
      "relationships": {
        "contentType": {...},,
        "category": {
          "data": {
            "type": "categories",
            "id": "529406be-17fa-4080-b98d-19d23eaabb7b"
          },
          "links": {
            "self": "https://example.com/jsonapi/recipes/a542e833-edfe-44a3-a6f1-7358b115af4b/relationships/category",
            "related": "https://example.com/jsonapi/recipes/a542e833-edfe-44a3-a6f1-7358b115af4b/category"
          }
        },
      },
      ...
    }
  ],
  "jsonapi": {...},
  "links": {...},
  "included": [
    {
      "type": "categories",
      "id": "529406be-17fa-4080-b98d-19d23eaabb7b",
      "attributes": {
        "internalId": 1,
        "name": "Salad",
        ...
      },
      "relationships": {
        "parent": {
          "data": []
        }
      },
      "links": {
        "self": "https://example.com/jsonapi/categories/529406be-17fa-4080-b98d-19d23eaabb7b"
      }
    }
  ]
}
```

## Request multiple embeds

JSON:API allows us to include relationships on included relationships on included relationships, and so on. Let's call this nested includes. From the consumer, we can indicate to the server that we want nested includes by adding the additional relationship separated by a dot. Keep in mind that *full linkage* requires you to include all the different steps in the nested includes. Something like `uid.user_picture` will not work; instead we need to provide `uid,uid.user_picture`.

Make the following request to get some articles along with their authors, the pictures of the authors, and the content type information in the relationship:

```
http https://example.org/jsonapi/node/article?include=uid,uid.user_picture,type
```

This will return the following response (trimmed for readability).

```
{
  "data": [
      {
        "type": "node--article",
        "id": "ea595154-8269-4f3f-b3c6-8ed1cdd3cfd3",
        "attributes": {
          "nid": 46,
          "uuid": "ea595154-8269-4f3f-b3c6-8ed1cdd3cfd3",
          "status": true,
          "title": "Ad Hendrerit Sagaciter Si",
          …
        },
        "relationships": {
          "type": {
            "data": {
              "type": "node_type--node_type",
              "id": "59e75399-24fd-4fe5-95c5-d94875cfad22"
            },
          },
          "uid": {
            "data": {
              "type": "user--user",
              "id": "31ce8475-eb62-4515-ad27-51cab282c387"
            }
          }
        }
      }
    ],
  "included": [
    {
      "type": "node_type--node_type",
      "id": "59e75399-24fd-4fe5-95c5-d94875cfad22",
      "attributes": {
        "uuid": "59e75399-24fd-4fe5-95c5-d94875cfad22",
        "langcode": "en",
        "name": "Article",
        "type": "article",
        "description": "Use <em>articles</em> for time-sensitive content like news, press releases or blog posts.",
        …
      },
    },
    {
      "type": "user--user",
      "id": "31ce8475-eb62-4515-ad27-51cab282c387",
      "attributes": {
        "uid": 1,
        "uuid": "31ce8475-eb62-4515-ad27-51cab282c387",
        "langcode": "en",
        "name": "admin",
        "created": 1499409728,
        "changed": 1500095913,
      },
      "relationships": {
        "user_picture": {
          "data": {
            "type": "file--file",
            "id": "7ba36aed-935b-4f46-925e-655bd9b81f9e",
            "meta": {
              "alt": "",
              "title": "",
              "width": "77",
              "height": "85"
            }
          }
        }
      }
    },
    {
      "type": "file--file",
      "id": "7ba36aed-935b-4f46-925e-655bd9b81f9e",
      "attributes": {
        "fid": 25,
        "uuid": "7ba36aed-935b-4f46-925e-655bd9b81f9e",
        "filename": "foo.jpeg",
        "uri": "public://pictures/2017-07/foo.jpeg",
        "filemime": "image/jpeg",
        "url": "/sites/default/files/pictures/2017-07/foo.jpeg"
      },
      "relationships": {
        …
      }
    }
  ]
}
```

We can observe how we requested two different branches from the articles relationship tree: `type` and `uid,uid.user_picture`. The JSON:API module for Drupal will return all the entities traversed in all of the branches. It will put them in a single pool of data under the `"included"` member.

## Recap

In this tutorial, we learned about one of the most powerful tools (in addition to collections) that the JSON:API module offers. Requesting all the related data that our Angular single page application will need, in a single request, will improve our page's performance greatly. Additionally, it will simplify the code in the consumer since we don't have to juggle with multiple HTTP requests; we only need one.

## Further your understanding

- What happens if you include a multi-value relationship (like `field_tags`)?
- Can you predict the result of nested includes in multivalue relationships that contain multivalue relationships?
- Trace the relationship tree from the article to the user picture. Find the entities in the `"included"` member based on the entity type and ID.
- Combine embedding with sparse fieldsets to request only the fields you're interested in from an included resource.

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API Collections](/tutorial/jsonapi-collections?p=3277)

Next
[JSON:API Sparse Fieldsets](/tutorial/jsonapi-sparse-fieldsets?p=3277)

Clear History

Ask Drupalize.Me AI

close
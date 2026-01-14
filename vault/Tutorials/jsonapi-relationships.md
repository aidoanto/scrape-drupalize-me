---
title: "JSON:API Relationships"
url: "https://drupalize.me/tutorial/jsonapi-relationships?p=3277"
guide: "[[decoupled-headless-drupal]]"
order: 13
---

# JSON:API Relationships

## Content

Drupal allows for a rich data model where entity reference fields can be used to relate any number of different items together in different ways. The data models that you can build with Drupal are often prolific in relationships, which means we need a way to handle these in our API. While Drupal treats a field with a string, and a field with an entity reference the same, JSON:API distinguishes between attributes and relationships.

In this tutorial we'll:

- Look at how JSON:API represents relationships between two or more resources
- How to distinguish between an attribute and a relationship in a response object
- Learn about what information is available for each relationship and how we can use it

By the end of this tutorial, you should have a better understanding of how the JSON:API specification represents relationships modeled using Drupal entity reference fields.

## Goal

Make an HTTP request for a node and explore the relationship section.

## Prerequisites

- [Modern Web Services with JSON:API and GraphQL](https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql)
- [Install JSON:API Module](https://drupalize.me/tutorial/install-jsonapi-module)
- [JSON:API Resource Requests](https://drupalize.me/tutorial/jsonapi-resource-requests)

Sprout Video

## Relationship structure

We learned how to request a node in [a previous tutorial](https://drupalize.me/tutorial/jsonapi-resource-requests). We saw that an example of a response can look like:

```
{
    "data": {
       "type": "node--article",
       "id": "d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1",
       "attributes": {
            …
            "title": "Abico Importunus",
        },
        "relationships": {
            …
            "field_image": {
                "data": {
                    "id": "e8eb2b4f-2d94-4c3e-8cc3-9dca66e7b295",
                    "meta": {
                        "alt": "Duis neque pertineo qui ullamcorper.",
                        "height": "494",
                        "title": "Pertineo qui ullamcorper",
                        "width": "422"
                    },
                    "type": "file--file"
                },
                "links": {
                    "related": "https://example.org/jsonapi/node/article/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/field_image",
                    "self": "https://example.org/jsonapi/node/article/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_image"
                }
            },
            "field_tags": {
                "data": [
                    {
                        "id": "db667e20-ddc6-478c-8d45-2d4d885b206e",
                        "type": "taxonomy_term--tags"
                    },
                    {
                        "id": "df6fbc75-7623-415a-ab9b-276936bdaeca",
                        "type": "taxonomy_term--tags"
                    }
                ],
                "links": {
                    "related": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/field_tags",
                    "self": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_tags"
                }
            }
        }
    }
}
```

(We've abbreviated this response for readability.)

The response above contains a [resource object](http://jsonapi.org/format/#document-resource-objects) (corresponding to a Drupal entity) inside of the `"data"` property. Let's focus on the `"relationships"` section inside the resource object.

The contents of the `"relationships"` member is [described in the specification](http://jsonapi.org/format/#document-resource-object-relationships) as an object with the names of the relationships as the keys and relationship objects as the values. These are the `"relationships"` of our example:

```
"field_image": {
    "data": {
        "id": "e8eb2b4f-2d94-4c3e-8cc3-9dca66e7b295",
        "meta": {
            "alt": "Duis neque pertineo qui ullamcorper.",
            "height": "494",
            "title": "Pertineo qui ullamcorper",
            "width": "422"
        },
        "type": "file--file"
    },
    "links": {
        "related": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/field_image",
        "self": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_image"
    }
},
"field_tags": {
    "data": [
        {
            "id": "db667e20-ddc6-478c-8d45-2d4d885b206e",
            "type": "taxonomy_term--tags"
        },
        {
            "id": "df6fbc75-7623-415a-ab9b-276936bdaeca",
            "type": "taxonomy_term--tags"
        }
    ],
    "links": {
        "related": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/field_tags",
        "self": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_tags"
    }
}
```

We can see how there is one relationship called `"field_image"` and another one called `"field_tags"`.

Each relationship object has three possible keys:

- `"data"`: Contains the information about the referenced resource entities.
- `"links"`: Contains the URLs of additional HTTP calls relevant for this relationship.
- `"meta"`: Contains meta information about the relationship.

### The "data" property

The data property always contains the necessary information to find the referenced entities in the relationship. With the information in this property we will be able to request the related entities from the JSON:API server.

Depending on whether the entity reference is single value or multivalue, the contents of the this `"data"` member will be an object or an array of objects. The contents in both cases is the same but the single relationship refers to the item directly, not an array. Compare the data for `"field_image"` and for `"field_tags"` to see the differences between single value and multivalue relationships.

The `"data"` member contains the crucial part about the relationship: the target type and the target ID. With this information we can request more information about the referenced entity. See how the examples above contain one pair of `"type"` and `"id"` for each item in every relationship.

Once we have the resource type and the resource ID we can constuct the URL to request the related entity. In the `"field_image"` example that would be:

```
# Request the Image based on the information present in the relationship.
http https://example.org/jsonapi/file/file/e8eb2b4f-2d94-4c3e-8cc3-9dca66e7b295
```

In a later tutorial we will see that we don't need to manually construct any URL. Instead we will use resource embedding to ask for a particular article and *include* the `"field_image"` in it.

### The "links" property

The links section is especially interesting for relationships. This section will provide us with a list of fully qualified URLs and a label for each link. In particular the Drupal module provides the *related* and *self* (aka *relationship*) links, [as suggested by the specification](http://jsonapi.org/format/#document-resource-object-relationships). More links can be added by extending the JSON:API module.

Make an HTTP request to the contents of the *self* link. You should see something like:

```
http https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_tags
```

```
{
    "data": [
        {
            "id": "db667e20-ddc6-478c-8d45-2d4d885b206e",
            "type": "taxonomy_term--tags"
        },
        {
            "id": "df6fbc75-7623-415a-ab9b-276936bdaeca",
            "type": "taxonomy_term--tags"
        }
    ],
    "links": {
        "related": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/field_tags",
        "self": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_tags"
    }
}
```

This link yields information about the relationship itself. In this particular case it does not provide more information than what you already had, but this is seldom the case. In fact the `"self"` link in a relationship is more useful when using it with the `POST` and `PATCH` HTTP methods [to update relationships](http://jsonapi.org/format/#crud-updating-relationships).

The main goal of the *links* member is to hold pointers ready to use by a consumer application. This way an iPad app could add a tag to an article by sending the JSON object for the tag into whatever the "self" link on the field\_tags relationship specifies.

### The "meta" property

According to the specification, the `"meta"` property is used to respond with relevant information about the relationship. This is true anywhere in the document where you can have a `"meta"` member, not only for relationships. The spirit of this `"meta"` section is to provide information that is not *content*. A good way to think about this is to ask ourselves the question, "Would an editor input this information?" If the answer is *Yes*, then the information is probably content and it's not appropriate to be returned in the `"meta"` section. Things like *the time the query took to execute in the server*, *the total number of records*, etc. are good candidates for the `"meta"` member.

The JSON:API module for Drupal violates this spirit to return important content about the relationship itself. This is because Drupal often stores information that belongs to neither the host entity nor the target entity: it belongs to the link between the two. The JSON:API specification doesn't anticipate that possibility. A good example of this is the *title* and *alt* attributes when creating an image.

Request the relationship for `"field_image"` using the `"self"` link in the response to the node. You can do:

```
http https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_image
```

```
{
    "data": {
        "id": "e8eb2b4f-2d94-4c3e-8cc3-9dca66e7b295",
        "meta": {
            "alt": "Duis neque pertineo qui ullamcorper.",
            "height": "494",
            "title": "Pertineo qui ullamcorper",
            "width": "422"
        },
        "type": "file--file"
    },
    "links": {
        "related": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/field_image",
        "self": "https://example.org/jsonapi/articles/d99f021b-c3c8-41f0-bd8d-c8d02c22e2a1/relationships/field_image"
    }
}
```

## Recap

In this tutorial we learned how the JSON:API server responses contain structured information about relationships.

- We were able to request a node from the server and identify the different relationships in there.
- We have discovered how links can be used by consumer applications to execute operations on the relationships.
- We saw that references in Drupal that contain additional information about the relationship return this information inside the `"meta"` member.

## Further your understanding

- What happens when you request the other `"links"` in the relationship? What about the rest of the links in the article?
- [Learn more about HATEOAS](https://en.wikipedia.org/wiki/HATEOAS), which is the idea of mostly using links to interact with the API.
- [Learn more about the `POST` and `PATCH` HTTP methods on the relationship endpoint](http://jsonapi.org/format/#crud-updating-relationships).

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API Resource Requests](/tutorial/jsonapi-resource-requests?p=3277)

Next
[JSON:API Collections](/tutorial/jsonapi-collections?p=3277)

Clear History

Ask Drupalize.Me AI

close
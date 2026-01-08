---
title: "JSON:API Filtering Collections"
url: "https://drupalize.me/tutorial/jsonapi-filtering-collections?p=3277"
guide: "[[decoupled-headless-drupal]]"
---

# JSON:API Filtering Collections

## Content

[Collections](https://drupalize.me/tutorial/jsonapi-collections) are a very powerful feature because they allow us to access multiple items at the same time. However, in many situations we do not want to access all the entities of a given type, but only the ones that meet some specific criteria. In order to reduce the set of entities in the collection to the ones we care about, we use filters.

In this tutorial we will:

- Look at the `filter` query string parameter and how it can be used with JSON:API collections
- Learn how to use filters in combination with the JSON:API module for Drupal to reduce the list of entities in a collection

By the end of this tutorial you should be able to request a list of entities in the form of a JSON:API collection and filter that list to include only the entities that match a specific set of requirements.

## Goal

Request a collection of articles from the JSON:API server that includes only those that match a set of requirements.

## Prerequisites

- [Modern Web Services with JSON:API and GraphQL](https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql)
- [Install JSON:API Module](https://drupalize.me/tutorial/install-jsonapi-module)
- [JSON:API Resource Requests](https://drupalize.me/tutorial/jsonapi-resource-requests)
- [JSON:API Collections](https://drupalize.me/tutorial/jsonapi-collections)

Sprout Video

## "Fancy Filters"

The official specification does not specify how consumers should interact with the server in order to apply filters to the response. All the specification requires is to use the `filter` query string parameter to specify those filters.

The Drupal module implements [a filtering strategy called *Fancy Filters*](https://gist.github.com/e0ipso/efcc4e96ca2aed58e32948e4f70c2460). This filtering strategy matches what the [`EntityQuery`](https://drupalize.me/tutorial/find-data-entityquery?p=2792) can do. In fact, this filter syntax is a one-to-one map with `EntityQuery`.

As in `EntityQuery`, there are two main forms of interaction: conditions and groups. Conditions are the main way to specify rules that the content has to meet in order to pass the filter. This normally involves a value and an operator for a certain field in an entity. Groups are a way to bundle conditions together. Each group is evaluated separately first, and then with the other groups using a conjuction (typically an `OR` or an `AND`). It's not the focus of this tutorial to explain the multiple capabilities of `EntityQuery` in depth.

## The shorthand filter form

The most common form of filtering is to specify a field and a value. With that kind of filter we will only get the entities that have the specified value in that specific field. The following filter will only return our articles with the title *LoremIpsum*. Make the following request:

```
http https://example.org/jsonapi/node/article?filter[title][value]=LoremIpsum
```

## The full form syntax

A condition filter needs five pieces:

- **filter ID**: This is some text that the consumer decides to use to refer to the filter in each option.
- **filter type**: Either `condition` or `group`. This corresponds to the options that `EntityQuery` offers.
- **path** property: The path to the field used to filter against. In this tutorial the **path** corresponds to the name of the field to filter against.
- **value**: This is used to compare the actual content of the field, in the provided path, for every eligible entity in Drupal.
- **operator** to compare: Sometimes checking if the field content is equal to a provided value is not enough. Sometimes we need to ask for entities where the field has a value different from the one provided, or greater than, etc.

The previous filter `filter[title][value]=LoremIpsum` is the shorthand for `filter[title][condition][path]=title&&filter[title][condition][value]=LoremIpsum`:

- Filter ID: `title`
- Filter type: `condition`
- Path: `title`
- Value: `LoremIpsum`
- Operator: `=`

Make a request that will select all the articles written after `06/07/2017 07:12`. You can do it like:

```
https://example.org/jsonapi/node/article
  ?filter[afterBirthday][condition][path]=created
  &filter[afterBirthday][condition][value]=1496757600
  &filter[afterBirthday][condition][operator]=>
```

The request will return a list of articles that were created after a given timestamp. We can break down that filter into its components in the following way:

- Filter ID: `afterBirthday`
- Filter type: `condition`
- Path: `created`
- Value: `1496757600`
- Operator: `>`

## Combining filters

Just like `EntityQuery`, the JSON:API module allows you to combine multiple filters. By default, the results will need to meet all the filters in order to be returned. This is because multiple API filters interact with each other with an `AND` operator unless otherwise specified using *groups*.

Imagine that we want to find the articles that are both written after a certain date and have the title *LoremIpsum*. In order to do that we need to concatenate the two different filters. Note how all the query string parameters for a given filter are under the same filter ID.

```
https://example.org/jsonapi/node/article
  ?filter[title][condition][path]=title
  &filter[title][condition][value]=LoremIpsum
  &filter[afterBirthday][condition][path]=created
  &filter[afterBirthday][condition][value]=1496757600
  &filter[afterBirthday][condition][operator]=>
```

## Groups of filters

If nothing else is specified, JSON:API for Drupal will assume that all the filters belong to a single group that operates with an `AND` conjunction. In order to change that we will need to use the *group* filter type.

If we want to retrieve all the articles that have title *LoremIpsum* and are written after a given date **or** that have the title *I Love Blue Cheese*, we will need to use groups.

In this example we have three groups. One group is for the date filter `AND` the title *LoremIpsum*. The second group is the title condition on *I Love Blue Cheese* (regardless of the date). The last group will link group 1 and group 2 with an `OR` conjunction. Make that filter query against JSON:API using *Fancy Filters*. We can do it like:

```
https://example.org/jsonapi/node/article?
  ?filter[lorem][group][conjunction]=AND
  &filter[lorem][group][memberOf]=root
    &filter[title][condition][path]=title
    &filter[title][condition][value]=LoremIpsum
    &filter[title][condition][memberOf]=lorem
    &filter[afterBirthday][condition][path]=created
    &filter[afterBirthday][condition][value]=1496757600
    &filter[afterBirthday][condition][operator]=>
    &filter[afterBirthday][condition][memberOf]=lorem
  &filter[cheese][group][conjunction]=AND
  &filter[cheese][group][memberOf]=root
    &filter[title][condition][path]=title
    &filter[title][condition][value]=I Love Blue Cheese
    &filter[title][condition][memberOf]=cheese
  &filter[root][group][conjunction]=OR
```

There are 2 new parts in the query above. The first is that we are using filters with the *group* type instead of the *condition* type. This type is used to specify options on the group of conditions. The group can be configured with 2 parameters: the parent group, and the conjunction applied to all the conditions in that group.

The other new thing is that in order to assign a condition or another group into a certain group we use the `memberOf` keyword.

In the end we'll have a grouping like:

```
root -> (
    lorem  -> (title == LoremIpsum AND created > 1496757600)
    OR
    cheese -> (title == I Love Blue Cheese)
)
```

Using this technique a consumer can discover the content that it needs. This is crucial to implement complex designs based on rich structured content. This feature is powerful, even if it can become verbose for complex queries.

## Recap

In this tutorial we learned how to find entities based on the contents of their fields. We used the `filter` parameter so the JSON:API module can execute an `EntityQuery` to find the desired entities. We have also learned the syntax of the *Fancy Filter* specification. This syntax allows us to express the query in the URL to find the content in Drupal. Combining conditions and groups, we learned that we can make complex queries to filter the collection of articles to get exactly the articles that we want.

## Further your understanding

- Read [the official documentation](https://www.drupal.org/docs/8/modules/json-api/collections-filtering-sorting-and-paginating) to find other operators you can use. Describe the components of a filter to filter all the articles that contain the words "Blue Cheese" in the title written before January 1st, 2007.
- [Learn about filters through relationships](https://drupalize.me/tutorial/jsonapi-filters-nested-relationships).

## Additional resources

- [JSON API Fancy Filters](https://gist.github.com/e0ipso/efcc4e96ca2aed58e32948e4f70c2460) (gist.github.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API Sparse Fieldsets](/tutorial/jsonapi-sparse-fieldsets?p=3277)

Next
[JSON:API Filters on Nested Relationships](/tutorial/jsonapi-filters-nested-relationships?p=3277)

Clear History

Ask Drupalize.Me AI

close
---
title: "JSON:API Filters on Nested Relationships"
url: "https://drupalize.me/tutorial/jsonapi-filters-nested-relationships?p=3277"
guide: "[[decoupled-headless-drupal]]"
---

# JSON:API Filters on Nested Relationships

## Content

Includes and filters are really powerful features. When combined together you can achieve almost any query your consumer application needs. *Fancy filters* we mentioned [in a previous tutorial](https://drupalize.me/tutorial/jsonapi-filtering-collections) allow us to filter a collection based on fields of related entities, in addition to the fields directly under that entity.

In this tutorial we will:

- Learn about filtering based on data in related resources
- Filter based on multiple conditions and multi-value fields
- Demonstrate how to filter a collection of articles based on author or tags

By the end of this tutorial you should be able to use nested filters in conjunction with relationships to further refine the list of content returned in a JSON:API collection.

## Goal

Request a collection of articles from the JSON:API server by using filters to restrict results based on data contained in nested resources.

## Prerequisites

In order to get the most out of this tutorial you should have finished the tutorial on [how to do basic filters using JSON:API](https://drupalize.me/tutorial/jsonapi-filtering-collections).

Sprout Video

## Filters on relationships

It is very common to have requirements like "Display on the front page a list of TV shows with an episode that aired last week" in our consumer application. In that example, we want to request data from the hypothetical TV shows resource, since we want TV show entities back from the API. In this particular case we want to limit the shows we get back based on the *field\_air\_date* field that lives in the episode entity. For this example the TV show entity contains a relationship to a season entity, which in turn contains a relationship to the episode entities that contain the *field\_air\_date* field.

In summary, we need to declare a filter on TV shows based on a property that lives in a related entity. To do so in JSON:API we only need to modify the `path` in our filter to traverse the relationships until we reach *field\_air\_date*. A filter like that would look like:

```
https://api.themoviesapi.local/show
?filter[date][condition][path]=field_season.field_episodes.field_air_date
&filter[date][condition][operator]=<
&filter[date][condition][value]=1500267831
```

Notice how the `path` property traverses the `field_season` entity reference in the TV show and the `field_episodes` in the seasons. Once we are at the episode entity, we specify that our condition applies to the `field_air_date`.

## Articles by author

Going back to our article example, imagine that we want to get all the articles written by a certain author. There we want to follow the `uid` relationship to get to the user, and then check the `name` to make sure it's the author we want. Make a request against the articles resource to get all the articles written by *famousauthor*.

```
https://example.org/jsonapi/node/article?filter[uid.name][value]=famousauthor
```

Notice how we used the shorthand syntax to provide the path through the `uid` relationship to the `name` property. Use `?filter[author][condition][path]=uid.name&filter[author][condition][value]=famousauthor` if you prefer the longer syntax.

## Multiple conditions on multi-value fields

There are occasions where you want to place multiple filters in a single multi-value field. Imagine that we are filtering on a multi-value date field. And we want to express the filter "Return all the items that have one date within the past week." We would probably use a filter like:

```
# The field date is
?filter[multiDates][condition][path]=field_dates
# Within the start of two weeks ago
&filter[multiDates][condition][value]=1500267831
&filter[multiDates][condition][operator]=<
&filter[multiDates][condition][path]=field_dates
# And the end of one week ago.
&filter[multiDates][condition][value]=1500872604
&filter[multiDates][condition][operator]=>
```

The intention of the query above is to match an entity that has at least one of the dates in the last week.

Now imagine that we want to match all of the entities that have both one of the dates after 2 weeks ago and one of the dates before last week. We would probably write the same exact filter we did above.

```
# Two field dates match two things
?filter[multiDates][condition][path]=field_dates
# One is after two weeks ago
&filter[multiDates][condition][value]=1500267831
&filter[multiDates][condition][operator]=<
&filter[multiDates][condition][path]=field_dates
# Another one is before one week ago.
&filter[multiDates][condition][value]=1500872604
&filter[multiDates][condition][operator]=>
```

In the first case our intention was that all of the filters were satisfied by an individual date in the multi-value date field. In the second case we intended each one of the filters to be satisfied by any date in the multi-value date field. But notice how the query we wrote is exactly the same. It is clear that we will only get the correct results for one of them, but which one is it?

Even though this problem is not specific to JSON:API it can make multi-condition filters on multi-value fields very confusing. Since the JSON:API module will pass all the filters to the `EntityQuery` component, the result of our filters will depend on the results of that query. In our example above we will get the expected results in the first scenario, where all the conditions need to match in the same date item of the multi-value field. That does not mean that we can't fulfill the second scenario; however, we will need to make 2 queries for that. The first query will get all the items before a certain date. The second query will add a filter by node id -- to only consider the results returned for the first query -- and then filter those further to only return the ones after a certain date.

## Articles by tags

With all that in mind, let's get back to our articles example and fetch all the articles that are tagged with either *yummy* or *delicious*.

```
https://example.org/jsonapi/node/article
?filter[or-group][group][conjunction]=OR
  &filter[t1][condition][path]=field_tags.name
  &filter[t1][condition][value]=yummy
  &filter[t1][condition][memberOf]=or-group
  &filter[t2][condition][path]=field_tags.name
  &filter[t2][condition][value]=delicious
  &filter[t2][condition][memberOf]=or-group
```

## Recap

In this tutorial we have learned how to filter entities by fields that are not in that entity, but in other related entities instead. In particular we have reduced the collection of articles to the ones written by a certain author. Then we did the same for those tagged with some specific tag names.

We have also learned about the complexity of adding multiple filters to multi-value fields, and what to expect when we do that.

## Further your understanding

- Some of the filters in the queries above can be converted to the shorthand syntax. What would they look like? Do you prefer the brief form or the more expressive one?
- How would you get all the articles tagged with the term *kitten* written by an author with the email [[email protected]\_](/cdn-cgi/l/email-protection#f1ae859994df959e92859e83b19489909c819d94df9e8396ae).

## Additional resources

- [Official API documentation for EntityQuery](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Query%21QueryInterface.php/interface/QueryInterface) (Drupal.org)
- [Learn more about the Entity API in Drupal and how to query it.](https://drupalize.me/tutorial/find-data-entityquery) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API Filtering Collections](/tutorial/jsonapi-filtering-collections?p=3277)

Next
[JSON:API Error Handling](/tutorial/jsonapi-error-handling?p=3277)

Clear History

Ask Drupalize.Me AI

close
---
title: "Overview: Relationships in Viewsfree"
url: "https://drupalize.me/tutorial/overview-relationships-views?p=2670"
guide: "[[views-drupal]]"
---

# Overview: Relationships in Viewsfree

## Content

In order to display values for referenced entities in views, you need to add a relationship. What is a relationship, how do they work, and what does it mean to require this relationship? What are some common use cases for adding a relationship to a view? By the end of this tutorial you should be able to:

- Explain some common use cases for adding a relationship to a view.
- Understand the concept of entity references and how those field values can be displayed in a view.

## Goal

Understand the concept of entity references and be able to explain some common use cases for adding a relationship to a view.

## Prerequisites

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Relationships, entities, and entity references

Fundamentally, *relationships* are a mechanism we can use in Views to be able to access data in a view that we would not otherwise be able to access. To completely understand how the *relationship* mechanism works, we need to take a few steps back and discuss the concepts of *entities* and *entity reference* fields.

### Entities in Drupal

In Drupal, *entity* is a general concept that represents a noun (person, place or thing). Out of the box, there are a number of different types of entities in Drupal, each meant to represent a specific type of data.

One type of entity is a *user*. A user entity contains information that is specific to people that visit our site, such as the user's email address and password. Within the concept that entities represent nouns, a user entity is a person.

Another entity type in Drupal is *content* (sometimes called a *node*) entity. Content entities contain data that is relevant for a something that is expected to be visited and consumed, such as a URL path, title, and body. Continuing with the concept that entities represent nouns, a content entity is a place. It has a URL and can be visited and it contains content that is meant to be consumed by a visitor.

Additionally, each content entity in Drupal has an owner. The owner (often referred to as the author) of a specific piece of content is a user entity. Most often the owner of some content is the user that created the content. Continuing with our analogy of a user representing a person and content representing a place, then it makes sense that a person would own a place. This concept of a user entity owning a content entity is a relationship. And that relationship is made practical in our site by the use of *entity reference* fields.

### Entity reference fields

When designing Drupal entities such as content types or users, we can create relationships between entities through an *entity reference* field. The entity reference field type allows us to create fields on one entity that can reference another entity.

> Entity reference fields allow us to link entities together so that we don't have to duplicate data.

Image

![Screenshot of add field form with entity references highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/relationships--add-entity-reference-field.png?itok=udQLubRg)

Consider a simple blog website where we'd like to show a picture of the author alongside their article. If we had to upload that author's picture to a field on each article that that person authored, then we'd be duplicating a lot of data on our site for very little value. Instead, it would be much more efficient for us to upload the author's picture to a field via the author's user entity, then reference the user on each article in the article's author field. This is exactly how Drupal's content entities are configured. This is the reason each content entity has an entity reference field that points to a user entity.

For example, let's take a look at the Article content type. Articles contain two entity reference fields: Tags and Author. Tags allows you to reference taxonomy terms in the Tag vocabulary. (Taxonomy terms are another type of entity.) The Author field allows you to reference a specific user entity as the author.

Image

![Screenshot of article edit form with tags and authored by fields highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/relationships--article-entity-reference-fields.png?itok=VcGoGxd0)

To summarize, an *entity* is a type of data that represents some "noun" and an *entity reference* is a means for one entity to reference another type of entity, thereby creating a relationship between those two entity types. Creating relationships between entities means we will rarely (if ever) need to duplicate data.

## Relationships in views

When adding a new view, we begin by choosing an entity type to use as our *base table*. (Let's call this our *base entity*.) We make this choice via the *Show* field on the *Add view* form. When making this choice, we want to ask ourselves, "I'm making a list of which entity?" Here we choose an entity to *show* and we can also specify options relevant to our chosen entity (which will add one or more filter criteria to our view's configuration). Our choice here becomes the primary adjective we'll use when describing our view, e.g. content view, comments view, etc. Or, alternatively, "view of content", "view of taxonomy terms", "view of users", etc.

Image

![Screenshot of add view form with options for show field highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/relationships--view-create-form.png?itok=dziccze2)

Adding relationships to a view is how we pull data from entities other than our base entity into our view. In order to do that, our chosen entity must have an entity reference field added to it. Our view can only add relationships to entities related via our base entity's *entity reference field*. (The entity reference field's configuration specifies which entity type/sub-type can be referenced in it.)

On the view edit form, the **Relationships** section is located within the **Advanced** column (collapsed/hidden by default). We can add relationships to our view in the same way we add other mechanisms to views, by selecting *Add* next to *Relationships*.

Image

![Screenshot of Views UI with Relationships section highlighted](/sites/default/files/styles/max_800w/public/tutorials/images/relationships--locate-add-relationship.png?itok=hJCgPQ-V)

When adding a relationship to a view we are presented with a list of available relationships to the type of *Entity* we selected for the *Show* field when creating our view. In this example, we're working on a view that is a list of *Content* entities.

Image

![Screenshot of add relationships modal window with available fields listed](/sites/default/files/styles/max_800w/public/tutorials/images/relationships--list-of-content-relationships.png?itok=mdrn5Kj5)

Notice how one of the available relationships is the *Content author*. Adding that relationship to our view will allow us to get data into our view about the author of the content. Without the relationship, the author's data (in a user entity) would not otherwise be available to our view of content entities.

After adding the *Content author* relationship to the view, we can now use the author's *User* entity data throughout the rest of the view as *fields*, *filter criteria*, *sort criteria*, *contextual filters*, and even in other *relationships*.

Image

![Screenshot of Views UI pointing author relationship to field and filter using that relationship](/sites/default/files/styles/max_800w/public/tutorials/images/relationships--field-and-filter-author.png?itok=pPf7nfYg)

## Recap

Adding relationships to a view allows us to pull in data from other *entities* that are related to our list of content by *entity reference* fields. Relationships are a powerful Views mechanism that allow us to access our reusable data to display, filter, or sort by that data. Without relationships, we would have to duplicate a lot of data in our Drupal site.

## Further your understanding

- Familiarize yourself with your site's content types or other entities. Which fields use the entity reference field type? Which types/sub-types of entities can be referenced? Think about the connections between your content types via entity reference fields and how you could enhance your content listings with data from related entities.

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Expose Sort Criteria to Users in Views](/tutorial/expose-sort-criteria-users-views?p=2670)

Next
[Add a Relationship to a View](/tutorial/add-relationship-view?p=2670)

Clear History

Ask Drupalize.Me AI

close
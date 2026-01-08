---
title: "JSON:API DELETE Requests: Delete an Entity"
url: "https://drupalize.me/tutorial/jsonapi-delete-requests-delete-entity?p=3279"
guide: "[[decoupled-headless-drupal]]"
---

# JSON:API DELETE Requests: Delete an Entity

## Content

Occasionally we need to remove entities from the backend using the API. REST APIs, and in particular JSON:API, use the HTTP DELETE method to accomplish this.

In this tutorial we'll create a request for deleting a single entity. By the end of this tutorial you should be able to issue requests that can delete any entity via JSON:API.

## Goal

Delete a specific article from the Drupal backend using the JSON:API web service.

## Prerequisites

- [Make an Authenticated Request Using OAuth 2](https://drupalize.me/tutorial/make-authenticated-request-using-oauth-2)
- [Install JSON:API](https://drupalize.me/tutorial/install-jsonapi-module)
- [JSON:API Resource Requests](https://drupalize.me/tutorial/jsonapi-resource-requests)
- [JSON:API POST Requests: Create an Entity](https://drupalize.me/tutorial/jsonapi-post-requests-create-entity)

## Delete an article

We can delete any article by issuing a DELETE request for the individual entity we want to remove. The DELETE HTTP method is the standard way of deleting persisted information in REST web services.

To delete an entity, we need to construct the URL based on its UUID. That is `/jsonapi/node/article/<entity-uuid>`. It is not possible to delete entities using the collections endpoint; we need to remove each entity explicitly. With that URL containing the UUID you need to use the DELETE HTTP method in the request. It's probable that the ability to remove an entity from Drupal requires the user to be authenticated and have the correct permissions. Therefore we will need to [send the authentication token with the request](https://drupalize.me/tutorial/make-authenticated-request-using-oauth-2).

An example request might look like:

```
http DELETE https://www.example.org/jsonapi/node/article/c0a07ee4-157f-4404-a64f-4f8797703867 'Authorization:Bearer eyJ0eXAi...dQOQw'
```

## Recap

To remove an entity, we need the JSON:API URL with the UUID, and the authentication token that identifies the user making the request. With those two pieces we can send a DELETE request to the server that will remove the selected entity from Drupal.

## Further your understanding

- What happens when you try to delete an article without the proper authentication?

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API PATCH Requests: Update an Entity](/tutorial/jsonapi-patch-requests-update-entity?p=3279)

Clear History

Ask Drupalize.Me AI

close
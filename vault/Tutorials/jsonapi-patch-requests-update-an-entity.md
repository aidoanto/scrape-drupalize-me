---
title: "JSON:API PATCH Requests: Update an Entity"
url: "https://drupalize.me/tutorial/jsonapi-patch-requests-update-entity?p=3279"
guide: "[[decoupled-headless-drupal]]"
order: 27
---

# JSON:API PATCH Requests: Update an Entity

## Content

Whenever we need our consumer application to change the contents of an entity we will need to issue a PATCH request. The JSON:API module will process that request and update the entity with the provided values.

In this tutorial, we'll:

- Define the appropriate HTTP headers for a PATCH request
- Construct the JSON object used to update an entity
- Issue a PATCH request that will update an entity in our Drupal backend

By the end of this tutorial, you should know how to update content via the JSON:API.

## Goal

Update the content of multiple fields of an existing article using JSON:API.

## Prerequisites

- [Make an Authenticated Request Using OAuth 2](https://drupalize.me/tutorial/make-authenticated-request-using-oauth-2)
- [Install JSON:API](https://drupalize.me/tutorial/install-jsonapi-module)
- [JSON:API Resource Requests](https://drupalize.me/tutorial/jsonapi-resource-requests)
- [JSON:API POST Requests: Create an Entity](https://drupalize.me/tutorial/jsonapi-post-requests-create-entity)

## Update an article

Imagine that we need our consumer applications to be able to update 2 fields in our user entity: the bio and contact information. In that scenario, the consumer application will show a form to the user with their current profile information. When the user clicks the submit button, the consumer application will have to send a PATCH request that contains any data that needs to be updated on the server. Such request will be [authenticated with an OAuth 2 token](https://drupalize.me/tutorial/make-authenticated-request-using-oauth-2) in the same way we did it to [create an article](https://drupalize.me/tutorial/jsonapi-post-requests-create-entity).

### Gather the authentication token

Our consumer application should have a way to safely store the authentication token for the logged-in user. There are multiple ways to do this, including the one described in [Get a Token for OAuth 2 Requests](https://drupalize.me/tutorial/get-token-oauth-2-requests). We need the authentication token to authenticate the user updating the content. With that, we can check if they have the required permissions to change the entity.

In this example we will assume that our token is: `eyJ0eXAi...dQOQw`

### Prepare the request headers

For the PATCH operation we will need to set the following request headers:

- `Content-Type: application/vnd.api+json`. This header will tell Drupal that the body that the request contains is structured in JSON:API format.
- `Accept: application/vnd.api+json`. This will instruct the server to return any responses back to our consumer using JSON:API format.
- `Authentication: Bearer eyJ0eXAi...dQOQw`. This one contains the authentication token obtained above. This is the proof the server needs to trust that the request was originated from a valid Drupal user through OAuth 2.

### Prepare the request body

So far we have been following the same steps we did when creating a new article. In fact, the only difference between PATCH and POST is the request body.

The body of the PATCH request will only contain the attributes and relationships that we want to change. Anything we don't add explicitly in the request body will remain unchanged on the server.

In this case the `id` property is required: Drupal needs it to know which entity to update.

For our current example, the PATCH request body could look like:

```
{
  "data": {
    "type": "user--user",
    "id": "ab3b164c-7b08-4a3c-ac82-845628ff2399",
    "attributes": {
      "field_bio": {
        "value": "There are no rivers where I grew up.",
        "format": "plain_text",
        "summary": "Only salty water."
      },
      "field_contact_info": "Reach me by email at [email protected]"
    }
  }
}
```

This is all we need to do to update the biography and contact information for the user `ab3b164c-7b08-4a3c-ac82-845628ff2399`.

The JSON:API module will load the user entity for that ID and set the specified fields according to the values in the request body of the PATCH request. After that, it will save the user including the new values for the bio and contact info. All other fields will retain their original values. All this happens internally in Drupal.

### Send the request

Our consumer app will send the HTTP request using the PATCH method to the Drupal server.

Requests should be sent to the endpoint for the specific resource you're trying to update. For example: `https://example.com/jsonapi/users/{user_uuid}`, where `{user_uuid}` is the same value as `id` in the request body.

The response to that request will be the JSON:API representation of the fully loaded user after the changes have been saved, or an error. [Learn more about handling errors](https://drupalize.me/tutorial/jsonapi-error-handling).

## Recap

We have updated a user entity using only the HTTP API. To do so, we sent only the fields that needed changes in the request body. We also included the JSON:API request headers and the OAuth 2 authentication token in the PATCH request.

## Further your understanding

- Try to update a relationship in one of your nodes. Did that work as expected? Remember to use the UUID for the relationship id.
- Make a PATCH request with a missing `id` property in the body. What is the response?

## Additional resources

- [Update existing resources (PATCH)](https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module/updating-existing-resources-patch) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API POST Requests: Create an Entity](/tutorial/jsonapi-post-requests-create-entity?p=3279)

Next
[JSON:API DELETE Requests: Delete an Entity](/tutorial/jsonapi-delete-requests-delete-entity?p=3279)

Clear History

Ask Drupalize.Me AI

close
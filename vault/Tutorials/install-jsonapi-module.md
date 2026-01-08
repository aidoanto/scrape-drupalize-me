---
title: "Install JSON:API Module"
url: "https://drupalize.me/tutorial/install-jsonapi-module?p=3277"
guide: "[[decoupled-headless-drupal]]"
---

# Install JSON:API Module

## Content

The JSON:API module is our recommended starting point for creating REST APIs with Drupal. JSON:API module is now part of Drupal core as of 8.7, so installing the module no longer requires a separate download step.

In this tutorial we'll:

- Walk through installing the JSON:API module for Drupal
- Look at what you get out of the box with the JSON:API module

By the end of this tutorial you should be able to install the JSON:API module, and know what tools it provides you with.

## Goal

Install the JSON:API module and test it out.

## Prerequisites

This tutorial, and the following, assume that you are familiar with HTTP requests. They also assume that you are familiar with [the goals of the JSON:API specification](https://drupalize.me/tutorial/modern-web-services-jsonapi-and-graphql). We will be issuing some requests during this tutorial. We recommend you install one of the HTTP clients listed below to simplify the process. This will also be important for other tutorials in this series.

- [Postman](https://www.getpostman.com/)
- [Paw](https://paw.cloud/)
- [Insomnia](https://insomnia.rest/)
- [HTTPie](https://github.com/jakubroztocil/httpie)

In this series we will be using HTTPie for the request examples and Postman for the authenticated request examples.

Sprout Video

## Download and install the module

JSON:API is included in Drupal core as of version 8.7. To download the module for different or previous version of Drupal, download and install the current stable version of the JSON:API module from <https://www.drupal.org/project/jsonapi>.

### Install the JSON:API module

From the Extend page, in the Web Services group, check the box next to JSON:API to install it. The Serialization module will also be installed (as it is a dependency).

### Configure allowed operations (if necessary)

By default, JSON:API is configured to "Accept only JSON:API read operations." If your site requires it, you can configure your site to "Accept all JSON:API create, read, update, and delete operations."

Check out these settings at: Extend > JSON:API > Configure or Configuration > Web Services > JSON:API (*admin/config/services/jsonapi*).

### Make a request and confirm it's working

If you make a request to the entry point in JSON:API you will get a list of links indicating where all the resources are situated. The entry point is located at the root of the API, in this case `/jsonapi`.

```
# Type this HTTPie command in your console.
http https://example.org/jsonapi
```

Depending on the entity types you have in your site the list of resources will be different. Here is an example of what the response should look like:

```
{
    "data": [],
    "links": {
        "action--action": "https://example.org/jsonapi/action/action",
        "entity_view_mode--entity_view_mode": "https://example.org/jsonapi/entity_view_mode/entity_view_mode",
        …
        "environment_indicator--environment_indicator": "https://example.org/jsonapi/environment_indicator/environment_indicator",
        "field_storage_config--field_storage_config": "https://example.org/jsonapi/field_storage_config/field_storage_config",
        "file--file": "https://example.org/jsonapi/file/file",
        "filter_format--filter_format": "https://example.org/jsonapi/filter_format/filter_format",
        "image_style--image_style": "https://example.org/jsonapi/image_style/image_style",
        "jsonapi_resource_config--jsonapi_resource_config": "https://example.org/jsonapi/jsonapi_resource_config/jsonapi_resource_config",
        "menu--menu": "https://example.org/jsonapi/menu/menu",
        "menu_link_content--menu_link_content": "https://example.org/jsonapi/menu_link_content/menu_link_content",
        "node--article": "https://example.org/jsonapi/node/article",
        "node--page": "https://example.org/jsonapi/node/page",
        "node_type--node_type": "https://example.org/jsonapi/node_type/node_type",
        …
        "self": "https://example.org/jsonapi",
        "user_role--user_role": "https://example.org/jsonapi/user_role/user_role",
        "view--view": "https://example.org/jsonapi/view/view"
    }
}
```

This response lists all the resources available in your new JSON:API server. It is called the *entry point* because it is the place where we start to learn what other resources are available.

## Recap

In this tutorial we learned that you get one resource for each entity type when you install JSON:API. In addition to that we also learned how to list all the available resources in your newly created web service.

## Further your understanding

- [Learn more about the different options that HTTPie can offer](https://httpie.org/doc).
- Try making a request to one of the resources in the list. What happens?
- What if you make a request to `/jsonapi/does-not-exist`? What is the response code?

## Additional resources

- [Postman](https://www.getpostman.com/) (getpostman.com)
- [Paw](https://paw.cloud/) (paw.cloud)
- [Insomnia](https://insomnia.rest/) (insomnia.rest)
- [HTTPie](https://github.com/jakubroztocil/httpie) (github.com)
- [Ignore some query parameters which violate the JSON API specification](https://www.drupal.org/project/jsonapi/issues/2984044) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[JSON:API Resource Requests](/tutorial/jsonapi-resource-requests?p=3277)

Clear History

Ask Drupalize.Me AI

close
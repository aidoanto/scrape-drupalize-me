---
title: "Automatic Documentation with Schemata"
url: "https://drupalize.me/tutorial/automatic-documentation-schemata?p=2960"
guide: "[[decoupled-headless-drupal]]"
---

# Automatic Documentation with Schemata

## Content

It is important to have good up-to-date documentation about your web services. Doing so will boost developer productivity in a decoupled project. Drupal offers several tools that help maintain your API documentation with minimal effort.

In this tutorial we'll:

- Learn about the [JSON schema](http://json-schema.org) format for describing data structures
- Generate schemas for our *fake* articles REST resource
- Visualize those schemas in a human-readable format

By the end of this tutorial you should be able to generate documentation for your REST resources that is kept up-to-date automatically by Drupal.

## Goal

Provide automatically generated documentation for the JSON *articles* resource for the front-end development team.

## Prerequisites

This tutorial assumes that you are familiar with HTTP requests. We will be issuing some requests during this tutorial. We recommend you install one of the HTTP clients listed below to simplify the process. This will also be important for other tutorials in this series.

- [Postman](https://www.getpostman.com/)
- [Paw](https://paw.cloud/)
- [Insomnia](https://insomnia.rest/)
- [HTTPie](https://github.com/jakubroztocil/httpie)

## Schemas

A schema is a declarative definition of how a particular piece of data is structured. It's a tool that aims to describe the shape of the data, so other processes can build around that information. Examples of these include the database schema and the XML DTD that describes an XML document.

In our particular case we will be describing the JSON object that our web service produces, or that it accepts, if we are writing to the web service. When describing the expected shape of a JSON object it's common to do it using [JSON schema](http://json-schema.org). The schema is a document that contains a set of keys that specify whether a given property inside of the JSON object being described is an array, an integer, a URL, etc. It also defines the hierarchy of the properties, so you can describe the whole data tree.

It is not critical to learn the JSON schema syntax, although it will help to further your understanding. The important part is that there is a JSON document that is used to describe the output of our API. That document is in a machine-friendly format, so other related tools can leverage it to:

- Create human-friendly documentation.
- [Generate forms](http://schemaform.io/) for your data automatically in the front end.
- [Validate your data](http://www.jsonschemavalidator.net/) in your consumer application before sending it to the server.
- [JSON schema and code generation](https://cesanta.com/blog/json-schema-and-code-generation/) for the front end.

The focus of this tutorial will be on creating human-friendly documentation in a few clicks. That documentation will be based on a JSON schema generated from Drupal's [Typed Data](https://www.drupal.org/docs/8/api/typed-data-api/typed-data-api-overview) structures.

### Enable the Schemata and Open API modules

Start by installing the following modules:

- [Schemata](https://www.drupal.org/project/schemata): Generates a JSON schema for a content type in a particular format
- Schemata in JSON Schema (*schemata\_json\_schema* is included with Schemata, but must be enabled separately): Provides a data models for entity types and bundles in JSON schema format.
- [Open API](https://www.drupal.org/project/openapi/): This module generates an Open API (a.k.a. Swagger) formatted description of your resources
- [OpenAPI for JSON:API](https://www.drupal.org/project/openapi_jsonapi): This module integrates with the base OpenAPI module to generate the definitions for JSON:API.
- [Open API UI](https://www.drupal.org/project/openapi_ui), and [Redoc for Open API UI](https://www.drupal.org/project/openapi_ui_redoc): The combination of these two provides a UI for viewing the generated documentation. You could alternatively skip these two modules and use any tool that can consume Open API formatted resource descriptions

My preferred way of installing modules is using Composer and Drush, but you can do it in your own way.

Type in a terminal:

```
composer require drupal/schemata drupal/openapi drupal/openapi_jsonapi drupal/openapi_ui drupal/openapi_ui_redoc
# This will enable all required dependencies as needed.
drush en -y schemata schemata_json_schema openapi openapi_jsonapi openapi_ui_redoc
```

Schemata module provides 1 permission, "Access the different data models". You may need to ensure that the appropriate role has this permission before continuing. (See *People* > *Permissions* (*admin/people/permissions*).)

### Request the schema for the *articles* resource

Assuming that the [JSON:API module is installed](https://drupalize.me/tutorial/install-jsonapi-module) already we can request a JSON schema of the articles resources as described by JSON:API.

Schemata exposes that JSON schema in the following URL (replace the domain name with your own):

```
https://example.org/schemata/node/article?_format=schema_json&_describes=api_json
```

Fetch that schema from Drupal by making a `GET` request to that URL. You should get a JSON object in return. That is the JSON schema.

Tip: You can fetch schema for other formats by varying the `&_describes=` parameter. For example; If [the HAL module](https://www.drupal.org/project/hal) is installed you could use `&_describes=hal_json`.

### Visualize the schema

You can see how exploring the schema generated above is not trivial. That is because JSON schema is designed to be machine-friendly. That makes it really difficult for an untrained human to extract meaningful information from that document. Luckily there are tools that will take that machine-friendly format and output nicely formatted HTML for a human to read. The Open API, and Open API UI module will do that for us in Drupal.

In the *Manage* administration menu navigate to *Configuration* > *Web services* > *OpenAPI* (admin/config/services/openapi). And then click the button labeled *Explore with ReDoc* in the row that starts with *JsonApi*.

Image

![Screenshot showing the OpenAPI documentation list with a circle around the Explore with Redoc button](../assets/images/openapi-resource-selection.png)

That will take you to the ReDoc page where you can click to expand and contract sections of the schema and explore the properties of different resources.

Image

![Explore the article resource in ReDoc](../assets/images/openapi-redoc-example.png)

## Recap

In this tutorial we learned to generate and explore a JSON schema for a particular resource. We used the Open API, and Open API UI modules to see a human-readable version of the schema.

In an intermediate step we learned how we can extract the schema for our resource from Schemata by making a `GET` request. This is interesting not only to learn about the internals of the process, but also because there are other relevant uses of the schema that are not covered in this tutorial, like:

- [Automated form generation](http://schemaform.io/)
- [Client side data validation](http://www.jsonschemavalidator.net/)
- [JSON schema and code generation](https://cesanta.com/blog/json-schema-and-code-generation/)

Our end goal in this tutorial was to ease front end development by producing documentation about our resources. In many cases the URL to view the schema in ReDoc should be enough.

## Further your understanding

- Learn more about the [JSON schema specification](http://json-schema.org/documentation.html).
- Evaluate whether you can benefit from any of the other [useful tools](http://json-schema.org/implementations.html) that leverage JSON schema.
- Learn more about the [OpenAPI project](https://www.openapis.org) and the [Drupal module](https://www.drupal.org/project/openapi)

## Additional resources

- [JSON schema specification](http://json-schema.org/documentation.html) (json-schema.org)
- [OpenAPI project](https://www.openapis.org) (openapis.org)
- [OpenAPI Drupal module](https://www.drupal.org/project/openapi) (Drupal.org)
- [Automated form generation](http://schemaform.io/) (schemaform.io)
- [Client side data validation](http://www.jsonschemavalidator.net/) (jsonschemavalidator.net)
- [JSON schema and code generation](https://cesanta.com/blog/json-schema-and-code-generation/) (cesanta.com)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Web Service Documentation](/tutorial/web-service-documentation?p=2960)

Clear History

Ask Drupalize.Me AI

close
---
title: "JSON:API Security Considerations"
url: "https://drupalize.me/tutorial/jsonapi-security-considerations?p=3277"
guide: "[[decoupled-headless-drupal]]"
---

# JSON:API Security Considerations

## Content

When you enable the JSON:API module you're significantly increasing the attack surface of your application. So it's a good idea to make sure that you understand the implications of doing so, and how to mitigate potential security issues. In most cases it doesn't require much work to do, but it's worth taking the time to make sure you've done it right.

In this tutorial we'll learn:

- What JSON:API already does to keep you secure
- How to protect against common attacks
- How to limit access to resources exposed by JSON:API

By the end of this tutorial you should know what to look for when auditing your JSON:API configuration to help prevent against common attacks.

## Goal

Configure your JSON:API web service to be as secure as possible.

## Prerequisites

The existing [Security considerations](https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module/security-considerations) documentation is a great resource. And we'll mostly be talking about how to implement suggestions provided there.

## Understand how JSON:API performs access control

At a high-level, the JSON:API module's goal is to take the existing Drupal Entity, Field, and Typed Data APIs, and expose them as a web service that conforms to the JSON:API specification. That is, JSON:API is an attempt to make the things a developer can do via PHP with Drupal's data APIs and make them available to web services clients. In doing so, JSON:API does not bypass any of Drupal's existing security measures, or try and layer on any of its own.

JSON:API respects the existing access control features of the Entity and Field APIs. And when data is updated via JSON:API the existing validation constraints are respected.

You can think of it this way; if a user can access, or update, a field via the UI then they can also do it via JSON:API. This is true for both anonymous and authenticated users.

For that reason, it's important to ensure your entity and field access controls are appropriately configured. Drupal's permissions matrix can be a bit overwhelming, so we recommend checking out the [Entity Access Audit module](https://www.previousnext.com.au/blog/introducing-entity-access-audit-module) as a starting point.

## Read-only mode

By default, JSON:API operates in read-only mode. That is, it only allows access to read operations for entity and field data. And in many cases this is sufficient. If your API clients are read-only and will not need to make any updates to the data, there's no reason to allow writes.

We recommend leaving your API in read-only mode unless you can articulate why a client needs create, update, or delete access. And if you do turn it on remember that JSON:API respects the CRUD permissions of the Entity and Field API so make sure they're configured correctly.

This setting can be changed by navigating to Configuration > Web Services > JSON:API (*admin/config/services/jsonapi*) in the Manage administration menu.

## Reduce your attack surface

There are a couple of things you can do to reduce the attack surface of your JSON:API web service. Namely don't expose things you don't have to.

By default, the JSON:API module will expose all available entity types for a site. Nodes, users, taxonomy, paths, files, roles, captcha point configuration, editor configurations, etc. It's unlikely that an API client needs access to all of these things. While JSON:API will respect the access control settings of Drupal and for example not expose editor configuration entities to non-admin users, there's no point in exposing them if you don't need to.

Bugs in Drupal's Entity and Field APIs, or contributed modules that misuse them, can result in security vulnerabilities. These bugs then affect the JSON:API web service. It's much easier for malicious users to access and exploit an HTTP API than a PHP API.

There are a few different ways to limit what's exposed:

- The contributed [JSON:API Extras module](https://www.drupal.org/project/jsonapi_extras) provides a UI that can be used to disable any unused resources or fields on specific resources.
- Authors of custom entity types can [use the `internal` flag](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21EntityTypeInterface.php/function/EntityTypeInterface%3A%3AisInternal/) to indicate that an entity type, field type, or specific property for an entity is for internal use only. JSON:API will not expose anything marked as `internal`.
- JSON:API resources, or individual fields on resources, [can be programmatically disabled](https://www.drupal.org/node/3079797) via the `ResourceTypeBuildEvent` event. [Learn about subscribing to events](https://drupalize.me/tutorial/what-are-events).

## Recap

Drupal's JSON:API module exposes the functionality of the Entity, Field, and other APIs via an HTTP web service. This greatly increases the attack surface of your application and makes it easier for malicious users to exploit bugs in these core systems. We can help keep our applications more secure by making sure we do an access control audit, leave JSON:API in read-only mode if possible, and use tools like JSON:API Extras to reduce the number or resources that JSON:API exposes to only those that are essential.

## Further your understanding

- Install the JSON:API Extras module to see all the resources exposed by the JSON:API module. Can you explain what each of them is for, and how an API client of your specific web service would make use of it? If not, consider disabling it.
- Create a list of all the CRUD operations that can be performed via your exposed API as a way to review permissions. Update as needed.

## Additional resources

- [Security considerations](https://www.drupal.org/docs/core-modules-and-themes/core-modules/jsonapi-module/security-considerations) (Drupal.org)
- [REST Security Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/REST_Security_Cheat_Sheet.html) (owasp.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[JSON:API Error Handling](/tutorial/jsonapi-error-handling?p=3277)

Clear History

Ask Drupalize.Me AI

close
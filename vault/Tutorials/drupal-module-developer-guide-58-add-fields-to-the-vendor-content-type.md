---
title: "Add Fields to the Vendor Content Type"
url: "https://drupalize.me/tutorial/add-fields-vendor-content-type?p=3243"
guide: "[[drupal-module-developer-guide]]"
order: 58
---

# Add Fields to the Vendor Content Type

## Content

To implement a custom vendor attendance status feature, we need to add new fields to the *Vendor* content type. This tutorial will guide you through adding these fields and discuss the considerations for choosing between Drupal's UI for data modeling versus code-based alterations of entity types.

In this tutorial, we'll:

- Add new fields to the *Vendor* content type required for the vendor attendance status feature.
- Discuss the pros and cons of modeling data with Drupal's Field UI compared to using hooks for modifying entity base fields.

By the end of this tutorial, you'll know how to update the *Vendor* content type with necessary fields and understand why this approach suits our specific case.

## Goal

Enhance the *Vendor* content type with fields for the vendor attendance status feature.

## Prerequisites

- [Concept: Field API and Fieldable Entities](https://drupalize.me/tutorial/concept-field-api-and-fieldable-entities)
- [6.3. Adding Basic Fields to a Content Type](https://drupalize.me/tutorial/user-guide/structure-fields) (Drupal User Guide)

## Video tutorial

Sprout Video

## Overview of vendor attendance feature

Our project for the Anytown Farmer's Market requires a feature that lets vendors indicate their attendance and provide a contact person if attending. The feature will provide a simplified UI for vendors to update this information each week.

To build this, we will:

- Add fields to the vendor content type for attendance status and contact details.
- Develop a custom module that uses the Entity API and provides a simplified form interface to update these fields.

Here's an example of the UI we're working on:

Image

![Screenshot of simplified attendance form UI](../assets/images/data--setup-content-types_form-example.png)

And the Vendor content type with additional fields:

Image

![Screenshot of Vendor content type with new fields](../assets/images/data--setup-content-types_vendor-example.png)

## Add the required fields

To the vendor content type, add the following fields using the administrative UI. For assistance, see [Adding Basic Fields to a Content Type](https://drupalize.me/tutorial/user-guide/structure-fields).

Ensure the field names and types match exactly for compatibility with future tutorials:

| Field Name | Machine Name | Drupal Field Type |
| --- | --- | --- |
| Vendor Attending | field\_vendor\_attending | Boolean (checkbox) |
| Vendor Contact Name | field\_vendor\_contact\_name | Text (plain) |
| Vendor Contact Email | field\_vendor\_contact\_email | Text (email) |

## Creating fields in code vs. the UI

Drupal excels in flexibility due to its entities and fields architecture. While it's faster to model data structures via the UI, this approach makes it difficult to assume the structure's specifics when coding. For site-specific modules, a hybrid approach works well: use the UI for structure creation and hard code details like field names. Such custom modules, often termed *glue code*, link Drupal's existing functionalities in innovative ways.

For broader-use modules, avoid hard coding field names to maintain applicability across different sites. Consider generic field referencing or hooks for adding base fields to entities.

Understanding your module's intended scope helps in deciding the best approach for interacting with Drupal's entity and field systems.

## Test with vendor nodes

Once the fields are added, create or edit a vendor entity to ensure the fields function as expected.

## Recap

We've successfully added fields to the Vendor content type for the Anytown Farmer's Market, which will enable the site to track vendor attendance.

## Further your understanding

- What drawbacks might arise from hard coding field assumptions in your module?
- Can you identify scenarios where *glue code* could customize a Drupal site effectively?

## Additional resources

- [6.3. Adding Basic Fields to a Content Type](https://drupalize.me/tutorial/user-guide/structure-fields) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Field API and Fieldable Entities](/tutorial/concept-field-api-and-fieldable-entities?p=3243)

Next
[Create a Form for Editing an Entity](/tutorial/create-form-editing-entity?p=3243)

Clear History

Ask Drupalize.Me AI

close
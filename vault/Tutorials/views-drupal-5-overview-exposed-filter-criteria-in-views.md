---
title: "Overview: Exposed Filter Criteria in Views"
url: "https://drupalize.me/tutorial/overview-exposed-filter-criteria-views?p=2670"
guide: "[[views-drupal]]"
order: 5
---

# Overview: Exposed Filter Criteria in Views

## Content

Exposing filter criteria allows the users of your site to choose how to filter a content list created in Views. When rendered on the page, the exposed filters will be displayed to the user as interactive form components.

By the end of this tutorial you will:

- Understand what it means to expose filter criteria and when it might be useful.
- Be able to identify when a view has exposed filters and which filters are exposed.

## Goal

- Understand what an exposed filter is, when filters are useful, and what they look like in a view.

## Prerequisites

- [Overview: Filter Criteria in Views](https://drupalize.me/tutorial/overview-filter-criteria-views)
- [Add Filter Criteria to a View](https://drupalize.me/tutorial/add-filter-criteria-view)

Examples and screenshots in this tutorial are from the demo site we set up in:

- [Set up Demo Site with Views and Content](https://drupalize.me/tutorial/set-demo-site-views-and-content)

If you are new to Views, check out these Drupal User Guide tutorials:

- [Concept: Uses of Views](https://drupalize.me/tutorial/user-guide/views-concept)
- [Concept: The Parts of a View](https://drupalize.me/tutorial/user-guide/views-parts)

## Exposed filter criteria

As we learned in the tutorial [Overview: Filter Criteria in Views](https://drupalize.me/tutorial/overview-filter-criteria-views), you can configure filter criteria to allow visitors to choose the values and operator for the filter, by checking "Expose this filter to visitors, to allow them to change it" in the filter criteria configuration form.

Let's take a look at the configuration options for exposed filters.

### Text field: exposed filter configuration

Image

![Screenshot of simple text filter exposed configuration form](../assets/images/exposed-filters-sorts--filter-text-example.png)

### Example: Title field exposed filter settings

| Setting | Description |
| --- | --- |
| **Filter type to expose** | *Single filter* means that all options on the exposed configuration form will work together as a single field on the exposed form. Selecting the *Grouped filters* option allows us to limit the exposed field options the visitor can choose to a specific set of operators and values. Most often we'll stick with the *Single filter* option. |
| **Required** | Whether or not this field will be required on the exposed form. |
| **Label** | The label text will appear above the exposed filter field. |
| **Description** | The description text will appear beneath the exposed filter field. |
| **Value** | The default value for this filter. |
| **Operator** | How the filter's *Value* will be compared to content field values in the database. |
| **Expose operator** | Whether or not to present the operator as a field on the exposed form. |
| **Remember the last selection** | If checked, Drupal will save the values a visitor selects for this exposed filter. When the visitor returns to this list of content later, their previous filter values continue to affect the view. This data is saved by Drupal on a per-user basis. |
| **Filter identifier** | This value is used by the Views module to identify this filter. When a visitor submits an exposed form, this is the *key* for the submitted value. Generally, whatever value Views places in this field by default is fine. See note below. |
| **Placeholder** | The placeholder text will appear within a simple text field until the visitor focuses on the field. |

**Note about filter identifiers**: As of 8.8.0, filter identifiers are limited to letters, digits, the dot (`.`), hyphen (`-`), underscore (`_`), and tilde (`~`). If your identifiers contain any other characters we recommend you update them. Change record: [Views exposed filters identifiers are now validated correctly](https://www.drupal.org/node/3040204).

### Example: Content type field exposed filter settings

Depending on the filter criteria, some of the available options may change.

Below is a screenshot of the exposed *Content Type* filter criteria configuration.

Image

![Screenshot of a list filter exposed configuration form](../assets/images/exposed-filters-sorts--filter-list-example.png)

| Setting | Description |
| --- | --- |
| **Operator** | How the filter's *Value* will be compared to content field values in the database. |
| **Expose operator** | Whether or not to present the operator as a field on the exposed form. |
| **Content types** | Instead of a *Value* field, we get a list of available content types configured on our site. Often when creating filters for fields that have a limited list of values, the Views module will present us with the known possible values to choose from. |
| **Allow multiple selections** | If checked, the user may select multiple values from the list. |
| **Remember the last selection** | If checked, Drupal will save the values a visitor selects for this exposed filter. When the visitor returns to this list of content later, their previous filter values continue to affect the view. This data is saved by Drupal on a per-user basis. |
| **Filter identifier** | This value is used by the Views module to identify this filter. When a visitor submits an exposed form, this is the *key* for the submitted value. Generally, whatever value Views places in this field by default is fine. |
| **Limit list to selected items** | When dealing with lists, we can configure the exposed filter criteria to only show the selected *Value* items on the form to visitors. This is useful if we want to expose a list filter criteria, but don't want the visitors to be able to choose from every possible item in the list. |

### Previewing exposed filter criteria

We can preview and test our exposed filter criteria while working on a view. Here is an example of a view with multiple exposed filters.

Image

![Screenshot of preview showing our exposed filters as fields in a form above the list of content](../assets/images/exposed-filters-sorts--filter-preview.png)

Notice that when a filter criteria is exposed its link in the view editor interface will be appended with the word *(exposed)*. This makes it easy to identify at a glance which filters are exposed.

## Exposed form options

When working with exposed filter and sort criteria there are a few additional configuration options we want to consider: the configuration of the exposed form itself. The view edit interface provides some options for for configuring the form. Those options are located in the *Advanced* column within the *Exposed form* section.

Image

![Screenshot of view edit form with the exposed form section highlighted](../assets/images/exposed-filters-sorts--highlight-form-options.png)

This section offers the following options:

- **Exposed form in block**: Whether or not we want the exposed form to created as a block. Doing so requires that we place the block ourselves on the appropriate page using the *Block System*.
- **Exposed form style**: Whether or not we want our exposed form to require the visitor input filter values before the view shows a list of content.
- **Exposed form settings**: Various options for the *Exposed form style*. Including:
  - **Submit button text**: Text the visitor will see for the exposed form submit button.
  - **Include reset button**: Whether or not to add a button to the form that will reset all the exposed filter and sort values when it is selected.
  - **Reset button label**: Text the visitor will see for the exposed reset button.
  - **Exposed sorts label**: Label text that will appear above the exposed sort criteria field.
  - **Allow people to choose the sort order**: Whether or not the *Order* field is exposed for sort criteria.
  - **Label for ascending sort**: Text for the *Sort ascending* option when the *Order* field is shown.
  - **Label for descending sort**: Text for the *Sort descending* option when the *Order* field is shown.

Image

![Screenshot of exposed form settings configuration form](../assets/images/exposed-filters-sorts--exposed-form-settings.png)

## Recap

When we expose filter criteria, we are creating a form that allows visitors to interact with and change our list of content.

Exposing filter criteria means that visitors to our site can change the value and operator that the filter criteria use when building a list of content.

These options can be used to change simple lists of content into powerful tools our site visitors and administrators can use to locate content and make their own custom lists.

## Further your understanding

- Add several different types of fields to your filter criteria. Check the "expose this filter" checkbox and familiarize yourself with settings available for each type of field.
- How does exposing filter criteria (and operators) affect the usability of your page? How does it make your users' lives easier (or more difficult)?

## Additional resources

- [Drupal User Guide: Chapter 9. Creating Listings with Views](https://drupalize.me/series/user-guide/views-chapter) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Add Filter Criteria to a View](/tutorial/add-filter-criteria-view?p=2670)

Next
[Expose Filter Criteria to Users in Views](/tutorial/expose-filter-criteria-users-views?p=2670)

Clear History

Ask Drupalize.Me AI

close
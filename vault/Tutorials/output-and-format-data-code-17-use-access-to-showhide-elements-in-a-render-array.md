---
title: "Use #access to Show/Hide Elements in a Render Array"
url: "https://drupalize.me/tutorial/use-access-showhide-elements-render-array?p=3252"
guide: "[[output-and-format-data-code]]"
order: 17
---

# Use #access to Show/Hide Elements in a Render Array

## Content

The `#access` property can be used with any element in a render array, including form elements, to control the visibility of that element and its children. This is an effective way to limit access to specific parts of a page's content to only those users with the required permissions, and to show or hide material based on other conditional logic.

In this tutorial we'll:

- Review the `#access` Render API property
- Demonstrate using the `#access` property to show/hide a field on a node depending on the current user's permissions

By the end of this tutorial you should be able to limit access to any element on the page via logic that returns a Boolean value.

## Goal

Use the `#access` Render API property to show/hide an element in a render array depending on whether the currently logged in user has a specific permission.

## Prerequisites

- [What Are Render Arrays?](https://drupalize.me/tutorial/what-are-render-arrays)

## The `#access` property

The `#access` property is a generic property that can be used on any render element or form element in a render array. It is a Boolean value that is used to control the visibility and use of an element. Common use cases include omitting elements on a form for users without sufficient permissions and hiding the content of fields from non-privileged users.

Because `#access` can be used to conditionally control the visibility of elements in an array, it is often used to show or hide things based on logic that isn't related to a user's access rights. For example, you might want an element on the page to be visible only on a certain day of the week.

The default value for the `#access` property is `TRUE`. When set to `FALSE`, the element is not displayed. In the case of forms, any user-submitted value is ignored during validation and submission handling. When set to `FALSE`, all child elements are also excluded from display.

## Example: Use `#access` to limit access to the image field on article nodes

As an example, here's how you could hide the contents of a field attached to article nodes from anyone that doesn't have the `'administer content'` permission. This might be a field that contains data that is intended to be used internally, not displayed to the public, such as information about the user who reviewed an article for publication.

### Implement `hook_ENTITY_TYPE_view_alter()`

Implement the hook [`hook_ENTITY_TYPE_view_alter()`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_ENTITY_TYPE_view_alter) in your module. This hook allows you to alter the render array representing a node prior to it being displayed.

```
/**
 * Implements hook_node_view_alter().
 */
function render_example_node_view_alter(array &$build, Drupal\Core\Entity\EntityInterface $entity, \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display) {
  // Code goes here ...
}
```

For more on implementing hooks see [What Are Hooks?](https://drupalize.me/tutorial/what-are-hooks).

### Determine the current user's permissions

Check to see if the user currently viewing the node has the `'administer content'` permission. We can do this by retrieving the account object for the current user and then use the `\Drupal\Core\Session\AccountInterface::hasPermission()` method to verify they are in a role that has the desired permission.

```
$current_user = Drupal::currentUser();
$current_user->hasPermission('administer content');
```

Read more about [working with the current user account](https://drupalize.me/tutorial/get-information-about-current-user).

### Set the value of `#access`

Finally, set the `#access` property to either `TRUE` or `FALSE`. In this case we can just use the value returned from `$current_user->hasPermission('administer content')` which will be `TRUE` if the user has the requested permission. Doing so ensures that only users with the `'administer content'` permission can view the `field_reviewed_by` field on article nodes.

Complete example:

```
/**
 * Implements hook_node_view_alter().
 */
function render_example_node_view_alter(array &$build, Drupal\Core\Entity\EntityInterface $entity, \Drupal\Core\Entity\Display\EntityViewDisplayInterface $display) {
  if ($entity->bundle() == 'article') {
    // Get the currently active user.
    $current_user = Drupal::currentUser();
    // Check to see if the user has the 'administer content' permission. The
    // hasPermission() method returns a Boolean value.
    $build['field_reviewed_by']['#access'] = $current_user->hasPermission('administer content');
  }
}
```

**Note:** This solution isn't perfect and is intended as an example only. The above code would only show/hide the field in the context of an entity view operation. It wouldn't, for example, be applied if the field was being displayed independently in a view.

## Recap

In this tutorial we looked at how you can use the `#access` property on an element in a render array in order to control that element's visibility.

## Further your understanding

- Can you think of an example where you might use the `#access` property to control the visibility of an element on a form?
- Check out the flow chart in the [Render Pipeline tutorial](https://drupalize.me/tutorial/render-pipeline) to see how `#access` is used when rendering an array to HTML.

## Additional resources

- [Get Information About the Current User](https://drupalize.me/tutorial/get-information-about-current-user) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Get Information about the Current User](/tutorial/get-information-about-current-user?p=3252)

Clear History

Ask Drupalize.Me AI

close
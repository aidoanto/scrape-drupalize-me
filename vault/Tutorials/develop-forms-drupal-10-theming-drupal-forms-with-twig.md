---
title: "Theming Drupal Forms with Twig"
url: "https://drupalize.me/tutorial/theming-drupal-forms-twig?p=2734"
guide: "[[develop-forms-drupal]]"
order: 10
---

# Theming Drupal Forms with Twig

## Content

By default, individual forms in Drupal are not output using Twig template files. It's possible to associate a form with a Twig template file by creating a new theme hook, and then referencing that theme hook from the `$form` array that defines the form. Doing so allows theme developers to customize the layout of the elements in the form using HTML and CSS.

This is useful when you want to change the layout of the entire form. For example, putting the elements into 2 columns. If you want to change individual elements in the form, you can often do so by overriding element specific Twig template files.

In this tutorial, we'll:

- Learn how to create a new theme hook that can be used to theme an element in a render array.
- Associate the `$form` we want to theme with the new theme hook we created.
- Create a Twig template file for the theme hook that will allow us to lay out the form elements using custom HTML.

By the end of this tutorial, you should be able to associate a Twig template file with any form in Drupal, so that you can customize its layout using HTML and CSS.

## Goal

Theme the user login form at */user/login* using a Twig template, and divide the form into 2 columns.

## Prerequisites

- [Override a Template File](https://drupalize.me/tutorial/override-template-file)
- [Alter an Existing Form with hook\_form\_alter()](https://drupalize.me/tutorial/alter-existing-form-hookformalter)

In this example, we'll theme the form that appears on the */user/login* page. Its unique ID is `user_login_form`.

Remember, form arrays are [renderable arrays](https://drupalize.me/tutorial/what-are-render-arrays). The process here is the same as the one outlined in [Output Content with a Template File](https://drupalize.me/tutorial/output-content-template-file). The difference is that instead of creating a new custom render element and using a template for its HTML, we're going to associate an existing `$form` element with a template of our choosing.

### Define a new theme hook

The first step in associating a form with a template is creating a new theme hook. This is the value that will be referenced via the `#theme` property in the form array. This can go either in a module's *MODULENAME.module* file or a theme's *THEMENAME.theme* file. In this example, we'll use our theme's [*THEMENAME.theme* file](https://drupalize.me/tutorial/add-logic-themenametheme).

Example *mytheme.theme*:

```
/**
 * Implements hook_theme().
 */
function mytheme_theme($existing, $type, $theme, $path) {
  return [
    // The key you use here will become the unique name for this theme hook.
    // It determines what will be used as the template file name and the
    // value of the #theme form array property.
    'user_login_form' => [
      'render element' => 'form',
      // You can optionally set the template file name to something other than
      // user-login-form.html.twig if you want to.
      # 'template' => 'form--user-login-form',
    ],
  ];
}
```

By using `'render element' => 'form'` here, we're telling Drupal to pass the `$form` renderable array to our template, and that we'll output it from there.

### Set the `#theme` property on the `$form`

In your *THEMENAME.theme* or *MODULENAME.module* file, add an implementation of `hook_form_alter` or `hook_form_FORM_ID_alter`, and use it to set a value for the `#theme` property of the `$form` array for the form you want to theme.

Example *mytheme.theme*:

```
use Drupal\Core\Form\FormStateInterface;

/**
 * Implements hook_form_alter()
 */
function mytheme_form_alter(&$form, FormStateInterface $form_state, $form_id) {
  if ($form_id === 'user_login_form') {
    // The value here is the same as the key from our hook_theme()
    // implementation above.
    $form['#theme'] = 'user_login_form';
  }
}
```

Adding a `#theme` property to the `$form` array will tell the [Drupal renderer](https://drupalize.me/tutorial/render-api-renderers) (a service that converts render arrays and form arrays to HTML) that you want to use the `user_login_form` theme hook from the `hook_theme()` implementation for this element of the render array. And in this case, we want to use it for the complete form, so we add it at the top level of the array.

**Tip:** If you don't know the ID of the form you want to theme, add `var_dump($form_id)` to the `hook_form_alter()` example above and visit the page that contains the form. The IDs of any forms on the page will be output.

### Create the Twig template file for the form

Next, create the Twig template file that corresponds with the new theme hook, `user_login_form`. By default, this will be the theme hook name with any underscores (`_`) converted to hyphens (`-`). In this case, `user_login_form` will become `user-login-form.html.twig`. Go ahead and create that file anywhere within the *templates/* subdirectory of your theme or module:

Example *templates/user-login-form.html.twig*:

```
<div class="wrapper">
  <div class="left">
    {{ form.name }}
  </div>
  <div class="right">
    {{ form.pass }}
  </div>
  {{ form | without('name', 'pass') }}
</div>
```

The `form` variable corresponds to the `$form` render array. Use Twig's `{{ dump(form) }}` to inspect the variable and figure out individual field names. Then render the fields like `{{ form.FIELD_NAME }}`. replacing `FIELD_NAME` with the name of the field you discover via `{{ dump(form) }}`.

When outputting a form in a template file, make sure you always print out the complete `form` variable somewhere in the template (usually at the end). Even if you've printed out all the fields on the form, this variable might contain hidden fields, CSRF tokens, and other HTML that's required for the form to work.

### Clear the cache and test the form

[Clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) so that Drupal will find your changes. Then, visit a page that contains your form to verify it's using your new template file.

You should now be able to theme the form like you would any other element that's displayed via a Twig template file. For example, you could [create an asset library](https://drupalize.me/tutorial/define-asset-library) and [attach it](https://drupalize.me/tutorial/attach-asset-library) to add a CSS grid and create a two-column layout.

## Recap

In this tutorial, we walked through the process of associating a Drupal form with a Twig template file, so that the form elements could be laid out using HTML and CSS. This required us to create a new theme hook and alter the existing `$form` array so that its `$form['#theme']` property referenced the new theme hook. Then we could create and customize the template file with a filename based on our form's theme hook.

## Further your understanding

- How would you use the same Twig template file for 2 forms with different unique IDs?
- Why is it important to remember to always print the complete `{{ form }}` array in your Twig template file?

## Additional resources

- [Define a New Form Controller and Route](https://drupalize.me/tutorial/define-new-form-controller-and-route) (Drupalize.Me)
- [Use #prefix and #suffix Properties to Wrap an Element](https://drupalize.me/tutorial/use-prefix-and-suffix-properties-wrap-element) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Retrieve and Display Forms](/tutorial/retrieve-and-display-forms?p=2734)

Clear History

Ask Drupalize.Me AI

close
---
title: "Exercise: Add an Asset Library"
url: "https://drupalize.me/tutorial/exercise-add-asset-library?p=3269"
guide: "[[frontend-theming]]"
---

# Exercise: Add an Asset Library

## Content

To add CSS or JavaScript files or libraries to your site, you can attach them as asset libraries in your theme. In this exercise, you'll create 2 asset libraries and attach them globally via your theme's info file. In this tutorial, we'll pull in the CSS and JavaScript from the popular Bootstrap framework so that we can make use of its layout utility classes later on. We'll also add a custom CSS file that contains global styles for our site, like setting the page background color.

If you want to try and complete this on your own first you'll need to:

- Add the [Bootstrap](https://getbootstrap.com) CSS and JavaScript files to your theme.
- Define an asset library using a *THEMENAME.libraries.yml* file in your theme.
- Tell Drupal to attach your asset library so that the CSS and JavaScript files it represents are included in the page.

Once that's done your site won't look all that different. But if you view the page source, or look closely, you should see that the Bootstrap files are included along with any CSS rules you placed into your custom style sheet.

**Note:** Since this course is focused on teaching the Drupal aspects of theme development, and not on writing CSS, we're using the Bootstrap CSS. Feel free to use the framework or library of your choice if you don't want to use Bootstrap.

You should try to complete the exercise steps on your own and use the video to help guide you if you get stuck.

At the end of this exercise, you'll find a video walk-through of the solution.

## Goal

Define asset libraries and include CSS and JavaScript files in a custom theme.

## Prerequisites

- [Set Up Demo Site for Theming Practice](https://drupalize.me/tutorial/set-demo-site-theming-practice)

In this tutorial, you'll be applying your knowledge of asset libraries! We assume that you're already familiar with the information in these tutorials:

- [What Are Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library)
- [Attach a Library](https://drupalize.me/tutorial/attach-asset-library)

## Exercise

In the following steps, we'll create 2 asset libraries in our theme. One for our custom CSS and one for Bootstrap files. Then, we'll apply CSS from the libraries to our site globally.

### Download Bootstrap

Download the Bootstrap files and place them in your theme. We'll use this as an example, so we can focus on the Drupal aspects of creating a theme.

Download the compiled and minified files from [Bootstrap](https://getbootstrap.com/) > *Download* (link next to current version) > *Compiled CSS and JS* (heading) > **Download** (button).

Unzip the archive and move the */css*, and */js* directories from the resulting directory into the root directory of your theme. This should result in */themes/THEMENAME/css*, and */themes/THEMENAME/js*.

### Create a libraries file

Create a new file */themes/THEMENAME/THEMENAME.libraries.yml*.

### Define an asset library for Bootstrap

Define a new asset library named `bootstrap` that includes the bootstrap-provided CSS and JavaScript files *css/bootstrap.min.css*, and *js/bootstrap.min.js*.

**Note:** The exact file names and their paths can vary depending on the version of Bootstrap you downloaded.

### Create a custom CSS file

Create a CSS file at */themes/THEMENAME/css/global.css* for your custom styles.

Add a rule like the following:

```
.jumbotron {
  background: #999;
  border: 1px solid #666;
  padding: 1em;
}
```

### Define another asset library

Define a new asset library named `global` in your *THEMENAME.libraries.yml* that tells Drupal to include the new *global.css* file.

### Attach the libraries

Edit your *THEMENAME.info.yml* file and add the 2 libraries you defined above to the info file so that they are included on every page.

### Verify it worked

Clear the cache and refresh the home page. It should look different.

View source on the page to ensure that your new CSS and JavaScript files are being added. (Hint: Turn off CSS and JS aggregation at *admin/config/development/performance*.)

## Recap

After completing this exercise when you view any public-facing page on your site you should see the Bootstrap frameworks CSS and JS files included in the source of the page. As well as the results of any CSS rules you add to the *global.css* file you created.

Sprout Video

## Further your understanding

- How would you extend or alter an existing asset library? Learn more in [Extend or Alter Existing CSS and JavaScript Asset Libraries](https://drupalize.me/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries).

## Additional resources

- [What Are Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries) (Drupalize.Me)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library) (Drupalize.Me)
- [Attach a Library](https://drupalize.me/tutorial/attach-asset-library) (Drupalize.Me)
- [Detailed documentation of asset library file properties](https://www.drupal.org/docs/theming-drupal/adding-stylesheets-css-and-javascript-js-to-a-drupal-theme) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Exercise: Create a New Theme](/tutorial/exercise-create-new-theme?p=3269)

Next
[Exercise: Configure Your Environment for Theme Development](/tutorial/exercise-configure-your-environment-theme-development?p=3269)

Clear History

Ask Drupalize.Me AI

close
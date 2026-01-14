---
title: "Define an Asset Library"
url: "https://drupalize.me/tutorial/define-asset-library?p=2860"
guide: "[[integrate-javascript-drupal]]"
---

# Define an Asset Library

## Content

New asset libraries can be defined by either modules or themes. In order to define a new asset library you need to create the requisite CSS and JavaScript files, and a new *THEMENAME.libraries.yml*, or *MODULENAME.libraries.yml* file that aggregates them together and provides metadata about the library itself and any dependencies.

In this tutorial we’ll:

- Look at the structure of a *\*.libraries.yml* file and demonstrate how to combine a couple of CSS and JS files together into an asset library that can be used in a theme or a module
- Look at how one asset library can declare that it is dependent on another in order to ensure the assets from the dependency are loaded as well

By the end of this tutorial you should know how to define a new asset library in either a module or a theme.

## Goal

Define a new asset library named "retro" that includes both CSS and JavaScript assets.

## Prerequisites

- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries)
- [An Introduction to YAML](https://drupalize.me/videos/introduction-yaml)

**Note:** While the example below covers how to define an asset library in a theme, the same steps work for a module. Just use *MODULENAME.libraries.yml* for the file name.

## Creating the retro library

The example library we're going to create is a custom asset library (called *retro*) that we can use to add some pizazz to our site. The first thing we need to do is to decide if this asset library belongs to a theme or a module. In our case, we're going to add this asset library to our theme. If you haven't created a theme before give this [Use a Base Theme](https://drupalize.me/tutorial/use-base-theme) a try.

We're going to use [Drush](https://drupalize.me/tutorial/what-drush-0) to create a theme, which we're also calling Retro. We can then add our asset library to our new custom theme.

```
drush generate theme
```

The theme generator will ask us for the name of our theme, as well as a description. We're going to use Olivero as a base theme, but feel free to accept the defaults for the other prompts. With our theme generated, we can now take a look at */themes/custom/retro* to see our new theme's files. In this directory we'll add a file called *retro.libraries.yml* with information about our new asset library.

- Theme name: `Retro`
- Theme machine name: `retro`
- Base theme: `olivero`
- Description: `An amazing Retro theme`
- Package: `Custom`

Sprout Video

**Note**: In the video at around 2:29, the video displays an info file with incorrect syntax for the `core/jquery` dependency. The graphics, code examples, and example [Custom Retro Theme download](https://drupalize.me/sites/default/files/tutorials/retro-drupal-10.zip) (.zip) show the correct syntax.

## Parts of an asset library

Image

![Parts of an asset library](../assets/images/define-an-asset-library.png)

## Declare a new asset library

First we'll specify the retro asset library, and set its version number to 1.0. Then we'll specify the CSS file associated with this library. We'll put a file called *fonts.css* in a *css* subdirectory within our theme to keep things organized. We'll also use attributes to set the weight of this CSS file which will help ensure it's added late in the attachment cycle. We'll also specify our custom JavaScript file *rainbow-headings.js*. Finally we'll declare a dependency on the rainbow library, a jQuery plugin which provides the rainbow effects we're looking to add to our site.

Let's declare a new asset library named `retro` that includes one new CSS file, one new JavaScript file, and depends on another asset library named `retro/rainbow`.

Add the following code to the *retro.libraries.yml*:

```
retro:
  version: 1.0
  css:
    theme:
      css/fonts.css: { weight: 10 }
  js:
    js/rainbow-headings.js: { }
  dependencies:
    - retro/rainbow
```

In the above code:

- The first line `retro:` is the name of the new asset library. It needs to be unique within this file. It will be used later to refer to the library.
- The `version: 1.0` line is optional, and provides information about a library's version for future reference. It's especially relevant when including CSS or JavaScript assets from a third-party library.
- Nested under the `css:` and `js:` keys, we tell Drupal about the CSS and JavaScript files that make up our new library. Note the additional nesting under `theme:` for CSS files. This will be discussed more in a moment.
- Finally, the lines `css/fonts.css: { weight: 10 }`, and `js/rainbow-headings.js: { }` tell Drupal about the files we want to include. The key is the path to the file to include, and the value is an object that is either empty, or contains additional configuration information specific to the file being loaded.

## Paths to CSS and JavaScript files

The path of the file is relative to the module or theme directory, unless it starts with a `/`, in which case it is relative to the Drupal root. If the file path starts with `//`, it will be treated as a protocol-free, external resource (e.g., `//cdn.com/library.js`). Full URLs (e.g., `http://cdn.com/library.js`) as well as URLs that use a valid stream wrapper (e.g., `public://path/to/file.js`) are also supported.

If the path starts with */libraries/* the `library.libraries_directory_file_finder` service is used to find the files and it will look in the following locations:

- A *libraries/* directory in the current site directory, for example: *sites/default/libraries*.
- The root *libraries/* directory.
- A *libraries/* directory in the selected installation profile, for example: *profiles/my\_profile/libraries*.

The following is an example of loading a file the */libraries* directory of a project:

```
retro-from-cdn:
  js:
    /libraries/rainbow-headings/rainbow-headings.min.js: {}
```

The following is an example of loading a file from an external CDN:

```
retro-from-cdn:
  js:
    //cdn.com/js/rainbow-headings.js: {type: external}
```

Note the use of `{type: external}` in the code above. More on this below.

## Additional per-asset configuration options

The following additional configuration options can be used with individual file assets:

**attributes:** (JavaScript only.) An object that contains HTML attributes to apply to the HTML `script` tag.

For example:

```
js:
  path/to/file.js: { attributes: { defer: true } }
```

Would result in:

```
<script src="path/to/file.js" defer="true"></script>
```

**browsers:** Specify which browser(s) this asset should be loaded for.

**deprecated:** As of Drupal 8.8 asset libraries can be marked as deprecated. When present, the library discovery service will trigger an error with the provided deprecation message.

**media:** (CSS only.) Value of the media attribute to use with the `link` tag.

For example:

```
css:
  theme:
    css/print.css: { media: 'print' }
```

Would result in:

```
<link src="css/print.css" media="print" ... />
```

**minified:** If the file is already minified, set this to true to avoid minifying it again. Defaults to `false`.

**preprocess:** Wether or not the to include the file in asset preprocessing and aggregation. Defaults to to `true`. Set to `false` to exclude a file from aggregation.

**type:** (JavaScript only) The type of asset. One of `file`, `external`, or `setting`.

The default value for `type:`, if you leave it blank, is `file`. When `file` assets are loaded Drupal appends a query string to the file path in some circumstances. (e.g., `/path/to/file.js?v={HASH}`) Mostly for cache busting purposes. If you're curious you can see an example of this code in `Drupal\Core\Asset\JsCollectionRenderer::render`.

For assets that are not hosted by Drupal, add `type: external`. This ensures that the additional, Drupal-specific, cache-busting query string isn't added.

In the code, a protocol-free URI (e.g., `//cdn.com/example.js`) will get automatically set to `type: external` by default. But, it's probably better to be explicit and always declare `external: true` for assets not hosted by Drupal. This prevents any issues when your asset library is loaded as a dependency of another asset library.

**version:** The version for this specific file. Appended to paths when a file is included.

For example:

```
js:
  path/to/file.js: { version: '1.2.3' }
```

Would result in:

```
<script src="path/to/file.js?v=1.2.3"></script>
```

## Asset loading order

All JavaScript files are loaded in the order in which the files are listed. By default all JavaScript assets are loaded in the footer. You can change this behavior by setting `header: true` for a library. Though be aware that once you declare a library as being part of the critical path like this all of its dependencies will also be loaded in the header.

### Example

```
modernizr:
  # Block the page from being loaded until Modernizr is initialized.
  header: true
  js:
    assets/vendor/modernizr/modernizr.min.js: {}
```

Drupal follows a SMACSS-style categorization and CSS files are loaded first based on their category, and then by the order they are listed within a given category. The categories are as follows:

1. `base` — CSS reset/normalize plus HTML element styling
2. `layout` — macro arrangement of a page, including any grid systems
3. `component` — discrete, reusable UI elements
4. `state` — styles that deal with client-side changes to components
5. `theme` — purely visual styling (look-and-feel) for a component

### Example

```
jquery.ui:
  js:
    assets/vendor/jquery.ui/ui/core-min.js: {}
  css:
    component:
      assets/vendor/jquery.ui/themes/base/core.css: {}
    theme:
      assets/vendor/jquery.ui/themes/base/theme.css: {}
```

For more information about SMACSS categorization and Drupal see [the documentation separation of concerns within CSS](https://www.drupal.org/node/1887918#separate-concerns).

Next we need to define this rainbow library, which is now a dependency. We'll link to the GitHub repository which contains the code. It's worth noting that there is no license file in the repository, but we can't leave that information out of our library definition without causing some serious issues. For our purposes here, we're going to assume it's MIT licensed. Next we point to the JavaScript file we've downloaded from GitHub, and specify another dependency on jQuery.

```
rainbow:
  version: 1.0
  remote: https://github.com/xoxco/rainbow-text
  license:
    name: MIT
    url: https://github.com/xoxco/Rainbow-Text/blob/master/README.md
    gpl-compatible: true
  js:
    js/rainbow.js: { }
  dependencies:
    - core/jquery
```

In the above example the `remote:` key isn't required, and is mostly non-functional metadata. It's used internally to help keep track of which libraries are part of Drupal core or a contributed module, and which are not. In this case you can probably read *remote* to mean *third party* more than anything else.

From the documentation:

- **remote:** If the library is a third-party script, this provides the repository URL for reference.
- **license:** If the remote property is set, the license information is required. It has 3 properties:

  - **name:** The human-readable name of the license.
  - **url:** The URL of the license file/information for the version of the library used.
  - **gpl-compatible:** A Boolean for whether this library is GPL-compatible.

Now when our retro asset library is added to a page it will include the rainbow library as well as jQuery automatically. Feel free to explore the *fonts.css* and *rainbow-headings.js* files in the [Custom Retro theme](https://drupalize.me/sites/default/files/tutorials/retro-drupal-10.zip) to see what we're trying to accomplish. Next we need to learn now to [Attach a Library](https://drupalize.me/tutorial/attach-asset-library) but here is a glimpse at the finished product:

Image

![Retro library in action](../assets/images/retro-olivero.gif)

## Recap

In this tutorial we defined a new asset library named *retro*. We learned how themes, and modules, can use a *\*.libraries.yml* file to define assets libraries consisting of CSS and JavaScript files both relative to the project on remotely hosted. Using asset libraries makes it possible for Drupal to ensure that only the CSS and JavaScript that's required for a specific page is loaded.

## Further your understanding

- With CSS aggregation disabled, try changing the SMACSS category of a CSS file included in a library and see how it changes the order in which it's loaded when you view source

## Additional resources

- [Custom Retro theme](https://drupalize.me/sites/default/files/tutorials/retro-drupal-10.zip) (.zip) (Drupalize.Me)
- [What Are Asset Libraries?](https://drupalize.me/tutorial/what-are-asset-libraries) (Drupalize.Me)
- [Define an Asset Library](https://drupalize.me/tutorial/define-asset-library) (Drupalize.Me)
- [Attach an Asset Library](https://drupalize.me/tutorial/attach-asset-library) (Drupalize.Me)
- [Extend or Alter Existing CSS and JavaScript Asset Libraries](https://drupalize.me/tutorial/extend-or-alter-existing-css-and-javascript-asset-libraries) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[What Are Asset Libraries?](/tutorial/what-are-asset-libraries?p=2860)

Next
[Attach an Asset Library](/tutorial/attach-asset-library?p=2860)

Clear History

Ask Drupalize.Me AI

close
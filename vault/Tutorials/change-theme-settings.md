---
title: "Change Theme Settings"
url: "https://drupalize.me/tutorial/change-theme-settings?p=3266"
guide: "[[frontend-theming]]"
---

# Change Theme Settings

## Content

Some, but not all, themes come with administrator-configurable settings that you can change through the UI. These might allow you to upload your own logo, choose between a couple of different pre-defined layouts, or turn features of a theme on or off. In this tutorial we’ll look at where you can find these theme settings if they exist, and how to go about changing them.

## Goal

Understand how to customize theme settings using the administrative UI.

## Prerequisites

- [Theme Settings Overview](https://drupalize.me/tutorial/theme-settings-overview)
- [Download and install a theme](https://drupalize.me/tutorial/download-install-and-uninstall-themes) or [create your own custom theme](https://drupalize.me/tutorial/describe-your-theme-info-file)

## Watch: Change Theme Settings

Sprout Video

## Configure your theme's settings

### Set permissions for theme administration

Ensure that the following permissions are set:

- Administer themes
- Use the administration toolbar
- View the administrative theme
- Use the administration pages and help (optional)

See the [Theme Settings Overview tutorial](https://drupalize.me/tutorial/theme-settings-overview) for a further explanation of permissions for theme administration.

### Navigate to *Appearance* in the administrative toolbar menu

Use the administrative menu to navigate to the *Appearance* page (*admin/appearance*). Decide which theme to configure and select the linked name of the theme or the **Settings** link under the theme name.

### Click on the Settings tab

Decide: Global or theme-specific?

Do you want to change a setting globally or just for a specific theme? Learn about the difference in this tutorial: [Theme Settings](https://drupalize.me/tutorial/theme-settings-overview).

If global, stay put. You're arrived on the Global settings page when you clicked the Settings tab.

### If theme-specific, navigate to the theme whose settings you want to view or change

Don't see your theme? [Make sure it's installed](https://drupalize.me/tutorial/download-install-and-uninstall-themes).

## User pictures in posts

User pictures typically display alongside the author of an article, for example. If the theme you are using displays the user picture and you want to hide it without overriding the template file, uncheck this box.

### User pictures in posts *checked*

Image

![User pictures in posts on](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-user-pic-posts.png?itok=sBhWedDg)

### User pictures in posts *unchecked*

Image

![User pictures in posts off](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-user-pic-posts-off.png?itok=96CWtXwe)

## User pictures in comments

Sometimes a theme will display the user picture next to the comment poster's name. Use this setting to toggle the display of the user's picture in comments, if the user has uploaded a picture to their profile. No picture will display if no default image has been configured in the user picture image field.

*Quick aside:* To set a default user image, go to Configuration > Account settings > Manage fields > Picture (Image field) > Edit. In the Default image section, there's a place to upload an image. Don't forget to click "Save settings" after uploading the image.

### User pictures in comments *on*

Image

![User pictures in comments on](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-user-pic-comments.png?itok=7kUu809T)

### User pictures in comments *off*

Image

![User pictures in comments off](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-user-pic-comments-off.png?itok=V4iqRmFv)

## User verification status in comments

A theme may display the "verification status" of a user — in particular, anonymous users: users who have either not signed in or who do not have an account, but are still allowed to post a comment.

Image

![User verification status in comments](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-verification-status.png?itok=_n_GGHAf)

## Shortcut icon

The shortcut icon, or "favicon," is a special type of image that some web browsers display next to the title of a website in a tab or window. If you have a custom theme, you will want to create and upload a favicon that fits with your site's identity. If you leave this setting checked, or do not override it in your theme's shortcut icon settings, the blue Drupal drop icon will display as the favicon for your site.

### Keeping the default icon

Image

![Default shortcut icon setting](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-default-shortcut-icon-settings.png?itok=UUohj1xf)

### The default Drupal favicon, as displayed in a browser tab

Image

![The default favicon for Drupal](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-default-favicon.png?itok=03T7nlBC)

### Use a custom shortcut icon or favicon

There are two ways to specify a new shortcut icon or favicon for your site. You can either upload a new default, which would apply globally, or you can navigate to your theme's settings, and upload or specify a path to a favicon that will only display for that theme. Even if you specify a new global favicon, you can still override it on a per-theme basis through theme-specific settings.

### Specify a custom favicon

Image

![Settings for a custom favicon](/sites/default/files/styles/max_800w/public/tutorials/images/global-theme-settings-custom-favicon.png?itok=_grutLSk)

## Logo image settings

Themes may display a logo image, and this setting will toggle its display. For example, in the Bartik theme, the "Druplicon" is displayed next to the title in the header region. To turn this off without hacking the template file, uncheck the setting "Use the default logo supplied by the theme." To specify a new default logo image, specify a path or upload a new image. If you choose to upload an image with this widget, it will upload to *sites/default/files*, by default. You may want to move this image to a more organized location, in which case, specify the path in the "Path to custom logo" field.

### Use the default logo supplied by the theme

If you don't want to change the default logo supplied by the theme, leave this checked.

Image

![Bartik's logo.svg](/sites/default/files/styles/max_800w/public/tutorials/images/theme-settings-bartik-logo-svg.png?itok=7xSv4t3M)

To provide a default logo for your theme, upload a file called *logo.svg* to your theme directory. For example, notice how the Bartik theme has done this:

Image

![Location of default logo in Bartik](/sites/default/files/styles/max_800w/public/tutorials/images/bartik-file-list-default-logo-svg.png?itok=k3RVaR0Q)

### Provide a custom logo image

To specify a file name or path other than the default path of *PATH/TO/THEME/logo.svg*, use this setting.

To provide a custom logo image, either globally or specifically, to a theme, either specify a path or upload an image. The path should be relative to the root of your Drupal install, i.e. *sites/default/files/logo/my-custom-logo.png*. If you leave out a path, it will assume *sites/default/files* or the default public directory configured via Configuration > File system (admin/config/media/file-system).

Image

![Theme settings to provide a custom logo](/sites/default/files/styles/max_800w/public/tutorials/images/theme-settings-custom-logo.png?itok=of6ZXF1x)

Image

![Result of specifying a custom logo path for the Ice Cream theme](/sites/default/files/styles/max_800w/public/tutorials/images/theme-settings-custom-icecream-logo.png?itok=et2uLD84)

### Add the default logo filename to your theme's info file

You can now specify a path to a custom default logo in your [theme's info file](https://drupalize.me/tutorial/describe-your-theme-info-file). Add a `logo` key and provide a path relative to your theme directory as the value.

```
logo: 'images/logo.png'
```

## Recap

In this tutorial, we walked through all the different ways you can configure your theme, including user pictures in posts and comments, customizing the shortcut icon, and updating the site logo.

## Further your understanding

- In addition to these theme settings, you can also add a screenshot to your theme's listing on the *Appearance* page. See [Add a Screenshot to Your Theme](https://drupalize.me/tutorial/add-screenshot-your-theme) to learn how.

## Additional resources

- [Add a Screenshot to Your Theme](https://drupalize.me/tutorial/add-screenshot-your-theme)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Theme Settings Overview](/tutorial/theme-settings-overview?p=3266)

Next
[Add a Screenshot to Your Theme](/tutorial/add-screenshot-your-theme?p=3266)

Clear History

Ask Drupalize.Me AI

close
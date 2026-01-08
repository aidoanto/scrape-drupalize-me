---
title: "6.12. Concept: Image Styles"
url: "https://drupalize.me/tutorial/user-guide/structure-image-styles?p=2412"
guide: "[[acquia-certified-drupal-developer-exam]]"
---

# 6.12. Concept: Image Styles

## Content

### Prerequisite knowledge

[Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type")

### What are image styles?

Image styles allow you to upload a single image but display it in several ways; each display variation, or *image style*, is the result of applying one or more *effects* to the original image.

As an example, you might upload a high-resolution image with a 4:3 aspect ratio, and display it scaled down, square cropped, or black-and-white (or any combination of these effects). The core software provides a way to do this efficiently:

1. Configure an image style with the desired effects on the *Image styles* page (*admin/config/media/image-styles*).
2. The effects will be applied the first time a particular image is requested in that style.
3. The resulting image is saved.
4. The next time that same style is requested, the saved image is retrieved without the need to recalculate the effects.

The core software provides several effects that you can use to define styles; others may be provided by contributed modules.

Visit the *Image styles* page via the *Manage* administrative menu, navigate to *Configuration* > *Media* > *Image styles* (*admin/config/media/image-styles*) to see the image styles that are defined by default.

### Related topics

- [Section 6.13, “Setting Up an Image Style”](https://drupalize.me/tutorial/user-guide/structure-image-style-create "6.13. Setting Up an Image Style")
- [Section 6.14, “Concept: Responsive Image Styles”](https://drupalize.me/tutorial/user-guide/structure-image-responsive "6.14. Concept: Responsive Image Styles")
- [Section 6.3, “Adding Basic Fields to a Content Type”](https://drupalize.me/tutorial/user-guide/structure-fields "6.3. Adding Basic Fields to a Content Type")

### Additional resources

[*Drupal.org* community documentation page "Working with images"](https://www.drupal.org/docs/core-modules-and-themes/core-modules/image-module/working-with-images)

**Attributions**

Adapted and edited by [Boris Doesborg](https://www.drupal.org/u/batigolix), and [Jojy Alphonso](https://www.drupal.org/u/jojyja) at [Red Crackle](http://redcrackle.com), from ["Working with images"](https://www.drupal.org/docs/core-modules-and-themes/core-modules/image-module/working-with-images) copyright 2000-2026 by the individual contributors to the [Drupal Community Documentation](https://www.drupal.org/documentation)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[6.11. Changing Content Display](/tutorial/user-guide/structure-content-display?p=2412)

Next
[6.13. Setting Up an Image Style](/tutorial/user-guide/structure-image-style-create?p=2412)

[![Creative Commons License](https://i.creativecommons.org/l/by-sa/4.0/88x31.png)](http://creativecommons.org/licenses/by-sa/4.0/)

This Drupal training resource is licensed under a [Creative Commons Attribution-ShareAlike 4.0 International License](http://creativecommons.org/licenses/by-sa/4.0/). Based on a work at <https://www.drupal.org/docs/user_guide/en/index.html>.

Clear History

Ask Drupalize.Me AI

close
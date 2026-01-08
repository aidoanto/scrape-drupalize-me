---
title: "What Are Media Sources in Drupal?"
url: "https://drupalize.me/tutorial/what-are-media-sources-drupal?p=3274"
guide: "[[media-and-responsive-images]]"
---

# What Are Media Sources in Drupal?

## Content

Media source plugins provide the link between media entities in Drupal and the actual media asset itself. They are the code that understand the difference between an image, a video, and a Tweet, and perform the translation that allows the media ecosystem to treat all media entities equally. For example, local image files, and remote YouTube videos, can both be catalogued in a similar way as media entities, but they need very different handling when it comes to displaying them.

Media sources are represented as plugins, there are a handful in Drupal core, and a developer can add new plugins to represent any type of media your application needs to catalogue.

In this tutorial we'll learn:

- How media source plugins relate to Media Types
- The responsibilities of a media source plugin

By the end of this tutorial you should be able to define the role of a media source plugin and understand what's required to define your own.

## Goal

Explain what Media sources are and the relationship between source plugins and media entity types.

## Prerequisites

- [Overview: Media Management in Drupal](https://drupalize.me/tutorial/overview-media-management-drupal)
- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)

## Media types and media source plugins

Media types (Media entity bundles) have an important distinction compared to other content entity types like Nodes. Every Media type inherits from a **specific media source plugin**. The source plugin provides domain-specific knowledge about the kind of resource being represented. For example, Media types dealing with images know how to validate file extensions and render `<img>` tags. Media types dealing with remotely hosted videos might know how to retrieve thumbnails from a remote API, and display an HTML video player and transcript.

All Media types are required to have a **source field**. When you create a new Media type this field is created by the associated source plugin and can not be modified. This field stores a value that uniquely identifies the resource to display. For an *Image* media type this is likely a pointer to the image file. For a YouTube-hosted remote video this would be the canonical URL of the video which can be used to identify the video when making requests to the YouTube API.

<drupal-media data-entity-type="media" data-entity-uuid="e954f26e-a73b-46d6-8c53-e7884288c413" alt="Screenshot of form for adding a new media entity type showing contents of the "Media source" dropdown which lists sources like audio, spotify, remote video, and Twitter.">

Media source plugins all implement a common interface `\Drupal\media\MediaSourceInterface` so that no matter what form the underlying asset takes the ecosystem of Media modules can perform some standard operations like cataloging and displaying without having to know the details.

There's a good chance that the media you're working with is already supported by core or a contributed module. Core's File, Image, and oEmbed source plugins allow you to work with any locally hosted files (think PDFs, text documents, video files, .zip archives), images, and videos on YouTube and Vimeo. And there are a bunch of existing contributed modules that provide additional sources. [There's a decent list here](https://www.drupal.org/node/2860796), and it's worth searching a bit before implementing your own.

If your media provider isn't supported though, a developer can write a plugin to add support.

## What even is media?

In Drupal, we define "media" as any resource, probably with a visual element, and its associated metadata. Images are probably the most common type of media on the web. They consist of a file (such as JPG, GIF, or PNG format), which is the part you see. They also hold information like alt text, photographer, and metadata (such as capture date and tags for organizing).

More broadly, you can think of a media asset as anything with a canonical resource identifier (filename, URL, ASIN number, Twitter post, Google Spreadsheet, etc.) that you might embed into your site's pages. And it doesn't have to be static like an image. The embedded media could be interactive like an embedded poll, or a Spotify playlist. There's a lot of possibilities.

## Media sources are plugins

From a technical perspective Media sources are plugins like blocks, or render elements. Learn more about Drupal plugins and how they work in [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins).

Specifically, they are plugins that implement the `\Drupal\media\MediaSourceInterface` interface, are annotated with `\Drupal\media\Annotation\MediaSource`, and live in the `{module_name}\Plugin\media\Source` namespace. Learn how to [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes). And for an example of defining a media source plugin see [Create a Custom Media Source Plugin](https://drupalize.me/tutorial/create-custom-media-source-plugin).

## Media source plugin responsibilities

The primary responsibility of a media source plugin is to take a media asset identifier, for example the URL of a YouTube video, or the path to a file on disk, that is associated with a Drupal Media entity, and use it to both display and provide data about the actual media. Including:

- Define how to store media associations. A media source isn't responsible for actually storing the media, only defining how it is represented on a media entity. Usually as some kind of field. In the YouTube example this might be declaring that the video is stored as a string, which is a URL, which points to the canonical item. This also includes the responsibility to validate content before it's saved. For example, is this a YouTube URL or some random other URL?
- Provide thumbnails for individual media assets, and a default fall back thumbnail. These are used by things like the Media Library UI. Drupal assumes that all media entities will have an associated thumbnail.
- Provide a default name (or label) for the media entity when it can be reliably determined automatically. Because all content entities require a label, but in many cases we can save users from having to manually enter it. This might be the filename for a local file, or the title attribute from a remotely hosted video.
- Provide media type specific metadata. Think of this as EXIF data for photos, ID3 tags for audio files, or data available from a remote API for YouTube videos. Additionally, media sources define how this data can be mapped to fields on the media entity in order to dynamically populate them. For example, consuming the video duration from YouTube and using it to fill a user configured `field_video_duration` field on the relevant entity.

The media source plugins defined by core are good reference material for learning, `\Drupal\media\Plugin\media\Source\Image`, and `\Drupal\media\Plugin\media\Source\OEmbed` especially. We've also found the contributed [Media Entity Twitter module](https://www.drupal.org/project/media_entity_twitter) to be an informative example.

## Recap

In this tutorial we learned that every media entity type is tied to a media source plugin. And that source plugins are responsible for creating the link between a media entity, and the media asset it represents. These plugins define how the association is stored, provide thumbnails for the Media Library, determine how a media asset will be displayed, and provide media type specific metadata that can be mapped to standard Drupal fields. Drupal core contains a couple of plugins for common media sources, and modules can add new ones that integrate with any media source not already available.

## Further your understanding

- Can you list some media sources that Drupal doesn't currently integrate with that might be useful for your application?
- When does it make sense to treat things like Tweets, or remotely hosted code snippets, as Media?

## Additional resources

- [Creating and configuring Media Types](https://www.drupal.org/docs/8/core/modules/media/creating-and-configuring-media-types) (Drupal.org)
- [Creating a custom MediaSource plugin for external assets](https://www.drupal.org/docs/8/core/modules/media/creating-a-custom-mediasource-plugin-for-external-assets) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Create a New Media Type in Drupal](/tutorial/create-new-media-type-drupal?p=3274)

Clear History

Ask Drupalize.Me AI

close
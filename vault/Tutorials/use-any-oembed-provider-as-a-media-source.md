---
title: "Use Any oEmbed Provider as a Media Source"
url: "https://drupalize.me/tutorial/use-any-oembed-provider-media-source?p=3274"
guide: "[[media-and-responsive-images]]"
---

# Use Any oEmbed Provider as a Media Source

## Content

If the Media assets you want to use in your library support oEmbed, then you might be able to use them with a minimal custom code. Before you go down the path of creating a custom media source plugin try this approach first.

[oEmbed](https://oembed.com/) is a standard way of allowing third party sites to embed an asset represented by a URL. The Remote Video source in core uses the oEmbed features of YouTube and Vimeo. When you paste a link into a Slack channel, and it displays a pretty card preview, or an embedded video or Spotify playlist, that's oEmbed in action. Does the Media you want to embed have a canonical URL? If so, [paste it into the tool here](http://debug.iframely.com/) and see if it displays oEmbed info in the results.

In this tutorial we'll:

- Learn how to enable additional oEmbed providers as Media sources
- Use the contributed [oEmbed Providers module](https://www.drupal.org/project/oembed_providers) for compatible providers
- Demonstrate how to create a custom oEmbed media source plugin to further customize the results

By the end of this tutorial you should be able to embed any oEmbed-compatible content as Media assets in Drupal.

## Goal

Use Codepen and Spotify (or any oEmbed enabled site) as a Media source.

## Prerequisites

- [What Are Media Sources?](https://drupalize.me/tutorial/what-are-media-sources-drupal)
- [Implement a Plugin Using PHP Attributes](https://drupalize.me/tutorial/implement-plugin-using-php-attributes)

Before you start writing a custom source plugin, check to see if the source you want to use supports oEmbed. There's a list of providers that Drupal core supports here: <https://oembed.com/providers.json>. But only YouTube and Vimeo (see the core Remote Video source) are enabled by default. You can enable additional providers in a couple of different ways.

If oEmbed isn't going to work for your use case, see [Create a Custom Media Source Plugin](https://drupalize.me/tutorial/create-custom-media-source-plugin)

## Contributed oEmbed Providers module

The contributed [oEmbed Providers module](https://www.drupal.org/project/oembed_providers) can enable any of the providers in the [oembed.com/providers.json](https://oembed.com/providers.json) list, and has a configuration form that allows you to add new providers not in the list. Use this if, for example, your organization has its own oEmbed service, or you want to integrate with a provider not in the *providers.json* list. Core doesn't currently support adding new providers to the list without this contributed module.

Using the oEmbed Providers module requires:

1. Defining a new provider if it's not in the existing *providers.json* list.
2. Creating a *Provider Bucket*, which acts as a Media Source plugin that groups one or more providers together.
3. Creating a new Media type that uses the new *Provider Bucket* as the source.

### Enable and configure the oEmbed Providers module

Start by installing the oEmbed Providers module:

```
composer require drupal/oembed_providers
```

In the *Manage* administration menu, navigate to *Configuration* > *Media* *oEmbed Providers* > *Provider Buckets* (*admin/config/media/oembed-providers/buckets*), then press the *Add provider bucket* button.

### Define a Provider Bucket

Fill in the form to add a new *Provider Bucket*. Select each provider you would like to enable.

For example: Create a bucket named "Social Media" and enable providers like Facebook and Twitter to allow content authors to add Media assets based on links to your social media posts.

Image

![Form for adding a new oembed provider bucket.](/sites/default/files/styles/max_800w/public/tutorials/images/oembed-providers-add-bucket.png?itok=96XQMhpb)

### Add a new Media type

Next add a new Media type and choose the Provider bucket you created earlier in the *Media source* select field.

Image

![Screenshot of media type creation form with an arrow pointing to the social media source option that you should select.](/sites/default/files/styles/max_800w/public/tutorials/images/oembed-providers-remove-video.png?itok=dt3afJSb)

## Custom oEmbed source plugins

If for some reason the default behavior of the core `\Drupal\media\Plugin\media\Source\OEmbed` media source plugin doesn't work for your needs, you can create a new custom plugin that inherits its features and build from there.

As an example, the core oEmbed plugin has [a bug with the way that it handles thumbnail images provided by an oEmbed source if the file name does not include an extension](https://www.drupal.org/project/drupal/issues/3080666).

Compare the value of the `thumbnail_url` field in the output from these two examples. The Spotify one doesn't have an extension, and will cause issues when used as a Media source provider where Drupal can't display a thumbnail.

- <https://codepen.io/api/oembed/?format=json&url=https://codepen.io/wesruv/pen/RjmVvV>
- <https://open.spotify.com/oembed?format=json&url=https://open.spotify.com/album/2zLOOyWzZoPrM9ZPQfeXBN?si=nll6M02fTxeXeaL6o7e7VA>

We can resolve this ourselves by creating a new Media source plugin and overriding the `\Drupal\media\Plugin\media\Source\OEmbed::getLocalThumbnailUri` method to force a `.jpg` extension when saving the images locally.

The code that you write needs to live in a module. Either create a new one, or add to an existing one. For this example we're adding to a module named `media_source_examples`.

[Complete source code can be found in this example GitHub repo](https://github.com/DrupalizeMe/demo-media-8x).

Example *media\_source\_examples/src/Plugin/media/Source/Spotify.php*:

```
<?php

namespace Drupal\media_source_examples\Plugin\media\Source;

use Drupal\Component\Utility\Crypt;
use Drupal\Core\File\Exception\FileException;
use Drupal\Core\File\FileSystemInterface;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\media\Attribute\OEmbedMediaSource;
use Drupal\media\OEmbed\Resource;
use Drupal\media\Plugin\media\Source\OEmbed;
use GuzzleHttp\Exception\RequestException;

/**
 * Spotify embed.
 */
#[OEmbedMediaSource(
  id: "spotify_oembed",
  label: new TranslatableMarkup("Spotify"),
  description: new TranslatableMarkup("Embed spotify content."),
  allowed_field_types: ["string"],
  providers: ["Spotify"],
  default_thumbnail_filename: "no-thumbnail.png",
)]
class Spotify extends OEmbed {
  // No need for anything in here; the base plugin can take care of typical interactions
  // with external oEmbed services.

  // \Drupal\media\Plugin\media\Source\OEmbed::getLocalThumbnailUri doesn't
  // handle images that do not have an extension. So we override it and force a
  // .jpg extension for file names. Without the extension Drupal's image
  // handling breaks.
  //
  // See https://www.drupal.org/project/drupal/issues/3080666
  protected function getLocalThumbnailUri(Resource $resource) {
    // If there is no remote thumbnail, there's nothing for us to fetch here.
    $remote_thumbnail_url = $resource->getThumbnailUrl();
    if (!$remote_thumbnail_url) {
      return NULL;
    }
    $remote_thumbnail_url = $remote_thumbnail_url->toString();

    // Compute the local thumbnail URI, regardless of whether it exists.
    $configuration = $this->getConfiguration();
    $directory = $configuration['thumbnails_directory'];
    $local_thumbnail_uri = "$directory/" . Crypt::hashBase64($remote_thumbnail_url) . '.' . pathinfo($remote_thumbnail_url, PATHINFO_EXTENSION);

    $local_thumbnail_uri .= '.jpg';

    // If the local thumbnail already exists, return its URI.
    if (file_exists($local_thumbnail_uri)) {
      return $local_thumbnail_uri;
    }

    // The local thumbnail doesn't exist yet, so try to download it. First,
    // ensure that the destination directory is writable, and if it's not,
    // log an error and bail out.
    if (!$this->fileSystem->prepareDirectory($directory, FileSystemInterface::CREATE_DIRECTORY | FileSystemInterface::MODIFY_PERMISSIONS)) {
      $this->logger->warning('Could not prepare thumbnail destination directory @dir for oEmbed media.', [
        '@dir' => $directory,
      ]);
      return NULL;
    }

    try {
      $response = $this->httpClient->get($remote_thumbnail_url);
      if ($response->getStatusCode() === 200) {
        $this->fileSystem->saveData((string) $response->getBody(), $local_thumbnail_uri, FileSystemInterface::EXISTS_REPLACE);
        return $local_thumbnail_uri;
      }
    }
    catch (RequestException $e) {
      $this->logger->warning($e->getMessage());
    }
    catch (FileException $e) {
      $this->logger->warning('Could not download remote thumbnail from {url}.', [
        'url' => $remote_thumbnail_url,
      ]);
    }
    return NULL;
  }

}
```

In the above code, the most important part for making this work with the existing oEmbed system is extending the core provided `OEmbed` class, and making use of the `providers` key in the attribute. As long as this key contains a value that matches a provider from this list <https://oembed.com/providers.json> it should work.

You can also use this approach as an alternative to the contributed oEmbed Providers module above if you want the provider to show up as a source in the Media sources list when creating new Media Entity types, rather than a generic oEmbed source that works with multiple providers.

Image

![Example of Media type creation form showing custom source plugins in the select list for Media source type.](/sites/default/files/styles/max_800w/public/tutorials/images/oembed-providers-custom-source.png?itok=UQgZhQ9t)

This would also allow you to further customize the behavior of that specific provider if necessary. An example, with the minimal amount of code, would be something like:

*media\_source\_examples/src/Plugin/media/Source/CodeSnippets.php*:

```
<?php

namespace Drupal\media_source_examples\Plugin\media\Source;

use Drupal\Core\StringTranslation\TranslatableMarkup;
use Drupal\media\Attribute\OEmbedMediaSource;
use Drupal\media\Plugin\media\Source\OEmbed;

/**
 * You can find possible values to use in the providers object in the list
 * here https://oembed.com/providers.json.
 */
#[OEmbedMediaSource(
  id: "codesnippets_oembed",
  label: new TranslatableMarkup("Code snippets"),
  description: new TranslatableMarkup("Embed code snippets."),
  allowed_field_types: ["string"],
  providers: ["Codepen", "Codesandbox"],
  default_thumbnail_filename: "no-thumbnail.png",
)]
class CodeSnippets extends OEmbed {
  // No need for anything in here; the base plugin can take care of typical
  // interactions with external oEmbed services. However, you can override any
  // of the parent classes methods to customize things as needed.
}
```

## Recap

In this tutorial we learned about using oEmbed providers as Media sources for use within a Drupal media library. We learned that even though core supports a large number of providers, only YouTube and Vimeo are enabled by default. To enable others you can either use the contributed oEmbed Providers module, or define a new Media source plugin in a module. There are benefits to both approaches, so you'll need to choose the one that works best for your use-case.

## Further your understanding

- Can you think of a scenario where you might still want to write a custom source plugin for a site like Spotify that supports oEmbed? Hint: What can the Spotify REST API do that oEmbed can't?
- What are the advantages and disadvantages of this approach?

## Additional resources

- [Learn more about the oEmbed spec](https://oembed.com/) (oembed.com)
- [oEmbed in Drupal 8](https://www.savaslabs.com/blog/oembed-drupal-8) (savaslabs.com) - Contains information about handling providers that don't conform to the spec.

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Create a New Media Type in Drupal](/tutorial/create-new-media-type-drupal?p=3274)

Next
[Create a Custom Media Source Plugin](/tutorial/create-custom-media-source-plugin?p=3274)

Clear History

Ask Drupalize.Me AI

close
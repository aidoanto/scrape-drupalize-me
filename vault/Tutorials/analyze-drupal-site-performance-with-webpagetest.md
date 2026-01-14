---
title: "Analyze Drupal Site Performance with WebPageTest"
url: "https://drupalize.me/tutorial/analyze-drupal-site-performance-webpagetest?p=3091"
guide: "[[drupal-site-administration]]"
---

# Analyze Drupal Site Performance with WebPageTest

## Content

WebPageTest ([webpagetest.org](https://webpagetest.org)) is a free [open source](https://github.com/WPO-Foundation/webpagetest/) resource that runs performance tests on a site, provides educational reports about what it finds, and suggests optimizations you can make. The tests performed via the WebPageTest interface include Lighthouse tests, performance-specific tests, [Core Web Vitals](https://drupalize.me/tutorial/what-are-core-web-vitals), visual comparisons, and traceroute tests. The tool also allows saving a history of tests if you sign up for a free account. This tool won't make your site faster on its own, but it will give you some good ideas about where to focus your efforts.

In this tutorial we'll:

- Learn how to run performance tests via the WebPageTest web interface
- Learn how to read and interpret the results

By the end of this tutorial, you should know how to use the WebPageTest online interface to analyze a Drupal site's performance.

## Goal

Test a Drupal site's performance with WebPageTest tool, analyze the results of the tests, and interpret the results to determine what to work on.

## Prerequisites

- The site you want to test needs to be publicly accessible via the web. You can't test a localhost site.

## Run WebPageTest test on your Drupal site

### Start a WebPageTest test run

Navigate to <https://www.webpagetest.org>. In the dropdown of tests, choose *Site Performance*. In the field where it says *Enter the site URL*, paste the URL to the front page of your site.

Image

![Screenshot of the WebPageTest site UI](../assets/images/webpagetest_top_ui.png)

Scroll down the page to the *Simple Configuration* section and open the accordion. For this tutorial, we’ll be focusing on the desktop tests. You can run tests on your own for mobile devices and different bandwidth scenarios by following the same steps. Choose the *Desktop cable* option.

Check the *Include Repeat View* checkbox. The Repeat View allows you to analyze the performance improvement on the second load of the page. It’s often helpful in assessing how well the page is cached.

Note: We focus on running and analyzing Lighthouse tests in [Analyze Drupal Site Performance with Lighthouse](https://drupalize.me/tutorial/analyze-drupal-site-performance-lighthouse). We’ll leave the *Run Lighthouse Audit* checkbox unchecked for this tutorial.

Image

![Screenshot of the WebPageTest simple test configuration](../assets/images/webpagetest_simple_config.png)

In the advanced configuration, you can refine location and speed settings. It’s helpful if you’re trying to test for a specific user audience or geographic region. For this tutorial, we’ll keep it unchanged.

In the *Repeat View* row, choose the *First View and Repeat View* option and uncheck the *Capture Video* checkbox to speed up the test run. We don’t need a video of the test at this time.

Image

![Screenshot of the WebPageTest simple test configuration](../assets/images/webpagetest_advanced_config.png)

Press the *Start Test* button. The test may take a while to run depending on the size of the queue.

Image

![Screenshot of the WebPageTest simple test configuration](../assets/images/webpagetest_waiting_screen.png)

### Review your test results

After the test completes, you'll see a general summary of the test.

Image

![Screenshot of the WebPageTest results summary](../assets/images/webpagetest_results_summary.png)

Scroll down the page, and you should see the *Observed Metrics* summary based on the median run. To generate this, WebPageTest runs a set of tests 3 times and then produces a median run. It’s helpful because performance test results fluctuate, and sites may perform differently under different sets of conditions.

Image

![Screenshot of the WebPageTest observed metrics](../assets/images/webpagetest_observed_metrics.png)

The metrics highlight the scores, and results, for Largest Contentful Paint (LCP), Cumulative Layout Shift (CLS), and Total Blocking Time (TBT). The results also include measurements like time to first byte, time to the first render, First Contentful Paint (FCP), and speed index.

If the metrics in the results are highlighted in yellow or red, they may need improvements. In our case, the metrics are highlighted in green, and overall the site performs well.

In the *Runs* section of the results, you can see results for each run. You should notice that subsequent page runs were slower in some cases than the original runs. It may indicate problems with the cache setup of the site. If your site uses a Varnish layer for caching, subsequent page loads *should* be faster. In our case, the site is a dev sandbox and doesn’t have a Varnish layer set up. You can see the cache headers in the browser’s *Network* tab.

Historically, one of the most critical performance metrics was speed index -- the average time at which visible parts of the page are displayed. It’s expressed in milliseconds and depends on the viewport's size. As the way we build sites has evolved and commonly means loading content via JavaScript that isn't initially visible to the user, this time increased and stopped reflecting the actual performance of the site. The more meaningful performance measurement shifted from speed index towards Core Web Vitals.

If you want to learn more about the speed index results, press on the *Speed index* label in the *Metrics* section.

### Understanding Core Web Vitals

The [Core Web Vitals](https://web.dev/vitals/) is an initiative by Google to provide unified guidance for quality signals essential to delivering a great user experience on the web. The Core Web Vitals consists of the following measurements:

- *Largest Contentful Paint (LCP)* - marks the time at which the browser paints the largest text or image; measures loading performance. This metric is healthy when it’s below 2.5 seconds.
- *Cumulative Layout Shift (CLS)* - measures the movement of visible elements within the viewport; measures visual stability. This metric is healthy when it’s below 0.1.
- *First Input Delay (FID) or Time to Interactive (TTI)* - the amount of time it takes for the page to become fully interactive; measures interactivity. FID can be measured as part of TBT. A healthy metric is below 100 milliseconds.
- *Total Blocking Time (TBT)* - Sum of all periods between FCP and TTI when task length exceeded 50 ms, expressed in milliseconds.

Taken together, these metrics provide a more comprehensive view of a site's performance. Most importantly, what the experience is like for a visitor. To learn more about the Core Web Vitals follow this [guide](https://product.webpagetest.org/core-web-vitals).

In the WebPageTest report we can dig deeper into the observed metrics.

Press on the *LCP* metric in the *Metrics* section of the results to dive deeper into the Core Web Vitals analysis.

Image

![Screenshot of LCP](../assets/images/webpagetest_lcp.png)

In our case, the largest content on the page is a hero banner. Since we optimized this image in [Analyze Drupal Site Performance with Lighthouse](https://drupalize.me/tutorial/analyze-drupal-site-performance-lighthouse), the metric is still within the range of under 2.5 seconds.

We could optimize the image more or deliver it in the next-gen web image format to improve the score further.

Image

![Screenshot of LCP details](../assets/images/webpagetest_lcp_details.png)

The test showed that our TBT is 0 ms which is a perfect result, and there is nothing to improve. Solutions for the improvement of TBT may vary based on the third-party libraries, scripts, and resources you are using on the site.

TBT is largely influenced by JavaScript execution. External libraries like Google Analytics, external video embeds, iFrames, and third-party JavaScript integrations might be primary contributors to this metric. The Umami site we are analyzing doesn't have any of these libraries, so we got a perfect result.

### Understanding Cumulative Layout Shift

The Cumulative Layout Shift (CLS) determines the visual stability of the page. When a visitor views a page that contains a large image, and the image is slow to load, they might see the text of the page initially; but, then it'll jump downwards once the image is rendered. This is known as layout shift.

If the layout shifts dramatically during the loading time, it delivers a suboptimal user experience. To avoid layout shift, you need to provide a placeholder space on the page where images and other dynamic content will load. These adjustments make the layout structure stable and minimize unexpected shifts. Press on the *CLS* metric to dive deeper into its results.

The test revealed 3 shifts.

The first shift happened when the logo loaded.

Image

![Screenshot of the logo loading shift – no logo](../assets/images/webpagetest_shft_1_a.png)

Image

![Screenshot of the logo loading shift – logo present](../assets/images/webpagetest_shft_1_b.png)

The next shift happened when the search icon was loaded.

Image

![Screenshot of the search icon loading shift – no icon](../assets/images/webpagetest_shft_2_a.png)

Image

![Screenshot of the search icon loading shift – icon](../assets/images/webpagetest_shft_2_b.png)

And the final shift happened when the font was replaced with the fully loaded Google Font and text on the page was rerendered with the font.

Image

![Screenshot of the font loading shift – no font](../assets/images/webpagetest_shft_3_a.png)

Image

![Screenshot of the font loading shift – font present](../assets/images/webpagetest_shft_3_b.png)

To fix the first 2 shifts, let's set a defined width and height for the image containers. You can apply the fix in the CSS for your theme by giving container elements for these images explicit dimensions, so they'll effectively hold the space necessary to display the image once it's loaded.

To fix the font shift, you may look into preloading the font, serving the font locally in `woff2` format, or using variable fonts instead of a regular font with subsets of weights.

### Understanding the content breakdown

Scroll to the individual runs results on the main results page. You should see the content breakdown. Follow the Content breakdown link to its page where you can see measurement of the types of content loaded for the page.

Image

![Screenshot of the content breakdown results](../assets/images/webpagetest_content_breakdown.png)

The results show that the majority of the content is images. Image optimization can influence the performance further. The second category is fonts. Preloading fonts or hosting them locally, and using variable fonts can also improve the performance.

## Recap

WebPageTest is a free web-based utility that allows running various performance tests against a site. It allows testing against different browsers, devices, and simulated Internet connection speeds. The reports provide visual reporting of the page load process and other metrics such as speed index, first-byte time, and Core Web Vitals.

The generated reports are detailed and allow us to dive deeper into any particular metric. WebPageTest also hosts a variety of educational resources and guides that you can use as a foundation during the performance optimization process.

## Further your understanding

- We tested desktop devices. Can you reconfigure the test to run against mobile devices? Is the score different? How? Why?
- Analyze the results of your own site. Based on the results, where do you think would be a good place to start with your optimization efforts?

## Additional resources

- [Core Web Vitals guide](https://product.webpagetest.org/core-web-vitals) (webpagetest.org)
- [Core Web Vitals overview](https://web.dev/vitals/) (web.dev)
- [How to preload web fonts](https://web.dev/codelab-preload-web-fonts/) (web.dev)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Analyze Drupal Site Performance with Lighthouse](/tutorial/analyze-drupal-site-performance-lighthouse?p=3091)

Next
[Overview: Drupal's Cache Modules and Performance Settings](/tutorial/overview-drupals-cache-modules-and-performance-settings?p=3091)

Clear History

Ask Drupalize.Me AI

close
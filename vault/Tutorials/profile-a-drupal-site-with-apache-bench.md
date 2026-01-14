---
title: "Profile a Drupal Site with Apache Bench"
url: "https://drupalize.me/tutorial/profile-drupal-site-apache-bench?p=3091"
guide: "[[drupal-site-administration]]"
order: 48
---

# Profile a Drupal Site with Apache Bench

## Content

[Apache Bench (`ab`)](https://httpd.apache.org/docs/2.4/programs/ab.html) is a tool that comes with the commonly used Apache HTTP server. It is designed to give you an impression of how your current Apache installation performs. It will work for any HTTP server, not just Apache. Apache Bench shows you how many requests per second your server can serve. This metric is in part a measure of how long it takes Drupal (PHP) to process the request and create a response. While there are other things that the HTTP server does too, executing PHP is by far the most expensive when serving Drupal pages.

Therefore, Apache Bench helps profile your PHP code for new features, patches after their application, and PHP libraries used on the site. You can quickly compare before and after metrics as an indicator of the scale of the impact a change has.

In this tutorial, we'll:

- Learn how to run the Apache Bench tool on our local environment
- Learn to interpret the result of the tests

By the end of this tutorial, you should know how to benchmark and profile your local Drupal installation using Apache Bench (`ab`).

## Goal

Use Apache bench to measure performance metrics before and after a code change and then compare the results.

## Prerequisites

- none

## Apache bench overview

Apache Bench (`ab`) is a profiling and benchmarking tool for Apache HTTP servers. It can be run from the terminal. It doesn’t require advanced knowledge of the load or performance testing concepts. It runs with one command that takes a set of [options](https://httpd.apache.org/docs/trunk/programs/ab.html) and a page URL to run tests against.

It comes pre-installed with Apache (`apt install apache2`) or can be installed as part of Apache Utilities (`apt install apache2-utils`). As of BigSur, Apache Bench (`ab`) is installed by default on MacOS.

Apache Bench is best for a local development environment. However, if you manage your own server, you may run the same tests on the development environment. We don’t recommend running this tool on a production environment. Instead, we recommend using third-party profiling monitoring tools like [New Relic](https://newrelic.com) or [Blackfire.io](https://www.blackfire.io/).

## To profile your Drupal site, follow these steps

For this tutorial, we will be profiling the site on the local environment and assume that you have your site running on your local using DDEV, Lando, or any other Drupal local environment setup. Make sure your local server is Apache; otherwise, you won’t be able to use this tutorial.

It's also common for developers to have development-environment-specific configuration that disables caching, and other performance-enhancing features of Drupal in order to make the developer experience better. For best results, make sure you're using settings close to what you would have for production. Or at least be aware of the impact of having these caching features disabled while benchmarking the new feature.

### Establish a baseline

Start by establishing a baseline, without your changes applied, so you have measurements you can compare to after making the changes.

If you have already finished working on a patch or new feature, export your changes and commit them to a local Git branch. Then switch back to the main branch of your project and run the following command in the terminal:

```
ab -c1 -n500 http://drupal9.localhost
```

What's happening here? `ab` is the command that calls the Apache Bench tool. The command is followed by the options:

- `-c`: The c stands for concurrency. Concurrency means the number of requests to perform at a time. Default is one request at a time. We recommend keeping it at one unless you are stress testing your server.
- `-n`: The n option stands for the number of requests to perform for the benchmarking session. The default is just to perform a single request which usually leads to non-representative benchmarking results. We recommend starting with 500 and increasing the number if the benchmarking results are non-representative. Apache bench will aggregate the results of all requests in the output it shows.

The options are followed by the URL of the site you are testing. In our case, we have Drupal 9's default Umami installation on the local environment.

The output of the command will look something like below:

```
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Finished 500 requests

Server Software:        Apache/2.4.53
Server Hostname:        localhost
Server Port:            80

Document Path:          /drupal9/web/index.php
Document Length:        100379 bytes

Concurrency Level:      1
Time taken for tests:   6.226 seconds
Complete requests:      500
Failed requests:        0
Total transferred:      50304500 bytes
HTML transferred:       50189500 bytes
Requests per second:    80.31 [#/sec] (mean)
Time per request:       12.452 [ms] (mean)
Time per request:       12.452 [ms] (mean, across all concurrent requests)
Transfer rate:          7890.36 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:     9   12   1.8     12      25
Waiting:        4    5   0.8      5      13
Total:          9   12   1.8     12      25

Percentage of the requests served within a certain time (ms)
  50%     12
  66%     12
  75%     13
  80%     13
  90%     14
  95%     16
  98%     18
  99%     22
 100%     25 (longest request)
```

### Interpreting the output

The first metric is *Time taken for tests*. The smaller the value, the better the overall performance of the site. Connected to this metric is *Requests per second*: the higher the value, the faster each request to the site was processed -- the better the site performs overall. These top-level latency metrics provide a quick read of the server’s overall performance, especially in comparison to other `ab` tests applied in similar conditions. This is good for seeing how something performs before and after a change is made.

The *Connection Times* timetable below the metrics shows the breakdown values for the time the requests took. We will take the *mean* column as a baseline. The mean value tells us how long a page request took on average (in milliseconds) in each phase. The lower the value, the better the site is performing. These metrics helps determine which part(s) of the request and response cycle should be investigated further.

Apache Bench provides a standard deviation value *[+/-sd]* - it’s an indicator of the accuracy of the result. The smaller the deviation value, the more accurate the test is.

The *Percentiles* help you see how much variation there is between the fastest responses and the slowest. It can highlight possible outliers.

### Run the test against your code

Now that you've run `ab` once and have a baseline, switch back to your feature branch and run the same command you ran before:

```
ab -c1 -n500 http://drupal9.localhost
```

The output we got is shown below:

```
This is ApacheBench, Version 2.3 <$Revision: 1879490 $>
Copyright 1996 Adam Twiss, Zeus Technology Ltd, http://www.zeustech.net/
Licensed to The Apache Software Foundation, http://www.apache.org/

Benchmarking localhost (be patient)
Completed 100 requests
Completed 200 requests
Completed 300 requests
Completed 400 requests
Completed 500 requests
Finished 500 requests

Server Software:        Apache/2.4.53
Server Hostname:        localhost
Server Port:            80

Document Path:          /drupal9/web/index.php
Document Length:        11890379 bytes

Concurrency Level:      1
Time taken for tests:   43.040 seconds
Complete requests:      500
Failed requests:        0
Total transferred:      5945304500 bytes
HTML transferred:       5945189500 bytes
Requests per second:    11.62 [#/sec] (mean)
Time per request:       86.079 [ms] (mean)
Time per request:       86.079 [ms] (mean, across all concurrent requests)
Transfer rate:          134897.93 [Kbytes/sec] received

Connection Times (ms)
              min  mean[+/-sd] median   max
Connect:        0    0   0.0      0       0
Processing:    85   86   2.1     86     132
Waiting:        3    3   0.8      3      21
Total:         85   86   2.2     86     132

Percentage of the requests served within a certain time (ms)
  50%     86
  66%     86
  75%     86
  80%     86
  90%     86
  95%     87
  98%     87
  99%     90
 100%    132 (longest request)
```

## Compare the results

As you can see, our second test shows a significant slowdown. This is visible right away in the *Requests per second* going from ~80 to ~11. This tells us something is going on, and we should investigate. Looking at the *Connection times* table, we can see an increase in the request's *processing* time. As a result, we can conclude that our new code slows down the site. Of course this doesn't tell you specifically *why* the code is slow, just that the processing (executing PHP code) is taking longer.

In this case, it’s correct. For emulation of this scenario, we put a long loop in the *index.php* file before the request section, as shown below:

```
/**
 * @file
 * The PHP page that serves all page requests on a Drupal installation.
 *
 * All Drupal code is released under the GNU General Public License.
 * See COPYRIGHT.txt and LICENSE.txt files in the "core" directory.
 */

use Drupal\Core\DrupalKernel;
use Symfony\Component\HttpFoundation\Request;

$autoloader = require_once 'autoload.php';

$kernel = new DrupalKernel('prod', $autoloader);

// Long slow loop for testing.
$num = 1000000;
for ($i = 0; $i < $num; $i++) {
    var_dump($i);
}

$request = Request::createFromGlobals();
$response = $kernel->handle($request);
$response->send();

$kernel->terminate($request, $response);
```

You will probably get a less drastic difference in the results in real-world scenarios. When the difference is insignificant and tests are inconclusive, you should also add or subtract deviation values to understand how different the total mean values are between 2 test results. If you are getting similar values, try increasing the number of requests.

## Recap

Apache Bench (`ab`) is an easy to use profiling and benchmarking tool that is part of the Apache installation. It doesn't require any particular setup or advanced knowledge of profiling and benchmarking concepts. It is a quick way to test the performance of your Drupal site before and after making changes to the code. Apache Bench runs with one command that takes a set of options and the page URL. It produces results that show time per request, waiting time and standard deviation. It can be used to understand the impact of any new code introduced to your Drupal installation.

## Further your understanding

- Try passing other options to the command -- what changed in the output?
- Try increasing the concurrency value. How different are the results? Why?

## Additional resources

- [Apache Bench documentation](https://httpd.apache.org/docs/trunk/programs/ab.html) (apache.org)
- [Load Testing Your Site with Siege](https://drupalize.me/blog/201507/load-testing-your-site-siege) (Drupalize.Me)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Overview: Benchmarking and Performance Budgets](/tutorial/overview-benchmarking-and-performance-budgets?p=3091)

Next
[Overview: New Relic as a Drupal Performance Monitor](/tutorial/overview-new-relic-drupal-performance-monitor?p=3091)

Clear History

Ask Drupalize.Me AI

close
---
title: "Reset Vendor Status with Cron"
url: "https://drupalize.me/tutorial/reset-vendor-status-cron?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Reset Vendor Status with Cron

## Content

Learn how to use a cron job combined with an entity query to reset the attending status of vendor nodes every week. This will ensure that the vendor entity data only contains current check-ins.

In this tutorial, we'll:

- Implement `hook_cron()` within the Anytown module.
- Use an entity query to identify all vendor nodes requiring updates.
- Apply Entity API methods to reset each vendor's attending status.

By the end, you'll know how to execute an entity query, retrieve nodes, and update their status with cron.

## Goal

Automatically update the *attending* status for all vendors at the beginning of the week.

## Prerequisites

- [Concept: Entity Queries](https://drupalize.me/tutorial/concept-entity-queries)
- [Update an Entity When The Form Is Submitted](https://drupalize.me/tutorial/update-entity-when-form-submitted)
- [Implement hook\_help()](https://drupalize.me/tutorial/implement-hookhelp)
- [Configuring Cron Maintenance Tasks](https://drupalize.me/tutorial/user-guide/security-cron)

## Video tutorial

Sprout Video

## Reset the "attending" status each week

To ensure vendors actively confirm their attendance each week, we'll reset their status to *not attending* early every week.

Implementing `hook_cron()` allows us to run this reset automatically, based on the site's cron configuration. We'll check a state variable to determine the reset's timing and use an entity query to identify and update all relevant vendor nodes.

### Implement `hook_cron()`

**Add** the following to *src/Hook/AnytownCron.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

use Drupal\Core\Hook\Attribute\Hook;

class AnytownCron {

  /**
   * Implements hook_cron().
   */
  #[Hook('cron')]
  public function cron() {
    // Get the current time.
    $current_time = new \DateTime();
    // Get the last time this was run.
    $last_run_timestamp = \Drupal::state()->get('anytown.last_cron_weekly_run', 0);
    $last_run = new \DateTime();
    if ($last_run_timestamp) {
      $last_run->setTimestamp($last_run_timestamp);
    }

    // If it's been more than 6 days since that last run, we're good, and if today
    // is Monday or later, we're good.
    $interval = $last_run->diff($current_time);

    // 1==1 is so that this will execute every time cron runs for demonstration
    // purposes.
    if (1 == 1 || $interval->days > 6 && $current_time->format('w') >= 1) {
      // Perform the weekly task.
      $this->clearVendorStatus();

      // Update the last run time.
      \Drupal::state()->set('anytown.last_cron_weekly_run', $current_time->getTimestamp());
    }
  }

  /**
   * Reset field_vendor_attending to FALSE for all vendor nodes.
   */
  public function clearVendorStatus() {
    $query = \Drupal::entityTypeManager()->getStorage('node')->getQuery()
      // Specifying an accessCheck of TRUE|FALSE is required.
      // Return all nodes, regardless of the users access. This is safe here
      // because we want cron (the system) to update them all.
      ->accessCheck(FALSE)
      // Filter by the 'vendor' bundle.
      ->condition('type', 'vendor')
      // Filter nodes where 'field_attending' is TRUE.
      ->condition('field_vendor_attending', TRUE);

    // Execute the query to get an array of node IDs that match the conditions.
    $node_ids = $query->execute();

    // Load the node entities.
    $nodes = \Drupal::entityTypeManager()->getStorage('node')->loadMultiple($node_ids);

    // Now you can work with the $nodes array.
    /** @var \Drupal\node\NodeInterface $node */
    foreach ($nodes as $node) {
      $node->set('field_vendor_attending', FALSE);
      $node->save();
    }
  }

}
```

In `hook_cron()`, we check if a week has passed since the last reset, then call the `clearVendorStatus()` helper method to reset all vendors' statuses. This method queries for all vendor type nodes with `field_vendor_attending` set to `TRUE`, then updates them.

Alternative function based implementation of `hook\_cron()` for Drupal 10 and earlier.

**Add** the following to *anytown.module*:

```
/**
 * Implements hook_cron().
 */
function anytown_cron() {
  // Get the current time.
  $current_time = new \DateTime();
  // Get the last time this was run.
  $last_run_timestamp = \Drupal::state()->get('anytown.last_cron_weekly_run', 0);
  $last_run = new \DateTime();
  if ($last_run_timestamp) {
  $last_run->setTimestamp($last_run_timestamp);
  }

  // If it's been more than 6 days since that last run, we're good, and if today
  // is Monday or later, we're good.
  $interval = $last_run->diff($current_time);

  // 1==1 is so that this will execute every time cron runs for demonstration
  // purposes.
  if (1 == 1 || $interval->days > 6 && $current_time->format('w') >= 1) {
    // Perform the weekly task.
    _anytown_clear_vendor_status();

    // Update the last run time.
    \Drupal::state()->set('anytown.last_cron_weekly_run', $current_time->getTimestamp());
  }
}

/**
 * Reset field_vendor_attending to FALSE for all vendor nodes.
 */
function _anytown_clear_vendor_status() : void {
  $query = \Drupal::entityTypeManager()->getStorage('node')->getQuery()
    // Specifying an accessCheck of TRUE|FALSE is required.
    // Return all nodes, regardless of the users access. This is safe here
    // because we want cron (the system) to update them all.
    ->accessCheck(FALSE)
  // Filter by the 'vendor' bundle.
    ->condition('type', 'vendor')
  // Filter nodes where 'field_attending' is TRUE.
    ->condition('field_vendor_attending', TRUE);

  // Execute the query to get an array of node IDs that match the conditions.
  $node_ids = $query->execute();

  // Load the node entities.
  $nodes = \Drupal::entityTypeManager()->getStorage('node')->loadMultiple($node_ids);

  // Now you can work with the $nodes array.
  /** @var \Drupal\node\NodeInterface $node */
  foreach ($nodes as $node) {
    $node->set('field_vendor_attending', FALSE);
    $node->save();
  }
}
```

### Clear the cache

We added a new hook implementation, so we need to [clear the cache](https://drupalize.me/tutorial/clear-drupals-cache) to make sure Drupal finds it.

### Verify it works

After setting one or more *Vendor* nodes' attending status to TRUE, run `drush cron`. Verify the vendor's attending status reset after the cron run process is complete.

## Recap

In this tutorial, we used cron and entity queries to reset vendor statuses weekly. This ensures that our vendor attendance data is up-to-date with an automated process, so that no one needs to manually update vendor attendance status every week. We implemented `hook_cron()` and crafted a query to find and update vendor nodes as needed.

## Further your understanding

- How would you encapsulate the vendor status reset logic into a service?
- Explore using `EntityStorageInterface::loadByProperties()` as an alternative in `_anytown_clear_vendor_status()`.

## Additional resources

- [Find Data with EntityQuery](https://drupalize.me/tutorial/find-data-entityquery) (Drupalize.Me)
- [`hook_cron()` documentation](https://api.drupal.org/api/drupal/core%21core.api.php/function/hook_cron/)
- [`QueryInterface` documentation](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21Query%21QueryInterface.php/interface/QueryInterface/) (api.drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Concept: Entity Queries](/tutorial/concept-entity-queries?p=3243)

Next
[Display a List of Vendors](/tutorial/display-list-vendors?p=3243)

Clear History

Ask Drupalize.Me AI

close
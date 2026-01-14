---
title: "Set up Migrate Demo Site and Source Data"
url: "https://drupalize.me/tutorial/set-migrate-demo-site-and-source-data?p=3115"
guide: "[[learn-migrate-drupal]]"
order: 56
---

# Set up Migrate Demo Site and Source Data

## Content

Before we can learn to write a custom migration, we need some sample data and a destination site for that data.

In this tutorial we'll obtain some source data to work with and configure our Drupal destination site by creating the necessary content types and fields to accommodate the source data. Then we'll look at the data that we'll be importing and start to formulate a migration plan.

By the end of this tutorial you'll have some source data and an empty but configured destination Drupal site ready for data import.

## Goal

Set up an example database of baseball statistics to use as a source for developing a custom migration.

## Prerequisites

- None

## Quickstart

If you use DDEV you can use our [pre-configured environment](https://github.com/DrupalizeMe/migrate-10x) to get started.

## Watch: Set up Migrate Demo Site and Source Data

Sprout Video

## Get the source data

We’ll use some sample data that we found which involves baseball statistics. The data is Creative Commons-licensed, so we can go ahead and make use of it here.

The data was retrieved from: <http://www.seanlahman.com/baseball-archive/statistics/>.

**Note:** As of May 2023 that site is no longer available, but the data is still published in various other locations. You can find it in the GitHub repo linked below, or by searching the web for "Lahman baseball database sql".

GitHub repo with a relatively current dataset: <https://github.com/WebucatorTraining/lahman-baseball-mysql/>

Import the data into MySQL on your development environment, so you have a place to test things out.

### Download the data

Download the file containing the SQL data to import: <https://raw.githubusercontent.com/WebucatorTraining/lahman-baseball-mysql/master/updated-lahman-mysql.sql>

### Import into a new MySQL database

Import the *updated-lahman-mysql.sql* file using a tool of your choice.

This file contains the following SQL which will automatically create and use a database named `lahmansbaseballdb`.

```
CREATE DATABASE  IF NOT EXISTS lahmansbaseballdb;
USE lahmansbaseballdb;
```

Open the file and edit that bit if you want to use a different name.

## Inspect the source data

Take a moment to familiarize yourself with the structure and data of the *people*, *appearances*, and *teams* tables. These are the 3 we're concerned with in this example.

- The *people* table contains information about players including their name and some profile information.
- The *teams* table contains team names.
- The *appearances* table contains a record for each time a player appeared in a game along with what team they were playing for. (We can use this to link players to teams.)

Example row from *people* table, shows player name and profile data:

| playerID | birthYear | birthMonth | birthDay | birthCountry | birthState | birthCity | deathYear | deathMonth | deathDay | deathCountry | deathState | deathCity | nameFirst | nameLast | nameGiven | weight | height | bats | throws | debut | finalGame | retroID | bbrefID |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| aaronto01 | 1939 | 8 | 5 | USA | AL | Mobile | 1984 | 8 | 16 | USA | GA | Atlanta | Tommie | Aaron | Tommie Lee | 190 | 75 | R | R | 1962-04-10 | 1971-09-26 | aarot101 | aaronto01 |

Example row from the *teams* table, shows team name and data:

| yearID | lgID | teamID | franchID | divID | Rank | G | Ghome | W | L | DivWin | WCWin | LgWin | WSWin | R | AB | H | 2B | 3B | HR | BB | SO | SB | CS | HBP | SF | RA | ER | ERA | CG | SHO | SV | IPouts | HA | HRA | BBA | SOA | E | DP | FP | name | park | attendance | BPF | PPF | teamIDBR | teamIDlahman45 | teamIDretro |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1871 | NA | NY2 | NNA |  | 5 | 33 |  | 16 | 17 |  |  | N |  | 302 | 1404 | 403 | 43 | 21 | 1 | 33 | 15 | 46 |  |  |  | 313 | 121 | 3.72 | 32 | 1 | 0 | 879 | 373 | 7 | 42 | 22 | 227 |  | 0.83 | New York Mutuals | Union Grounds (Brooklyn) |  | 90 | 88 | NYU | NY2 | NY2 |

Example rows from *appearances* which contains one record for each year a player played, and which team they played for. Maps players to teams:

| yearID | teamID | lgID | playerID | G\_all | GS | G\_batting | G\_defense | G\_p | G\_c | G\_1b | G\_2b | G\_3b | G\_ss | G\_lf | G\_cf | G\_rf | G\_of | G\_dh | G\_ph | G\_pr |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2010 | SEA | AL | aardsda01 | 53 | 0 | 4 | 53 | 53 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2012 | NYA | AL | aardsda01 | 1 | 0 | 0 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2013 | NYN | NL | aardsda01 | 43 | 0 | 41 | 43 | 43 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2015 | ATL | NL | aardsda01 | 33 | 0 | 30 | 33 | 33 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

## Set up a Drupal destination site

Start by installing a fresh copy of [the latest version of Drupal](https://www.drupal.org/node/3098327). And then create two new content types listed below. Unlike when you perform a [Drupal-to-Drupal migration](https://drupalize.me/tutorial/prepare-drupal-drupal-migration), when migrating from a custom data source you'll need to create the content types ahead of time. These content types are where we'll import our data.

Create a content type named *Player* (machine name: `player`), with the following fields:

| Field name | Machine Name | Type |
| --- | --- | --- |
| Name | title | Node module element |
| Player ID | field\_player\_id | Text (plain) |
| Given name | field\_player\_given\_name | Text (plain) |
| Weight | field\_player\_weight | Number (integer) |
| Height | field\_player\_height | Number (integer) |
| Throws | field\_player\_throws | List (text) - possible values are "R,Right, L,Left" |
| Bats | field\_player\_bats | List (text) - possible values are "R,Right, L,Left" |
| Birth | field\_player\_birth | Date - date only |
| Death | field\_player\_death | Date - date only |
| Notes | field\_player\_notes | Text (plain, long) |
| Teams | field\_player\_teams | Entity Reference - multiple value, references Team content type |

Create a content type named *Team* (machine name: `team`), with the following fields:

| Field name | Machine Name | Type |
| --- | --- | --- |
| Team Name | title | Node module element |
| Park | field\_team\_park | Text |

Note: You'll need to edit the machine names of the fields when creating them if you want to match exactly what is above. This isn't required though, as long as you adjust later code samples to use whatever machine names you used.

## Tell your destination site where the source data lives

We need to tell our destination Drupal site where to find the data that it's going to import. We do this by updating our *sites/default/settings.php* file and adding a new database connection configuration array that the migration system will find and make use of.

Update your *settings.php* and add a database connection configuration for the database where your source data lives. This could be the same host, or an external host. For more about how to define a database connection configuration look for the related docblock in your *settings.php* file.

The important part is to name your configuration `$databases['migrate']['default']` so that the SQL Source can find it easily.

Example from our *settings.php*:

```
// Note the key 'migrate' here is important.
$databases['migrate']['default'] = array (
  // The database that contains the source data we're going to import.
  'database' => 'lahmansbaseballdb',
  'username' => 'root',
  'password' => 'root',
  'prefix' => '',
  'host' => 'localhost',
  'port' => '3306',
  'namespace' => 'Drupal\\Core\\Database\\Driver\\mysql',
  'driver' => 'mysql',
);
```

## Recap

In this tutorial we:

- Downloaded an SQL file full of baseball player data to use as sample source data and imported it into a new MySQL database
- Took a look at that data to get an idea of what we're working with
- Set up a Drupal destination site with two new content types -- player and team -- into which we'll import data

## Further your understanding

- The fields we created for our content type are not an exact match for the fields in the source data. Can you create a list that shows how you might map source fields to their Drupal equivalent?

## Additional resources

- [Baseball Statistics example data](http://www.seanlahman.com/baseball-archive/statistics/) (seanlahman.com)
- [Change record: Upgrade paths for Drupal 8 site from before Drupal 8.8.0 have been removed from Drupal 9](https://www.drupal.org/node/3098327) (drupal.org/list-changes)

Was this helpful?

Yes

No

Any additional feedback?

Next
[Source Plugins](/tutorial/source-plugins?p=3115)

Clear History

Ask Drupalize.Me AI

close
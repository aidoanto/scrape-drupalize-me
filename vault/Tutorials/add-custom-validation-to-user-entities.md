---
title: "Add Custom Validation to User Entities"
url: "https://drupalize.me/tutorial/add-custom-validation-user-entities?p=3243"
guide: "[[drupal-module-developer-guide]]"
---

# Add Custom Validation to User Entities

## Content

Validation happens whenever an entity is created or updated, ensuring data integrity across form submissions, JSON:API requests, and direct entity object manipulation. Drupal's Entity Validation API, consists of constraints, validators, and their integration. As module developer, we'll use this API to enforce custom rules about what constitutes valid data.

In this tutorial, we'll:

- Learn about the roles of constraints and validators within Drupal's validation system.
- See how to create and integrate custom validation rules.
- Apply custom validation to an entity type that enforces specific data integrity rules.

By the end of this tutorial, you should be able to define new constraints and validators, and associate them with entity types.

## Goal

Implement a custom entity validation rule to prevent the use of "anytown" as a username.

## Prerequisites

- [Implement a Block Plugin](https://drupalize.me/tutorial/implement-block-plugin)
- [Implement hook\_help()](https://drupalize.me/tutorial/implement-hookhelp)

## Video tutorial

Sprout Video

## Understanding entity validation

In [Alter the User Registration Form](https://drupalize.me/tutorial/alter-user-registration-form) we added logic to the user registration form that validates that a user account cannot have the name "anytown". That logic only applies to the registration form and not all the other ways that a user entity could be created. To make our validation more robust we should apply it at the entity creation level.

Drupal's Entity Validation API ensures consistent validation across entity CRUD operations, regardless of the interaction method. It uses *constraints* (rules) and *validators* (logic) to validate data and maintain data integrity.

- **Constraints**: Rules or conditions used to evaluate whether a particular piece of data is valid or not. They are defined as Drupal plugins.
- **Validators**: Code responsible for doing the actual comparison or evaluation. Each validator is associated with a specific constraint.

Let's add some custom validation logic in the *anytown* module that applies to the username field .

### Define a constraint plugin

Constraints are defined as plugins with a `\Drupal\Core\Validation\Attribute\Constraint` attribute, and live in the `Drupal\MODULE_NAME\Plugin\Validation\Constraint` namespace. They extend `\Symfony\Component\Validator\Constraint`, or one of the existing constraint classes like `\Symfony\Component\Validator\Constraints\EqualTo`.

Create *anytown/src/Plugin/Validation/Constraint/UserNameConstraint.php*:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Plugin\Validation\Constraint;

use Drupal\Core\Validation\Attribute\Constraint;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Symfony\Component\Validator\Constraints\NotEqualTo;

/**
 * Provides a UserNameConstraint constraint.
 *
 * @see https://www.drupal.org/node/2015723.
 */
#[Constraint(
  id: 'AnytownUserNameConstraint',
  label: new TranslatableMarkup('User name cannot be anytown', [], ['context' => 'Validation'])
)]
final class UserNameConstraint extends NotEqualTo {

  /**
   * Message to display for invalid username.
   *
   * @var string
   */
  public string $message = 'Invalid user name. Cannot use "anytown" as the user name.';

  /**
   * The value to compare.
   *
   * @var string
   */
  public mixed $value = 'anytown';
}
```

This code creates a new constraint plugin with the ID, `AnytownUserNameConstraint`. Constraint IDs should be prefixed with the module name to avoid collisions.

### Implement the validator class

Validators handle the logic for constraint verification, typically by defining a `validate()` method.

Every constraint plugin needs an associated validator which contains the custom validation logic. By default, the 2 are associated based on a naming convention. The validator class should be the fully qualified name of the constraint class suffixed with "Validator". You can override this behavior by using the `validatedBy()` method.

Our **constraint** is `Drupal\anytown\Plugin\Validation\Constraint\UserNameConstraint`, so we'll name our **validator**, `Drupal\anytown\Plugin\Validation\Constraint\UserNameConstraintValidator`. Note the addition of **Validator** in the class name.

Validators:

- Extend `\Symfony\Component\Validator\ConstraintValidator`.
- Implement `\Symfony\Component\Validator\ConstraintValidatorInterface`. In most cases this will require adding a custom `validate()` method.

Create the file *anytown/src/Plugin/Validation/Constraint/UserNameConstraintValidator.php* with the following code:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Plugin\Validation\Constraint;

use Drupal\user\UserInterface;
use Symfony\Component\Validator\Constraint;
use Symfony\Component\Validator\ConstraintValidator;

/**
 * Validates the UserNameConstraint constraint.
 */
final class UserNameConstraintValidator extends ConstraintValidator {

  /**
   * {@inheritdoc}
   */
  public function validate(mixed $value, Constraint $constraint): void {
    if (!$value instanceof UserInterface) {
      throw new \InvalidArgumentException(
        sprintf('The validated value must be an instance of \Drupal\user\UserInterface, %s was given.', get_debug_type($value))
      );
    }

    /** @var \Drupal\user\UserInterface $value */
    if ($value->getAccountName() === 'anytown') {
      $this->context->buildViolation($constraint->message)
        ->atPath('name')
        ->addViolation();
    }
  }

}
```

This validator:

- Verifies that the entity it's being asked to validate is a `User` entity.
- Checks the value of the name field, and sets a violation if the name is `anytown`.

### Associate the constraint with an entity

Use `hook_entity_type_alter()` to associate the new constraint with the `User` entity type.

Create the file, *src/Hook/AnytownEntityHooks.php*, with the following content:

```
<?php

declare(strict_types=1);

namespace Drupal\anytown\Hook;

use Drupal\Core\Hook\Attribute\Hook;

class AnytownEntityHooks {

  /**
   * Implements hook_entity_type_alter().
   */
  #[Hook('entity_type_alter')]
  public function entityTypeAlter(array &$entity_types) : void {
    // Add validation constraint to user entities.
    $entity_types['user']->addConstraint('AnytownUserNameConstraint');
  }

}
```

This code attaches the new `AnytownUserNameConstraint` plugin to the existing `user` entity type.

Alternatively use a function based hook implementation for Drupal 10 and earlier.

For Drupal 10 and earlier, update the *anytown.module* file, and add the following hook implementation:

```
/**
 * Implements hook_entity_type_alter().
 */
function anytown_entity_type_alter(array &$entity_types) {
  // Add validation constraint to user entities.
  $entity_types['user']->addConstraint('AnytownUserNameConstraint');
}
```

### Verify it works

To verify it works create a new user without using the user registration form. In the *Manage* administration menu navigate to *People* > *Add user* (*admin/people/create*). Fill out the form to add a new user, try making the *Name* "anytown". Submit the form and verify that an error is returned.

Example:

Image

![Screenshot of add user form with error returned](../assets/images/data--entity-validation_user-add-form.png)

## Recap

This tutorial introduced Drupal's Entity Validation API, showing how to create and apply custom validation rules to entities. We implemented a constraint preventing "anytown" as a username, illustrating the API's ability to enforce data integrity universally.

## Further your understanding

- Why should we apply validation at the Entity API level rather than just at the Form API level?
- Discuss the benefits of separating constraint definitions from validation logic.

## Additional resources

- [Entity Validation API](https://drupalize.me/tutorial/entity-validation-api) (Drupalize.Me)
- [Entity Validation API overview](https://www.drupal.org/docs/drupal-apis/entity-api/entity-validation-api/entity-validation-api-overview) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Use Parameter Upcasting for Entities in Routes](/tutorial/use-parameter-upcasting-entities-routes?p=3243)

Next
[Concept: Entity Queries](/tutorial/concept-entity-queries?p=3243)

Clear History

Ask Drupalize.Me AI

close
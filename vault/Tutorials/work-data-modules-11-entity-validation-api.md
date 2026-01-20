---
title: "Entity Validation API"
url: "https://drupalize.me/tutorial/entity-validation-api?p=2607"
guide: "[[work-data-modules]]"
order: 11
---

# Entity Validation API

## Content

Drupal includes the [Symfony Validator component](http://symfony.com/doc/2.8/components/validator.html), and provides an Entity Validation API to assist in validating the values of fields on an entity. By using the Entity Validation API you can ensure that you're validation logic is applied to Entity CRUD operations regardless of how they are triggered. Whether editing an Entity via a Form API form, or creating a new Entity via the REST API, the same validation code will be used.

Using the Entity Validation API in order to validate the value of a field on an entity requires:

- Defining (or choosing) a constraint plugin
- Defining (or choosing) a validation plugin
- Adding the constraint to the field definition

In this tutorial, we'll look at how this Validation API works and how it can be used in custom code to ensure our entities have properly constructed values. We'll look at how this validation works in Drupal core and how we can add our own additional constraints. We'll also see how to work with the error messages returned from the validator when our entity doesn't pass validation.

## Goal

- Learn how the Entity Validation API works, both in specifying constraints for our fields and as a consumer trying to validate data.

## Prerequisites

- [What Are Plugins?](https://drupalize.me/tutorial/what-are-plugins)
- [Implement a Plugin of Any Type](https://drupalize.me/tutorial/implement-plugin-any-type)
- [Entity API Implementation Basics](https://drupalize.me/tutorial/entity-api-implementation-basics)
- [Create a Custom Content Entity](https://drupalize.me/tutorial/create-custom-content-entity)

## The Symfony validator component

There are two main pieces required to understand how Symfony's validator component works: constraints and validators. *Constraints* are the rules or conditions used to evaluate whether a particular piece of data is valid or not. *Validators* are the code responsible for doing the actual comparison or evaluation. You can read more about the [Symfony validator component](https://symfony.com/doc/current/components/validator.html) and how [Symfony handles validation](http://symfony.com/doc/2.8/validation.html) in the Symfony documentation.

## Constraints provided by Drupal core

Drupal's implementation of the validator component requires the implementation of a validation plugin. The validation plugins provided by Drupal core can be found in `/core/lib/Drupal/Core/Validation`. You can see from the code in the `Attribute/Constraint.php` file in this directory that implementations of validation plugins will have a constraint attribute. These validation constraint attributes consist of an `id`, a `label`, and an array of `DataTypes` that the validation is able to evaluate.

We can see the validation and constraint implementations included in Drupal core in more detail by looking at the `/core/lib/Drupal/Core/Validation/Plugin/Validation/Constraint` directory. Here we will find several implementations of constraint and validation plugins that can be used elsewhere in the codebase.

Symfony validation components are composed of both a constraint and a validator; both of these pieces are required.

In particular, let's take a closer look at how the `UniqueFieldConstraint` and `UniqueFieldValueValidator` combination can help us determine if our data is indeed unique.

Drupal knows about this (or any) constraint thanks to the plugin's attributes. The constraint for checking a field's uniqueness can be found in `/core/lib/Drupal/Core/Validation/Plugin/Validation/Constraint/UniqueFieldConstraint.php`. This file contains the `Constraint` attribute and class that provides the error message used when this validation fails and a class namespace that can be used to actually validate this constraint.

```
namespace Drupal\Core\Validation\Plugin\Validation\Constraint;

use Drupal\Core\Validation\Attribute\Constraint;
use Drupal\Core\StringTranslation\TranslatableMarkup;
use Symfony\Component\Validator\Constraint;

/**
 * Checks if an entity field has a unique value.
 */
 #[Constraint(
  id: "UniqueField",
  label: new TranslatableMarkup("Unique field constraint", [], "Validation"),
 )]
class UniqueFieldConstraint extends Constraint {

  public $message = 'A @entity_type with @field_name %value already exists.';

  /**
   * {@inheritdoc}
   */
  public function validatedBy() {
    return '\Drupal\Core\Validation\Plugin\Validation\Constraint\UniqueFieldValueValidator';
  }
}
```

The validator for this constraint can be found in a class within the `UniqueFieldValueValidator.php` file (also in this directory). This file includes one method `validate()` that is responsible for doing the actual work to make sure the value being validated matches the provided constraints. This is done by retrieving some metadata about the entity we're validating and then attempting to query for an entity with a particular field value. If the query returns any matches for a particular field, then we can say that the field value being validated is not unique. If this happens, the message provided by our constraint class is returned (along with some additional metadata). It's worth noting that the values for this message may contain placeholders that represent additional dynamic data relevant to the particular details of the entity constraint being evaluated.

```
namespace Drupal\Core\Validation\Plugin\Validation\Constraint;

use Drupal\Component\Utility\Unicode;
use Symfony\Component\Validator\Constraint;
use Symfony\Component\Validator\ConstraintValidator;

/**
 * Validates that a field is unique for the given entity type.
 */
class UniqueFieldValueValidator extends ConstraintValidator {

  /**
   * {@inheritdoc}
   */
  public function validate($items, Constraint $constraint) {
    if (!$item = $items->first()) {
      return;
    }
    $field_name = $items->getFieldDefinition()->getName();
    /** @var \Drupal\Core\Entity\EntityInterface $entity */
    $entity = $items->getEntity();
    $entity_type_id = $entity->getEntityTypeId();
    $id_key = $entity->getEntityType()->getKey('id');

    $value_taken = (bool) \Drupal::entityQuery($entity_type_id)
      // We want to check all entities, not just those that the current user
      // can view.
      ->accessCheck(FALSE)
      // The id could be NULL, so we cast it to 0 in that case.
      ->condition($id_key, (int) $items->getEntity()->id(), '<>')
      ->condition($field_name, $item->value)
      ->range(0, 1)
      ->count()
      ->execute();

    if ($value_taken) {
      $this->context->addViolation($constraint->message, [
        '%value' => $item->value,
        '@entity_type' => $entity->getEntityType()->getLowercaseLabel(),
        '@field_name' => Unicode::strtolower($items->getFieldDefinition()->getLabel()),
      ]);
    }
  }

}
```

## Validation in action

Now that we've seen how constraints and validators are constructed, let's see how they can be used in custom code to both apply constraints to custom entities and validate any user-submitted information. Constraints can be added to custom entities or to those that are already provided by other modules. Adding a constraint to a custom entity includes a call to the `->addConstraint()` method when building the base field definitions for an entity. This `->addConstraint()` method is passed the name of the plugin ID for the constraint. The `User` entity type defines several constraints with this technique. A portion of this from `/core/modules/user/src/Entity/User.php` can be seen here:

```
public static function baseFieldDefinitions(EntityTypeInterface $entity_type) {
...

    $fields['mail'] = BaseFieldDefinition::create('email')
      ->setLabel(t('Email'))
      ->setDescription(t('The email of this user.'))
      ->setDefaultValue('')
      ->addConstraint('UserMailUnique')
      ->addConstraint('UserMailRequired')
      ->addConstraint('ProtectedUserField');

...
}
```

This code adds 3 distinct constraints to the email address of a user entity. They make sure the email address is unique, required and protected.

If you'd like to add validation to an existing entity provided by another module, you need to alter the field bundle information for that entity type. This can be done by implementing [`hook_entity_bundle_field_info_alter`](https://api.drupal.org/api/drupal/core%21lib%21Drupal%21Core%21Entity%21entity.api.php/function/hook_entity_bundle_field_info_alter/). This hook can be used to select a particular entity type (and bundle) and make modifications to a particular field's definition. Let's say we have a content type with the machine name `jackpot_winner` and that this content type has an integer field `random_number`. We can add a constraint to ensure that field has a unique value by adding the `unique_integer` constraint to that field definition by implementing this hook.

```
function hook_entity_bundle_field_info_alter(&$fields, \Drupal\Core\Entity\EntityTypeInterface $entity_type, $bundle) {
  if ($entity_type->id() == 'node' && $bundle == 'jackpot_winner' && !empty($fields['random_number'])) {
    // Alter the mymodule_text field to use a custom class.
    $fields['random_number']->addConstraint('unique_integer');
  }
}
```

Once we've established the constraints that apply to our entities, elsewhere in our code we may want to validate data before attempting to save or update an entity. We can do this on our entities, fields, or any typed data object by calling the `validate()` method. This method will return any violation messages that we need to fix before our data will save properly.

```
// You can validate entities as a whole
$violations = $entity->validate();
// Or just a particular field
//$violations = $entity->field_name->validate();

// Validation failed.
if ($violations->count() > 0) {
    // Display an error message helping the user fix the problem.
    // These will be available indivudally in the $violations array
    // and can be accessed by $violations[0]->getMessage() for each violation.
}
```

## Recap

In this tutorial, we took a look at how Drupal leverages the validator component from Symfony to make it easier to ensure our data is properly structured. We learned about the 2 main components that make up this validation process: constraints and validators. We saw how Drupal's implementation of these components are created, and where some of them can be found. We also saw how constraints can be added to entity and field definitions and how our custom code can use validation.

## Further your understanding

- What other constraints and validators are provided by Drupal core? Do any modules provide additional constraints or validatators apart from the ones in the `/core/lib/Drupal/Core/Validation` directory?
- What other types of core entities provide constraints on their base fields?
- What does the protected user field constraint actually do?

## Additional resources

- [Symfony validator](http://symfony.com/doc/2.8/validation.html) (symfony.com)
- [Entity Validation API overview](https://www.drupal.org/docs/drupal-apis/entity-api/entity-validation-api/entity-validation-api-overview) (Drupal.org)

Was this helpful?

Yes

No

Any additional feedback?

Previous
[Using Entity Bundle Classes for Site-Specific Features](/tutorial/using-entity-bundle-classes-site-specific-features?p=2607)

Next
[Entity Access Control](/tutorial/entity-access-control?p=2607)

Clear History

Ask Drupalize.Me AI

close
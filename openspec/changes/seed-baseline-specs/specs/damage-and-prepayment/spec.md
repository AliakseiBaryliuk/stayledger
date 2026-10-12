# Spec Delta

## Purpose

Records damaged items and reduces prepayment by the damage amount. Owned by the `damage-and-prepayment` mini-scenario.

## ADDED Requirements

### Requirement: Record damaged items
The system SHALL store a record of each damaged item.

#### Scenario: Damage is stored
- **WHEN** an item is reported as damaged
- **THEN** the system keeps a stored record of that damaged item

#### Scenario: No damage reported
- **WHEN** no items are reported as damaged
- **THEN** the system MUST NOT store a damaged-item record

### Requirement: Reduce prepayment by damage amount
The system SHALL reduce the prepayment by the recorded damage amount.

#### Scenario: Prepayment reduced after damage
- **WHEN** damaged items totaling an amount are recorded against a rental that has a prepayment
- **THEN** the prepayment is reduced by that amount

#### Scenario: Unchanged prepayment without damage
- **WHEN** no damage amount is recorded
- **THEN** the prepayment MUST NOT be reduced

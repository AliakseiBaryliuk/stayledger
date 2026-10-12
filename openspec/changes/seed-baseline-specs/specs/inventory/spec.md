# Spec Delta

## Purpose

Tracks inventory for rentals. Owned by the `inventory` mini-scenario.

## ADDED Requirements

### Requirement: Track rental inventory
The system SHALL keep a record of inventory items associated with rentals.

#### Scenario: Inventory item is recorded
- **WHEN** an inventory item is associated with a rental
- **THEN** the system stores that item as part of rental inventory

#### Scenario: No inventory yet
- **WHEN** a rental has no associated inventory items
- **THEN** the inventory record for that rental is empty

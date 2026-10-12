# Spec Delta

## Purpose

Accepts client rental orders submitted through Telegram. Owned by the `telegram-order-intake` mini-scenario.

## ADDED Requirements

### Requirement: Accept Telegram rental orders
The system SHALL accept a rental order that a client submits through Telegram.

#### Scenario: Valid order is accepted
- **WHEN** a client submits a complete rental order through Telegram
- **THEN** the system records the order for further processing

#### Scenario: Incomplete order is not accepted
- **WHEN** a client submits an order through Telegram that is missing required details
- **THEN** the system MUST NOT record it as an accepted rental order

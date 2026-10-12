# Spec Delta

## Purpose

Tracks apartment booking dates. Owned by the `booking-calendar` mini-scenario.

## ADDED Requirements

### Requirement: Track apartment booking dates
The system SHALL record the dates on which each apartment is booked.

#### Scenario: Booking dates are stored
- **WHEN** an apartment is booked for a date range
- **THEN** those dates are visible on that apartment's booking calendar

#### Scenario: Empty calendar
- **WHEN** an apartment has no bookings
- **THEN** its booking calendar shows no booked dates

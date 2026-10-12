# Proposal

## Why

StayLedger has product rules (Telegram order intake, AI replies, booking calendar, inventory, damage and prepayment) only in agent context, so they are not versioned capabilities. This change records that intended behavior as baseline OpenSpec specs before implementation starts inventing it.

## What Changes

- Add five baseline capabilities that match the mini-scenarios in `docs/architecture.md`.
- Capture current intended behavior only: no new product rules beyond what was previously listed as core logic.
- No application code, APIs, or persistence in this change.

Out of scope: implementing mini-scenarios, adapters, Telegram webhook wiring, LLM prompts, schema/migrations, and any change to how prepayment is calculated beyond documenting the existing rule.

## Capabilities

### New Capabilities

- `telegram-order-intake`: Clients submit rental orders through Telegram.
- `ai-client-replies`: The system replies to clients with AI-generated messages.
- `booking-calendar`: The system tracks apartment booking dates.
- `inventory`: The system tracks inventory for rentals.
- `damage-and-prepayment`: Damaged items are recorded and the prepayment is reduced by the damage amount.

### Modified Capabilities

- None. There are no main specs yet.

## Impact

- Affected mini-scenarios (documentation only): `telegram-order-intake`, `ai-client-replies`, `booking-calendar`, `inventory`, `damage-and-prepayment`.
- User-visible flow: none yet; this change does not ship runtime behavior.
- Money/prepayment: the `damage-and-prepayment` spec records that damaged items are stored and prepayment is reduced by the damage amount. No payment code changes.
- Implementation, tests, and package-info links happen in later changes that apply these capabilities.

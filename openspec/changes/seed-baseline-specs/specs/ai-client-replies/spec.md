# Spec Delta

## Purpose

Sends AI-generated replies to clients. Owned by the `ai-client-replies` mini-scenario.

## ADDED Requirements

### Requirement: Reply to clients with AI
The system SHALL send the client an AI-generated reply to their message.

#### Scenario: Successful reply
- **WHEN** a client message needs a reply and generation succeeds
- **THEN** the client receives that generated reply

#### Scenario: Generation failure
- **WHEN** a client message needs a reply and generation fails
- **THEN** the system MUST NOT send the client a fabricated successful reply

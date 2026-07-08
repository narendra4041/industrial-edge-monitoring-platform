# Functional Requirements

## Project Name

Industrial Edge Monitoring Platform

## 1. Device Management

### FR-001: Register Device

The system shall allow an administrator to register a new industrial device.

Required fields:

- device_id
- device_name
- device_type
- location
- manufacturer
- model
- firmware_version

Acceptance Criteria:

- device_id must be unique
- device is created with ACTIVE status by default
- duplicate device_id must return a validation error
- created_at and updated_at timestamps must be captured

### FR-002: View Device

The system shall allow authorized users to view device details.

Acceptance Criteria:

- user can fetch device by device_id
- unknown device_id returns 404
- response includes current device status

### FR-003: List Devices

The system shall allow authorized users to list all registered devices.

Acceptance Criteria:

- response supports pagination
- response supports filtering by status
- response supports filtering by device_type
- response supports filtering by location

### FR-004: Update Device

The system shall allow an administrator to update device metadata.

Acceptance Criteria:

- device_id cannot be changed
- allowed fields can be updated
- updated_at timestamp must be changed
- update should fail if device does not exist

### FR-005: Disable Device

The system shall allow an administrator to disable a device.

Acceptance Criteria:

- disabled device cannot send telemetry
- device record should not be physically deleted
- status should be changed to DISABLED
- audit log should capture the action

---

## 2. Telemetry Ingestion

### FR-006: Ingest Telemetry

The system shall allow a registered active device to send telemetry data.

Required fields:

- event_id
- device_id
- timestamp
- temperature
- pressure
- vibration
- flow_rate
- status

Acceptance Criteria:

- event_id must be unique
- device_id must exist
- device must be ACTIVE
- timestamp must be valid
- valid telemetry must be stored
- duplicate event_id must not create duplicate records

### FR-007: Validate Telemetry

The system shall validate telemetry before storing it.

Validation Rules:

- temperature must be within configured range
- pressure must not be negative
- vibration must not be negative
- flow_rate must not be negative
- status must be one of allowed values

Acceptance Criteria:

- invalid telemetry should not enter main telemetry table
- validation error should be clear
- rejected events should be stored in quarantine where applicable

### FR-008: Quarantine Invalid Telemetry

The system shall store invalid telemetry in a quarantine table.

Acceptance Criteria:

- original payload must be preserved
- rejection reason must be stored
- timestamp must be captured
- support engineers can view quarantine records

---

## 3. Alert Management

### FR-009: Generate Alert

The system shall generate alerts when telemetry violates configured rules.

Example Rules:

- temperature greater than threshold
- pressure below threshold
- vibration above threshold
- device heartbeat missing

Acceptance Criteria:

- alert should include device_id
- alert should include severity
- alert should include reason
- duplicate open alerts should be avoided where possible

### FR-010: View Alerts

The system shall allow users to view alerts.

Acceptance Criteria:

- user can list active alerts
- user can filter alerts by status
- user can filter alerts by severity
- user can filter alerts by device_id

### FR-011: Acknowledge Alert

The system shall allow an operator to acknowledge an open alert.

Acceptance Criteria:

- alert status changes from OPEN to ACKNOWLEDGED
- acknowledged_by is captured
- acknowledged_at is captured

### FR-012: Resolve Alert

The system shall allow an operator to resolve an alert.

Acceptance Criteria:

- alert status changes to RESOLVED
- resolved_by is captured
- resolved_at is captured
- resolution_note can be added

---

## 4. Edge Agent

### FR-013: Generate Simulated Telemetry

The Linux edge agent shall generate simulated machine telemetry.

Acceptance Criteria:

- agent can simulate multiple devices
- values should be realistic
- configuration should come from YAML or environment variables

### FR-014: Send Telemetry to Backend

The Linux edge agent shall send telemetry to the backend API.

Acceptance Criteria:

- agent uses device API key
- failed requests are retried
- network failures do not immediately lose data

### FR-015: Local Buffering

The Linux edge agent shall buffer telemetry locally when backend is unavailable.

Acceptance Criteria:

- failed events are stored locally
- agent retries buffered events later
- successful resend removes event from buffer

---

## 5. Security

### FR-016: Authenticate Users

The system shall authenticate users before allowing access to protected APIs.

Acceptance Criteria:

- login returns JWT token
- protected APIs require token
- invalid token returns 401

### FR-017: Authorize Users by Role

The system shall authorize users based on role.

Roles:

- ADMIN
- OPERATOR
- VIEWER
- DEVICE

Acceptance Criteria:

- ADMIN can manage devices
- OPERATOR can manage alerts
- VIEWER can only read
- DEVICE can only send telemetry

### FR-018: Authenticate Devices

The system shall authenticate devices using API keys.

Acceptance Criteria:

- telemetry API requires valid device API key
- disabled device key should not work
- invalid key returns 401

---

## 6. Observability

### FR-019: Health Check

The system shall expose a health check endpoint.

Acceptance Criteria:

- /health returns service status
- /live returns liveness status
- /ready returns readiness status

### FR-020: Structured Logging

The system shall produce structured logs.

Acceptance Criteria:

- logs should include timestamp
- logs should include level
- logs should include service name
- logs should include correlation_id

### FR-021: Metrics

The system shall expose application metrics.

Acceptance Criteria:

- total requests
- request latency
- telemetry received count
- invalid telemetry count
- alert count
- database error count

---

## 7. Audit

### FR-022: Audit Important Actions

The system shall audit important business actions.

Actions:

- device created
- device disabled
- alert acknowledged
- alert resolved
- user login
- failed authentication

Acceptance Criteria:

- action is captured
- timestamp is captured
- old and new values are captured where applicable
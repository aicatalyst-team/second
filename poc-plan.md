# PoC Plan: second

## Project Classification
- **Type:** web-app
- **Key Technologies:** Next.js 16, React 19, Hono, TypeScript, MongoDB 8.0, Redis 7, Claude Agent SDK
- **ODH Relevance:** Demonstrates a multi-service agentic AI platform deployment on OpenShift, validating orchestration of interconnected services including web frontend, worker backend, database, and cache layers.

## PoC Objectives
1. Validate that the multi-service architecture (web + worker + MongoDB + Redis) deploys correctly on OpenShift
2. Verify the web frontend is accessible and serves the application UI
3. Confirm service-to-service communication between web and worker components
4. Demonstrate OpenShift's ability to handle stateful workloads (MongoDB replica set) alongside stateless services

## Infrastructure Requirements
- **Resource Profile:** medium
- **GPU Required:** No
- **Persistent Storage:** 1Gi for MongoDB data
- **Sidecar Containers:** None (MongoDB and Redis as separate deployments)

## PoC Components
- **web**: Next.js frontend (port 3000 -> 8080 for OpenShift)
- **worker**: Hono backend worker (port 3001 -> 8081 for OpenShift)
- **mongo**: MongoDB 8.0 with replica set (port 27017)
- **redis**: Redis 7 (port 6379)

## Test Scenarios

### Scenario 1: web-health-check
- **Description:** Verify the web application responds to the health endpoint
- **Type:** http
- **Input:** GET /api/health
- **Expected:** Returns HTTP 200 with health status
- **Timeout:** 60 seconds

### Scenario 2: web-homepage
- **Description:** Verify the web frontend serves the main page
- **Type:** http
- **Input:** GET /
- **Expected:** Returns HTTP 200 with HTML content
- **Timeout:** 30 seconds

### Scenario 3: worker-health-check
- **Description:** Verify the worker service is running and responding
- **Type:** http
- **Input:** GET /health (or GET /)
- **Expected:** Returns HTTP 200
- **Timeout:** 60 seconds

## Dockerfile Considerations
- Convert existing Dockerfiles from node:20-alpine/node:22-slim to UBI nodejs images
- Web: Multi-stage build (deps -> build -> runner) using ubi9/nodejs-22
- Worker: Single-stage using ubi9/nodejs-22, install system deps via dnf
- MongoDB and Redis: Use official images (no UBI conversion needed for infrastructure)
- All app containers must run as USER 1001 with group 0 permissions

## Deployment Considerations
- **Deployment model:** deployment (all components are long-running services)
- **Services:** ClusterIP for all components (web exposed externally, worker internal)
- **MongoDB:** Needs initialization as a replica set via init script
- **Redis:** Standard deployment, no special config needed
- **Environment variables:** MONGODB_URI, REDIS_URL, WORKER_URL for service discovery
- **Auth mode:** Set SECOND_AUTH_MODE=none for PoC (skip WorkOS authentication)

# Blog Abstract: Deploying Second on OpenShift

## Thesis

Deploying Second, a multi-service platform for AI-augmented internal tooling, on OpenShift validates that complex Node.js applications with MongoDB and Redis dependencies can be containerized with UBI images and run reliably on OpenShift with minimal modifications, though real-world challenges like registry rate limits and database replica set configuration require practical workarounds.

## Target audience

Platform engineers and DevOps practitioners evaluating OpenShift for deploying multi-service Node.js applications, particularly those involving AI-augmented workflows.

## Blog type

Red Hat Developer Blog

## Key points

1. A multi-service Node.js application (Next.js frontend, Hono worker, MongoDB, Redis) can be containerized with UBI-based Dockerfiles and deployed to OpenShift using binary builds and standard Kubernetes manifests.
2. Real-world deployment surfaces practical challenges: Quay registry rate limiting, MongoDB replica set initialization with directConnection=true, UBI filesystem permission constraints, and missing system packages like ripgrep.
3. Three of four PoC validation tests passed (health check, API, worker responsiveness), demonstrating that the core platform functions correctly on OpenShift despite the encountered issues.

## Products and projects

- Red Hat OpenShift AI
- Red Hat Universal Base Image (UBI)
- Second (open source, Apache-2.0)

## CTA

Try deploying your own multi-service application on OpenShift using the AutoPoC workflow, or explore the Second fork at https://github.com/aicatalyst-team/second.

## Proposed section outline

1. What is Second?
2. Why it matters for OpenShift AI
3. Containerizing for OpenShift
4. Building and deploying
5. Running the PoC tests
6. What we learned
7. Try it yourself

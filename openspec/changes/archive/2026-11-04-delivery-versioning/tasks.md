# Tasks

## 1. Local Nexus registry

- [x] 1.1 Add a loopback-only Nexus Compose deployment with persistent data and verify its UI/API responds on `127.0.0.1:8082` while the Docker endpoint is bound on `127.0.0.1:5000`.
- [x] 1.2 Add ignored credential input and a committed example, then verify no credential values are tracked by Git.
- [x] 1.3 Implement idempotent Nexus bootstrap for `stayledger-hosted`, publisher permissions, anonymous pull, and immutable tags; verify authenticated push, anonymous pull, and duplicate-tag rejection.

## 2. Versioned application image

- [x] 2.1 Add a multi-stage Java 21 Dockerfile that builds `:_ms:bootJar` with `-PappVersion` and verify the selected boot JAR name contains the requested version.
- [x] 2.2 Add `.dockerignore` and a non-root runtime stage containing only the application artifact; verify the image user is non-root and Git/credential files are absent.
- [x] 2.3 Expose the application port and launch the exact boot JAR; verify a container without database variables serves `/actuator/health` on port 8081.

## 3. Shared delivery commands and documentation

- [x] 3.1 Add a reusable image build/push command that derives the branch default or accepts an explicit version; verify default, SNAPSHOT, and `-RELEASE` image tags match their Gradle versions.
- [x] 3.2 Add a smoke-test command that waits for the database-free technical health endpoint and verify it fails clearly when Docker is unavailable or the endpoint is unhealthy.
- [x] 3.3 Update Stage 2 documentation with Nexus setup, login, build, push, and smoke commands; verify every documented command maps to a committed script or Compose asset.
- [x] 3.4 Run the complete local delivery path and verify `localhost:5000/stayledger:<version>` can be built, smoke-tested, pushed, and anonymously pulled.

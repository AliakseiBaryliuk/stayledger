# syntax=docker/dockerfile:1
FROM gradle:9.8.2-jdk21 AS builder

WORKDIR /workspace

COPY gradlew gradlew.bat settings.gradle.kts build.gradle.kts gradle.properties ./
COPY gradle gradle
COPY _core _core
COPY _infra _infra
COPY _ms _ms

ARG APP_VERSION
RUN gradle --no-daemon :_ms:bootJar -PappVersion=${APP_VERSION}

FROM eclipse-temurin:21-jre-jammy

WORKDIR /app

RUN groupadd --system stayledger && useradd --system --gid stayledger --home-dir /app --shell /usr/sbin/nologin stayledger

ARG APP_VERSION
COPY --from=builder /workspace/_ms/build/libs/_ms-${APP_VERSION}.jar /app/stayledger.jar

USER stayledger:stayledger

EXPOSE 8081

ENTRYPOINT ["java", "-jar", "/app/stayledger.jar"]

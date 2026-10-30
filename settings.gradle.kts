pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

rootProject.name = "stayledger"

include("core-api", "core-impl", "postgres_adapter", "_ms")

project(":core-api").projectDir = file("_core/core-api")
project(":core-impl").projectDir = file("_core/core-impl")
project(":postgres_adapter").projectDir = file("_infra/postgres_adapter")
project(":_ms").projectDir = file("_ms")

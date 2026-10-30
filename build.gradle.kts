plugins {
    id("org.springframework.boot") version "4.1.2" apply false
}

allprojects {
    group = "com.stayledger"
    version = "0.1.0-SNAPSHOT"

    repositories {
        mavenCentral()
    }
}

subprojects {
    apply(plugin = "java-library")

    extensions.configure<org.gradle.api.plugins.JavaPluginExtension> {
        toolchain.languageVersion.set(org.gradle.jvm.toolchain.JavaLanguageVersion.of(21))
    }

    tasks.withType<org.gradle.api.tasks.testing.Test>().configureEach {
        useJUnitPlatform()
    }
}

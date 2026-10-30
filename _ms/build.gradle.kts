plugins {
    id("org.springframework.boot")
}

dependencies {
    implementation(platform("org.springframework.boot:spring-boot-dependencies:4.1.2"))
    implementation(project(":core-impl"))
    implementation(project(":postgres_adapter"))
    implementation("org.springframework.boot:spring-boot-starter")
}

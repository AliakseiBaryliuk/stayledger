package com.stayledger.runtime;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import jakarta.annotation.Nonnull;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.regex.Pattern;

import org.junit.jupiter.api.Test;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
class TechnicalPingHttpTest {

    @Value("${local.server.port}")
    private int port;

    @Test
    void respondsWithoutBusinessModules() throws Exception {
        HttpResponse<String> response = get("/internal/ping");

        assertEquals(200, response.statusCode());
        assertEquals("OK", response.body());
    }

    @Test
    void reportsHealthyStatusForOverallAndAvailabilityProbes() throws Exception {
        for (String path : new String[] {
            "/actuator/health",
            "/actuator/health/liveness",
            "/actuator/health/readiness"
        }) {
            HttpResponse<String> response = get(path);

            assertEquals(200, response.statusCode(), path);
            assertTrue(response.body().contains("\"status\":\"UP\""), path);
        }
    }

    @Test
    void servesPrometheusMetricSamples() throws Exception {
        HttpResponse<String> response = get("/actuator/prometheus");

        assertEquals(200, response.statusCode());
        assertTrue(response.headers().firstValue("content-type").orElse("").contains("text/plain"));
        assertTrue(Pattern.compile("(?m)^[a-zA-Z_:][a-zA-Z0-9_:]*(\\{[^\\n]*\\})? [0-9]")
            .matcher(response.body()).find());
    }

    @Test
    void doesNotExposeOtherActuatorEndpoints() throws Exception {
        assertEquals(404, get("/actuator/env").statusCode());
    }

    @Nonnull
    private HttpResponse<String> get(@Nonnull String path) throws Exception {
        HttpRequest request = HttpRequest.newBuilder(URI.create("http://localhost:" + port + path))
            .GET()
            .build();

        try (HttpClient client = HttpClient.newHttpClient()) {
            return client.send(request, HttpResponse.BodyHandlers.ofString());
        }
    }
}

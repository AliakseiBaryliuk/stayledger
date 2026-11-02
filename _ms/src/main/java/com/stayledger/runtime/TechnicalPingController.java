package com.stayledger.runtime;

import jakarta.annotation.Nonnull;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class TechnicalPingController {

    @Nonnull
    @GetMapping("/internal/ping")
    public String ping() {
        return "OK";
    }
}

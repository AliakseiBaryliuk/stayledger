package com.stayledger;

import jakarta.annotation.Nonnull;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class StayLedgerApplication {

    @Nonnull
    public static void main(@Nonnull String[] args) {
        SpringApplication.run(StayLedgerApplication.class, args);
    }
}

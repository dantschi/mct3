/* VL09: funktionale Host-Pruefung mit C11-Atomics und POSIX Threads.
 * Kein MESI-Timing, keine RISC-V-Firmware, kein racy gewoehnliches C-Experiment.
 * gcc -std=c11 -O2 -Wall -Wextra -Werror -pedantic -pthread lab09_atomics.c
 */
#include <pthread.h>
#include <sched.h>
#include <stdatomic.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define ITERATIONS 20000u
#define CHECK(condition) do { \
    if (!(condition)) { \
        fprintf(stderr, "Prueffehler in Zeile %d\n", __LINE__); \
        return 1; \
    } \
} while (0)

/* Der erste Worker darf niemals auf die Erzeugung des zweiten warten.
 * So ist auch der Fehlerpfad einer fehlgeschlagenen zweiten Erzeugung sicher.
 * 0: beide erfolgreich beendet. -1: Fehler; keine Ergebnisse auswerten.
 */
static int run_pair(void *(*first)(void *), void *first_arg,
                    void *(*second)(void *), void *second_arg) {
    pthread_t threads[2];
    int error = pthread_create(&threads[0], NULL, first, first_arg);
    if (error != 0) {
        fprintf(stderr, "pthread_create: %s\n", strerror(error));
        return -1;
    }
    error = pthread_create(&threads[1], NULL, second, second_arg);
    if (error != 0) {
        fprintf(stderr, "pthread_create: %s\n", strerror(error));
        const int join_error = pthread_join(threads[0], NULL);
        if (join_error != 0) {
            fprintf(stderr, "pthread_join: %s\n", strerror(join_error));
        }
        return -1;
    }
    int failed = 0;
    for (size_t i = 0; i < 2; ++i) {
        error = pthread_join(threads[i], NULL);
        if (error != 0) {
            fprintf(stderr, "pthread_join: %s\n", strerror(error));
            failed = -1;
        }
    }
    return failed;
}

struct sum_job {
    const uint32_t *values;
    size_t begin, end;
    uint64_t result;
};

static void *sum_worker(void *arg) {
    struct sum_job *job = arg;
    uint64_t sum = 0;
    for (size_t i = job->begin; i < job->end; ++i) {
        sum += job->values[i];
    }
    job->result = sum;  /* Jeder Worker schreibt sein eigenes Objekt. */
    return NULL;
}

static atomic_uint counter = 0;
static void *atomic_worker(void *arg) {
    (void)arg;
    for (unsigned int i = 0; i < ITERATIONS; ++i) {
        atomic_fetch_add_explicit(&counter, 1u, memory_order_relaxed);
    }
    return NULL;
}

static atomic_flag lock = ATOMIC_FLAG_INIT;
static unsigned int protected_counter = 0;
static void *locked_worker(void *arg) {
    (void)arg;
    for (unsigned int i = 0; i < ITERATIONS; ++i) {
        while (atomic_flag_test_and_set_explicit(&lock, memory_order_acquire)) {
            /* Nur Hostthreads: Besitzer muss weiterlaufen koennen. */
        }
        ++protected_counter;
        atomic_flag_clear_explicit(&lock, memory_order_release);
    }
    return NULL;
}

/* Einmalige Publikation: kein Rewrite und kein Ruecksetzen von ready. */
static int payload = 0;
static atomic_bool ready = false;
static int observed_payload = 0;
static void *publisher(void *arg) {
    (void)arg;
    payload = 42;
    atomic_store_explicit(&ready, true, memory_order_release);
    return NULL;
}
static void *subscriber(void *arg) {
    (void)arg;
    while (!atomic_load_explicit(&ready, memory_order_acquire)) {
        sched_yield();
    }
    observed_payload = payload;
    return NULL;
}

int main(void) {
    const uint32_t values[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    struct sum_job jobs[2] = {{values, 0, 4, 0}, {values, 4, 8, 0}};
    CHECK(run_pair(sum_worker, &jobs[0], sum_worker, &jobs[1]) == 0);
    CHECK(jobs[0].result == 10 && jobs[1].result == 26);
    CHECK(jobs[0].result + jobs[1].result == 36);
    puts("Teilsummen: 10 26, gesamt 36");

    /* Serielle Nachbildung eines Interleavings: keine tatsaechliche C-Data-Race.
     * Jeder Load/Store ist atomar, die ganze Gruppe aber keine atomare RMW.
     */
    atomic_uint split = 0;
    const unsigned int old0 = atomic_load_explicit(&split, memory_order_relaxed);
    const unsigned int old1 = atomic_load_explicit(&split, memory_order_relaxed);
    atomic_store_explicit(&split, old0 + 1u, memory_order_relaxed);
    atomic_store_explicit(&split, old1 + 1u, memory_order_relaxed);
    CHECK(atomic_load_explicit(&split, memory_order_relaxed) == 1u);
    puts("Getrennte atomare Zugriffe: Endwert 1");

    CHECK(run_pair(atomic_worker, NULL, atomic_worker, NULL) == 0);
    const unsigned int final_counter = atomic_load_explicit(&counter, memory_order_relaxed);
    CHECK(final_counter == 2u * ITERATIONS);
    printf("Atomare RMW: %u\n", final_counter);

    CHECK(run_pair(locked_worker, NULL, locked_worker, NULL) == 0);
    CHECK(protected_counter == 2u * ITERATIONS);
    printf("Geschuetzter Zaehler: %u\n", protected_counter);

    /* Produzent zuerst: Bei fehlender Konsumentenerzeugung ist er unabhaengig. */
    CHECK(run_pair(publisher, NULL, subscriber, NULL) == 0);
    CHECK(observed_payload == 42);
    printf("Veroeffentlichte Daten: %d\n", observed_payload);
    puts("Alle Prueffaelle bestanden.");
    return 0;
}

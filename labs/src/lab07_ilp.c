/* VL07: zwei funktional gleiche vorzeichenlose Reduktionen.
   Vorbedingung: a zeigt auf mindestens n gueltige Elemente.
   Fuer n == 0 ist auch a == NULL erlaubt; es wird nichts gelesen.
   Kein Zyklusmodell, keine Geraetezugriffe, kein Leistungsmesswert. */
#include <stddef.h>
#include <stdint.h>
#include <inttypes.h>
#include <stdio.h>

static uint64_t reduce_chain(const uint32_t *a, size_t n) {
    uint64_t sum = 0;
    for (size_t i = 0; i < n; ++i)
        sum += a[i];
    return sum;
}

static uint64_t reduce_split(const uint32_t *a, size_t n) {
    uint64_t sum0 = 0;
    uint64_t sum1 = 0;
    size_t pairs = n / 2;
    for (size_t j = 0; j < pairs; ++j) {
        sum0 += a[2 * j];
        sum1 += a[2 * j + 1];
    }
    if (n % 2 != 0)
        sum0 += a[n - 1];
    return sum0 + sum1;
}

int main(void) {
    const uint32_t a[] = {1, 2, 3, 4, 5, 6, 7, 8};
    const uint64_t expected[] = {0, 1, 3, 6, 10, 15, 21, 28, 36};
    if (reduce_chain(NULL, 0) != 0 || reduce_split(NULL, 0) != 0)
        return 1;
    for (size_t n = 0; n <= 8; ++n) {
        if (reduce_chain(a, n) != expected[n] ||
            reduce_split(a, n) != expected[n]) {
            fprintf(stderr, "Falsche Summe bei n=%zu\n", n);
            return 1;
        }
    }
    const uint32_t wide[] = {UINT32_MAX, 1, 7, 0, UINT32_MAX};
    const uint64_t wide_expected = UINT64_C(8589934598);
    if (reduce_chain(wide, 5) != wide_expected ||
        reduce_split(wide, 5) != wide_expected)
        return 1;

    printf("n=8: Kette=%" PRIu64 ", geteilt=%" PRIu64 "\n",
           reduce_chain(a, 8), reduce_split(a, 8));
    printf("n=5: Kette=%" PRIu64 ", geteilt=%" PRIu64 "\n",
           reduce_chain(a, 5), reduce_split(a, 5));
    puts("Alle Prueffaelle bestanden.");
    return 0;
}

/* Lehrbeispiel VL07. Host-GCC prueft nur die Ergebnisgleichheit.
   Kein OoO-Zyklusmodell und kein RISC-V-Scheduling. */
#include <stdio.h>

static unsigned long long reduce_chain(const unsigned *a, unsigned n) {
    unsigned long long s = 0;
    for (unsigned i = 0; i < n; i++)
        s += a[i];
    return s;
}

static unsigned long long reduce_split(const unsigned *a, unsigned n) {
    unsigned long long s0 = 0;
    unsigned long long s1 = 0;
    unsigned i = 0;
    for (; i + 1 < n; i += 2) {
        s0 += a[i];
        s1 += a[i + 1];
    }
    if (i < n)
        s0 += a[i];
    return s0 + s1;
}

int main(void) {
    unsigned a[8] = {1, 2, 3, 4, 5, 6, 7, 8};
    unsigned long long x = reduce_chain(a, 8);
    unsigned long long y = reduce_split(a, 8);
    if (x != 36 || y != 36 || x != y)
        return 1;
    printf("%llu\n", x);
    return 0;
}

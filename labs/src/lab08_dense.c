/* VL08: numerische Host-Pruefung. Kein trainiertes Netz, TFLM oder Timingmodell.
 * gcc -std=c11 -O2 -Wall -Wextra -Werror -pedantic lab08_dense.c -lm
 */
#include <float.h>
#include <limits.h>
#include <math.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>

/* Feste 2x3-Integer-Schicht: Nullpunkte null, keine Aktivierung/Requantisierung.
 * Alle Pointer zeigen auf Objekte mit den angegebenen Dimensionen.
 * 0: beide Int32-Ausgaenge geschrieben; -1: Fehler, Ausgabe unveraendert.
 */
static int dense_2x3(const int8_t weights[2][3], const int8_t input[3],
                     const int32_t bias[2], int32_t output[2]) {
    if (weights == NULL || input == NULL || bias == NULL || output == NULL) {
        return -1;
    }
    int32_t result[2];
    for (size_t row = 0; row < 2; ++row) {
        int64_t sum = bias[row];
        for (size_t i = 0; i < 3; ++i) {
            sum += (int64_t)input[i] * weights[row][i];
        }
        if (sum < INT32_MIN || sum > INT32_MAX) {
            return -1;
        }
        result[row] = (int32_t)sum;
    }
    output[0] = result[0];
    output[1] = result[1];
    return 0;
}

/* q = clip(round(real/scale) + zero_point).
 * Lehrregel: naechster Integer, exakte Halbfalle weg von null.
 * real und scale endlich, scale > 0, zero_point in [-128,127].
 * 0: Code geschrieben; -1: Fehler, Ausgabe unveraendert.
 * Begrenzung vor dem Cast vermeidet undefinierte Float-zu-Integer-Konversion.
 */
static int quantize_i8(double real, double scale, int zero_point, int8_t *out) {
    if (out == NULL || !isfinite(real) || !isfinite(scale) || scale <= 0.0 ||
        zero_point < INT8_MIN || zero_point > INT8_MAX) {
        return -1;
    }
    const double code = round(real / scale) + zero_point;
    if (code >= INT8_MAX) {
        *out = INT8_MAX;
    } else if (code <= INT8_MIN) {
        *out = INT8_MIN;
    } else {
        *out = (int8_t)code;
    }
    return 0;
}

#define CHECK(condition) do { \
    if (!(condition)) { \
        fprintf(stderr, "Prueffehler in Zeile %d\n", __LINE__); \
        return 1; \
    } \
} while (0)

int main(void) {
    const int8_t weights[2][3] = {{1, 2, 3}, {0, -1, 4}};
    const int8_t input[3] = {2, 1, 3};
    const int32_t bias[2] = {1, -2};
    int32_t output[2] = {0, 0};
    CHECK(dense_2x3(weights, input, bias, output) == 0);
    CHECK(output[0] == 14 && output[1] == 9);
    printf("Dense: %d %d\n", (int)output[0], (int)output[1]);

    const int8_t extreme_weights[2][3] = {{-128, -128, -128}, {127, 127, 127}};
    const int8_t extreme_input[3] = {-128, -128, -128};
    const int32_t zero_bias[2] = {0, 0};
    CHECK(dense_2x3(extreme_weights, extreme_input, zero_bias, output) == 0);
    CHECK(output[0] == 49152 && output[1] == -48768);

    const int8_t unit_weights[2][3] = {{1, 0, 0}, {1, 0, 0}};
    const int8_t unit_input[3] = {1, 1, 1};
    const int32_t overflow_bias[2] = {0, INT32_MAX};
    output[0] = 777;
    output[1] = 888;
    CHECK(dense_2x3(unit_weights, unit_input, overflow_bias, output) == -1);
    CHECK(output[0] == 777 && output[1] == 888);
    const int8_t negative_input[3] = {-1, 0, 0};
    const int32_t underflow_bias[2] = {INT32_MIN, 0};
    CHECK(dense_2x3(unit_weights, negative_input, underflow_bias, output) == -1);
    CHECK(output[0] == 777 && output[1] == 888);
    CHECK(dense_2x3(NULL, input, bias, output) == -1);
    CHECK(dense_2x3(weights, NULL, bias, output) == -1);
    CHECK(dense_2x3(weights, input, NULL, output) == -1);
    CHECK(dense_2x3(weights, input, bias, NULL) == -1);

    const int8_t a[2][2] = {{1, 2}, {3, 4}};
    const int8_t b[2][2] = {{5, 6}, {7, 8}};
    const int32_t expected[2][2] = {{19, 22}, {43, 50}};
    int32_t c[2][2] = {{0, 0}, {0, 0}};
    for (size_t i = 0; i < 2; ++i) {
        for (size_t j = 0; j < 2; ++j) {
            for (size_t k = 0; k < 2; ++k) {
                c[i][j] += (int32_t)a[i][k] * b[k][j];
            }
            CHECK(c[i][j] == expected[i][j]);
        }
    }
    printf("Matrix: %d %d %d %d\n", (int)c[0][0], (int)c[0][1],
           (int)c[1][0], (int)c[1][1]);

    struct quant_case { double real, scale; int zero, expected; };
    const struct quant_case cases[] = {
        {1.24, 0.1, 0, 12}, {-1.24, 0.1, 0, -12},
        {20.0, 0.1, 0, 127}, {-20.0, 0.1, 0, -128},
        {0.0, 0.1, -3, -3}, {1.24, 0.1, -3, 9},
        {0.5, 1.0, 0, 1}, {-0.5, 1.0, 0, -1},
        {0.5, 1.0, -3, -2}, {-0.5, 1.0, -3, -4},
        {DBL_MAX, DBL_MIN, 0, 127}, {-DBL_MAX, DBL_MIN, 0, -128},
        {0.64, 0.05, -2, 11}
    };
    int8_t q = 0;
    for (size_t i = 0; i < sizeof cases / sizeof cases[0]; ++i) {
        CHECK(quantize_i8(cases[i].real, cases[i].scale, cases[i].zero, &q) == 0);
        CHECK(q == cases[i].expected);
    }
    q = 42;
    CHECK(quantize_i8(NAN, 0.1, 0, &q) == -1);
    CHECK(quantize_i8(INFINITY, 0.1, 0, &q) == -1);
    CHECK(quantize_i8(1.0, NAN, 0, &q) == -1);
    CHECK(quantize_i8(1.0, INFINITY, 0, &q) == -1);
    CHECK(quantize_i8(1.0, 0.0, 0, &q) == -1);
    CHECK(quantize_i8(1.0, -0.1, 0, &q) == -1);
    CHECK(quantize_i8(1.0, 0.1, 128, &q) == -1);
    CHECK(quantize_i8(1.0, 0.1, -129, &q) == -1);
    CHECK(quantize_i8(1.0, 0.1, 0, NULL) == -1);
    CHECK(q == 42);

    /* Zweites, separat quantisiertes Skalarprodukt aus Folie/Aufgabe 5. */
    const int64_t accum = (12 - (-3)) * 2 + (-4 - (-3)) * 3 + 5;
    CHECK(accum == 32);
    CHECK(fabs(0.1 * 0.2 * (double)accum - 0.64) < 1e-12);
    CHECK(quantize_i8(0.64, 0.05, -2, &q) == 0 && q == 11);
    CHECK(fabs(0.05 * ((int)q + 2) - 0.65) < 1e-12);

    int8_t codes[3];
    CHECK(quantize_i8(1.24, 0.1, 0, &codes[0]) == 0);
    CHECK(quantize_i8(20.0, 0.1, 0, &codes[1]) == 0);
    CHECK(quantize_i8(-20.0, 0.1, 0, &codes[2]) == 0);
    printf("Quantisierung: %d %d %d\n", (int)codes[0], (int)codes[1], (int)codes[2]);
    puts("Alle Prueffaelle bestanden.");
    return 0;
}

/* Host-Prüfung des VL08-Beispiels. Kein TFLM und kein RISC-V. */
#include <stdint.h>
#include <stdio.h>

static int dense_y0(void) {
    return 1 * 2 + 2 * 1 + 3 * 3 + 1;
}

static int dense_y1(void) {
    return 0 * 2 + (-1) * 1 + 4 * 3 + (-2);
}

static int8_t quantize(float real, float scale, int zero_point) {
    int q = (int)(real / scale + (real >= 0 ? 0.5f : -0.5f)) + zero_point;
    if (q > 127) q = 127;
    if (q < -128) q = -128;
    return (int8_t)q;
}

int main(void) {
    if (dense_y0() != 14 || dense_y1() != 9) return 1;
    if (quantize(1.24f, 0.1f, 0) != 12) return 2;
    if (quantize(20.0f, 0.1f, 0) != 127) return 3;
    int c00 = 1 * 5 + 2 * 7;
    int c11 = 3 * 6 + 4 * 8;
    if (c00 != 19 || c11 != 50) return 4;
    printf("%d %d\n", dense_y0(), dense_y1());
    return 0;
}

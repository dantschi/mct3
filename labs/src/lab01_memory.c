/* VL01: logical teaching models on the host, no device access.
 * Single execution context; no analogue SRAM/DRAM or flash controller model.
 */
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <string.h>

#define CHECK(condition) do { \
    if (!(condition)) { \
        fprintf(stderr, "Prueffehler in Zeile %d: %s\n", __LINE__, #condition); \
        return 1; \
    } \
} while (0)

enum { FIFO_CAPACITY = 4 };
struct fifo {
    char values[FIFO_CAPACITY];
    size_t read, write, count;
};

static bool fifo_push(struct fifo *f, char value)
{
    if (f == NULL || f->count >= FIFO_CAPACITY)
        return false;
    f->values[f->write] = value;
    f->write = (f->write + 1) % FIFO_CAPACITY;
    ++f->count;
    return true;
}

static bool fifo_pop(struct fifo *f, char *value)
{
    if (f == NULL || value == NULL || f->count == 0)
        return false;
    *value = f->values[f->read];
    f->read = (f->read + 1) % FIFO_CAPACITY;
    --f->count;
    return true;
}

/* Bit rule only: real flash can impose additional programming restrictions. */
static bool flash_program(uint8_t *value, uint8_t desired)
{
    if (value == NULL || (*value & desired) != desired)
        return false;
    *value = desired;
    return true;
}

static void flash_erase(uint8_t *block, size_t length)
{
    /* Caller supplies a valid block and length. */
    memset(block, 0xff, length);
}

/* Addresses are integers, not pointers to host objects. End is exclusive. */
static bool word_start_valid(uint32_t address, uint32_t start, uint32_t end)
{
    return start <= end && address >= start && address < end &&
           end - address >= 4 && address % 4 == 0;
}

int main(void)
{
    /* Exhaustively check all 65536 old/desired byte combinations. */
    for (unsigned old = 0; old <= UINT8_MAX; ++old) {
        for (unsigned desired = 0; desired <= UINT8_MAX; ++desired) {
            uint8_t value = (uint8_t)old;
            bool expected = true;
            for (unsigned bit = 0; bit < 8; ++bit)
                if ((old & (1u << bit)) == 0 && (desired & (1u << bit)) != 0)
                    expected = false;
            CHECK(flash_program(&value, (uint8_t)desired) == expected);
            CHECK(value == (expected ? desired : old));
        }
    }
    uint8_t block[4] = {0xa5, 0x3c, 0xff, 0xff};
    uint8_t saved[sizeof block];
    CHECK(flash_program(&block[0], 0x81));
    block[0] = 0xa5; /* Begin a separate teaching case, not a flash write. */
    CHECK(!flash_program(&block[0], 0xaf));
    CHECK(block[0] == 0xa5);
    memcpy(saved, block, sizeof block);
    saved[0] = 0xaf;
    flash_erase(block, sizeof block);
    for (size_t i = 0; i < sizeof block; ++i) {
        CHECK(block[i] == 0xff);
        CHECK(flash_program(&block[i], saved[i]));
    }
    CHECK(block[0] == 0xaf && block[1] == 0x3c);
    CHECK(!flash_program(NULL, 0));
    puts("Flashmodell: A5 -> 81 erlaubt, A5 -> AF braucht Loeschen");

    CHECK(word_start_valid(0x1000fffc, 0x10000000, 0x10010000));
    CHECK(!word_start_valid(0x1000ffff, 0x10000000, 0x10010000));
    CHECK(!word_start_valid(0x10010000, 0x10000000, 0x10010000));
    CHECK(!word_start_valid(0x0ffffffc, 0x10000000, 0x10010000));
    CHECK(!word_start_valid(0xfffffffc, 0, UINT32_MAX));
    CHECK(!word_start_valid(4, 8, 4));
    puts("Adressmodell: letzter ausgerichteter Wortstart 1000FFFC");

    const uint8_t data_image[] = {3, 0, 0, 0};
    uint8_t data_runtime[sizeof data_image] = {0xff, 0xff, 0xff, 0xff};
    uint8_t bss_runtime[16];
    memset(bss_runtime, 0x5a, sizeof bss_runtime);
    memcpy(data_runtime, data_image, sizeof data_runtime);
    memset(bss_runtime, 0, sizeof bss_runtime);
    CHECK(memcmp(data_runtime, data_image, sizeof data_runtime) == 0);
    for (size_t i = 0; i < sizeof bss_runtime; ++i)
        CHECK(bss_runtime[i] == 0);
    /* Bytes are checked directly: no host-endianness assumption for uint32_t. */
    puts("Startupmodell: Initialwerte kopiert, BSS auf null");

    struct fifo f = {0};
    char value = '?';
    CHECK(!fifo_pop(&f, &value) && value == '?');
    CHECK(f.count == 0 && f.read == 0 && f.write == 0);
    CHECK(fifo_push(&f, 'A') && fifo_push(&f, 'B') && fifo_push(&f, 'C'));
    CHECK(fifo_pop(&f, &value) && value == 'A');
    CHECK(fifo_push(&f, 'D') && fifo_push(&f, 'E'));
    CHECK(f.read == 1 && f.write == 1 && f.count == 4);
    struct fifo before = f;
    CHECK(!fifo_push(&f, 'F'));
    CHECK(f.read == before.read && f.write == before.write && f.count == before.count);
    CHECK(memcmp(f.values, before.values, sizeof f.values) == 0);
    CHECK(!fifo_pop(&f, NULL));
    CHECK(fifo_pop(&f, &value) && value == 'B');
    CHECK(fifo_push(&f, 'F'));
    CHECK(f.read == 2 && f.write == 2 && f.count == 4);
    const char remaining[] = {'C', 'D', 'E', 'F'};
    for (size_t i = 0; i < sizeof remaining; ++i)
        CHECK(fifo_pop(&f, &value) && value == remaining[i]);
    value = '?';
    CHECK(!fifo_pop(&f, &value) && value == '?');
    CHECK(f.count == 0 && f.read == f.write);
    CHECK(!fifo_push(NULL, 'X') && !fifo_pop(NULL, &value));
    puts("FIFO-Modell: volle und leere Zustaende korrekt");
    puts("Alle Prueffaelle bestanden.");
    return 0;
}

/* Native object inspection, not a linked or bootable firmware. */
#include <stdint.h>

const uint32_t lookup[4] = {1, 2, 3, 4};
uint32_t counter = 3;
uint8_t buffer[16];

uint32_t read_snapshot(void)
{
    return lookup[counter % 4] + buffer[0];
}

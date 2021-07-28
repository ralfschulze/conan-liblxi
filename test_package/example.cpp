#include <stdlib.h>
#include <lxi.h>

int main()
{
    // Initialize LXI library
    if (lxi_init() == LXI_OK)
        exit(0);
    else
        exit(1);
}

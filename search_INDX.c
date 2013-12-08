// we have to support big disks
#define _FILE_OFFSET_BITS 64

#include <stdio.h>


// 4kb sector does not work if NTFS partition starts with sector 63 :-(
const int SECT_SIZE = 512;

int main(int argc, char **argv)
{
    if (argc != 2) {
        fprintf(stderr, "Error: Invalid arguments.\n"
        "Usage: %s <disk_image>\n", argv[0]);
        return 1;
    }

    FILE *fp = fopen(argv[1], "rb");
    if (fp == NULL) {
        perror("fopen");
        return 1;
    }

    off_t sec = 0;

    while (!feof(fp)) {
        char buf[SECT_SIZE];

        if (fread(buf, sizeof(buf), 1, fp) < 0) {
            perror("fread");
            fclose(fp);
            return 1;
        }

        if (strncmp(buf, "INDX", 4) == 0) {
            printf("%lld\n", sec);
        }

        sec++;
    }

    fclose(fp);
    return 0;
}

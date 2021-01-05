/*
  gcc -o nicer nicer.c -Wall -Werror -pedantic -std=c99
  chmod 700 nicer
  sudo setcap CAP_SYS_NICE+ep nicer
*/
#include <sys/time.h>
#include <sys/resource.h>
#include <unistd.h>
#include <stdint.h>
#include <errno.h>

int main(void) {
  for(;;) {
    int32_t values[3];

    size_t expected = sizeof(values);
    ssize_t r = read(0, &values, expected);
    if (r != expected) {
      return 1;
    }

    int32_t out;
    if (setpriority(values[0], values[1], values[2]) == 0) {
      out = 0;
    } else {
      out = errno;
    }

    if (write(1, &out, sizeof(out)) != sizeof(out)) {
      return 2;
    }
  }
}

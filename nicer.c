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
#include <stdlib.h>
#include <limits.h>

static int conv(const char *v, int *out) {
  char *p;
  long l = strtol(v, &p, 10);
  if (p == v) {
    return 0;
  }
  if ((l == LONG_MAX || l == LONG_MIN) && errno == ERANGE) {
    return 0;
  }

  *out = l;
  return 1;
}

int main(int argc, char *argv[]) {
  if (argc != 4) {
    return 255;
  }

  int which, pid, value;
  if (!conv(argv[1], &which) || !conv(argv[2], &pid) || !conv(argv[3], &value)) {
    return 255;
  }

  if (setpriority(which, pid, value) != 0) {
    return errno;
  }

  return 0;
}

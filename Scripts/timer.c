#include<stdio.h>
#include<unistd.h>
#include<time.h>
#include<sys/time.h>
#include<stdlib.h>

int main(){

	struct timespec start, end;
	clock_gettime(CLOCK_MONOTONIC_RAW, &start);
	
	usleep( 4000 );

	clock_gettime(CLOCK_MONOTONIC_RAW, &end);

	__uint64_t delta_us = (end.tv_sec - start.tv_sec) * 1000000 + (end.tv_nsec - start.tv_nsec) / 1000;
	printf("took %lu\n", delta_us);

	return 0;
}

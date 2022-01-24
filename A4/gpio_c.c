/*	Name: Sipeng He
 * UCID: 30113342
 * Functions:
 * (1) iniGPIO: mapping the pointer to the GPIO memory
 * (2) release: unmap the GPIO memory, release the pointer
 * (3) peek: read and return the 32-bit data from the given register
 * (4) poke: write the given 32-bit data into the specified register
 * */

#include <stdio.h>
#include <stddef.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <unistd.h>

#define GPIO_BASE_ADDRESS 0xFE200000
#define BLOCK_SIZE 4096 

volatile unsigned int *gpio;
void *gpioMap;

int fd;

/*
 * Function: iniGPIO
 * Feature: open the dev/gpiomem file; map the pointer to the GPIO memory
 */
int iniGPIO(){
	
	int fd = open("/dev/gpiomem", O_RDWR|O_SYNC);
	if (fd<0) {
		printf("Can't open /dev/gpiomem \n");
		return -1;
	}
			
	gpioMap = (unsigned int *) mmap(NULL,BLOCK_SIZE,PROT_READ|PROT_WRITE,MAP_SHARED, fd, GPIO_BASE_ADDRESS);
	
	if(gpioMap == MAP_FAILED) {
		printf("Error: gpio_mmap\n");
		return -1;
	}
	
	gpio = (volatile unsigned int *) gpioMap;
	
	return 0;
}

/*
 * Function: releaseGPIO
 * Feature: unmap the GPIO memory; release the pointer
 */
void releaseGPIO(){
	munmap(gpioMap, BLOCK_SIZE);
	close(fd);
}
/*
 * Function: peek
 * Feature: read and return the 32-bit data from the given register
 * Input: 
 * int offset: offset of a given register
 */

long peek(int offset){
	iniGPIO();
	long r;
	r = gpio[offset];
	releaseGPIO();
	return r;
}

/*
 * Function: poke
 * Feature: write the given 32-bit data into the specified register
 * Input: 
 * long value: a given 32-bit piece of data to be written into a register
 * int offset: offset of a given register
 */

void poke(long value, int offset){
	iniGPIO();
	gpio[offset] = value;
	releaseGPIO();
}






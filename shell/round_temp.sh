#include <stdio.h>
 
float fround(float f) {
	float fractional = f - (long) f;
 
	if (fractional < .25) {
		fractional = 0;	
	} else if (fractional >= .25 && fractional <= .75) {
		fractional = .5;
	} else {
		fractional = 1;
	}
 
	return (long) f + fractional;
}
 
int main(void) {
	float x = 2.25;
	float y = 2.75;
	float z = 2.99;
	float w = 2.01;
 
	printf("%f -> %f; %f -> %f; %f -> %f; %f -> %f", x, fround(x), y, fround(y), z, fround(z), w, fround(w));
	return 0;
}
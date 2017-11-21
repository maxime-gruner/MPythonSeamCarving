#include<stdlib.h>

int calculate_energy(int i, int j, int w, int[] data){
    int current = j*w+i;
    int current_minus_w = current - w;
    int corner = data[current_minus_w - 1] - data[current + w + 1];
    int x = data[current_minus_w + 1];
    int y = data[current + w - 1];
    int tmpx = 2*data[current-1] - 2*data[current+1] + corner + y - x;
    int tmpy = 2*data[current_minus_w] - 2*data[current+w] + corner + x - y;
    return abs(tmpx) + abs(tmpy);
}
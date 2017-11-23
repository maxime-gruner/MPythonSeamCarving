#include<stdlib.h>
#include<stdio.h>
int* res;

int* calculate_energy(int w, int h, int* data){
    int wh = w*h;
    res = malloc(wh*sizeof(int));
    for(int j =0; j<h; j++){
        int wj = w*j;
        res[wj] = 255;
        res[wj+(w-1)] = 255;
        }
    for(int i =0; i<w;i++){
        res[i] = 255;
        res[wh-(i+1)] = 255;
    }
    for(int j = 1; j<h-1; j++){

        for(int i = 1; i<w-1;i++){
            int current = j*w+i;
            int current_minus_w = current - w;
            int corner = data[current_minus_w - 1] - data[current + w + 1];
            int x = data[current_minus_w + 1];
            int y = data[current + w - 1];
            int tmpx = 2*data[current-1] - 2*data[current+1] + corner + y - x;
            int tmpy = 2*data[current_minus_w] - 2*data[current+w] + corner + x - y;
            res[current] =  abs(tmpx) + abs(tmpy);
        }
    }
    return res;
}

void free_p(){
    free(res);
}
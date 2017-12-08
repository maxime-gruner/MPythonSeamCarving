#include<stdlib.h>
#include<stdio.h>
int* res;

int* calculate_energy(int w, int h, int* data){
    int wh = w*h;
    int i,j,current,current_minus_w,corner,x,y,tmpx,tmpy,wj;
    res = malloc(wh*sizeof(int));
    for(j =0; j<h; j++){
        wj = w*j;
        res[wj] = 255;
        res[wj+(w-1)] = 255;
        }
    for(i =0; i<w;i++){
        res[i] = 255;
        res[wh-(i+1)] = 255;
    }
    for(j = 1; j<h-1; j++){

        for(i = 1; i<w-1;i++){
            current = j*w+i;
            current_minus_w = current - w;
            corner = data[current_minus_w - 1] - data[current + w + 1];
            x = data[current_minus_w + 1];
            y = data[current + w - 1];
            tmpx = 2*data[current-1] - 2*data[current+1] + corner + y - x;
            tmpy = 2*data[current_minus_w] - 2*data[current+w] + corner + x - y;
            res[current] =  abs(tmpx) + abs(tmpy);
        }
    }
    return res;
}

void free_p(){
    free(res);
}
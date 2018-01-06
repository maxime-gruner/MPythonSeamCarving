#include<stdlib.h>
#include<stdio.h>

int* res;

int* getPath(int w, int h, int* data){
    int wh = w*h;
    int i,j,tmp,upper_pixel,wi, bottom_line = 0;
    int* val = calloc(wh, sizeof(int));
    int* parent = malloc(wh*sizeof(int));
    for(i=1; i<w; i++) val[wh-i] = data[wh-i];
    for(i=w;i<wh;i+=w){
        for(j=1;j<w-1;j++){
            tmp = i+j;
            upper_pixel = tmp+w;
            if(val[upper_pixel-1]<val[upper_pixel] && val[upper_pixel-1]<val[upper_pixel+1]){
                val[tmp] = data[tmp] + val[upper_pixel-1];
                parent[tmp] = upper_pixel-1;
            }
            else if(val[upper_pixel+1]<val[upper_pixel]){
                val[tmp] = data[tmp] + val[upper_pixel+1];
                parent[tmp] = upper_pixel+1;
            }
            else {
                val[tmp] = data[tmp] + val[upper_pixel];
                parent[tmp] = upper_pixel;
            }
        }
        val[i]=val[bottom_line]+255;
        parent[i] = bottom_line;
        val[i+j]=val[bottom_line+j]+255;
        parent[i+j] = bottom_line+j;
        bottom_line = i;
    }
    int min = val[w+1];
    int pos = 1;
    for(i=2; i<w-1;i++){
        if(val[w+i]<min){
            min = val[w+i];
            pos = i;
        }
    }
    res = malloc(h*sizeof(int));
    res[0] = pos;
    pos = pos+w;
    res[1] = pos;
    for(i=2; i<h;i++){
        pos = parent[pos];
        res[i] = pos;
    }
    free(val);
    free(parent);
    return res;
}


void free_p(){
    free(res);
}

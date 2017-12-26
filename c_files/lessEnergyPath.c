#include<stdlib.h>
#include<stdio.h>

int* res;

int* getPath(int w, int h, int* data){
    int wh = w*h;
    int i,j,tmp,bottom_line,wi;
    int* val = calloc(wh, sizeof(int));
    int* parent = malloc(wh*sizeof(int));
    for(i=1; i<w; i++) val[wh-i] = data[wh-i];
    for(i=h-1;i>=0;i--){
        wi = w*i;
        for(j=1;j<w-1;j++){
            tmp = wi+j;
            bottom_line = tmp+w;
            if(val[bottom_line-1]<val[bottom_line] && val[bottom_line-1]<val[bottom_line+1] && (bottom_line-1)%w!=0){
                val[tmp] = data[tmp] + val[bottom_line-1];
                parent[tmp] = bottom_line-1;
            }
            else if(val[bottom_line+1]<val[bottom_line-1] && val[bottom_line+1]<val[bottom_line+1] && (bottom_line+2)%w!=0){
                val[tmp] = data[tmp] + val[bottom_line+1];
                parent[tmp] = bottom_line+1;
            }
            else {
                val[tmp] = data[tmp] + val[bottom_line];
                parent[tmp] = bottom_line;
            }
        }
        val[wi]=val[wi+1]+1;
        val[wi+j]=val[wi+j-1]+1;
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
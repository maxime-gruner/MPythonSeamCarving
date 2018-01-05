#include<stdlib.h>
#include<stdio.h>

int* res;

int* getPath(int w, int h, int* data, int orientation){
    int i,j,increment1,increment2,fin1,fin2, bord,tmp, res_length, previous_line;
    if(orientation==0){
        increment1 = 1;
        increment2 = w;
        fin1 = w;
        fin2 = w*h;
        bord=h;
        res_length = w;
    }
    else{
        increment1 = w;
        increment2 = 1;
        fin1 = w*h;
        fin2 = w;
        bord = w;
        res_length = h;
    }
    int* val = calloc(w*h, sizeof(int));
    int* parent = calloc(w*h,sizeof(int));
    for(i=0; i<fin2; i+= increment2) val[i]=data[i];
    for(i = increment1; i < fin1 ; i+=increment1){
        for(j=increment2; j<fin2-increment2; j+=increment2){
            tmp = i+j;
            previous_line = tmp-increment1;
            if(val[previous_line-increment2]<val[previous_line] && val[previous_line-increment2]<val[previous_line+increment2]){
                val[tmp] = data[tmp] + val[previous_line-increment2];
                parent[tmp] = previous_line-increment2;
            }
            else if(val[previous_line+increment2]<val[previous_line-increment2] && val[previous_line+increment2]<val[previous_line]){
                val[tmp] = data[tmp] + val[previous_line+increment2];
                parent[tmp] = previous_line+increment2;
            }
            else {
                val[tmp] = data[tmp] + val[previous_line];
                parent[tmp] = previous_line;
            }
        }
        val[i]=val[i-increment1]+255;
        parent[i]=i-increment1;
        val[i+j]=val[i+j-increment1]+255;
        parent[i+j]=val[i+j-increment1];
    }
    int start_pos = (w*(h-1))-2;
    int pos = start_pos;
    int min = val[pos];
    if(orientation==1){
        for(i=0; i<bord-3;i+=increment2){
            if(val[start_pos-i]<min){
                pos = start_pos-i;
                min = val[pos];
            }
        }
    }
    else{
        for(i=0; i<w*(h-2);i+=increment2){
            if(val[start_pos-i]<min){
                pos = start_pos-i;
                min = val[pos];
            }
        }

    }
    res = malloc(res_length*sizeof(int));
    res[res_length-1] = pos+increment1;
    //pos = pos+w;
    res[res_length-2] = pos;
    for(i=res_length-3; i>=0 ; i--){
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
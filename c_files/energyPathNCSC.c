#include<stdlib.h>
#include<stdio.h>

int* res;
int* sum_for_each_path;
int* parent;
int* sum_tab;

int calculatePath(int position,int w, int h, int* data, int current_line){
    if(current_line == h-1) return data[position];
    int next_line = position+w;
    if( data[next_line-1]<data[next_line] && data[next_line-1]< data[next_line+1] ){
        parent[position] = next_line-1;
        if(parent[next_line-1]!=0) return sum_tab[next_line-1];
        sum_tab[position] = data[position]+calculatePath(next_line-1, w, h, data, current_line+1);
        return sum_tab[position];
    }
    if( data[next_line]<=data[next_line+1]){
        parent[position] = next_line;
        if(parent[next_line]!=0) return sum_tab[next_line];
        sum_tab[position] = data[position]+calculatePath(next_line, w, h, data, current_line+1);
        return sum_tab[position];
    }
    else{
        parent[position] = next_line+1;
        if(parent[next_line+1]!=0) return sum_tab[next_line+1];
        sum_tab[position] = data[position]+calculatePath(next_line+1, w, h, data, current_line+1);
        return sum_tab[position];
    }
}

int* getPath(int w, int h, int* data){
    int wh=w*h;
    sum_for_each_path = malloc(w*sizeof(int));
    sum_tab = malloc(wh*sizeof(int));
    parent = calloc(wh,sizeof(int));
    res = malloc(h*sizeof(int));
    for(int i =1; i<w-1; i+=1){
        sum_for_each_path[i]=calculatePath(i,w,h,data,0);
    }
    int min = sum_for_each_path[1];
    int pos = 1;
    for(int i = 2; i<w-1; i++){
        if(sum_for_each_path[i] < min){
            min = sum_for_each_path[i];
            pos = i;
        }
    }
    for(int i=0; i<h-1; i++){
        res[i] = pos;
        pos = parent[pos];
    }
    res[h-1] = pos;
    free(sum_for_each_path);
    free(sum_tab);
    free(parent);
    return res;
}


void free_p(){
    free(res);
}

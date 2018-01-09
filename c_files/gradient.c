#include<stdlib.h>
#include<stdio.h>
#include<math.h>
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


int* calculate_energy_hog(int w, int h, int* data){
    int wh = w*h;
    int i2 = 0,j2=0;
    int i,j,current,current_minus_w,corner,x,y,gx,gy,wj;
    res = malloc(wh*sizeof(int));
    double *angle = calloc(wh,sizeof(double));
    for(j =0; j<h; j++){
        wj = w*j;
        res[wj] = 255;
        res[wj+(w-1)] = 255;
        angle[wj] = 0;
        angle[wj+(w-1)] = 0;
        }
    for(i =0; i<w;i++){
        res[i] = 255;
        res[wh-(i+1)] = 255;

        angle[i] = 0;
        angle[wh-(i+1)] = 0;

    }


    for(j = 1; j<h-1; j++){
        for(i = 1; i<w-1;i++){
            current = j*w+i;
            current_minus_w = current - w;
            corner = data[current_minus_w - 1] - data[current + w + 1];
            x = data[current_minus_w + 1];
            y = data[current + w - 1];
            gx = 2*data[current-1] - 2*data[current+1] + corner + y - x;
            gy = 2*data[current_minus_w] - 2*data[current+w] + corner + x - y;
            res[current] =  abs(gx) + abs(gy);
            if(gx == 0) gx=1; //evite la div par 0
            angle[current] = atan(gy/gx)*(180/M_PI);
        }
    }


    for(j = 5; j<h-6; j++){
        for(i = 5; i<w-6;i++){
            int histo[8] = {0};
            for(j2 = j-5; j2<= j+5; j2++ ){
                for(i2 = i-5; i2 <= i+5; i2++){

                        float d = angle[j2*w+i2] ;
                        if(d < 0) d= d+360;

                        if(d< 22) histo[0] +=  1;
                        else if(d < 67) histo[1] +=  1;
                        else if(d < 112) histo[2] +=  1;
                        else if(d < 157) histo[3] += + 1;
                        else if(d < 202) histo[4] += + 1;
                        else if(d < 247) histo[5] +=  1;
                        else if(d < 292) histo[6] +=  1;
                        else histo[7] += 1;

                }
            }
            int max = -1;
            int save = 0;
            for(i2=0; i2<8;i2++){
                //printf("%d ", histo[i2]);
                if(max < histo[i2]){
                    max = histo[i2];
                    save = i2;
                }

            }
            //printf("\n save: %d \n", save);

            int b = save*45;

            if(b != 0)
                res[current] = res[current]/(b);


        }
    }


    free(angle);

    return res;
}

void free_p(){
    free(res);
}
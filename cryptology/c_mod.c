#include <stdio.h>
int c_pic_map[16][16];

void init(){
    int count = 0;
    for(int i = 0; i < 16; i++)
        for(int j = 0; j < 16; j++)
        {
            c_pic_map[i][j] = count++;
        }
}

void c_str2numpy(unsigned char * str_array, double * out_array, int len){
    int i, a, b;
    for(i = 0;i < len;i++){
        a = str_array[2*i] - 'a';
        b = str_array[2*i+1] - 'a';
        if(a < 0) a = 0;
        out_array[i] = c_pic_map[a][b];
    }
}
#include <stdio.h>
#include <stdlib.h>

#define L3_WIDTH 480
#define L3_HEIGHT 204 
#define L3_STRIDE 1920 

int main() {

  FILE * pFile = NULL; 
  FILE * pUFile = NULL; 
  FILE * pVFile = NULL; 
  int * in_data = NULL;  
  char * unormal = NULL; 
  char * vnormal = NULL; 

  // allocate memory 
  in_data = (int *) malloc(L3_STRIDE*L3_HEIGHT);
  unormal = (char *) malloc(L3_WIDTH*L3_HEIGHT);  
  vnormal = (char *) malloc(L3_WIDTH*L3_HEIGHT); 

  // Get L1 output data
  pFile = fopen("outputimage_dof_l3.bin", "rb"); 
  fread((void*)in_data, 1,  L3_STRIDE*L3_HEIGHT, pFile); 
  fclose(pFile); 

  for (int iter = 0; iter < L3_HEIGHT; iter++) {
    for (int jter = 0; jter < L3_WIDTH; jter++) {
      int apixel = in_data[L3_WIDTH*iter + jter];
      // Get bit 22->31
      int upart = (apixel >> 22) >> 2; // Shift 2 bit to transform to 8bit data 
      // Get bit 12->21
      int vpart = (apixel & 0x003FFFFF) >> 12 >> 2; // Shift 2 bit to transform to 8bit data
      if (apixel > 0 && upart > 0 && vpart > 0) {
        //printf("apixel 0x%X\n", apixel);
        //printf("upart 0x%X\n", upart); 
        //printf("vpart 0x%x\n", vpart);   
      }

      unormal[L3_WIDTH*iter + jter] = upart; 
      vnormal[L3_WIDTH*iter + jter] = vpart; 
    }
  }

  pUFile = fopen("U_L3.bin", "wb"); 
  fwrite(unormal, 1, L3_WIDTH*L3_HEIGHT, pUFile); 
  fclose(pUFile); 

  pVFile = fopen("V_L3.bin", "wb"); 
  fwrite(vnormal, 1, L3_WIDTH*L3_HEIGHT, pVFile); 
  fclose(pVFile); 

  free(unormal); 
  free(vnormal); 
  free(in_data); 
}

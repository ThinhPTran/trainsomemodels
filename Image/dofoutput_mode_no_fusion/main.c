#include <stdio.h>
#include <stdlib.h>

#define L1_WIDTH 960 
#define L1_HEIGHT 408 
#define L1_STRIDE 3840 

int main() {

  FILE * pFile = NULL; 
  FILE * pUFile = NULL; 
  FILE * pVFile = NULL; 
  FILE * pUFR0FILE = NULL; 
  FILE * pVFR10FILE = NULL; 
  int * in_data = NULL;  
  char * unormal = NULL; 
  char * vnormal = NULL; 
  char * ufrom0 = NULL; 
  char * vfrom10 = NULL; 

  // allocate memory 
  in_data = (int *) malloc(L1_STRIDE*L1_HEIGHT);
  unormal = (char *) malloc(L1_WIDTH*L1_HEIGHT);  
  vnormal = (char *) malloc(L1_WIDTH*L1_HEIGHT); 
  ufrom0 = (char *) malloc(L1_WIDTH*L1_HEIGHT); 
  vfrom10 = (char *) malloc(L1_WIDTH*L1_HEIGHT); 

  // Get L1 output data
  pFile = fopen("outputimage_dof_l1.bin", "rb"); 
  fread((void*)in_data, 1,  L1_STRIDE*L1_HEIGHT, pFile); 
  fclose(pFile); 

  for (int iter = 0; iter < L1_HEIGHT; iter++) {
    for (int jter = 0; jter < L1_WIDTH; jter++) {
      int apixel = in_data[L1_WIDTH*iter + jter];
      // Get bit 22->31
      int upart = (apixel >> 22) >> 2; // Shift 2 bit to transform to 8bit data 
      // Get bit 12->21
      int vpart = (apixel & 0x003FFFFF) >> 12 >> 2; // Shift 2 bit to transform to 8bit data
      if (apixel > 0 && upart > 0 && vpart > 0) {
        //printf("apixel 0x%X\n", apixel);
        //printf("upart 0x%X\n", upart); 
        //printf("vpart 0x%x\n", vpart);   
      }

      int upartfrom0 = (apixel & 0x000003FF) >> 2; // Shift 2 bit to transform to 8bit data
      int vpartfrom10 = ((apixel >> 10) & 0x000003FF) >> 2; 

      unormal[L1_WIDTH*iter + jter] = upart; 
      vnormal[L1_WIDTH*iter + jter] = vpart; 
      ufrom0[L1_WIDTH*iter + jter] = upartfrom0; 
      vfrom10[L1_WIDTH*iter + jter] = vpartfrom10; 
    }
  }

  pUFile = fopen("U_L1.bin", "wb"); 
  fwrite(unormal, 1, L1_WIDTH*L1_HEIGHT, pUFile); 
  fclose(pUFile); 

  pVFile = fopen("V_L1.bin", "wb"); 
  fwrite(vnormal, 1, L1_WIDTH*L1_HEIGHT, pVFile); 
  fclose(pVFile); 

  pUFR0FILE = fopen("U_L1_From0.bin", "wb"); 
  fwrite(ufrom0, 1, L1_WIDTH*L1_HEIGHT, pUFR0FILE); 
  fclose(pUFR0FILE); 

  pVFR10FILE = fopen("V_L1_From10.bin", "wb"); 
  fwrite(vfrom10, 1, L1_WIDTH*L1_HEIGHT, pVFR10FILE); 
  fclose(pVFR10FILE);

  free(ufrom0); 
  free(vfrom10); 
  free(unormal); 
  free(vnormal); 
  free(in_data); 
}

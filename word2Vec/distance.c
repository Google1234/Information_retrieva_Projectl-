//  Copyright 2013 Google Inc. All Rights Reserved.
//
//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

//根据GOOGLE distance.c 文件更改，版权仍归GOOGLE COMPANG 所有
//作者 jiangtao
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <malloc.h>

const long long max_size = 2000;         // max length of strings
const long long N = 40;                  // number of closest words that will be shown
const long long max_w = 50;              // max length of vocabulary entries

char *bestw[40];
char file_name[2000], st[100][2000];
float dist, len, bestd[40], vec[2000];
long long words, size, a, b, c, d, cn, bi[100];
char ch;
float *M;
char *vocab;

struct RESULT{
    char *bestw[40];
    float bestd[40];
    int length;
};

//int main(int argc, char **argv) {
int loadFile(char filename[max_size]) {
  FILE *f;
  //extern char st1[max_size];

  //if (argc < 2) {
    //printf("Usage: ./distance <FILE>\nwhere FILE contains word projections in the BINARY FORMAT\n");
    //return 0;
  //}
  //strcpy(file_name, argv[1]);
  f = fopen(filename, "rb");
  printf ("%s\n",filename);
  //f = fopen(file_name, "rb");
  if (f == NULL) {
    printf("Input file not found\n");
    return -1;
  }
  fscanf(f, "%lld", &words);
  fscanf(f, "%lld", &size);
  vocab = (char *)malloc((long long)words * max_w * sizeof(char));
  for (a = 0; a < N; a++) bestw[a] = (char *)malloc(max_size * sizeof(char));
  M = (float *)malloc((long long)words * (long long)size * sizeof(float));
  if (M == NULL) {
    printf("Cannot allocate memory: %lld MB    %lld  %lld\n", (long long)words * size * sizeof(float) / 1048576, words, size);
    return -1;
  }
  for (b = 0; b < words; b++) {
    a = 0;
    while (1) {
      vocab[b * max_w + a] = fgetc(f);
      if (feof(f) || (vocab[b * max_w + a] == ' ')) break;
      if ((a < max_w) && (vocab[b * max_w + a] != '\n')) a++;
    }
    vocab[b * max_w + a] = 0;
    for (a = 0; a < size; a++) fread(&M[a + b * size], sizeof(float), 1, f);
    len = 0;
    for (a = 0; a < size; a++) len += M[a + b * size] * M[a + b * size];
    len = sqrt(len);
    for (a = 0; a < size; a++) M[a + b * size] /= len;
  }
  fclose(f);

  return 0;
}
struct RESULT cal(char st1[max_size])
 {
        struct RESULT result;

        for (a = 0; a < N; a++) bestd[a] = 0;
        for (a = 0; a < N; a++) bestw[a][0] = 0;
        //printf("Enter word or sentence (EXIT to break): ");
        //a = 0;
        //while (1) {
          //st1[a] = fgetc(stdin);
          //if ((st1[a] == '\n') || (a >= max_size - 1)) {
            //st1[a] = 0;
            //break;
          //}
          //a++;
        //}
        cn = 0;
        b = 0;
        c = 0;
        while (1) {
          st[cn][b] = st1[c];
          b++;
          c++;
          st[cn][b] = 0;
          if (st1[c] == 0) break;
          if (st1[c] == ' ') {
            cn++;
            b = 0;
            c++;
          }
        }
        cn++;
        for (a = 0; a < cn; a++) {
          for (b = 0; b < words; b++) if (!strcmp(&vocab[b * max_w], st[a])) break;
          if (b == words) b = -1;
          bi[a] = b;
          //printf("\nWord: %s  Position in vocabulary: %lld\n", st[a], bi[a]);
          if (b == -1) {
            printf("Out of dictionary word!\n");
            result.length=0;
            break;
          }
        }
        if (b == -1) return  result;
        //printf("\n                                              Word       Cosine distance\n------------------------------------------------------------------------\n");
        for (a = 0; a < size; a++) vec[a] = 0;
        for (b = 0; b < cn; b++) {
          if (bi[b] == -1) continue;
          for (a = 0; a < size; a++) vec[a] += M[a + bi[b] * size];
        }
        len = 0;
        for (a = 0; a < size; a++) len += vec[a] * vec[a];
        len = sqrt(len);
        for (a = 0; a < size; a++) vec[a] /= len;
        for (a = 0; a < N; a++) bestd[a] = -1;
        for (a = 0; a < N; a++) bestw[a][0] = 0;
        for (c = 0; c < words; c++) {
          a = 0;
          for (b = 0; b < cn; b++) if (bi[b] == c) a = 1;
          if (a == 1) continue;
          dist = 0;
          for (a = 0; a < size; a++) dist += vec[a] * M[a + c * size];
          for (a = 0; a < N; a++) {
            if (dist > bestd[a]) {
              for (d = N - 1; d > a; d--) {
                bestd[d] = bestd[d - 1];
                strcpy(bestw[d], bestw[d - 1]);
              }
              bestd[a] = dist;
              strcpy(bestw[a], &vocab[c * max_w]);
              break;
            }
          }
        }

        //for (a = 0; a < N; a++) printf("%50s\t\t%f\n", bestw[a], bestd[a]);

        for (a = 0; a < N; a++)
        {
            result.bestw[a]=bestw[a];
            result.bestd[a]=bestd[a];
        }
        result.length=N;
        return result;
}
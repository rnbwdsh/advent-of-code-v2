#include <stdio.h>


void bubble_sort(int* arr, int cur_line) {
  for (int i = 0; i < cur_line; i++) {
    for (int j = 0; j < cur_line - i - 1; j++) {
      if (arr[j] > arr[j + 1]) {
        int temp = arr[j];
        arr[j] = arr[j + 1];
        arr[j + 1] = temp;
      }
    }
  }
}

int read_num(char* curr, FILE* f) {
  int curr_num = 0;
  unsigned int read_ret = 1;
  while (*curr != ' ' && *curr != '\n' && read_ret) {
    curr_num = curr_num * 10 + *curr - '0';
    read_ret = fread(curr, 1, 1, f);
  }
  return curr_num;
}

int count_in_until(const int i, const int* arr, int curr_line)
{
  int total = 0;
  for (int j = 0; j < curr_line; j++) {
    if (arr[j] == i) {
      total++;
    }
  }
  return total;
}

void main(int argc, char** argv) {
  int left[1000];
  int right[1000];
  char curr;
  int curr_line = 0;
  unsigned int read_ret = 0;

  FILE* f = fopen("01.in", "r");
  read_ret = fread(&curr, 1, 1, f);
  while (read_ret) {
    left[curr_line] = read_num(&curr, f);
    // consume all spaces
    while (curr == ' ') {
      fread(&curr, 1, 1, f);
    }
    right[curr_line] = read_num(&curr, f);
    curr_line++;
    read_ret = fread(&curr, 1, 1, f);
  }
  // bubble sort left and right up to curLine
  bubble_sort(left, curr_line);
  bubble_sort(right, curr_line);
  int sum = 0;

  if(argc > 1)
  {
    // sum up left * right
    for (int i = 0; i < curr_line; i++) {
      int diff = left[i] - right[i];
      if (diff < 0) {
        diff = -diff;
      }
      sum += diff;
    }
  } else
  {
    for (int i = 0; i < curr_line; i++) {
      int cnt = count_in_until(left[i], right, curr_line);
      sum += left[i] * cnt;
    }
  }
  printf("%d\n", sum);
}

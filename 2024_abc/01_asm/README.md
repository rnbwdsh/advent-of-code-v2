Compile and run via

```bash
nasm -f elf64 -g -F dwarf -o 01_a.o 01_a.asm
gcc -no-pie -o 01_a 01_a.o -lc -g
./01_a

nasm -f elf64 -g -F dwarf -o 01_b.o 01_b.asm
gcc -no-pie -o 01_b 01_b.o -lc -g
./01_b

rm 01_a 01_a.o 01_b 01_b.o
```
awk -v RS= -f 03_a.awk 03.in
grep -oP 'mul\(\K\d{1,3},\d{1,3}(?=\))' 03.in | sed 's/,/*/g' | bc | paste -sd+ - | bc
awk -v RS= -f 03_b.awk 03.in

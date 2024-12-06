fid = fopen('04.in', 'r');
fc = fread(fid, '*char')';
m = strsplit(fc, '\n');
needle = "MAS";

total = 0;
im = length(m);
jm = length(m{1});

% Boolean findDiagonal (char[][] m, int i, int j, int di, int dj, String needle, int im, int jm)
function found = findDiagonal(m, i, j, needle)
    found = false;
    if m{i}(j) == needle(2)
        top_left = m{i-1}(j-1);
        top_right = m{i-1}(j+1);
        bottom_left = m{i+1}(j-1);
        bottom_right = m{i+1}(j+1);
        diag1 = (top_left == needle(1) && bottom_right == needle(3)) || (top_left == needle(3) && bottom_right == needle(1));
        diag2 = (top_right == needle(1) && bottom_left == needle(3)) || (top_right == needle(3) && bottom_left == needle(1));
        if diag1 && diag2
            found = true;
        end
    end
end

for i = 2:im-1
    for j = 2:jm-1
        if findDiagonal(m, i, j, needle)
            total = total + 1;
        end
    end
end

disp(total)

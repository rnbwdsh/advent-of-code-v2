fid = fopen('04.in', 'r');
fc = fread(fid, '*char')';
m = strsplit(fc, '\n');
needle = "XMAS";

total = 0;
im = length(m);
jm = length(m{1});

% Boolean findDiagonal (char[][] m, int i, int j, int di, int dj, String needle, int im, int jm)
function found = findDiagonal(m, i, j, di, dj, needle, im, jm)
    found = true;

    for k = 0:length(needle)-1
        ia = i + di * k;
        ja = j + dj * k;

        if ia <= 0 || ja <= 0 || ia > im || ja > jm || m{ia}(ja) ~= needle(k+1)
            found = false;
            break;
        end
    end
end

for i = 1:im
    for j = 1:jm
        for di = -1:1
            for dj = -1:1
                if findDiagonal(m, i, j, di, dj, needle, im, jm)
                    total = total + 1;
                end
            end
        end
    end
end

total
import numpy as np
from sympy.ntheory.modular import crt

def test_13(data, level):
    offset, times = data
    offset, times = int(offset), [int(x) if x.isdigit() else None
                                  for x in times.strip().split(",")]
    if level:  # x % offset_i == -i
        mod_rem = {t: -i for i, t in enumerate(times) if t}
        return int(crt(mod_rem.keys(), mod_rem.values())[0])  # sympy.crt returns (mpz, unrelated-int)
    else:  # some t can be None. -offset % t yields a positive number
        return np.prod(min([[-offset % t, t] for t in times if t]))

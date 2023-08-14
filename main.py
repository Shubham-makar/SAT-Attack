import circuitgraph as cg
from logiclocking import locks, write_key, attacks
import time
import sys
import ast
from deb_miter_attack_mod2_orig import miter_attack_mod_2

key_len = 64
c_orig = cg.from_file(f"E:/SAT_Attack/bench/b14_c.bench")
c_locked = cg.from_file(f"E:/SAT_Attack/bench/b14_c_locked1.v")




open(f"E:/SAT_Attack/results/result.txt", "w").close()

correct_key = miter_attack_mod_2(c_locked, c_orig, f"E:/SAT_Attack/bench/b14_c_locked_key1.txt")
print("correct_key", correct_key['attack_key'])

import circuitgraph as cg
from logiclocking import locks, write_key, attacks
import time

key_len = 64

c3 = cg.from_file(f"E:/SAT_Attack/bench/b22_c.v")
# from_file : Create a new Circuit from a verilog file.
##c3 = cg.from_file(f"E:/SAT_Attack/bench/c6288.v", fmt='bench' )


cl3, k3 = locks.xor_lock(c3, key_len)
# c13 is locked circuit
# k3 is correct key value for each key input

cg.to_file(cl3, f"E:/SAT_Attack/RLL_XOR_Locked/Verilog_files/b22_c_XOR_{key_len}.v")
#  to_file : Write a Circuit to a Verilog file
cg.to_file(cl3, f"E:/SAT_Attack/RLL_XOR_Locked/Bench_files/b22_c_XOR_{key_len}.bench", fmt='bench' )

write_key(k3, f"E:/SAT_Attack/RLL_XOR_Locked/Correct_key_through_which_file_is_locked/b22_c_locked_xor_key{key_len}.txt")
# Write a key dictionary to a file.
start = time.process_time()
result = attacks.miter_attack(cl3, k3, verbose=True, code_on_error=False)
attack_time = time.process_time() - start
print("attack time - ", attack_time)
print("Number of SAT iterations = ", result['Iterations'])
print(k3)
##print(result['dis'])
try:
    geeky_file = open(f'E:/SAT_Attack/results/b22_c_xor_{key_len}_result.txt', 'wt')
    geeky_file.write(str(result))
    geeky_file.close()
    print("Able to write to file")
except:
    print("Unable to write to file")
import circuitgraph as cg

from cnf_func import cnf

c_orig = cg.from_file(f"E:/SAT_Attack/bench/cx2.v")
# open(f"E:/SAT_Attack/results/cnf_file.txt", "w").close()

#cnf_formula = cnf(f"E:/SAT_Attack/bench/b14_c.bench")
#cnf_formula = cnf(c_orig)

cnf_para = cnf(c_orig)
print(cnf_para)
#cnf_variables, cnf_formula = cnf(c_orig)
#print(cnf_variables, cnf_formula)


try:
    geeky_file = open(f'E:/SAT_Attack/results/cx2.txt', 'wt')
    geeky_file.write(str(cnf_para))
    geeky_file.close()
    print("Able to write to file")
except:
    print("Unable to write to file")

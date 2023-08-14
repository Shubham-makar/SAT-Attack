"""Apply logic locks to circuits."""
import random
from itertools import product, zip_longest
from random import choice, choices, randint, sample, shuffle

import circuitgraph as cg

def xor_lock(c, keylen, key_prefix="key_", replacement=False):
   
    # create copy to lock
    cl = c.copy()

    # randomly select gates to lock
    if replacement:
        gates = choices(tuple(cl.nodes() - cl.outputs()), k=keylen)
    else:
        gates = sample(tuple(cl.nodes() - cl.outputs()), keylen)

    # insert key gates
    key = {}
    for i, gate in enumerate(gates):
        # select random key value
        key[f"{key_prefix}{i}"] = choice([True, False])

        # create xor/xnor,input
        gate_type = "xnor" if key[f"{key_prefix}{i}"] else "xor"
        fanout = cl.fanout(gate)
        cl.disconnect(gate, fanout)
        cl.add(f"key_gate_{i}", gate_type, fanin=gate, fanout=fanout)
        cl.add(f"{key_prefix}{i}", "input", fanout=f"key_gate_{i}")

    cg.lint(cl)
    #Raise ValueError if circuit has invalid connections or types.
    return cl, key
import circuitgraph
import circuitgraph as cg

def cnf(c):
    """
    Convert circuit to CNF using the Tseitin transformation.

    Parameters
    ----------
    c : Circuit
            Circuit to transform.

    Returns
    -------
    variables : pysat.IDPool
            Formula variable mapping.
    formula : pysat.CNF
            CNF formula.

    """
    try:
        from pysat.formula import CNF, IDPool
    except ImportError as e:
        raise ImportError(
            "Install 'python-sat' to use satisfiability functionality"
        ) from e
    variables = IDPool()
    formula = CNF()

    for n in c.nodes():
        variables.id(n)
        n_type = c.type(n)
        if n_type in ["and", "or", "xor"] and len(c.fanin(n)) == 1:
            n_type = "buf"
        elif n_type in ["nand", "nor", "xnor"] and len(c.fanin(n)) == 1:
            n_type = "not"

        if n_type == "and":
            for f in c.fanin(n):
                formula.append([-variables.id(n), variables.id(f)])
            formula.append([variables.id(n)] + [-variables.id(f) for f in c.fanin(n)])
        elif n_type == "nand":
            for f in c.fanin(n):
                formula.append([variables.id(n), variables.id(f)])
            formula.append([-variables.id(n)] + [-variables.id(f) for f in c.fanin(n)])
        elif n_type == "or":
            for f in c.fanin(n):
                formula.append([variables.id(n), -variables.id(f)])
            formula.append([-variables.id(n)] + [variables.id(f) for f in c.fanin(n)])
        elif n_type == "nor":
            for f in c.fanin(n):
                formula.append([-variables.id(n), -variables.id(f)])
            formula.append([variables.id(n)] + [variables.id(f) for f in c.fanin(n)])
        elif n_type == "not":
            if c.fanin(n):
                f = c.fanin(n).pop()
                formula.append([variables.id(n), variables.id(f)])
                formula.append([-variables.id(n), -variables.id(f)])
        elif n_type in ["buf", "bb_input"]:
            if c.fanin(n):
                f = c.fanin(n).pop()
                formula.append([variables.id(n), -variables.id(f)])
                formula.append([-variables.id(n), variables.id(f)])
        elif n_type in ["xor", "xnor"]:
            # break into hierarchical xors
            nets = list(c.fanin(n))

            # xor gen
            def xor_clauses(a, b, c):
                formula.append([-variables.id(c), -variables.id(b), -variables.id(a)])
                formula.append([-variables.id(c), variables.id(b), variables.id(a)])
                formula.append([variables.id(c), -variables.id(b), variables.id(a)])
                formula.append([variables.id(c), variables.id(b), -variables.id(a)])

            while len(nets) > 2:
                # create new net
                new_net = "xor_" + nets[-2] + "_" + nets[-1]
                variables.id(new_net)

                # add sub xors
                xor_clauses(nets[-2], nets[-1], new_net)

                # remove last 2 nets
                nets = nets[:-2]

                # insert before out
                nets.insert(0, new_net)

            # add final xor
            if n_type == "xor":
                xor_clauses(nets[-2], nets[-1], n)
            else:
                # invert xor
                variables.id(f"xor_inv_{n}")
                xor_clauses(nets[-2], nets[-1], f"xor_inv_{n}")
                formula.append([variables.id(n), variables.id(f"xor_inv_{n}")])
                formula.append([-variables.id(n), -variables.id(f"xor_inv_{n}")])
        elif n_type == "0":
            formula.append([-variables.id(n)])
        elif n_type == "1":
            formula.append([variables.id(n)])
        elif n_type in ["bb_output", "input"]:
            formula.append([variables.id(n), -variables.id(n)])
        else:
            raise ValueError(f"Unknown gate type '{n_type}'")

    return formula, variables
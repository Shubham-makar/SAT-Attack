# SAT-Attack


Implemented the SAT-attack methodology to compromise Logic Encryption techniques like Random Logic Locking (RLL), characterized by various key sizes of 32, 64, and 128 bits for Logic Encryption. Applied the SAT-attack approach to decrypt RLL-encrypted ISCAS’89 and ITC’99 benchmark circuits in order to ascertain the correct encryption key. Analyzed the time required and the number of iterations taken to successfully break the Logic Encryption.

The SAT Attack:
Before 2015, the main focus of most logic locking schemes was on enhancing the degree of output corruption in logic circuits. However, a potent attack method emerged in 2015 known as the SAT attack. This attack leverages boolean satisfiability to undermine the security of a wide array of logic locking schemes. It requires two fundamental components: the locked gate-level netlist and an activated chip (oracle).

In this attack paradigm, a miter circuit is constructed using the locked netlist. This miter circuit incorporates two distinct keys while maintaining the same primary inputs. Clauses are formulated for the miter circuit, and a clause that satisfies the primary input is identified, ensuring distinct outputs for the two keys. This specific satisfying clause is termed a distinguishing input pattern (DIP).

Subsequently, the DIP is applied to the oracle to determine the accurate output. The correct output corresponding to the provided DIP is included as a constraint within the SAT solver. This constraint ensures that for the given DIP, the solver excludes all keys with outputs that deviate from the accurate output. As a result, in a single iteration, multiple keys can be eliminated. This iterative process is conducted until no more DIPs remain. Ultimately, the key that conforms to all the constraints imposed by the DIPs is identified as the correct encryption key.

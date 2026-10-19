import picos as pc
import cvxopt as cvx
import numpy as np
class SDP:
    def solve(self,groups, function, in_dim, out_dim):
        program = pc.Problem()
        I = pc.new_param('I',cvx.spmatrix([1]*in_dim,
                                              range(in_dim),
                                              range(in_dim),
                                              (in_dim,in_dim)))
        X = program.add_variable('X',(in_dim, in_dim),'symmetric') 
        z = program.add_variable('z',1)

        program.add_constraint(I|X <= out_dim)

        program.add_constraint(X >> 0)
        program.add_constraint(X << I)
        if function.is_minmax():
            program.set_objective('min',z)
        else:
            program.set_objective('max',z)

        for group in groups:
            program.add_constraint(function.get_sdp_constraint(group, X, z, out_dim))

        sol = program.solve(verbose = 0,solver='cvxopt')
        e_vals, e_vecs = np.linalg.eig(X.value)
        vecs = []
        for i in range(out_dim):
            vecs.append( np.real(e_vecs[:, np.argsort(e_vals)[-1 - i]]))
        return vecs, z
    
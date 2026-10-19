from src.util.helpers_2d import angle_to_euclidean, euclidean_to_angle
from src.util.helpers_general import projected_variance
import numpy as np
import math
class Sweep:
    def solve(self,groups, function, in_dim, out_dim):
        print('go')
        events = []
        for i in range(len(groups)):
            group_i = groups[i]
            min_vec = group_i.vecs[0]
            min_val = function.get_value_from_pvs(group_i.vals[0], group_i.vals)
            min_is_upper_envelope = True
            for k in range(len(groups)):
                if k!=i:
                    min_val_on_other_group = function.evaluate(min_vec, groups[k])
                    if (min_val<min_val_on_other_group):
                        print('not upper',  [euclidean_to_angle(min_vec), min_val])

                        min_is_upper_envelope = False
                        break
            if min_is_upper_envelope:
                print('upper',  [euclidean_to_angle(min_vec), min_val])
                events.append( [euclidean_to_angle(min_vec), min_val])
            for j in range(i+1,len(groups)):
                group_j = groups[j]
                intersects = function.find_intersects(group_i, group_j)
                for intersect in intersects:
                    if (not np.isnan(intersect[0])):
                        intersect_vec =angle_to_euclidean(intersect[0])
                        intersect_is_upper_envelope = True
                        for k in range(len(groups)):
                            if k!=i and k!= j:
                                intersect_val_on_other_group = function.evaluate(intersect_vec, groups[k])
                                if (intersect[1]<intersect_val_on_other_group):
                                    print('not upper', intersect)
                                    intersect_is_upper_envelope = False
                                    break
                        if intersect_is_upper_envelope:
                            print('upper', intersect)

                            events.append(intersect)
        opt = [0,math.inf]
        for event in events:
            
            if opt[1]>event[1]:
                print('better', event)
                opt = event
            else:
                print(opt[1], '< ', event[1])
        '''
        for event in events:
            if (not np.isnan(event[0])):
                vec = angle_to_euclidean(event[0])
                is_upper_envelope = True
                for group in groups:
                    val = function.evaluate(vec, group)
                    if (abs(event[1]-val)>1e-8 and event[1]<val):
                        is_upper_envelope=False
                        break
                if is_upper_envelope:
                    if (opt[1]>event[1]):
                        opt = event
            '''     
        if ( opt[1] == np.inf):
            print( "FOUT IN SWEEP")
            print(opt)
            for event in events:
                print(event)
        return [angle_to_euclidean(opt[0])], opt[1]

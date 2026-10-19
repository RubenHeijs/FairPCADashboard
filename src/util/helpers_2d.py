import numpy as np

def angle_to_euclidean(alpha):
    return np.array([np.cos(alpha), np.sin(alpha)])

def euclidean_to_angle(vec):
    angle = np.atan2(vec[1],vec[0])
    angle = 2*np.pi+angle if angle < 0 else angle
    return angle

def get_sin_params(A):
    a = A[0,0]
    b = A[1,0]
    c = A[1,1]
    offset = (a + c)/2.0 
    sign = 1.0  if a-c == 0 else np.sign(a-c)
    amplitude =  sign * np.sqrt( (a - c)**2 + (2 * b)**2) / 2.0
    frequency = 2.0
    if(a-c == 0):
        phase = np.pi/2
    else:
        phase = np.arctan(- (2 * b) / (a - c) ) 
    return offset, amplitude, frequency, phase

def projected_variance(x,y, A):
    a = A[0,0]
    b = A[0,1]
    c = A[1,1]
    return(x*a + y*b)*x + (x*b + y*c)*y

def sin_find_zeros(offset, amplitude, frequency, phase):
    alph_1 = (np.arccos(-offset/amplitude)-phase)/frequency
    alph_1 = (alph_1+np.pi)%np.pi
    alph_2 = (-np.arccos(-offset/amplitude)-phase)/frequency
    alph_2 = (alph_2+np.pi)%np.pi
    return [alph_1, alph_2]

def get_sin_params(A):
    a = A[0,0]
    b = A[1,0]
    c = A[1,1]
    offset = (a + c)/2.0 
    sign = 1.0  if a-c == 0 else np.sign(a-c)
    amplitude =  sign * np.sqrt( (a - c)**2 + (2 * b)**2) / 2.0
    frequency = 2.0
    if(a-c == 0):
        phase = np.pi/2
    else:
        phase = np.arctan(- (2 * b) / (a - c) ) 
    return offset, amplitude, frequency, phase
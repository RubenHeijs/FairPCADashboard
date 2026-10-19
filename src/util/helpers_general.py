import numpy as np

def whiten_svd(A):
    # A: (n_samples, n_features)
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    # Construct B
    B = U @ Vt
    return B

def get_angle(vec1, vec2):
    angle =  np.arccos(np.dot(normalize(vec1),normalize(vec2)))
    return angle

def normalize(vec):
    return vec/np.linalg.norm(vec,axis = -1,keepdims=True)

def get_orth_in_dir(vec,dir):
    vec = normalize(vec)
    return normalize(dir - np.dot(vec, dir) * vec)

def get_vec_between_vecs(vec1,vec2,alpha):
    vec2 = vec2 - np.dot(vec1,vec2)*vec1
    return np.cos(alpha)*vec1 + np.sin(alpha)*vec2

def rotate_towards(vec_from, vec_towards, beta):
    orth_towards = get_orth_in_dir(vec_from,vec_towards)
    c = np.cos(beta) * vec_from + np.sin(beta) * orth_towards
    return c

def sin_find_zeros(offset, amplitude, frequency, phase):
    alph_1 = (np.arccos(-offset/amplitude)-phase)/frequency
    alph_1 = (alph_1+np.pi)%np.pi
    alph_2 = (-np.arccos(-offset/amplitude)-phase)/frequency
    alph_2 = (alph_2+np.pi)%np.pi
    return [alph_1, alph_2]

def interpolate(val_in, val_in_min, val_in_max, val_out_min, val_out_max):
    if (val_in_max-val_in_min) == 0 :
        return 0 
    return (val_in-val_in_min) / (val_in_max-val_in_min) * (val_out_max-val_out_min) + val_out_min

def qcolor_to_pv_color(qcolor):
    return (qcolor.redF(), qcolor.greenF(), qcolor.blueF(), qcolor.alphaF())

def qcolor_to_mpl_color(qcolor):
    div = 255
    pv_color = (qcolor.redF()/div, qcolor.greenF()/div, qcolor.blueF()/div, qcolor.alphaF()/div)
    return pv_color
def projected_variance(vec, A):
    return np.sum((vec @ A) * vec, axis=-1)
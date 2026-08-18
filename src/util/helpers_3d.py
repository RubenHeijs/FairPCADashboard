from src.util.helpers_general import normalize, get_angle, get_orth_in_dir, rotate_towards
import numpy as np

def euclidean_to_stereographic(euclidean):
    euclidean = np.asarray(normalize(euclidean))
    x = euclidean[...,0]
    y = euclidean[...,1]
    z = euclidean[...,2]
    p = (x/(1-z))
    q = (y/(1-z))
    return  np.stack([p,q], axis=-1)


def stereographic_to_euclidean(stereographic):
    stereographic = np.asarray(stereographic)
    p = stereographic[...,0]
    q = stereographic[...,1]
    r2 = p**2+q**2
    x = (2*p)/(1+r2)
    y = (2*q)/(1+r2)
    z = (-1 + r2)/(1+r2)
    return np.stack([x,y,z], axis=-1)


def angles_to_euclidean(angles, origin = np.array([1,0,0]), alpha_dir= np.array([0,1,0])):
    #beta is left right, alpha is towards the intersection space
    alpha = angles[0]
    beta = angles[1]
    return np.array(angles_to_euclidean_split(alpha, beta, origin, alpha_dir))

def angles_to_euclidean_split(alpha, beta, origin = np.array([1,0,0]), alpha_dir= np.array([0,1,0])):
    alpha_dir = normalize(alpha_dir)
    origin = normalize(origin)
    beta_dir = np.cross(alpha_dir, origin)
    rotated_to_beta = normalize(rotate_towards(origin, beta_dir, beta ))
    rotated_to_beta_then_alpha = normalize(rotate_towards(rotated_to_beta, alpha_dir, alpha ))
    return rotated_to_beta_then_alpha[0], rotated_to_beta_then_alpha[1], rotated_to_beta_then_alpha[2]

def euclidean_to_angles(euclidean, origin = np.array([1,0,0]), alpha_dir= np.array([0,1,0])):
    alpha_dir = normalize(alpha_dir)
    origin = normalize(origin)
    beta_dir = np.cross(alpha_dir, origin)
    euclidean = normalize(euclidean)
    removed_alpha = normalize(np.dot(euclidean,origin)*origin + np.dot(euclidean,beta_dir)*beta_dir)
    alpha = get_angle(removed_alpha, euclidean)
    beta = get_angle(removed_alpha, origin)
    return np.array([alpha, beta])

def euclidean_to_angles_split(x, y, z, origin = np.array([1,0,0]), alpha_dir= np.array([0,1,0])):
    euclidean = np.array([x,y,z])
    polar = euclidean_to_angles(euclidean, origin, alpha_dir)
    return polar[0], polar[1]

def polar_to_euclidean(polar):
    polar = np.asarray(polar)
    alpha = polar[..., 0]
    beta = polar[..., 1]
    x = np.cos(alpha)
    y = np.sin(alpha) * np.cos(beta)
    z = np.sin(alpha) * np.sin(beta)
    return np.stack([x, y, z], axis=-1)

def euclidean_to_polar(euclidean):
    euclidean = np.asarray(euclidean)
    x = euclidean[..., 0]
    y = euclidean[..., 1]
    z = euclidean[..., 2]
    alpha = np.arccos(x)
    beta = np.arctan2(z, y)
    return np.stack([alpha, beta], axis=-1)


def get_up_orth(vec):
    return get_orth_in_dir(vec, np.array([0,0,1]))

def rotate_around_vec(vec, v, theta):
    vec = np.asarray(vec, dtype=float)
    vec = vec / np.linalg.norm(vec) 
    x, y, z = vec
    c = np.cos(theta)
    s = np.sin(theta)
    C = 1 - c
    R = np.array([
        [c + x*x*C,     x*y*C - z*s,   x*z*C + y*s],
        [y*x*C + z*s,   c + y*y*C,     y*z*C - x*s],
        [z*x*C - y*s,   z*y*C + x*s,   c + z*z*C]
    ])
    return v@R

def get_basis_from_angles(alpha, beta, gamma ):
    v1 = polar_to_euclidean([alpha,beta])
    v2 = rotate_around_vec(v1,get_up_orth(v1),gamma)
    v3 = np.cross(v1,v2)
    return v1,v2,v3

#vectorized PV calculation
def projected_variance(vec, A):
    return np.sum((vec @ A) * vec, axis=-1)
    #a = A[0,0]
    #b = A[1,1]
    #c = A[2,2]
    #d = A[0,1]
    #e = A[0,2]
    #f = A[1,2]
    #return (x*a + y*d + z*e)*x + (x*d + y*b + z*f)*y + (x*e + y*f + z*c)*z

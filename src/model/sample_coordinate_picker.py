from PySide6.QtCore import *
import numpy as np
from src.util.helpers_3d import *
from src.util.helpers_2d import *

from scipy.spatial import ConvexHull, Delaunay
from dataclasses import dataclass
'''
Sets sample vectors and coordinates used for every surface
'''
class SampleCoordinatePicker(QObject):

    resolution_changed = Signal(object)
    @dataclass
    class SurfaceData3D:
        vecs: object
        vec_faces: object
        polar: object
        polar_faces: object
        stereographic: object
        stereographic_faces: object

    @dataclass
    class SurfaceData2D:
        vecs: object
        angles:object

    def __init__(self, n_samples, is_2d):
        super().__init__()
        self.is_2d = is_2d
        self.set_resolution(n_samples)

    def fibonacci_half_sphere(self,n_samples):
        i = np.arange(n_samples)
        golden_angle = np.pi * (3 - np.sqrt(5))  
        z = 1 - (i / (n_samples))     
        radius = np.sqrt(1 - z**2)
        theta = golden_angle * i
        x = np.cos(theta) * radius
        y = np.sin(theta) * radius

        return np.column_stack([x,y,z])
    
    def circle_on_xy(self, n_samples):
        i = np.arange(n_samples)
        z = i*0
        theta = 2 * np.pi * (i / n_samples)
        x = np.cos(theta)
        y = np.sin(theta)
        return np.column_stack([x,y,z])
    def get_vec_faces(self, vecs, n_fib_samples):
        #Construct faces that connect half-sphere only, keep the ring open
        hull = ConvexHull(vecs)
        simplices = []
        for s in hull.simplices: #Dit kan wss beter
            if (s[0]<n_fib_samples or s[1]<n_fib_samples or s[2]<n_fib_samples):
                simplices.append(s) 
        simplices = np.array(simplices)

        vec_faces = np.hstack([
            np.full((simplices.shape[0], 1), 3),
            simplices        
        ]).astype(np.int64).ravel()
        return vec_faces
    def set_resolution(self,n_samples):
        if self.is_2d:
            self.set_resolution_2d(n_samples)
        else :
            self.set_resolution_3d(n_samples)

    def set_resolution_2d(self, n_samples):
        alphas = np.linspace(0,np.pi,n_samples)
        vecs = []
        for alpha in alphas:
            vecs.append(angle_to_euclidean(alpha))
        self.surface_data = self.SurfaceData2D(np.array(vecs), alphas)
        self.resolution_changed.emit(self.surface_data)

    def set_resolution_3d(self, n_samples):
        circle_sample_ratio = 0.2
        n_circle_samples = np.ceil(n_samples*circle_sample_ratio)
        n_fib_samples = n_samples - n_circle_samples 
        fibonacci_vecs = self.fibonacci_half_sphere(n_fib_samples)
        ring_vecs = self.circle_on_xy(n_circle_samples-2)

        vecs = np.vstack([fibonacci_vecs,ring_vecs])
        vec_faces = self.get_vec_faces(vecs, n_fib_samples)


        
        polar = euclidean_to_polar(vecs)
        print(np.min(polar[:,0]),np.max(polar[:,0]), np.min(polar[:,1]),np.max(polar[:,1]))
        polar_corners = np.array([[0,0],[0,np.pi],[np.pi,0],[np.pi,np.pi]])
        polar_coords = np.vstack([polar,polar_corners])
        polar_delauney = Delaunay(polar_coords)
        polar_faces = np.hstack([
            np.full((polar_delauney.simplices.shape[0], 1), 3),
            polar_delauney.simplices        
        ]).astype(np.int64).ravel()

        vecs = np.vstack([vecs, polar_to_euclidean(polar_corners)])
        stereographic = [ euclidean_to_stereographic(vecs), euclidean_to_stereographic(-vecs)]

        self.surface_data = self.SurfaceData3D(vecs, vec_faces, polar_coords, polar_faces, stereographic, vec_faces)
        self.resolution_changed.emit(self.surface_data)

    def get_surface_data(self):
        return self.surface_data
        
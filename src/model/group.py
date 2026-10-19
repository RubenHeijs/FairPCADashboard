from scipy.spatial import distance_matrix
import numpy as np
from src.util.helpers_general import whiten_svd
from PySide6.QtCore import *
from dataclasses import dataclass
from PySide6.QtGui import QColor
class Group(QObject):
    data_changed = Signal(object)
    group_changed = Signal(object)
    delete_requested = Signal(object)
    color_changed = Signal(QColor)
    @dataclass
    class SummaryData:
        label: object
        A: object
        vecs: object
        vals: object
        projected_variances: object

    def __init__(self, init_A, label, color,n_points=20):
        self.label = label
        self.color = color
        super().__init__()
        self.A = init_A
        self.dims = self.A.shape[0]

        self.check_and_update_eigen(init_A)
        self.reroll_data(n_points)

    def check_and_update_eigen(self, A):
        e_vals, e_vecs = np.linalg.eig(A)
        idx = e_vals.argsort()[::-1]
        if (e_vals[idx[-1]]<0 ):
            print('NOT Positive Semi-Definite')
            return False
        self.set_A(A)
        if self.dims!=self.A.shape[0]:
            self.dims = self.A.shape[0]
            self.reroll_data()
        self.set_ED(e_vecs[:,idx],e_vals[idx])
        return True

    def reroll_data(self,n=50):
        data = np.random.normal(0, 1.0, (n,self.dims))
        data = data - data.mean(axis=0)
        self.data_whitened = whiten_svd(data)

        self.adjust_data()
    
    def update_by_A(self, A):
        if(self.check_and_update_eigen(A)):
            self.adjust_data()
            self.group_changed.emit(self.get_summary_data())

    @Slot(QColor)
    def on_color_changed(self, col):
        self.color = col
        self.color_changed.emit(col)
    @Slot(object, object, float)
    def update_by_eig(self,e_vals,e_vecs,var):
        if(len(e_vals)!=len(e_vecs)):
            raise Exception('Invalid input')
        self.set_ED(np.array(e_vecs).T, np.array(e_vals)*var)
        self.retrieve_A()
        self.adjust_data()
        self.group_changed.emit(self.get_summary_data())

    def get_summary_data(self):
        return self.SummaryData(self.label,self.get_A(),self.e_vecs.T,self.e_vals, None)

    def get_label(self):
        return self.label
    
    def set_A(self, new_A):
        self.A = new_A
        
    def set_ED(self, vecs, vals):
        self.e_vals = vals
        self.e_vecs = np.real(vecs)

    def retrieve_A(self):
        self.set_A(self.e_vecs @ np.diag(self.e_vals) @ self.e_vecs.T )
        if self.dims!=self.A.shape[0]:
            self.dims = self.A.shape[0]
            self.reroll_data()
            
    def adjust_data(self):
        D_sqrt = np.diag(np.sqrt(self.e_vals))
        Sigma_sqrt = self.e_vecs @ D_sqrt @ self.e_vecs.T
        self.data = self.data_whitened @ Sigma_sqrt
        self.data_changed.emit(self.data)
        self.max = np.max(np.abs(self.data))
        data_cov = self.data.T@ self.data
        if (not np.allclose(data_cov,self.A,rtol = 1e-10)):
            print('----DATA COLORING FAILED----')
            print('target', self.A)
            print('curren', data_cov)
            print('difference', self.A - data_cov)
            print('-----------------------------')
        self.distance_matrix = distance_matrix(self.data,self.data)

    def get_projected_distance_matrix(self, vec):
        projected_data = (self.data@vec)[:,np.newaxis]
        return distance_matrix(projected_data,projected_data)
    
    def get_current_distance_matrix(self):
        return self.distance_matrix 
    
    def get_PC(self,i_pc):
        return self.e_vecs[:,i_pc]

    def get_lambda(self, i_lambda):
        return self.e_vals[i_lambda]

    def get_max(self):
        return self.max
    
    def get_var(self):
        return self.e_vals.sum()

    def get_evecs(self):
        return self.e_vecs

    def get_evals(self):
        return self.e_vals

    def get_A(self):
        return self.A
    
    def get_data(self):
        return self.data
    def get_color(self):
        return self.color
    @Slot()
    def on_delete_requested(self):
        self.delete_requested.emit(self)
import os.path

from bokeh.plotting import curdoc

DIRNAME = os.path.dirname(__file__)
DATAFILE = os.path.join(DIRNAME,
                        'data',
                        '2D_magnetosphere.csv')
IMGPATH = os.path.join(os.path.basename(DIRNAME),
                        'static',
                        'images')

INIT_KMEANS_FEATURES = ['gap', 'mean', 'zeros', 'partials']
KMEANS_FEATURES = [
    'mean',
    'zeros',
    'partials',
    'gap',
    'spatial_x',
    'spatial_y',
    'spatial_z',
    'm0_density',
    'm1_velocity_0',
    'm1_velocity_1',
    'm1_velocity_2',
    'm1_speed',
    'm2_pressure_diag_0',
    'm2_pressure_diag_1',
    'm2_pressure_diag_2',
    'm2_pressure_offdiag_0',
    'm2_pressure_offdiag_1',
    'm2_pressure_offdiag_2',
    's10_min',
    's10_max','s10_mean',
    's10_median',
    's10_var',
    's10_skew',
    's10_kurt',
    's10_zeros'
]

from model import VDFKmeansModel
from view import VDFKmeansUI

class VDFKmeansApp:
    def __init__(self):
        self.WIDTH = 840
        self.HEIGHT = 600
        self.MARKERSIZE = 12
        self.IMGPATH = IMGPATH

        self.DATAFILE = DATAFILE
        self.MAX_N_CLUSTERS = 10
        self.INIT_N_CLUSTERS = 6
        self.KMEANS_FEATURES = KMEANS_FEATURES
        self.INIT_KMEANS_FEATURES = INIT_KMEANS_FEATURES

        self.model = VDFKmeansModel(self)
        self.ui = VDFKmeansUI(self,
                              self.model.datasource,
                              self.update_cluster_count,
                              self.update_features)

    def update_cluster_count(self, attr, old, new):
        self.model.cluster_count = new

    def update_features(self, attr, old, new):
        self.model.features = new

    def run(self):
        curdoc().add_root(self.ui.layout)
        curdoc().title = "VDF k-means clustering"

VDFKmeansApp().run()

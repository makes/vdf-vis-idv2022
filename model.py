import pandas as pd
from sklearn.cluster import KMeans
from bokeh.models import ColumnDataSource

class VDFKmeansModel:
    def __init__(self, app):
        self.__data = pd.read_csv(app.DATAFILE)
        self.__cluster_count = app.INIT_N_CLUSTERS
        self.__features = app.INIT_KMEANS_FEATURES
        self.__ds = ColumnDataSource(self.compute_kmeans())

    @property
    def datasource(self):
        return self.__ds

    def compute_kmeans(self):
        kmeans = KMeans(n_clusters=self.__cluster_count).fit(self.__data[self.__features].values)
        kmeans_df = pd.DataFrame(self.__data[['fileid', 'cellid', 'spatial_x', 'spatial_y', 'spatial_z', 'pngfile']])
        kmeans_df.insert(2, 'class', kmeans.labels_)

        # Transform classes to strings as Bokeh wants them as strings
        kmeans_df['class'] = ['class_'+str(i) for i in kmeans_df['class']]

        return(kmeans_df)

    def __update(self):
        self.__ds.data = self.compute_kmeans()

    @property
    def cluster_count(self):
        return self.__cluster_count

    @cluster_count.setter
    def cluster_count(self, value):
        self.__cluster_count = value
        self.__update()

    @property
    def features(self):
        return self.__features

    @features.setter
    def features(self, value):
        self.__features = value
        self.__update()

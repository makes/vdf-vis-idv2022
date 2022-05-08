import bokeh
from bokeh.models import HoverTool, Slider, MultiChoice
from bokeh.transform import factor_cmap
from bokeh.palettes import Category10

class VDFKmeansUI:
    def __init__(self, app, datasource, update_cluster_count, update_features):
        tooltip = self.create_vdf_tooltip(app.IMGPATH)
        cmap = self.create_colormap(app.MAX_N_CLUSTERS)
        fig = self.create_figure(datasource,
                                 [tooltip],
                                 app.WIDTH,
                                 app.HEIGHT,
                                 app.MARKERSIZE,
                                 cmap)
        cluster_slider = self.create_cluster_slider("Number of clusters",
                                                    update_cluster_count,
                                                    app.MAX_N_CLUSTERS,
                                                    app.INIT_N_CLUSTERS)
        feature_selector = self.create_feature_selector("Selected features",
                                                        update_features,
                                                        app.KMEANS_FEATURES,
                                                        app.INIT_KMEANS_FEATURES)
        self.__layout = self.create_layout(fig, cluster_slider, feature_selector)

    @property
    def layout(self):
        return self.__layout

    def create_colormap(self, max_n_clusters):
        """Create color map for clusters"""
        classlabels = [f'class_{i}' for i in range(max_n_clusters)]
        return factor_cmap('class',
                           palette = list(Category10[10]),
                           factors=classlabels)

    def create_vdf_tooltip(self, vdf_imgpath):
        """Create hover tooltip to display the cell's VDF"""
        tooltip = f"""
        <div>
            <img
                src="{vdf_imgpath}/@pngfile" alt="@cellid"
                style="margin: 0px 0px 10px 0px; border: 1px solid #000; width: 100px; height: 100px;"
            />
            <div style="font-size: 15px; font-weight: bold;">@cellid</div>
            <div style="font-size: 13px; color: #696;">($x, $y)</div>
        </div>
        """
        return HoverTool(tooltips = tooltip)

    def create_figure(self, datasource, tools, width, height, markersize, colormap):
        fig = bokeh.plotting.figure(title = "2D Magnetosphere",
                                    width = width,
                                    height = height,
                                    tools = tools)

        # Render the data to scatter plot
        fig.circle('spatial_x', 'spatial_z',
                   source = datasource,
                   fill_alpha = 1,
                   size = markersize,
                   fill_color = colormap,
                   line_width = 0)

        fig.toolbar.logo = None
        fig.toolbar_location = None
        return fig

    def create_cluster_slider(self, title, callback, max_n_clusters, init_n_clusters):
        cluster_slider = Slider(start = 2,
                                end = max_n_clusters,
                                value = init_n_clusters,
                                step = 1,
                                title = title)
        cluster_slider.on_change('value', callback)
        return cluster_slider

    def create_feature_selector(self, title, callback, feature_options, init_selection):
        feature_selector = MultiChoice(value = init_selection,
                                       options = feature_options,
                                       title = title)
        feature_selector.on_change('value', callback)
        return feature_selector

    def create_layout(self, fig, cluster_slider, feature_selector):
        widgets = bokeh.layouts.column(cluster_slider, feature_selector)
        layout = bokeh.layouts.row(fig, widgets)
        return layout

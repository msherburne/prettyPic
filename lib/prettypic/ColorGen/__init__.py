from PIL import Image
import pandas as pd
from sklearn.cluster import KMeans, DBSCAN
from sklearn.preprocessing import StandardScaler


def initial_filters(df):
    rows_to_drop = []
    for index, row in df.iterrows():
        if row["r"] < 90 and row["g"] < 90 and row["b"] < 90:
            rows_to_drop.append(index)
        elif row["r"] > 170 and row["g"] > 170 and row["b"] > 170:
            rows_to_drop.append(index)
    filtered_df = df.drop(rows_to_drop)
    return filtered_df


class ColorGenerator:
    def __init__(self, imagePath, initial_filters=initial_filters):
        self.imagePath = imagePath
        self.image = Image.open(imagePath)
        self._imageWidth, self._imageHeight = self.image.size
        self._imagePixels = self.image.load()
        rgb = list(self.image.getdata())
        self.dataframe = initial_filters(pd.DataFrame([
            {"r": pixel[0], "g": pixel[1], "b": pixel[2]} for pixel in list(self.image.getdata())
        ]))
        self._ks = None

    def _normalize(self):
        scaler = StandardScaler()
        scale = scaler.fit_transform(self.dataframe)
        self.scaled_df = pd.DataFrame([
            {"r": pixel[0], "g": pixel[1], "b": pixel[2]} for pixel in list(scale)
        ])

    def _kmeans_df(self, k):
        kmeans = KMeans(n_clusters=k, n_init="auto")
        kmeans.fit(self.scaled_df)
        ks = []
        for i in kmeans.labels_:
            if i not in ks:
                ks.append(i)
        self.ks = ks
        self.scaled_df["cluster"] = kmeans.labels_
        self.dataframe["cluster"] = kmeans.labels_
        return self.dataframe

    def _dbscan_df(self, overdrive):
        cpus = 1
        if overdrive:
            cpus = -1
        dbscan = DBSCAN(eps=.08, n_jobs=cpus)
        dbscan.fit(self.scaled_df)
        ks = []
        for i in dbscan.labels_:
            if i not in ks:
                ks.append(i)
        self.ks = ks
        self.scaled_df["cluster"] = dbscan.labels_
        self.dataframe['cluster'] = dbscan.labels_
        return self.dataframe

    def _find_densist_scale(self):
        largest_set = {
            "cluster": None,
            "size": 0
        }
        for k in self.ks:
            if largest_set["size"] < len(self.dataframe[self.dataframe["cluster"] == k]):
                largest_set["cluster"] = k
                largest_set["size"] = len(
                    self.dataframe[self.dataframe["cluster"] == k])
        self.densist_scale = largest_set["cluster"]
        return largest_set["cluster"]

    def _use_densist_color(self):
        cluster = self._find_densist_scale()
        filtered = self.dataframe[self.dataframe["cluster"] == cluster]
        filtered = filtered.drop(columns=["cluster"])
        r, g, b = round(filtered["r"].mean(
        )), round(filtered["g"].mean()), round(filtered["b"].mean())
        self.color_as_image = Image.new(
            "RGB", (self._imageWidth, self._imageHeight), (r, g, b))
        self.color_as_RGB = f"rgb({r},{g},{b})"
        self.color = (r, g, b)
        return (r, g, b)


def color_from_image(imagePath, algorithm="kmeans", initial_filters=initial_filters, overdrive=False):
    """Turns an image into a plain color

    Parameters
    ----------
    imagePath : str
        path to the image
    algorithm: str
        the algorithm to use for clustering
        - kmeans (default)
        - dbscan
    initial_filters : function
        function to filter out the colors that are not wanted. Should recieve a dataframe with columns: r, g, b and return the same columns filtered down. Used to make sure that megadarks and megawhites are not used in the algorithm.

    Returns
    -------
    ColorGenerator
        ColorGenerator object with the following attributes:
            - color
            - color_as_image
            - color_as_RGB
    """
    colorGen = ColorGenerator(
        imagePath, initial_filters=initial_filters)
    colorGen._normalize()
    if algorithm == "kmeans":
        colorGen._kmeans_df(4)
    elif algorithm == "dbscan":
        colorGen._dbscan_df(overdrive=overdrive)
    else:
        colorGen._kmeans_df(4)
    colorGen._use_densist_color()
    return colorGen

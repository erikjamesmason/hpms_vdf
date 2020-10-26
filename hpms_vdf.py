class ValidationDataframe:
    """
    FHWA has two exports for Validations on HPMS 8.0 webapp.
    One is a shapefile and the other is a table.
    This class allows either to be read with a specific method
    and turned into a dataframe.
    The dataframe can be manipulated/processed like a normal
    Pandas DataFrame, but there are also two plotting methods included
    for ease of comparison between updated validation exports.
    """

    def __init__(self):
        """
        method __init__ to create object
        self.data is for shapefile (shapefile data, table is read separately):

        Example: vd = ValidationData()
        """

        self.data = None

    def get_path(self):
        """
        Method using input() to define filepath and filename.
        Example: C:\\Users\\your_username\\Documents\\Validations_shapefile\\SHAPE_4\\Validation_Results.shp
        then assign to variable like shp_path = vd.get_path
        """

        file_path = input()
        file_path = str(file_path)

        return file_path

    def read_shapefile(self, shp_path):
        """
        Read a shapefile into a Pandas dataframe with a 'polyline' column holding
        the geometry information. This uses the pyshp package
        Credit: https://gist.github.com/aerispaha/f098916ac041c286ae92d037ba5c37ba

        Example: vdf = vd.read_shapefile(shp_path)
        """

        import shapefile
        import pandas as pd
        import numpy as np

        # read file, parse out the records and shapes
        sf = shapefile.Reader(shp_path)
        fields = [x[0] for x in sf.fields][1:]
        records = sf.records()
        shps = [s.points for s in sf.shapes()]

        # write into a dataframe
        data = pd.DataFrame(columns=fields, data=records)
        self.data = data
        self.data = self.data.assign(polyline=shps)
        return self.data

    def read_table(self, table_path):
        """
        Simple method to read HPMS 8.0 Validations Table export.
        The use of the pipe "|" deliminter is necessary for their export
        Example: tdf = vd.read_table(tbl_path)
        """

        tdf = pd.read_csv(table_path, delimiter="|")
        return tdf

    def px_plot(self, df, column):
        """
        Using Plotly Express, this method produces a Histogram
        based upon the argment df (dataframe) and column (values to be counted)

        Example: vd.px_plot(vdf, "DATA_ITEM")
        """

        import plotly.express as px

        fig = px.histogram(df[column])
        fig.show()

    def px_compare(self, df, compare_df, column):
        """
        Using Plotly Express, this method compares two Dataframes with matching columns.
        This is useful to track progress between data uploads to HPMS 8.0

        Example: vd.px_compare(updated_vdf, original_vdf, "DATA_ITEM")
        """

        import plotly.graph_objects as go

        fig = go.Figure(data=[go.Bar(name='updated',
                                     x=df[column].unique(),
                                     y=df[column].value_counts()),
                              go.Bar(name='original',
                                     x=compare_df[column].unique(),
                                     y=compare_df[column].value_counts())])
        # Change the bar mode
        fig.update_layout(barmode='group')
        fig.show()

    def plt_plot(self, df, column):
        """
        Using Matplotlib, this method produces a Histogram
        based upon the argment df (dataframe) and column (values to be counted)

        Example: ValidationData.plt_plot(vdf, "DATA_ITEM")
        """

        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt

        p = plt.hist(df[column])
        plt.xticks(rotation='vertical')

        plt.show()

    def plt_compare(self, df, compare_df, column):
        """
        Using Matplotlib, this method compares two Dataframes with matching columns.
        This is useful to track progress between data uploads to HPMS 8.0
        Example: vd.plt_compare(updated_vdf, original_vdf, "DATA_ITEM")
        """

        import numpy as np
        import matplotlib
        import matplotlib.pyplot as plt

        labels = df[column].unique()

        x = np.arange(len(labels))  # the label locations
        width = 0.35  # the width of the bars

        fig, ax = plt.subplots()
        rects1 = ax.bar(x - width / 2, df[column].value_counts(), width, label='Updated')
        rects2 = ax.bar(x + width / 2, compare_df[column].value_counts(), width, label='Original')

        ax.set_ylabel('Data Item Count')
        ax.set_title('Validation DataFrame Comparison')
        ax.set_xticks(x)
        ax.set_xticklabels(labels)
        ax.legend()

        def autolabel(rects):
            """Attach a text label above each bar in *rects*, displaying its height."""
            for rect in rects:
                height = rect.get_height()
                ax.annotate('{}'.format(height),
                            xy=(rect.get_x() + rect.get_width() / 2,
                                height),
                            xytext=(0, 3),  # 3 points vertical offset
                            textcoords="offset points",
                            ha='center', va='bottom')

        autolabel(rects1)
        autolabel(rects2)

        fig.tight_layout()
        plt.xticks(rotation='vertical')
        fig.set_size_inches((15, 8))

        plt.show()
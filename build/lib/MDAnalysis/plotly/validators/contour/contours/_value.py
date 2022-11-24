import _plotly_utils.basevalidators


class ValueValidator(_plotly_utils.basevalidators.AnyValidator):
    def __init__(self, plotly_name="value", parent_name="contour.contours", **kwargs):
        super(ValueValidator, self).__init__(
            plotly_name=plotly_name,
            parent_name=parent_name,
            edit_type=kwargs.pop("edit_type", "calc"),
            **kwargs,
        )

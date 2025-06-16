import datetime

from django.contrib.admin import SimpleListFilter


def default_date_filter_gen(
        title="Date",
        parameter_name="delivery_date",
        filter_queryset=True,
        filter_path="delivery_date",
        default_date_func=None,
        distinct=None,
        is_datetime=True,
        is_filter_default=True,
        template="admin/inputdatefilter.html",
):
    """
    Generate a date filter with improved template.

    Parameters
    ----------
    title: basestring, optional
        Title to be displayed above filter.
    parameter_name: basestring, optional
        str that would be used in query params of url
    filter_path: basestring, optional
        Model field name, use '__' if nested field, by default parameter name is used
    filter_queryset: bool, optional
        To filter the queryset or not.
    default_date_func: optional
        function that returns datetime.date obj representing default date.
    distinct: bool, optional
        Filtering on nested field date may produce duplicated result, this is to prevent that.
        (By default distinct is True whenever a nested field is found)
    is_datetime: bool, optional
        Pass true if target field is datetime
    is_filter_default: bool, optional
        Controls whether records are filtered by default or not.
    template:
        specify template used to specify filter.
        In case when default is not working fine use admindatewidgetfilter.html.
        AdminDateWidget JS need to loaded on page for this to work

    Returns
    -------
    InputDateFilter

    """
    if distinct is None:
        if parameter_name.find("__") != -1:
            distinct = True
        else:
            distinct = False

    class InputDateFilter(SimpleListFilter):
        def __init__(self, request, params, model, model_admin):
            self.title = title
            self.parameter_name = parameter_name
            self.filter_path = filter_path
            self.template = template

            super().__init__(request, params, model, model_admin)

        def lookups(self, request, model_admin):
            return [()]

        def choices(self, changelist):
            # Grab only the "all" option.
            all_choice = next(
                super().choices(changelist)
            )  # next(super().choices(changelist))
            all_choice["query_parts"] = (
                (k, v) for k, v in changelist.params.items() if k != self.parameter_name
            )

            if default_date_func:
                default_date = default_date_func()
            else:
                default_date = datetime.date.today()
            if is_filter_default:
                all_choice["date"] = str(default_date)
            else:
                all_choice["date"] = None

            yield all_choice

        def queryset(self, request, queryset, **kwargs):
            filter_date = self.value()  # Get the selected date from the filter
            if filter_date is None:
                filter_date = datetime.date.today()  # Default to today's date if no value is selected

            return queryset.filter(delivery_date=filter_date)

    return InputDateFilter
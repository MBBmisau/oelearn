from django.conf import settings

class TablePaginationMixin:

    def get_table_pagination(self, table):
        return dict(per_page=settings.TABLE_ROWS_PER_PAGE)

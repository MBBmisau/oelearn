from django_tables2 import Table
from django.conf import settings

import itertools

class MainTable(Table):
    icon = None

    def get_table_icon(self):
        return self.icon

    def get_table_title(self):
        return self.table_title

    def render_sn(self):
        self.row_counter = getattr(self, 'row_counter', itertools.count(self.page.start_index()))
        return next(self.row_counter + 1)

    class Meta:
        template_name = "tables/main_table.html"

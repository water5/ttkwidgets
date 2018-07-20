# -*- coding: utf-8 -*-

# Copyright (c) Juliette Monsel 2017
# For license see LICENSE

from ttkwidgets import Table
from tests import BaseWidgetTest


class TestTable(BaseWidgetTest):
    def test_table_init(self):
        table = Table(self.window, drag_cols=False, sortable=False)
        table.pack()
        self.window.update()

    def test_table_get_set(self):
        table = Table(self.window, columns=('A', 'B', 'C'))
        table.pack()
        self.window.update()

        self.assertTrue(table.cget('sortable'))
        self.assertTrue(table['drag_cols'])
        self.assertEqual(table.cget('columns'), ('A', 'B', 'C'))
        self.assertTrue(table.heading('A', 'command'))

        table.configure(sortable=False)
        self.assertFalse(table._sortable)
        self.assertFalse(table.heading('A', 'command'))
        table.configure(drag_cols=False)
        self.assertFalse(table._drag_cols)
        table.configure(sortable=True)
        self.assertTrue(table._sortable)
        table.configure(drag_cols=True)
        self.assertTrue(table._drag_cols)

        self.assertEqual(table.config('sortable'), ('sortable', table._sortable))
        self.assertEqual(table.config('drag_cols'), ('drag_cols', table._drag_cols))

    def test_table_visual_drag(self):
        table = Table(self.window, columns=('A', 'B', 'C'))
        table.pack()
        self.window.update()

        self.assertEqual(table._visual_drag.cget('columns'), ('A', 'B', 'C'))
        table.configure(columns=('E', 'F', 'G'))
        self.assertEqual(table.cget('columns'), ('E', 'F', 'G'))
        self.assertEqual(table._visual_drag.cget('columns'), ('E', 'F', 'G'))

        for i in range(20):
            table.insert('', 'end', str(i), values=tuple(a + str(i) for a in 'EFG'))

        self.assertEqual(table.get_children(""), table._visual_drag.get_children(""))

        table.delete('0', '2')
        self.assertFalse('2' in table._visual_drag.get_children(""))
        self.assertEqual(table.get_children(""), table._visual_drag.get_children(""))

        table.detach('1', '7')
        self.assertFalse('1' in table._visual_drag.get_children(""))
        self.assertEqual(table.get_children(""), table._visual_drag.get_children(""))
        table.reattach('1', '', 0)
        self.assertTrue('1' in table._visual_drag.get_children(""))
        self.assertEqual(table.get_children(""), table._visual_drag.get_children(""))

        table.heading('E', text='col E')
        self.assertEqual(table._visual_drag.heading('E', 'text'), 'col E')

        table.item('4', values=('a', 'b', 'c'), text='4')
        self.assertEqual(table._visual_drag.item('4', 'values'), ('a', 'b', 'c'))
        self.assertEqual(table._visual_drag.item('4', 'text'), '4')

        keys = ['columns',
                'displaycolumns',
                'show',
                'selectmode',
                'height',
                'padding',
                'xscrollcommand',
                'yscrollcommand',
                'takefocus',
                'cursor',
                'style',
                'class',
                'sortable',
                'drag_cols']
        self.assertEqual(sorted(table.keys()), sorted(keys))

        table.move('4', '', 0)
        self.assertEqual(table.get_children('')[0], '4')
        self.assertEqual(table._visual_drag.get_children('')[0], '4')

        table.configure(height=10)
        self.assertEqual(table.bbox('19'), '')
        self.assertEqual(table._visual_drag.bbox('19'), '')

        self.assertEqual(table.set('3', 'F'), 'F3')
        table.set('3', 'F', 'f')
        self.assertEqual(table._visual_drag.set('3', 'F'), 'f')

        table.set_children("", '4', '7')
        self.assertEqual(table.get_children(""), ('4', '7'))
        self.assertEqual(table._visual_drag.get_children(""), ('4', '7'))

    def test_table_sort(self):
        table = Table(self.window, drag_cols=False, sortable=True,
                      columns=list('AB'))

        table.pack()
        for i in range(10):
            table.insert('', 'end', str(i), values=(i, 10 - i))
        self.window.update()
        table.column('A', type=int)

        table._sort_column('A', True)
        self.assertEqual(table.get_children(""), tuple(str(i) for i in range(9, -1, -1)))
        table._sort_column('B', False)
        self.assertEqual(table.get_children(""), ('9', '0', '8', '7', '6', '5', '4', '3', '2', '1'))


    def test_table_drag(self):
        table = Table(self.window, drag_cols=True, sortable=False,
                      columns=list('ABC'))
        table.pack()
        for i in range(10):
            table.insert('', 'end', str(i), values=(i, 10 - i))
        self.window.update()

        table.event_generate('<ButtonPress-1>', x=10, y=5)
        self.window.update()
        self.assertTrue(table._visual_drag.winfo_ismapped())
        table.event_generate('<Motion>', x=10 + table.column('#1', 'width'), y=5)
        table.event_generate('<ButtonRelease-1>')
        self.assertFalse(table._visual_drag.winfo_ismapped())
        self.assertEqual(table['displaycolumns'], ('B', 'A', 'C'))
        table.event_generate('<ButtonPress-1>', x=table.winfo_width() - 20, y=5)
        self.window.update()
        self.assertFalse(table._visual_drag.winfo_ismapped())
        table.event_generate('<ButtonPress-1>', x=table.column('#1', 'width') + 10, y=5)
        self.window.update()
        self.assertTrue(table._visual_drag.winfo_ismapped())
        table.event_generate('<Motion>', x=10, y=5)
        table.event_generate('<ButtonRelease-1>')
        self.assertFalse(table._visual_drag.winfo_ismapped())
        self.assertEqual(table['displaycolumns'], ('A', 'B', 'C'))



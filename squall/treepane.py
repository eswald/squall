r'''Squall schema tree implementation.
    These model classes represent the server, schemas, tables, and columns
    for a given connection.
'''#"""#'''

# Copyright 2012 Eric Wald
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from PyQt4.QtCore import QAbstractItemModel, QModelIndex, Qt
from PyQt4.QtGui import QIcon, QPixmap
import squall.gui.icons_rc

class TreeItem(object):
    icon_name = None
    _icon = None
    
    def __init__(self, data, parent = None):
        self.parentItem = parent
        self.itemData = data
        self.children = list(self.collect())
    
    def row(self):
        if self.parentItem:
            return self.parentItem.children.index(self)
        return 0
    
    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None
    
    def parent(self):
        return self.parentItem
    
    def collect(self):
        r'''Find any children of this node.
            May involve database queries.
        '''#"""#'''
        for n in range(1,3):
            yield Server(["Server "+str(n)], self)
    
    def icon(self):
        if self.icon_name and not self._icon:
            print "Creating icon %s for %s" % (self.icon_name, self.__class__.__name__)
            icon = QIcon()
            icon.addPixmap(QPixmap(self.icon_name), QIcon.Normal, QIcon.Off)
            self.__class__._icon = icon
        return self._icon

class Server(TreeItem):
    icon_name = ":/silk/server.png"
    
    def collect(self):
        for n in range(1,3):
            yield Schema(["Schema "+str(n)], self)

class Schema(TreeItem):
    icon_name = ":/silk/database.png"
    
    def collect(self):
        for n in range(1,5):
            yield Table(["Table "+str(n)], self)

class Table(TreeItem):
    icon_name = ":/silk/table.png"
    
    def collect(self):
        for n in range(1,8):
            yield Column(["Column "+str(n), "int(10) unsigned not null default 1"], self)

class Column(TreeItem):
    # Todo: Consider basing the icon on the data type.
    icon_name = ":/silk/text_columns.png"
    
    def collect(self):
        return []

class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent = None):
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = TreeItem(["Object", "Notes"])
    
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        
        parentItem = parent.internalPointer() if parent.isValid() else self.rootItem
        childItem = parentItem.children[row]
        return self.createIndex(row, column, childItem) if childItem else QModelIndex()
    
    def parent(self, index):
        if not index.isValid():
            return QModelIndex()
        
        parentItem = index.internalPointer().parent()
        if parentItem == self.rootItem:
            return QModelIndex()
        
        return self.createIndex(parentItem.row(), 0, parentItem)
    
    def rowCount(self, parent):
        if parent.column() > 0:
            return 0
        parentItem = parent.internalPointer() if parent.isValid() else self.rootItem
        return len(parentItem.children)
    
    def columnCount(self, parent):
        return 2
    
    def data(self, index, role):
        if index.isValid():
            if role == Qt.DisplayRole:
                return index.internalPointer().data(index.column())
            elif role == Qt.DecorationRole and index.column() == 0:
                return index.internalPointer().icon()
    
    def flags(self, index):
        if not index.isValid():
            return 0
        
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)

def populate(view):
    model = TreeModel(None)
    view.setModel(model)
    return model

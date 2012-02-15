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

from PyQt4.QtCore import QAbstractItemModel, QModelIndex, QString, QVariant, Qt

class TreeItem(object):
    def __init__(self, data, parent = 0):
        self.parentItem = parent
        self.itemData = data
        self.childItems = []
    
    def appendChild(self, child):
        self.childItems.append(child)
    
    def child(self, row):
        return self.childItems[row]
    
    def childCount(self):
        return len(self.childItems)
    
    def row(self):
        if self.parentItem:
            return self.parentItem.childItems.index(self)
        return 0
    
    def columnCount(self):
        return len(self.itemData)
    
    def data(self, column):
        try:
            return self.itemData[column]
        except IndexError:
            return None
    
    def parent(self):
        return self.parentItem

class TreeModel(QAbstractItemModel):
    def __init__(self, data, parent = None):
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = TreeItem(["Title", "Summary"])
        self.setupData(data.split("\n"))
    
    def index(self, row, column, parent):
        if not self.hasIndex(row, column, parent):
            return QModelIndex()
        
        parentItem = parent.internalPointer() if parent.isValid() else self.rootItem
        childItem = parentItem.child(row)
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
        return parentItem.childCount()
    
    def columnCount(self, parent):
        parentItem = parent.internalPointer() if parent.isValid() else self.rootItem
        return parentItem.columnCount()
    
    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        
        if role != Qt.DisplayRole:
            return QVariant()
        
        item = index.internalPointer()
        return item.data(index.column())
    
    def flags(self, index):
        if not index.isValid():
            return 0
        
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable
    
    def headerData(self, section, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.rootItem.data(section)
        
        return QVariant()
    
    def setupData(self, lines):
        parents = [self.rootItem]
        indentations = [0]
        
        for line in lines:
            data = line.strip()
            if data:
                position = line.find(data[0])
                columns = [QString(s.strip()) for s in data.split("  ") if s.strip()]
                if position > indentations[-1]:
                    if parents[-1].childCount() > 0:
                        parents.append(parents[-1].child(parents[-1].childCount() - 1))
                        indentations.append(position)
                else:
                    while position < indentations[-1] and parents:
                        parents.pop()
                        indentations.pop()
                
                parents[-1].appendChild(TreeItem(columns, parents[-1]))

sample_data = r'''
Server 1
    Schema 1
        Table 1
            Column 1    int(10) default null
            Column 2    varchar(80)
            Column 3    blob
            Column 4    tinytext not null
        Table 2
            Column 1
            Column 2
            Column 3
            Column 4
    Schema 2
        Table 1
            Column 1    int(10) default null
            Column 2    varchar(80)
            Column 3    blob
            Column 4    tinytext not null
        Table 2
            Column 1
            Column 2
            Column 3
            Column 4
    Schema 3
        Table 1
            Column 1    int(10) default null
            Column 2    varchar(80)
            Column 3    blob
            Column 4    tinytext not null
        Table 2
            Column 1
            Column 2
            Column 3
            Column 4
Server 2
    Schema 1            More power to you
        Table 1         InnoDB
            Column 1    int(10) default null
            Column 2    varchar(80)
            Column 3    blob
            Column 4    tinytext not null
        Table 2         45 rows
            Column 1
            Column 2
            Column 3
            Column 4
    Schema 2
        Table 1
            Column 1    int(10) default null
            Column 2    varchar(80)
            Column 3    blob
            Column 4    tinytext not null
        Table 2
            Column 1
            Column 2
            Column 3
            Column 4
    Schema 3
        Table 1
            Column 1    int(10) default null
            Column 2    varchar(80)
            Column 3    blob
            Column 4    tinytext not null
        Table 2
            Column 1
            Column 2
            Column 3
            Column 4
'''#"""#'''

def populate(view):
    model = TreeModel(sample_data)
    view.setModel(model)
    return model

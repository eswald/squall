r'''Squall main application
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

from PyQt4.QtGui import QApplication, QMainWindow, QSplitter
from squall.gui.Ui_window import Ui_MainWindow
from squall.gui.Ui_tripane import Ui_Tripane
from squall.treepane import populate
import sys

def main():
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    
    Tripane = QSplitter(MainWindow)
    tripane = Ui_Tripane()
    tripane.setupUi(Tripane)
    MainWindow.setCentralWidget(Tripane)
    
    ui.actionConnect.triggered.connect(lambda *args: populate(tripane.treeView))
    
    MainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

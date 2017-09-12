#
#  Project: MXCuBE
#  https://github.com/mxcube.
#
#  This file is part of MXCuBE software.
#
#  MXCuBE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  MXCuBE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with MXCuBE.  If not, see <http://www.gnu.org/licenses/>.

from QtImport import *

from BlissFramework import Qt4_Icons
from BlissFramework.Qt4_BaseComponents import BlissWidget


__credits__ = ["MXCuBE colaboration"]
__version__ = "2.3"
__category__ = 'General'


class Qt4_ToolsBrick(BlissWidget):
    """
    Descript. : Brick is like a menu in the menuBar or/and in the toolbar
    """
 
    def __init__(self, *args):
        """
        Descript. :
        """
        BlissWidget.__init__(self, *args)

        # Hardware objects ----------------------------------------------------
        self.tools_hwobj = None
        self.action_dict = {}

        # Internal values -----------------------------------------------------

        # Properties ----------------------------------------------------------
        self.addProperty('mnemonic', 'string', '')

        # Signals ------------------------------------------------------------

        # Slots ---------------------------------------------------------------

        # Graphic elements ----------------------------------------------------

        # Layout --------------------------------------------------------------

        # SizePolicies --------------------------------------------------------

        # Qt signal/slot connections ------------------------------------------

        # Other ---------------------------------------------------------------

    def run(self):
        self.tools_menu = QMenu("Tools", self)
        self.tools_menu.addSeparator()
        BlissWidget._menuBar.insert_menu(self.tools_menu, 2)
        self.init_tools()

    def propertyChanged(self, property_name, old_value, new_value):
        """
        """
        if property_name == "mnemonic":
            self.tools_hwobj = self.getHardwareObject(new_value)
        else:
            BlissWidget.propertyChanged(self, property_name, old_value, new_value)

    def set_expert_mode(self, is_expert_mode):
        pass

    def init_tools(self):
        """Gets available methods and populates menubar with methods
           If icon name exists then adds icon
        """
        self.tools_list = self.tools_hwobj.get_tools_list()
        for index, tool in enumerate(self.tools_list):
            if tool == "separator":
                self.tools_menu.addSeparator()
            elif hasattr(tool["hwobj"], tool["method"]):
                temp_action = self.tools_menu.addAction(\
                    tool["display"],
                    self.execute_tool)
                if tool.get("icon"):
                    temp_action.setIcon(Qt4_Icons.load_icon(tool["icon"]))
                self.action_dict[temp_action] = tool

    def execute_tool(self):
        """Executes tool asigned to the menu action
           Asks for a confirmation if a tool has a conformation msg.
        """
        for key in self.action_dict.keys():
            if key == self.sender():
                tool = self.action_dict[key]
                if tool.get("confirmation"):
                    conf_dialog = QMessageBox.warning(None, "Question",
                         tool["confirmation"], QMessageBox.Ok, QMessageBox.Cancel)
                    if conf_dialog == QMessageBox.Ok:
                        getattr(tool["hwobj"], tool["method"])()
                else:
                    getattr(tool["hwobj"], tool["method"])()

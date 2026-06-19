'''
A port of the Explode Geometry .NET plug-in on the ADN-DevTech GitHub:
https://github.com/ADN-DevTech/3dsMax-Explode-Geometry
This example illustrates using PySide in Max, and working with TriObject and Mesh objects

'''

from PySide6 import QtCore, QtWidgets
import pymxs
import qtmax
import random

rt = pymxs.runtime

class _GCProtector(object):
    widgets = []

################## GUI DEFINITION #############################

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setMinimumWidth(320)

        mainLayout = QtWidgets.QVBoxLayout(Form)
        mainLayout.setContentsMargins(10, 10, 10, 10)
        mainLayout.setSpacing(6)

        # Explode Options group box
        self.groupBox = QtWidgets.QGroupBox(Form)
        self.groupBox.setObjectName("groupBox")
        groupBoxLayout = QtWidgets.QVBoxLayout(self.groupBox)

        # Shell modifier row
        shellRow = QtWidgets.QHBoxLayout()
        self.add_shell_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.add_shell_checkbox.setObjectName("add_shell_checkbox")
        shellRow.addWidget(self.add_shell_checkbox)

        self.offset_label = QtWidgets.QLabel(self.groupBox)
        self.offset_label.setFixedWidth(40)
        self.offset_label.setObjectName("offset_label")
        shellRow.addWidget(self.offset_label)

        self.shell_offset = QtWidgets.QDoubleSpinBox(self.groupBox)
        self.shell_offset.setAlignment(QtCore.Qt.AlignCenter)
        self.shell_offset.setMinimum(0.1)
        self.shell_offset.setMaximum(1000.0)
        self.shell_offset.setSingleStep(0.1)
        self.shell_offset.setObjectName("shell_offset")
        shellRow.addWidget(self.shell_offset)
        groupBoxLayout.addLayout(shellRow)

        self.add_edit_mesh_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.add_edit_mesh_checkbox.setObjectName("add_edit_mesh_checkbox")
        groupBoxLayout.addWidget(self.add_edit_mesh_checkbox)

        self.collapse_modifier_stack_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.collapse_modifier_stack_checkbox.setObjectName("collapse_modifier_stack_checkbox")
        groupBoxLayout.addWidget(self.collapse_modifier_stack_checkbox)

        self.center_pivot_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.center_pivot_checkbox.setObjectName("center_pivot_checkbox")
        groupBoxLayout.addWidget(self.center_pivot_checkbox)

        self.delete_original_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.delete_original_checkbox.setObjectName("delete_original_checkbox")
        groupBoxLayout.addWidget(self.delete_original_checkbox)

        # Geometry Type sub-group
        self.groupBox_2 = QtWidgets.QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName("groupBox_2")
        geoTypeLayout = QtWidgets.QHBoxLayout(self.groupBox_2)

        self.trimesh_option = QtWidgets.QRadioButton(self.groupBox_2)
        self.trimesh_option.setChecked(True)
        self.trimesh_option.setObjectName("trimesh_option")
        geoTypeLayout.addWidget(self.trimesh_option)

        self.mnmesh_option = QtWidgets.QRadioButton(self.groupBox_2)
        self.mnmesh_option.setObjectName("mnmesh_option")
        geoTypeLayout.addWidget(self.mnmesh_option)

        groupBoxLayout.addWidget(self.groupBox_2)
        mainLayout.addWidget(self.groupBox)

        # Selection label row
        selRow = QtWidgets.QHBoxLayout()
        self.select_label = QtWidgets.QLabel(Form)
        self.select_label.setFixedSize(QtCore.QSize(100, 35))
        self.select_label.setObjectName("select_label")
        selRow.addWidget(self.select_label)

        self.selected_objects_string = QtWidgets.QLabel(Form)
        self.selected_objects_string.setMinimumHeight(35)
        self.selected_objects_string.setObjectName("selected_objects_string")
        selRow.addWidget(self.selected_objects_string)
        mainLayout.addLayout(selRow)

        # Explode button
        self.explode_button = QtWidgets.QPushButton(Form)
        self.explode_button.setFixedHeight(50)
        self.explode_button.setObjectName("explode_button")
        mainLayout.addWidget(self.explode_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtCore.QCoreApplication.translate("Form", "Explode Geometry"))
        self.groupBox.setTitle(QtCore.QCoreApplication.translate("Form", "Explode Options"))
        self.groupBox_2.setTitle(QtCore.QCoreApplication.translate("Form", "Geometry Type"))
        self.trimesh_option.setText(QtCore.QCoreApplication.translate("Form", "TriMesh"))
        self.mnmesh_option.setText(QtCore.QCoreApplication.translate("Form", "MNMesh"))
        self.add_shell_checkbox.setText(QtCore.QCoreApplication.translate("Form", "Add Shell Modifier    ---->"))
        self.offset_label.setText(QtCore.QCoreApplication.translate("Form", "Offset:"))
        self.add_edit_mesh_checkbox.setText(QtCore.QCoreApplication.translate("Form", "Add Edit Mesh Modifier"))
        self.collapse_modifier_stack_checkbox.setText(QtCore.QCoreApplication.translate("Form", "Collapse Modifier Stack"))
        self.center_pivot_checkbox.setText(QtCore.QCoreApplication.translate("Form", "Center Pivot"))
        self.delete_original_checkbox.setText(QtCore.QCoreApplication.translate("Form", "Delete Original"))
        self.select_label.setText(QtCore.QCoreApplication.translate("Form", "Selected Object(s):"))
        self.selected_objects_string.setText(QtCore.QCoreApplication.translate("Form", "None"))
        self.explode_button.setText(QtCore.QCoreApplication.translate("Form", "Explode"))


''' Form class that allows the user to select options for the script
'''
class Form(QtWidgets.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Form, self).__init__()
        self.setupUi(self)
        _GCProtector.widgets.append(self)
        self.updateSelectionLabel()
        self.explode_button.clicked.connect(self.do_explode)
        rt.callbacks.addScript(rt.Name('selectionSetChanged'), self.updateSelectionLabel, id=rt.Name('explodeGeom'))

    def updateSelectionLabel(self, arg=None):
        nr_of_selected_elements = len(rt.selection)
        if nr_of_selected_elements == 0:
            selection_set = "None"
        elif nr_of_selected_elements == 1:
            selection_set = rt.selection[0].name
        else:
            selection_set = "{} objects selected".format(nr_of_selected_elements)
        self.selected_objects_string.setText(selection_set)

    def do_explode(self):
        addShell = self.add_shell_checkbox.isChecked()
        shell_amount = self.shell_offset.value()
        addEditMesh = self.add_edit_mesh_checkbox.isChecked()
        collapseNode = self.collapse_modifier_stack_checkbox.isChecked()
        centerPivot = self.center_pivot_checkbox.isChecked()
        deleteOriginal = self.delete_original_checkbox.isChecked()
        mode = "TriMesh" if self.trimesh_option.isChecked() else "MNMesh"

        print("[ExplodeGeometry] --- Explode triggered ---")
        print("[ExplodeGeometry] Mode:            {}".format(mode))
        print("[ExplodeGeometry] Add Shell:        {} (offset={})".format(addShell, shell_amount))
        print("[ExplodeGeometry] Add Edit Mesh:    {}".format(addEditMesh))
        print("[ExplodeGeometry] Collapse Stack:   {}".format(collapseNode))
        print("[ExplodeGeometry] Center Pivot:     {}".format(centerPivot))
        print("[ExplodeGeometry] Delete Original:  {}".format(deleteOriginal))
        print("[ExplodeGeometry] Selected objects: {}".format(len(rt.selection)))

        if len(rt.selection) <= 0:
            msg = "Nothing selected. Please select a node to explode."
            print("[ExplodeGeometry] ERROR: {}".format(msg))
            self.show_alert(msg)
        else:
            with pymxs.undo(True, "Explode Geometry"):
                if self.trimesh_option.isChecked():
                    transformation_set = list(rt.selection)
                    print("[ExplodeGeometry] [TriMesh] Processing {} object(s)".format(len(transformation_set)))
                    for i, n in enumerate(transformation_set, 1):
                        print("[ExplodeGeometry] [TriMesh] Object {}/{}: '{}'".format(i, len(transformation_set), n.name))
                        convert_to_triangle_faces(n, addShell, shell_amount,
                                                  addEditMesh, collapseNode,
                                                  centerPivot)
                        if deleteOriginal:
                            print("[ExplodeGeometry] [TriMesh] Deleting original '{}'".format(n.name))
                            rt.delete(n)

                if self.mnmesh_option.isChecked():
                    transformation_set = list(rt.selection)
                    print("[ExplodeGeometry] [MNMesh] Processing {} object(s)".format(len(transformation_set)))
                    for i, node in enumerate(transformation_set, 1):
                        print("[ExplodeGeometry] [MNMesh] Object {}/{}: '{}'".format(i, len(transformation_set), node.name))
                        convert_to_mnmesh_faces(node, addShell, shell_amount,
                                                addEditMesh, collapseNode,
                                                centerPivot)
                        if deleteOriginal:
                            print("[ExplodeGeometry] [MNMesh] Deleting original '{}'".format(node.name))
                            rt.delete(node)

            print("[ExplodeGeometry] Done. Redrawing views.")
            rt.redrawViews()
            rt.callbacks.removeScripts(id=rt.Name('explodeGeom'))
            self.close()

    def show_alert(self, message):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setText(message)
        msgBox.exec()

################## MAIN LOGIC #################################

app = QtWidgets.QApplication.instance()
if not app:
    app = QtWidgets.QApplication([])


def _random_wire_color():
    return rt.Color(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def convert_to_triangle_faces(node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot):
    print("[ExplodeGeometry] [TriMesh] Converting '{}' to mesh...".format(node.name))
    rt.convertToMesh(node)
    # After convertToMesh the stack is collapsed and getVert returns world-space positions
    num_faces = rt.getNumFaces(node)
    print("[ExplodeGeometry] [TriMesh] '{}' has {} face(s) to explode".format(node.name, num_faces))
    for face_idx in range(1, num_faces + 1):
        face = rt.getFace(node, face_idx)
        v1 = rt.getVert(node, int(face.x))
        v2 = rt.getVert(node, int(face.y))
        v3 = rt.getVert(node, int(face.z))
        print("[ExplodeGeometry] [TriMesh] Face {}/{}: verts=({:.2f},{:.2f},{:.2f}) ({:.2f},{:.2f},{:.2f}) ({:.2f},{:.2f},{:.2f})".format(
            face_idx, num_faces, v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, v3.x, v3.y, v3.z))

        new_node = rt.mesh(vertices=rt.Array(v1, v2, v3),
                           faces=rt.Array(rt.Point3(1, 2, 3)))
        rt.update(new_node)
        new_node.wireColor = _random_wire_color()
        print("[ExplodeGeometry] [TriMesh] Created piece '{}' for face {}".format(new_node.name, face_idx))

        applySettings(new_node, addShell, shell_amount,
                      addEditMesh, collapseNode, centerPivot)
    print("[ExplodeGeometry] [TriMesh] Finished exploding '{}'".format(node.name))


def convert_to_mnmesh_faces(node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot):
    print("[ExplodeGeometry] [Poly] Converting '{}' to poly...".format(node.name))
    rt.convertToPoly(node)
    num_faces = rt.polyop.getNumFaces(node)
    print("[ExplodeGeometry] [Poly] '{}' has {} face(s) to explode".format(node.name, num_faces))

    # Detach faces in reverse order so earlier face indices stay valid as later ones are removed.
    # polyop.detachFaces returns a boolean (not the new INode), so we snapshot existing node
    # handles before each detach and find the newly added node by handle exclusion.
    for face_idx in range(num_faces, 0, -1):
        print("[ExplodeGeometry] [Poly] Detaching face {}/{}".format(face_idx, num_faces))
        rt.polyop.detachFaces(node, rt.Array(face_idx), asNode=True) # True/False
        new_node = rt.objects[-1]
        # print (new_node) # Check if the node is valid
        if new_node is None:
            print("[ExplodeGeometry] [Poly] WARNING: Could not find detached node for face {}".format(face_idx))
            continue
        new_node.wireColor = _random_wire_color()
        print("[ExplodeGeometry] [Poly] Created piece '{}' for face {}".format(new_node.name, face_idx))
        applySettings(new_node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot)
    print("[ExplodeGeometry] [Poly] Finished exploding '{}'".format(node.name))


def applySettings(n, addShell, shell_amount, addEditMesh, collapseNode, centerPivot):
    print("[ExplodeGeometry] applySettings on '{}': shell={} (amt={}) editMesh={} collapse={} centerPivot={}".format(
        n.name, addShell, shell_amount, addEditMesh, collapseNode, centerPivot))
    if addShell:
        print("[ExplodeGeometry] Adding Shell modifier (outerAmount={})".format(shell_amount))
        mod = rt.Shell()
        mod.outerAmount = shell_amount
        rt.addModifier(n, mod)

    if addEditMesh:
        print("[ExplodeGeometry] Adding Edit Mesh modifier")
        mod = rt.Edit_Mesh()
        rt.addModifier(n, mod)

    if collapseNode:
        print("[ExplodeGeometry] Collapsing modifier stack")
        rt.maxOps.collapseNode(n, True)

    if centerPivot:
        print("[ExplodeGeometry] Centering pivot")
        rt.centerPivot(n)


def main():
    form = Form()
    form.setParent(qtmax.GetQMaxMainWindow())
    form.setWindowFlags(QtCore.Qt.WindowType.Tool)
    form.show()


if __name__ == '__main__':
    main()

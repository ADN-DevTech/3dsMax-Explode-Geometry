'''
A port of the Explode Geometry .NET plug-in on the ADN-DevTech GitHub:
https://github.com/ADN-DevTech/3dsMax-Explode-Geometry
This example illustrates using PySide in Max, and working with TriObject and Mesh objects

'''

from PySide6 import QtCore, QtWidgets
import pymxs
import qtmax
import random
import logging
import sys
import time

rt = pymxs.runtime

# Logger that pushes messages to the MAXScript Listener (stdout). When the
# "Show Debug Messages" option is enabled the level is lowered to DEBUG so all
# messages flow through; otherwise only WARNING/CRITICAL messages are emitted.
logger = logging.getLogger("ExplodeGeometry")
logger.setLevel(logging.WARNING)
logger.propagate = False
if not logger.handlers:
    _handler = logging.StreamHandler(sys.stdout)
    _handler.setFormatter(logging.Formatter("[ExplodeGeometry] %(levelname)s: %(message)s"))
    logger.addHandler(_handler)

class _GCProtector(object):
    widgets = []

################## GUI DEFINITION #############################

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.setMinimumWidth(400)

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
        self.add_shell_checkbox.setChecked(True)
        shellRow.addWidget(self.add_shell_checkbox)

        self.offset_label = QtWidgets.QLabel(self.groupBox)
        self.offset_label.setObjectName("offset_label")
        self.offset_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
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
        self.delete_original_checkbox.setChecked(True)
        groupBoxLayout.addWidget(self.delete_original_checkbox)

        self.show_debug_checkbox = QtWidgets.QCheckBox(self.groupBox)
        self.show_debug_checkbox.setObjectName("show_debug_checkbox")
        groupBoxLayout.addWidget(self.show_debug_checkbox)

        self.debug_warn_label = QtWidgets.QLabel(self.groupBox)
        self.debug_warn_label.setObjectName("debug_warn_label")
        self.debug_warn_label.setStyleSheet("color: red;")
        self.debug_warn_label.setVisible(False)
        groupBoxLayout.addWidget(self.debug_warn_label)

        # Only show the debug warning label when the debug checkbox is checked
        self.show_debug_checkbox.checkStateChanged.connect(lambda checkState: self.debug_warn_label.setVisible(checkState == QtCore.Qt.Checked))

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

        # Progress panel (hidden by default) -- shown above the explode button
        # only while an explode operation is running.
        self.progress_panel = QtWidgets.QWidget(Form)
        self.progress_panel.setObjectName("progress_panel")
        progressLayout = QtWidgets.QVBoxLayout(self.progress_panel)
        progressLayout.setContentsMargins(0, 4, 0, 0)
        progressLayout.setSpacing(4)

        self.progress_bar = QtWidgets.QProgressBar(self.progress_panel)
        self.progress_bar.setObjectName("progress_bar")
        self.progress_bar.setMinimum(0)
        self.progress_bar.setMaximum(100)
        self.progress_bar.setValue(0)
        progressLayout.addWidget(self.progress_bar)

        nodeNameRow = QtWidgets.QHBoxLayout()
        self.lbl_label_pro_node = QtWidgets.QLabel(self.progress_panel)
        self.lbl_label_pro_node.setObjectName("lbl_label_pro_node")
        nodeNameRow.addWidget(self.lbl_label_pro_node)
        self.lbl_node_name = QtWidgets.QLabel(self.progress_panel)
        self.lbl_node_name.setObjectName("lbl_node_name")
        nodeNameRow.addWidget(self.lbl_node_name)
        nodeNameRow.addStretch()
        progressLayout.addLayout(nodeNameRow)

        counterRow = QtWidgets.QHBoxLayout()
        self.lbl_label_node = QtWidgets.QLabel(self.progress_panel)
        self.lbl_label_node.setObjectName("lbl_label_node")
        counterRow.addWidget(self.lbl_label_node)
        self.lbl_curr_node = QtWidgets.QLabel(self.progress_panel)
        self.lbl_curr_node.setObjectName("lbl_curr_node")
        counterRow.addWidget(self.lbl_curr_node)
        self.lbl_label_of = QtWidgets.QLabel(self.progress_panel)
        self.lbl_label_of.setObjectName("lbl_label_of")
        counterRow.addWidget(self.lbl_label_of)
        self.lbl_tot_node = QtWidgets.QLabel(self.progress_panel)
        self.lbl_tot_node.setObjectName("lbl_tot_node")
        counterRow.addWidget(self.lbl_tot_node)
        counterRow.addStretch()
        progressLayout.addLayout(counterRow)

        self.progress_panel.setVisible(False)
        mainLayout.addWidget(self.progress_panel)

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
        self.show_debug_checkbox.setText(QtCore.QCoreApplication.translate("Form", "Show Debug Messages"))
        self.debug_warn_label.setText(QtCore.QCoreApplication.translate("Form", "NOTE: Debug messages will affect performance."))
        self.select_label.setText(QtCore.QCoreApplication.translate("Form", "Selected Object(s):"))
        self.selected_objects_string.setText(QtCore.QCoreApplication.translate("Form", "None"))
        self.explode_button.setText(QtCore.QCoreApplication.translate("Form", "Explode"))
        self.lbl_label_pro_node.setText(QtCore.QCoreApplication.translate("Form", "Processing Node:"))
        self.lbl_label_node.setText(QtCore.QCoreApplication.translate("Form", "Node:"))
        self.lbl_label_of.setText(QtCore.QCoreApplication.translate("Form", "of"))


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

        # Show all messages when debugging is enabled, otherwise only let
        # warnings and critical messages through to the Listener.
        logger.setLevel(logging.DEBUG if self.show_debug_checkbox.isChecked() else logging.WARNING)

        logger.debug("--- Explode triggered ---")
        logger.debug("Mode:            %s", mode)
        logger.debug("Add Shell:        %s (offset=%s)", addShell, shell_amount)
        logger.debug("Add Edit Mesh:    %s", addEditMesh)
        logger.debug("Collapse Stack:   %s", collapseNode)
        logger.debug("Center Pivot:     %s", centerPivot)
        logger.debug("Delete Original:  %s", deleteOriginal)
        logger.debug("Selected objects: %s", len(rt.selection))

        if len(rt.selection) <= 0:
            msg = "Nothing selected. Please select a node to explode."
            logger.error(msg)
            self.show_alert(msg)
        else:
            pymxs.print_("[ExplodeGeometry] Explode started\n")
            self.progress_panel.setVisible(True)
            QtWidgets.QApplication.processEvents()
            start_time = time.perf_counter()

            def _prog(cur, tot):
                self.progress_bar.setValue(int(cur * 100 / tot) if tot else 0)
                QtWidgets.QApplication.processEvents()

            with pymxs.undo(True, "Explode Geometry"):
                if self.trimesh_option.isChecked():
                    transformation_set = list(rt.selection)
                    self.lbl_tot_node.setText(str(len(transformation_set)))
                    logger.debug("[TriMesh] Processing %s object(s)", len(transformation_set))
                    for i, n in enumerate(transformation_set, 1):
                        logger.debug("[TriMesh] Object %s/%s: '%s'", i, len(transformation_set), n.name)
                        self.lbl_node_name.setText(n.name)
                        self.lbl_curr_node.setText(str(i))
                        QtWidgets.QApplication.processEvents()
                        convert_to_triangle_faces(n, addShell, shell_amount,
                                                  addEditMesh, collapseNode,
                                                  centerPivot, on_progress=_prog)
                        if deleteOriginal:
                            logger.debug("[TriMesh] Deleting original '%s'", n.name)
                            rt.delete(n)

                if self.mnmesh_option.isChecked():
                    transformation_set = list(rt.selection)
                    self.lbl_tot_node.setText(str(len(transformation_set)))
                    logger.debug("[MNMesh] Processing %s object(s)", len(transformation_set))
                    for i, node in enumerate(transformation_set, 1):
                        logger.debug("[MNMesh] Object %s/%s: '%s'", i, len(transformation_set), node.name)
                        self.lbl_node_name.setText(node.name)
                        self.lbl_curr_node.setText(str(i))
                        QtWidgets.QApplication.processEvents()
                        convert_to_mnmesh_faces(node, addShell, shell_amount,
                                                addEditMesh, collapseNode,
                                                centerPivot, on_progress=_prog)
                        if deleteOriginal:
                            logger.debug("[MNMesh] Deleting original '%s'", node.name)
                            rt.delete(node)

            elapsed = time.perf_counter() - start_time
            logger.debug("Done. Redrawing views.")
            rt.redrawViews()

            # Always surface the completion summary on the Listener, regardless
            # of the debug-messages toggle.
            pymxs.print_("[ExplodeGeometry] Explode completed in {:.2f} seconds.\n".format(elapsed))
            
            self.progress_panel.setVisible(False)
            self.progress_bar.setValue(0)
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


def convert_to_triangle_faces(node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot, on_progress=None):
    logger.debug("[TriMesh] Converting '%s' to mesh...", node.name)
    rt.convertToMesh(node)
    num_faces = rt.getNumFaces(node)
    logger.debug("[TriMesh] '%s' has %s face(s) to explode", node.name, num_faces)
    if on_progress:
        on_progress(0, num_faces)
    for face_idx in range(1, num_faces + 1):
        face = rt.getFace(node, face_idx)
        v1 = rt.getVert(node, int(face.x))
        v2 = rt.getVert(node, int(face.y))
        v3 = rt.getVert(node, int(face.z))
        logger.debug("[TriMesh] Face %s/%s: verts=(%.2f,%.2f,%.2f) (%.2f,%.2f,%.2f) (%.2f,%.2f,%.2f)",
                     face_idx, num_faces, v1.x, v1.y, v1.z, v2.x, v2.y, v2.z, v3.x, v3.y, v3.z)

        new_node = rt.mesh(vertices=rt.Array(v1, v2, v3),
                           faces=rt.Array(rt.Point3(1, 2, 3)))
        rt.update(new_node)
        new_node.wireColor = _random_wire_color()
        logger.debug("[TriMesh] Created piece '%s' for face %s", new_node.name, face_idx)

        applySettings(new_node, addShell, shell_amount,
                      addEditMesh, collapseNode, centerPivot)
        if on_progress:
            on_progress(face_idx, num_faces)
    logger.debug("[TriMesh] Finished exploding '%s'", node.name)


def convert_to_mnmesh_faces(node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot, on_progress=None):
    logger.debug("[Poly] Converting '%s' to poly...", node.name)
    rt.convertToPoly(node)
    num_faces = rt.polyop.getNumFaces(node)
    logger.debug("[Poly] '%s' has %s face(s) to explode", node.name, num_faces)

    if on_progress:
        on_progress(0, num_faces)
    _processed = 0
    for face_idx in range(num_faces, 0, -1):
        logger.debug("[Poly] Detaching face %s/%s", face_idx, num_faces)
        rt.polyop.detachFaces(node, rt.Array(face_idx), asNode=True)
        new_node = rt.objects[-1]
        if new_node is None:
            logger.warning("[Poly] Could not find detached node for face %s", face_idx)
            continue
        new_node.wireColor = _random_wire_color()
        logger.debug("[Poly] Created piece '%s' for face %s", new_node.name, face_idx)
        applySettings(new_node, addShell, shell_amount, addEditMesh, collapseNode, centerPivot)
        _processed += 1
        if on_progress:
            on_progress(_processed, num_faces)
    logger.debug("[Poly] Finished exploding '%s'", node.name)


def applySettings(n, addShell, shell_amount, addEditMesh, collapseNode, centerPivot):
    logger.debug("applySettings on '%s': shell=%s (amt=%s) editMesh=%s collapse=%s centerPivot=%s",
                 n.name, addShell, shell_amount, addEditMesh, collapseNode, centerPivot)
    if addShell:
        logger.debug("Adding Shell modifier (outerAmount=%s)", shell_amount)
        mod = rt.Shell()
        mod.outerAmount = shell_amount
        rt.addModifier(n, mod)

    if addEditMesh:
        logger.debug("Adding Edit Mesh modifier")
        mod = rt.Edit_Mesh()
        rt.addModifier(n, mod)

    if collapseNode:
        logger.debug("Collapsing modifier stack")
        rt.maxOps.collapseNode(n, True)

    if centerPivot:
        logger.debug("Centering pivot")
        rt.centerPivot(n)


def main():
    form = Form()
    form.setParent(qtmax.GetQMaxMainWindow())
    form.setWindowFlags(QtCore.Qt.WindowType.Tool)
    form.show()


if __name__ == '__main__':
    main()

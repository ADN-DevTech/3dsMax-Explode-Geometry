'''
A port of the Explode Geometry .NET plug-in on the ADN-DevTech GitHub:
https://github.com/ADN-DevTech/3dsMax-Explode-Geometry
This example illustrates using PySide in Max, and working with TriObject and Mesh objects
'''

from PySide import QtCore, QtGui
import pymxs
import MaxPlus
import threading

rt = pymxs.runtime
class _GCProtector(object):
    widgets = []

################## GUI DEFINITION #############################

## Form implementation generated (by: pyside-uic 0.2.15)
## from reading ui file 'explode_geometry.ui'
## Added here to be a single file
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(320, 330)
        Form.setMinimumSize(QtCore.QSize(320, 330))
        Form.setMaximumSize(QtCore.QSize(320, 330))
        self.formLayout = QtGui.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtGui.QGroupBox(Form)
        self.groupBox.setMinimumSize(QtCore.QSize(0, 200))
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 200))
        self.groupBox.setObjectName("groupBox")
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 150, 281, 41))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget = QtGui.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 241, 20))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.trimesh_option = QtGui.QRadioButton(self.layoutWidget)
        self.trimesh_option.setChecked(True)
        self.trimesh_option.setObjectName("trimesh_option")
        self.horizontalLayout_4.addWidget(self.trimesh_option)
        self.mnmesh_option = QtGui.QRadioButton(self.layoutWidget)
        self.mnmesh_option.setEnabled(True)
        self.mnmesh_option.setObjectName("mnmesh_option")
        self.horizontalLayout_4.addWidget(self.mnmesh_option)
        self.layoutWidget1 = QtGui.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 291, 121))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(-1, -1, 5, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.add_shell_checkbox = QtGui.QCheckBox(self.layoutWidget1)
        self.add_shell_checkbox.setMaximumSize(QtCore.QSize(150, 16777215))
        self.add_shell_checkbox.setObjectName("add_shell_checkbox")
        self.horizontalLayout_3.addWidget(self.add_shell_checkbox)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.offset_label = QtGui.QLabel(self.layoutWidget1)
        self.offset_label.setMinimumSize(QtCore.QSize(40, 0))
        self.offset_label.setMaximumSize(QtCore.QSize(40, 16777215))
        self.offset_label.setObjectName("offset_label")
        self.horizontalLayout_2.addWidget(self.offset_label)
        self.shell_offset = QtGui.QDoubleSpinBox(self.layoutWidget1)
        self.shell_offset.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.shell_offset.sizePolicy().hasHeightForWidth())
        self.shell_offset.setSizePolicy(sizePolicy)
        self.shell_offset.setBaseSize(QtCore.QSize(0, 0))
        self.shell_offset.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.shell_offset.setAlignment(QtCore.Qt.AlignCenter)
        self.shell_offset.setMinimum(0.1)
        self.shell_offset.setMaximum(1000.0)
        self.shell_offset.setSingleStep(0.1)
        self.shell_offset.setObjectName("shell_offset")
        self.horizontalLayout_2.addWidget(self.shell_offset)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.add_edit_mesh_checkbox = QtGui.QCheckBox(self.layoutWidget1)
        self.add_edit_mesh_checkbox.setObjectName("add_edit_mesh_checkbox")
        self.verticalLayout.addWidget(self.add_edit_mesh_checkbox)
        self.collapse_modifier_stack_checkbox = QtGui.QCheckBox(self.layoutWidget1)
        self.collapse_modifier_stack_checkbox.setObjectName("collapse_modifier_stack_checkbox")
        self.verticalLayout.addWidget(self.collapse_modifier_stack_checkbox)
        self.center_pivot_checkbox = QtGui.QCheckBox(self.layoutWidget1)
        self.center_pivot_checkbox.setObjectName("center_pivot_checkbox")
        self.verticalLayout.addWidget(self.center_pivot_checkbox)
        self.delete_original_checkbox = QtGui.QCheckBox(self.layoutWidget1)
        self.delete_original_checkbox.setObjectName("delete_original_checkbox")
        self.verticalLayout.addWidget(self.delete_original_checkbox)
        self.verticalLayout_2.addWidget(self.groupBox)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.select_label = QtGui.QLabel(Form)
        self.select_label.setMinimumSize(QtCore.QSize(100, 35))
        self.select_label.setMaximumSize(QtCore.QSize(100, 35))
        self.select_label.setObjectName("select_label")
        self.horizontalLayout.addWidget(self.select_label)
        self.selected_objects_string = QtGui.QLabel(Form)
        self.selected_objects_string.setMinimumSize(QtCore.QSize(0, 35))
        self.selected_objects_string.setMaximumSize(QtCore.QSize(16777215, 35))
        self.selected_objects_string.setObjectName("selected_objects_string")
        self.horizontalLayout.addWidget(self.selected_objects_string)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.explode_button = QtGui.QPushButton(Form)
        self.explode_button.setMinimumSize(QtCore.QSize(300, 50))
        self.explode_button.setMaximumSize(QtCore.QSize(300, 50))
        self.explode_button.setObjectName("explode_button")
        self.verticalLayout_2.addWidget(self.explode_button)
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Explode Geometry", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Form", "Explode Options", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("Form", "Geometry Type", None, QtGui.QApplication.UnicodeUTF8))
        self.trimesh_option.setText(QtGui.QApplication.translate("Form", "TriMesh", None, QtGui.QApplication.UnicodeUTF8))
        self.mnmesh_option.setText(QtGui.QApplication.translate("Form", "MNMesh", None, QtGui.QApplication.UnicodeUTF8))
        self.add_shell_checkbox.setText(QtGui.QApplication.translate("Form", "Add Shell Modifier    ---->", None, QtGui.QApplication.UnicodeUTF8))
        self.offset_label.setText(QtGui.QApplication.translate("Form", "Offset:", None, QtGui.QApplication.UnicodeUTF8))
        self.add_edit_mesh_checkbox.setText(QtGui.QApplication.translate("Form", "Add Edit Mesh Modifier", None, QtGui.QApplication.UnicodeUTF8))
        self.collapse_modifier_stack_checkbox.setText(QtGui.QApplication.translate("Form", "Collapse Modifier Stack", None, QtGui.QApplication.UnicodeUTF8))
        self.center_pivot_checkbox.setText(QtGui.QApplication.translate("Form", "Center Pivot", None, QtGui.QApplication.UnicodeUTF8))
        self.delete_original_checkbox.setText(QtGui.QApplication.translate("Form", "Delete Original", None, QtGui.QApplication.UnicodeUTF8))
        self.select_label.setText(QtGui.QApplication.translate("Form", "Selected Object(s):", None, QtGui.QApplication.UnicodeUTF8))
        self.selected_objects_string.setText(QtGui.QApplication.translate("Form", "None", None, QtGui.QApplication.UnicodeUTF8))
        self.explode_button.setText(QtGui.QApplication.translate("Form", "Explode", None, QtGui.QApplication.UnicodeUTF8))



''' Form class that allows the user to select options for the script
'''
class Form(QtGui.QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(Form, self).__init__()
        self.setupUi(self)
        _GCProtector.widgets.append(self)
        self.updateSelectionLabel()
        self.explode_button.clicked.connect(self.do_explode)
        MaxPlus.NotificationManager.Register(MaxPlus.NotificationCodes.SelectionsetChanged, self.updateSelectionLabel)

    def updateSelectionLabel(self,arg=None):
        nr_of_selected_elements = len(rt.selection)
        selection_set = rt.selection[0].name if nr_of_selected_elements == 1 else "{} objects selected".format(nr_of_selected_elements)
        self.selected_objects_string.setText(selection_set)

    # Gather the settings from the form, and call convert_to_triangle_faces
    def do_explode(self):
        # get values from window
        addShell = self.add_shell_checkbox.isChecked()
        shell_amount = self.shell_offset.value()
        addEditMesh = self.add_edit_mesh_checkbox.isChecked()
        collapseNode = self.collapse_modifier_stack_checkbox.isChecked()
        centerPivot = self.center_pivot_checkbox.isChecked()
        deleteOriginal = self.delete_original_checkbox.isChecked()

        # iterate through the selected nodes
        if MaxPlus.SelectionManager.GetCount() <= 0:
            msg = "Nothing selected. Please select a node to explode."
            print msg
            self.show_alert(msg)
        else:
            if(self.trimesh_option.isChecked()):
                transformation_set = [node for node in MaxPlus.SelectionManager.Nodes]
                for n in transformation_set:
                    convert_to_triangle_faces(n, addShell, shell_amount,
                                          addEditMesh, collapseNode,
                                          centerPivot)
                    if deleteOriginal:
                        n.Delete()

            if(self.mnmesh_option.isChecked()):
                transformation_set = [node for node in rt.selection]
                for node in transformation_set:
                    convert_to_mnmesh_faces(node, addShell, shell_amount,
                                            addEditMesh, collapseNode,
                                            centerPivot)
                    if deleteOriginal:
                        rt.delete(node)

            rt.redrawViews()
            # close the dialog
            MaxPlus.NotificationManager.Unregister(MaxPlus.NotificationManager.Handlers[-1])
            self.close()

    # alert dialog
    def show_alert(self, message):
        msgBox = QtGui.QMessageBox()
        msgBox.setText(message)
        msgBox.exec_()
################## MAIN LOGIC #################################

app = QtGui.QApplication.instance()
if not app:
    app = QtGui.QApplication([])



def convert_to_triangle_faces(node, addShell, shell_amount, addEditMesh, collapseNode,
                                          centerPivot):
    # convert to a mesh geometry, then use EvalWOrldState() to get an instance of the object
    node.Convert(MaxPlus.ClassIds.TriMeshGeometry)
    object_state = node.EvalWorldState()
    obj_original = object_state.Getobj()
    
    # is this a TriObject already?
    if not obj_original.IsSubClassOf(MaxPlus.ClassIds.TriMeshGeometry):
        # find a way to convert it anyway?
        pass

    # save node settings to apply on mesh:
    mat = node.GetLocalTM()
    offset_pos = node.GetObjOffsetPosition()
    offset_rot = node.GetObjOffsetRotation()
    offset_scale = node.GetObjOffsetScale()
    
    # cast to TriObject object and get the mesh so we can work with it
    tri_obj = MaxPlus.TriObject._CastFrom(obj_original)    
    tri_mesh = tri_obj.GetMesh()
    
    # create a new TriObject for each new face, and set it up:
    for face in tri_mesh.Faces:
        
        new_face = MaxPlus.Factory.CreateNewTriObject()
        n = MaxPlus.Factory.CreateNode(new_face)
        mesh = new_face.GetMesh()
        mesh.SetNumFaces(1)
        mesh.SetNumVerts(3)
        mesh.GetFace(0).SetVerts(0,1,2)        
        mesh.GetFace(0).SetEdgeVisFlags(1,1,1)
        mesh.GetFace(0).SetSmGroup(2)

        # now for each vertex, get the old face's points and store into new
        for i in range (0,3):
            pt = tri_mesh.GetVertex(face.GetVert(i))
            mesh.SetVert(i,pt)
        
        # force re-draw
        mesh.InvalidateGeomCache()

        # update node to match object being exploded:
        n.SetLocalTM(mat)
        n.SetObjOffsetPosition(offset_pos)
        n.SetObjOffsetRotation(offset_rot)
        n.SetObjOffsetScale(offset_scale)

        applySettings(n,addShell,shell_amount,
                      addEditMesh,collapseNode,centerPivot)



def convert_to_mnmesh_faces(node, addShell, shell_amount,addEditMesh, collapseNode,centerPivot):


    selection = rt.ConvertToPoly(node)
    if selection == None:
        print "Convertion to Poly failed"
        return

    # # TODO: parallelize this
    for index, face in enumerate(selection.faces):
        vertices = rt.polyop.getFaceVerts(selection, index + 1)
        new_node = createPolyFromVertices(vertices,selection)
        applySettings(new_node, addShell, shell_amount,addEditMesh, collapseNode,centerPivot)


def createPolyFromVertices(vertices, selection):

    vertex_array = [selection.verts[vertex - 1] for vertex in vertices]
    geom = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.PolyMeshObject)
    poly = MaxPlus.PolyObject._CastFrom(geom)
    mnmesh = poly.mnmesh
    nr_vertices = len(vertex_array)

    mnmesh.SetNumVerts(nr_vertices)
    mnmesh.SetNumEdges(nr_vertices)
    mnmesh.SetNumFaces(1)
    for index, vertex in enumerate(vertex_array):
        mnmesh.V(index).p = MaxPlus.Point3(vertex.pos.x, vertex.pos.y, vertex.pos.z)
    vislist = MaxPlus.CreateBoolList([1 for i in range(nr_vertices)])
    mnmesh.F(0).MakePoly(nr_vertices,
                         MaxPlus.CreateIntList([i for i in range(nr_vertices)]),
                         vislist)
    mnmesh.FillInMesh()
    poly_node = MaxPlus.Factory.CreateNode(poly)
    return poly_node


def applySettings(n,addShell, shell_amount,addEditMesh, collapseNode,centerPivot):

    # add shell modifier
    if addShell:
        mod = MaxPlus.Factory.CreateObjectModifier(MaxPlus.ClassIds.Shell)
        mod.ParameterBlock.outerAmount.Value = shell_amount
        n.AddModifier(mod)

    # add edit mesh modifier
    if addEditMesh:
        mod = MaxPlus.Factory.CreateObjectModifier(MaxPlus.ClassIds.Edit_Mesh)
        n.AddModifier(mod)

    # collapse the node
    if collapseNode:
        n.Collapse(True)

    if centerPivot:
        t = MaxPlus.Core.GetCurrentTime()
        n.CenterPivot(t, False)
        n.AlignPivot(t, False)


def main():        
    #MaxPlus.FileManager.Reset(True)
    form = Form()
    form.setParent(MaxPlus.GetQMaxWindow())
    MaxPlus.MakeQWidgetDockable(form,4)
    form.show()   

    
    
if __name__ == '__main__':
    main()




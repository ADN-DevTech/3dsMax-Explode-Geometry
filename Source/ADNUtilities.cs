#region Copyright
//      .NET Sample
//
//      Copyright (c) 2013 by Autodesk, Inc.
//
//      Permission to use, copy, modify, and distribute this software
//      for any purpose and without fee is hereby granted, provided
//      that the above copyright notice appears in all copies and
//      that both that copyright notice and the limited warranty and
//      restricted rights notice below appear in all supporting
//      documentation.
//
//      AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS.
//      AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
//      MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.  AUTODESK, INC.
//      DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
//      UNINTERRUPTED OR ERROR FREE.
//
//      Use, duplication, or disclosure by the U.S. Government is subject to
//      restrictions set forth in FAR 52.227-19 (Commercial Computer
//      Software - Restricted Rights) and DFAR 252.227-7013(c)(1)(ii)
//      (Rights in Technical Data and Computer Software), as applicable.
//
#endregion

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Windows.Media;

using System.Runtime.InteropServices;
using System.Diagnostics;

using ManagedServices;
// for 2012: using MaxCustomControls;
// for 2013:
using UiViewModels.Actions;
using Autodesk.Max;

namespace ADNExplodeGeometry
{
    /// <summary>
    /// Utility functions to do all the explode work.
    /// They are setup so that they could also be used individually called directly from MAXScript.
    /// </summary>
    static public class ADN_Utility
    {
        /// <summary>
        /// This class handles the user break when processing many nodes and faces.
        /// </summary>
        public class ADN_UserBreakCheck
        {
            private Autodesk.Max.MaxSDK.IWindowsMessageFilter m_MessageFilter;

            public ADN_UserBreakCheck()
            {
                IntPtr hwnd = ManagedServices.AppSDK.GetMaxHWND();
                IGlobal global = Autodesk.Max.GlobalInterface.Instance;
                m_MessageFilter = global.MaxSDK.WindowsMessageFilter.Create();
                m_MessageFilter.AddUnfilteredWindow(hwnd);
            }
            public bool Check()
            {
                m_MessageFilter.RunNonBlockingMessageLoop();
                return m_MessageFilter.Aborted;
            }
        }

        static private ExplodeGeomUserControl1 m_ctrlProgress = null;
        static private bool m_bUsingProgress = false;

        /// <summary>
        /// Used to initialize a progress control
        /// </summary>
        /// <param name="ctrlProgress"> Input the progress control to use. </param>
        static public void SetProgressControl(ExplodeGeomUserControl1 ctrlProgress)
        {
            m_bUsingProgress = true;
            m_ctrlProgress = ctrlProgress;
        }

        /// <summary>
        /// Cleanup progress control
        /// </summary>
        /// <param name="ctrlProgress"> Input the progress control to clear. </param>
        static public void ClearProgressControl(ExplodeGeomUserControl1 ctrlProgress)
        {
            m_bUsingProgress = false;
            m_ctrlProgress = null;
        }

        /// <summary>
        /// This will return a modifier from the stack
        /// </summary>
        /// <param name="nodeToSearch"> Input node to search. </param>
        /// <param name="cid"> Input the class id of the modifier to find. </param>
        /// <returns> The found modifier or null if not found. </returns>
        static public IModifier GetModifier(IINode nodeToSearch, IClass_ID cid)
        {
            IGlobal global = Autodesk.Max.GlobalInterface.Instance;

            IIDerivedObject dobj = nodeToSearch.ObjectRef as IIDerivedObject;

            while (dobj != null)
            {
                int nmods = dobj.NumModifiers;
                for (int i = 0; i < nmods; i++)
                {
                    IModifier mod = dobj.GetModifier(i);
                    // have to compare ClassID Parts A and B separately. The equals operator is not 
                    // implemented so it will return false even when they are equal.
                    if ((mod.ClassID.PartA == cid.PartA) && (mod.ClassID.PartB == cid.PartB))
                        return mod;
                }
                dobj = dobj.ObjRef as IIDerivedObject;
            }

            return null;
        }

        /// <summary>
        /// Adds an object space modifier to provided node (by handle).
        /// </summary>
        /// <param name="nodeHandle"> Input the node handle to add the modifier to. </param>
        /// <param name="cid"> Input the class id of the modifier add. </param>
        /// <returns> Returns 1 if successful or -1 if not. </returns>
        static public int AddOsmModifier(uint nodeHandle, IClass_ID cid)
        {
            try
            {

                IGlobal global = Autodesk.Max.GlobalInterface.Instance;
                IInterface14 ip = global.COREInterface14;

                IINode node = ip.GetINodeByHandle(nodeHandle);

                IObject obj = node.ObjectRef;
                IIDerivedObject dobj = global.CreateDerivedObject(obj);
                object objMod = ip.CreateInstance(SClass_ID.Osm, cid as IClass_ID);
                IModifier mod = (IModifier)objMod;

                dobj.AddModifier(mod, null, 0); // top of stack
                node.ObjectRef = dobj;
            }
            catch (Exception ex)
            {
                Debug.Print(ex.Message);
                return -1;
            }

            return 1;
        }

        /// <summary>
        /// Adds the Edit Mesh modifier to the provided node (by handle).
        /// </summary>
        /// <param name="nodeHandle"> Input the node handle to add the modifier to. </param>
        /// <returns> Returns 1 if successful or -1 if not. </returns>
        static public int AddOsmEditMesh(uint nodeHandle)
        {
            try
            {

                IGlobal global = Autodesk.Max.GlobalInterface.Instance;
                IInterface14 ip = global.COREInterface14;

                IClass_ID cidOsmEditMesh = global.Class_ID.Create(0x00050, 0);
                AddOsmModifier(nodeHandle, cidOsmEditMesh);
            }
            catch (Exception ex)
            {
                Debug.Print(ex.Message);
                return -1;
            }

            return 1;
        }

        /// <summary>
        /// Adds the Shell modifier to the provided node (by handle).
        /// </summary>
        /// <param name="nodeHandle"> Input the node handle to add the modifier to. </param>
        /// <param name="shellAmount"> Input the amount of shell thickness as float. </param>
        /// <returns> Returns 1 if successful or -1 if not. </returns>
        static public int AddOsmShell(uint nodeHandle, float shellAmount)
        {
            try
            {

                IGlobal global = Autodesk.Max.GlobalInterface.Instance;
                IInterface14 ip = global.COREInterface14;

                IClass_ID cidOsmShell = global.Class_ID.Create(0x3b9b1a16, 0x6d84e8d0);
                AddOsmModifier(nodeHandle, cidOsmShell);

                IINode node = ip.GetINodeByHandle(nodeHandle);
                IModifier mod = GetModifier(node, cidOsmShell);
                if (mod != null)
                {
                    IIParamBlock2 pb = mod.GetParamBlock(0);
                    pb.SetValue(0, 0, shellAmount, 0); // innerAmount parameter is at index zero of the parameter block.
                }
            }
            catch (Exception ex)
            {
                Debug.Print(ex.Message);
                return -1;
            }

            return 1;
        }

        /// <summary>
        /// This is the routine to convert the input node to triangle faces.
        /// </summary>
        /// <param name="nodeHandle"> Input the node by handle. </param>
        /// <param name="convertToTri"> Input whether to convert to a tri object first. </param>
        /// <param name="addShell"> Input whether to add the shell modifier when finished converting to face. </param>
        /// <param name="shell"> Input the shell thickness amount. </param>
        /// <param name="addEditMesh"> Input whether to add the Edit Mesh modifier when finished converting to face. </param>
        /// <param name="collapseNode"> Input whether to collapse the node afterwards. </param>
        /// <param name="centerPivot"> Input whether to center the pivot on each new face. </param>
        /// <returns> Returns 1 if successful or -1 if not. </returns>
        static public int ConvertToTriangleFaces(uint nodeHandle,
                                                bool convertToTri = true, // C# now supports default parameters
                                                bool addShell = true,
                                                float shell = 0.1f,
                                                bool addEditMesh = true,
                                                bool collapseNode = true,
                                                bool centerPivot = true)
        {
            try
            {

                IGlobal global = Autodesk.Max.GlobalInterface.Instance;
                IInterface14 ip = global.COREInterface14;

                IINode node = ip.GetINodeByHandle(nodeHandle);

                // Get it's current object state. If a modifier has been applied, for example,
                // it is going to return the OS of the mesh in it's current form in the timeline.
                IObjectState os = node.ObjectRef.Eval(ip.Time);

                // Now grab the object itself.
                IObject objOriginal = os.Obj;

                // Let's make sure it is a TriObject, which is the typical kind of object with a mesh
                if (!objOriginal.IsSubClassOf(global.TriObjectClassID))
                {
                    // If it is NOT, see if we can convert it...
                    if (convertToTri && objOriginal.CanConvertToType(global.TriObjectClassID) == 1)
                        objOriginal = objOriginal.ConvertToType(ip.Time, global.TriObjectClassID);
                    else
                        return -1;
                }

                // Now we should be safe to know it is a TriObject and we can cast it as such.
                // An exception will be thrown...
                ITriObject triOriginal = objOriginal as ITriObject;


                // Let's first setup a class ID for the type of objects are are creating.
                // New TriObject in this case to hold each face.
                IClass_ID cid = global.Class_ID.Create((uint)BuiltInClassIDA.TRIOBJ_CLASS_ID, 0);

                IMatrix3 mat = node.GetNodeTM(0, null);
                IPoint3 ptOffsetPos = node.ObjOffsetPos;
                IQuat quatOffsetRot = node.ObjOffsetRot;
                IScaleValue scaleOffsetScale = node.ObjOffsetScale;

                // We can grab the faces as a List and iterate them in .NET API.
                IMesh mesh = triOriginal.Mesh;
                IList<IFace> faces = triOriginal.Mesh.Faces;
                
                int nNumFaces = faces.Count;
                if (m_bUsingProgress)
                {
                    m_ctrlProgress.PB_ProgressMaxNum = nNumFaces;
                }

                ADN_UserBreakCheck checkUserBreak = new ADN_UserBreakCheck();
                int count = 0;
                foreach (IFace face in faces)
                {
                    if (checkUserBreak.Check() == true)
                    {
                        return -1;
                    }
                    if (m_bUsingProgress)
                    {
                        m_ctrlProgress.PB_ProgressCurrNum = ++count;
                    }

                    // Create a new TriObject for each new face.
                    object objectNewFace = ip.CreateInstance(SClass_ID.Geomobject, cid as IClass_ID);

                    // Create a new node to hold it in the scene.
                    IObject objNewFace = (IObject)objectNewFace;
                    IINode n = global.COREInterface.CreateObjectNode(objNewFace);

                    // Name it and ensure it is unique...
                    string newname = "ADN-Sample-Face";
                    ip.MakeNameUnique(ref newname);
                    n.Name = newname;

                    // Based on what we created above, we can safely cast it to TriObject
                    ITriObject triNewFace = objNewFace as ITriObject;

                    // Setup the new TriObject with 1 face, and the vertex count from the original object's face we are processing
                    triNewFace.Mesh.SetNumFaces(1, false, false);
                    triNewFace.Mesh.SetNumVerts(face.V.Count(), false, false);

                    // Finish setting up the face (always face '0' because there will only be one per object).
                    triNewFace.Mesh.Faces[0].SetVerts(0, 1, 2);
                    triNewFace.Mesh.Faces[0].SetEdgeVisFlags(EdgeVisibility.Vis, EdgeVisibility.Vis, EdgeVisibility.Vis);
                    triNewFace.Mesh.Faces[0].SmGroup = 2;

                    // Now, for each vertex, get the old face's points and store into new.
                    for (int i = 0; i < face.V.Count(); i++)
                    {
                        //Get the vertex from the original object's face we are processing
                        IPoint3 point = triOriginal.Mesh.GetVert((int)face.GetVert(i));
                        // Set the vertex point in the new face vertex
                        triNewFace.Mesh.SetVert(i, point);
                    }

                    // make it draw.
                    triNewFace.Mesh.InvalidateGeomCache();
                    
                    if (addShell)
                        AddOsmShell(n.Handle, shell);

                    if (addEditMesh)
                        AddOsmEditMesh(n.Handle);

                    if (collapseNode)
                        ip.CollapseNode(n, true);

                    // update transform to match object being exploded.
                    n.SetNodeTM(0, mat);
                    n.ObjOffsetPos = ptOffsetPos;
                    n.ObjOffsetRot = quatOffsetRot;
                    n.ObjOffsetScale = scaleOffsetScale;
                    n.ObjOffsetPos = ptOffsetPos;
                    if (centerPivot)
                        n.CenterPivot(0, false);

                }
            }
            catch (Exception)
            {
                return -1;
            }

            return 1;
        }

        /// <summary>
        /// This is the routine to convert the input node to polygon faces.
        /// </summary>
        /// <param name="nodeHandle"> Input the node by handle. </param>
        /// <param name="convertToTri"> Input whether to convert to a poly object first. </param>
        /// <param name="addShell"> Input whether to add the shell modifier when finished converting to face. </param>
        /// <param name="shell"> Input the shell thickness amount. </param>
        /// <param name="addEditMesh"> Input whether to add the Edit Mesh modifier when finished converting to face. </param>
        /// <param name="collapseNode"> Input whether to collapse the node afterwards. </param>
        /// <param name="centerPivot"> Input whether to center the pivot on each new face. </param>
        /// <returns> Returns 1 if successful or -1 if not. </returns>
        static public int ConvertToPolygonFaces(uint nodeHandle,
                                                bool convertToPoly = true, // C# now supports default parameters
                                                bool addShell = true,
                                                float shell = 0.1f,
                                                bool addEditMesh = true,
                                                bool collapseNode = true,
                                                bool centerPivot = true)
        {
            try
            {

                IGlobal global = Autodesk.Max.GlobalInterface.Instance;
                IInterface14 ip = global.COREInterface14;

                IINode node = ip.GetINodeByHandle(nodeHandle);
                if (node == null)
                    return -1;

                // Get it's current object state. If a modifier has been applied, for example,
                // it is going to return the OS of the mesh in it's current form in the timeline.
                IObjectState os = node.ObjectRef.Eval(ip.Time);

                // Now grab the object itself.
                IObject objOriginal = os.Obj;

                IPolyObject polyObject = objOriginal as IPolyObject;

                IClass_ID cid = global.Class_ID.Create((uint)BuiltInClassIDA.POLYOBJ_CLASS_ID, 0);
                IPolyObject polyObj = ip.CreateInstance(SClass_ID.Geomobject, cid as IClass_ID) as IPolyObject;

                if (polyObject == null && convertToPoly)
                {
                    if (objOriginal.CanConvertToType(global.TriObjectClassID) == 1)
                        objOriginal = objOriginal.ConvertToType(ip.Time, global.TriObjectClassID);
                    else
                    {
                        return -1;
                    }
                    ITriObject triOriginal = objOriginal as ITriObject;
                    polyObj.Mesh.AddTri(triOriginal.Mesh);
                    polyObj.Mesh.FillInMesh();
                    polyObj.Mesh.EliminateBadVerts(0, false);
                    polyObj.Mesh.MakePolyMesh(0, true);
                }
                else if (polyObject == null)
                {
                    polyObj = polyObject;
                }
                else
                {
                    return -1;
                }

                IMatrix3 mat = node.GetNodeTM(0, null);
                IPoint3 ptOffsetPos = node.ObjOffsetPos;
                IQuat quatOffsetRot = node.ObjOffsetRot;
                IScaleValue scaleOffsetScale = node.ObjOffsetScale;

                // We can grab the faces as a List and iterate them in .NET API.

                int nNumFaces = polyObj.Mesh.FNum;
                if (m_bUsingProgress)
                {
                    m_ctrlProgress.PB_ProgressMaxNum = nNumFaces;
                }

                ADN_UserBreakCheck checkUserBreak = new ADN_UserBreakCheck();

                for (int i = 0; i < nNumFaces; i++)
                {
                    if (checkUserBreak.Check() == true)
                    {
                        return -1;
                    }
                    if (m_bUsingProgress)
                    {
                        m_ctrlProgress.PB_ProgressCurrNum = i;
                    }

                    // Create a new poly object for each new face.
                    object objectNewFace = ip.CreateInstance(SClass_ID.Geomobject, cid as IClass_ID);

                    // Create a new node to hold it in the scene.
                    IObject objNewFace = (IObject)objectNewFace;
                    IINode n = global.COREInterface.CreateObjectNode(objNewFace);

                    // Name it and ensure it is unique...
                    string newname = "ADN-Sample-Face";
                    ip.MakeNameUnique(ref newname);
                    n.Name = newname;

                    // Based on what we created above, we can safely cast it to TriObject
                    IPolyObject polyNewFace = objNewFace as IPolyObject;

                    // Setup the new poly object with 1 face, and the vertex count from the original object's face we are processing
                    polyNewFace.Mesh.SetNumFaces(1);
                    polyNewFace.Mesh.SetMapNum(2);
                    IMNFace f = polyObj.Mesh.F(i);

                    polyNewFace.Mesh.F(0).Assign(f);

                    IMNFace fnew = polyNewFace.Mesh.F(0);

                    IList<int> vtx = f.Vtx;

                    polyNewFace.Mesh.SetNumVerts(vtx.Count);
                    for (int k = 0; k < vtx.Count; k++)
                    {
                        int nvindex = vtx[k];
                        IMNVert vert = polyObj.Mesh.V(nvindex);
                        Debug.Print("\nVertex = " + k + ", " + nvindex);
                        polyNewFace.Mesh.V(k).Assign(vert);
                        fnew.Vtx[k] = k;
                    }


                    int nedge = nedge = polyNewFace.Mesh.SimpleNewEdge(0, 1);
                    IMNEdge edge = polyNewFace.Mesh.E(nedge);
                    edge.Track = -1;
                    edge.F1 = 0;
                    edge.F2 = -1;
                    polyNewFace.Mesh.SetEdgeVis(nedge, true);

                    nedge = polyNewFace.Mesh.SimpleNewEdge(1, 2);
                    edge = polyNewFace.Mesh.E(nedge);
                    edge.Track = -1;
                    edge.F1 = 0;
                    edge.F2 = -1;
                    polyNewFace.Mesh.SetEdgeVis(nedge, true);

                    nedge = polyNewFace.Mesh.SimpleNewEdge(2, 3);
                    edge = polyNewFace.Mesh.E(nedge);
                    edge.Track = -1;
                    edge.F1 = 0;
                    edge.F2 = -1;
                    polyNewFace.Mesh.SetEdgeVis(nedge, true);

                    nedge = polyNewFace.Mesh.SimpleNewEdge(3, 0);
                    edge = polyNewFace.Mesh.E(nedge);
                    edge.Track = -1;
                    edge.F1 = 0;
                    edge.F2 = -1;
                    polyNewFace.Mesh.SetEdgeVis(nedge, true);

                    polyNewFace.Mesh.FillInMesh();
                    // make it update.
                    polyNewFace.Mesh.InvalidateGeomCache();

                    if (addShell)
                        AddOsmShell(n.Handle, shell);

                    if (addEditMesh)
                        AddOsmEditMesh(n.Handle);

                    if (collapseNode)
                        ip.CollapseNode(n, true);

                    // update transform to match object being exploded.
                    n.SetNodeTM(0, mat);
                    n.ObjOffsetPos = ptOffsetPos;
                    n.ObjOffsetRot = quatOffsetRot;
                    n.ObjOffsetScale = scaleOffsetScale;
                    n.ObjOffsetPos = ptOffsetPos;
                    if (centerPivot)
                        n.CenterPivot(0, false);
                }
            }
            catch (Exception ex)
            {
                Debug.Print(ex.Message);
                return -1;
            }

            return 1;
        }

        // Not used by this code, but is useful when exploring the APIs

        /// <summary>
        /// Input an obj to reflect
        /// </summary>
        /// <param name="obj"> Input object to reflect. </param>
        /// <returns> 1 </returns>
        static public int ReflectAPI(object obj)
        {
            try
            {


                System.Reflection.PropertyInfo[] propertyInfo = obj.GetType().GetProperties();
                string strOutput;

                strOutput = "\n The object is of type: " + obj.GetType().ToString() + " has the following reflected property info: ";
                for (int i = 0; i < propertyInfo.Length; i++)
                {
                    string name = propertyInfo[i].Name;
                    string s;
                    try
                    {
                        s = obj.GetType().InvokeMember(name, System.Reflection.BindingFlags.GetProperty, null, obj, null).ToString();
                        strOutput += "\n    " + name + ":  " + s + "  IsSpecialName == " + propertyInfo[i].IsSpecialName.ToString();
                    }
                    catch (System.Exception invokeMemberException)
                    {
                        strOutput += "\n" + name + ": EXCEPTION: " + invokeMemberException.Message;
                    }
                }
                System.Diagnostics.Debug.Write(strOutput);
            }
            catch (Exception e)
            {
                MessageBox.Show("Exception occurred: " + e.Message);
            }

            return 1;
        }
    }
}
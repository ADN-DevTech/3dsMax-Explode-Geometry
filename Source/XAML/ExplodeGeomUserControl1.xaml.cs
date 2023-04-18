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
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

using System.Diagnostics; // Useful for debugging

using Autodesk.Max;

namespace ADNExplodeGeometry
{

	/// <summary>
	/// Interaction logic for UserControl1.xaml
	/// </summary>
	public partial class ExplodeGeomUserControl1 : UserControl
	{
        System.Windows.Window m_winParent;
        bool m_bOk = false;

		public ExplodeGeomUserControl1(System.Windows.Window creator)
		{
            m_winParent = creator;
            InitializeComponent();

            IGlobal global = Autodesk.Max.GlobalInterface.Instance;
            IInterface14 ip = global.COREInterface14;

            IIColorManager cm = global.ColorManager;
            System.Drawing.Color dcolBack = cm.GetColor(Autodesk.Max.GuiColors.Background, Autodesk.Max.IColorManager.State.Normal);

            // due to a bug in the 3ds Max .NET API before 2017, you would have to reverse the R and B values to assign color properly. 
            // The Autodesk.Max assembly mapped them incorrectly
            // pre 2017: System.Windows.Media.Color mcolorBack = System.Windows.Media.Color.FromRgb(dcolBack.B, dcolBack.G, dcolBack.R);

            // Get current background color and match our dialog to it
            System.Windows.Media.Color mcolorBack = System.Windows.Media.Color.FromRgb(dcolBack.R, dcolBack.G, dcolBack.B);
            Brush colorBack = new SolidColorBrush(mcolorBack);
            // Note, if you want just a fixed color, you can comment this out and use the XAML defined value.
            LayoutRoot.Background = colorBack;

            // Get current text color and match our dialog to it.
            System.Drawing.Color dcolText = cm.GetColor(Autodesk.Max.GuiColors.Text, Autodesk.Max.IColorManager.State.Normal);
            // pre 2017: System.Windows.Media.Color mcolorText = System.Windows.Media.Color.FromRgb(dcolText.B, dcolText.G, dcolText.R);
            System.Windows.Media.Color mcolorText = System.Windows.Media.Color.FromRgb(dcolText.R, dcolText.G, dcolText.B);
            Brush colorText = new SolidColorBrush(mcolorText);
            
            // To use pure white, we can just set a system brush.
            //Brush colorText = Brushes.White;

            m_gbExplodeTypes.Foreground = colorText;
            m_rbTriangles.Foreground = colorText;
            m_rbPolygons.Foreground = colorText;

            m_gbExplodeOptions.Foreground = colorText;
            m_cbConvertTri.Foreground = colorText;
            m_cbConvertPoly.Foreground = colorText;
            m_cbAddShell.Foreground = colorText;
            m_lblNumOffset.Foreground = colorText;
            m_cbAddEditMesh.Foreground = colorText;
            m_cbCollapseStack.Foreground = colorText;
            m_cbCenterPivot.Foreground = colorText;
            m_cbDeleteOriginal.Foreground = colorText;
            // This is a button control, and we are not setting its color.
            // So we will not change the text color either.
            //m_btnExplodeIt.Foreground = colorText;

            m_lblLabelProNode.Foreground = colorText;
            m_lblNodeName.Foreground = colorText;
            m_lblLabelNode.Foreground = colorText;
            m_lblCurrNode.Foreground = colorText;
            m_lblLabelOf.Foreground = colorText;
            m_lblTotNode.Foreground = colorText;
            m_lblLabelEscape.Foreground = colorText;

		}

        public bool EI_IsOk 
        {
            get { return m_bOk; }
        }

        public bool EI_ConvertTypePoly
        {
            get 
            {
                if (m_rbPolygons.IsChecked.HasValue)
                {
                    return (bool)m_rbPolygons.IsChecked;
                }
                else 
                    return true;
            }
        }

        public bool EI_AttemptConvertToPoly
        {
            get
            {
                if (m_cbConvertPoly.IsChecked.HasValue)
                {
                    return (bool)m_cbConvertPoly.IsChecked;
                }
                else
                    return true;
            }
        }

        public bool EI_AttemptConvertToTri
        {
            get
            {
                if (m_cbConvertTri.IsChecked.HasValue)
                {
                    return (bool)m_cbConvertTri.IsChecked;
                }
                else
                    return true;
            }
        }

        public bool EI_AddShellModifier
        {
            get
            {
                if (m_cbAddShell.IsChecked.HasValue)
                {
                    return (bool)m_cbAddShell.IsChecked;
                }
                else
                    return true;
            }
        }

        public float EI_ShellAmount
        {
            get
            {
                return m_numOffset.Value;
            }
        }

        public bool EI_AddEditMeshModifier
        {
            get
            {
                if (m_cbAddEditMesh.IsChecked.HasValue)
                {
                    return (bool)m_cbAddEditMesh.IsChecked;
                }
                else
                    return true;
            }
        }

        public bool EI_CollapseStack
        {
            get
            {
                if (m_cbCollapseStack.IsChecked.HasValue)
                {
                    return (bool)m_cbCollapseStack.IsChecked;
                }
                else
                    return true;
            }
        }

        public bool EI_CenterPivot
        {
            get
            {
                if (m_cbCenterPivot.IsChecked.HasValue)
                {
                    return (bool)m_cbCenterPivot.IsChecked;
                }
                else
                    return true;
            }
        }

        public bool EI_DeleteOriginal
        {
            get
            {
                if (m_cbDeleteOriginal.IsChecked.HasValue)
                {
                    return (bool)m_cbDeleteOriginal.IsChecked;
                }
                else
                    return true;
            }
        }

        public int PB_ProgressCurrNum
        {
            set
            {
                m_progBar.Value = value;
            }
        }

        public int PB_ProgressMaxNum
        {
            set
            {
                m_progBar.Minimum = 0;
                m_progBar.Maximum = value;
            }
        }

        private void m_btnExplodeIt_Click(object sender, RoutedEventArgs e)
        {
            //
            IGlobal global = Autodesk.Max.GlobalInterface.Instance;
            IInterface14 ip = global.COREInterface14;
            this.m_pnlProgressPanel.Visibility = System.Windows.Visibility.Visible;

            try
            {
                global.TheHold.Begin();

                ADN_Utility.SetProgressControl(this);

                bool convertPoly = EI_ConvertTypePoly; // true = poly, false = tri
                bool attemptConvert;
                if (convertPoly)
                    attemptConvert = EI_AttemptConvertToPoly;
                else
                    attemptConvert = EI_AttemptConvertToTri;
                bool addShell = EI_AddShellModifier;
                float shellAmount = EI_ShellAmount;
                bool addEditMesh = EI_AddEditMeshModifier;
                bool collapseStack = EI_CollapseStack;
                bool deleteNode = EI_DeleteOriginal;

                //ip.DisableSceneRedraw();
                int stat = 0;
                int nNumSelNodes = ip.SelNodeCount;
                m_lblTotNode.Content = nNumSelNodes.ToString();

                for (int i = 0; i < nNumSelNodes; i++)
                {
                    IINode nodeCur = ip.GetSelNode(i);
                    m_lblNodeName.Content = nodeCur.Name;
                    m_lblCurrNode.Content = i+1;
                    if (convertPoly)
                    {
                        stat = ADN_Utility.ConvertToPolygonFaces(nodeCur.Handle, attemptConvert, addShell, shellAmount, addEditMesh, collapseStack);
                        if (stat < 0)
                            break;
                    }
                    else
                    {
                        stat = ADN_Utility.ConvertToTriangleFaces(nodeCur.Handle, attemptConvert, addShell, shellAmount, addEditMesh, collapseStack);
                        if (stat < 0)
                            break;
                    }

                }


                if (stat < 0)
                    global.TheHold.Cancel();
                else
                {
                    // now we need to start at the top to delete the original nodes. 
                    if (deleteNode)
                    {
                        IINodeTab tabNodes = global.INodeTab.Create();
                        ip.GetSelNodeTab(tabNodes);
                        if (tabNodes != null)
                            ip.DeleteNodes(tabNodes, true, true, false);
                    }
                    global.TheHold.Accept("ADN-PolygonExplode");
                }

                ip.RedrawViews(0, RedrawFlags.Normal, null);
            }
            catch (Exception ex)
            {
                Debug.Print(ex.Message);
                global.TheHold.Cancel();
            }

            this.m_pnlProgressPanel.Visibility = System.Windows.Visibility.Hidden;
            ADN_Utility.ClearProgressControl(this);
               
            m_winParent.Close();
            m_bOk = true;
        }

        private void m_btnCancel_Click(object sender, RoutedEventArgs e)
        {
            m_winParent.Close();
            m_bOk = false;
        }

        private void m_rbPolygons_Checked(object sender, RoutedEventArgs e)
        {
            if (IsInitialized)
            {
                m_cbConvertPoly.IsEnabled = true;
                m_cbConvertTri.IsEnabled = false;
            }
        }

        private void m_rbTriangles_Checked(object sender, RoutedEventArgs e)
        {
            if (IsInitialized)
            {
                m_cbConvertPoly.IsEnabled = false;
                m_cbConvertTri.IsEnabled = true;
            }
        }

        private void m_cbAddShell_Checked(object sender, RoutedEventArgs e)
        {
            if (IsInitialized)
            {
                if (EI_AddShellModifier == true)
                {
                    m_numOffset.IsEnabled = true;
                    m_lblNumOffset.IsEnabled = true;
                }
                else
                {
                    m_numOffset.IsEnabled = false;
                    m_lblNumOffset.IsEnabled = false;
                }
            }

        }

	}
}

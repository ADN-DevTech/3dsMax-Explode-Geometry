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
using System.Runtime;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows;
using System.Diagnostics; // Useful for debugging

using ManagedServices;
// for 2012: using MaxCustomControls;
// for 2013:
using UiViewModels.Actions;
using Autodesk.Max;

namespace ADNExplodeGeometry
{

    // Tip create a abstract base from CuiActionCommandAdapter, 
    // so you do not have to reimplement everything for each action.
    // You can also directly implement the ICuiActionCommand interface on your own class.
    // It is a bit more work, but gives you even more control.

    /// <summary>
    /// Used a a base class to implement specific strings constants. 
    /// </summary>
    public abstract class AbstractCustom_CuiActionCommandAdapter : CuiActionCommandAdapter
    {
        public override string ActionText
        {
            get { return InternalActionText; }
        }

        public override string Category
        {
            get { return InternalCategory; }
        }

        public override string InternalActionText
        {
            get { return CustomActionText; }
        }

        public override string InternalCategory
        {
            get { return "ADN Samples"; }
        }

        public override void Execute(object parameter)
        {
            try
            {
                CustomExecute(parameter);
            }
            catch (Exception e)
            {
                MessageBox.Show("Exception occurred: " + e.Message);
            }
        }

        public abstract string CustomActionText { get; }
        public abstract void CustomExecute(object parameter);
    }

    /// <summary>
    /// This is the specific action item that can be added to a UI element like the menus.
    /// </summary>
    public class AdnCui_ExplodeGeometry : AbstractCustom_CuiActionCommandAdapter
    {

        public override string CustomActionText
        {
            get { return "Explode Selected Geometry"; }
        }

        public override void CustomExecute(object parameter)
        {
            Console.WriteLine("Custom Execute");

            try
            {
                IGlobal global = Autodesk.Max.GlobalInterface.Instance;
                IInterface14 ip = global.COREInterface14;

                int nNumSelNodes = ip.SelNodeCount;
                if (nNumSelNodes <= 0)
                {
                    Console.WriteLine("1");
                    ip.PushPrompt("No nodes are selected. Please select at least one node to convert, before running the command.");
                    return;
                }

                Console.WriteLine("2");
                System.Windows.Window dialog = new System.Windows.Window();
                dialog.Title = "Explode It!";
                dialog.SizeToContent = System.Windows.SizeToContent.WidthAndHeight;
                ExplodeGeomUserControl1 ctlExplode = new ExplodeGeomUserControl1(dialog);
                dialog.Content = ctlExplode;
                dialog.WindowStartupLocation = System.Windows.WindowStartupLocation.CenterOwner;
                dialog.ShowInTaskbar = false;
                dialog.ResizeMode = System.Windows.ResizeMode.NoResize;

                System.Windows.Interop.WindowInteropHelper windowHandle =
                    new System.Windows.Interop.WindowInteropHelper(dialog);
                windowHandle.Owner = ManagedServices.AppSDK.GetMaxHWND();
                ManagedServices.AppSDK.ConfigureWindowForMax(dialog);

                dialog.ShowDialog(); //modal version; this prevents changes being made to model while our dialog is running, etc.

            }
            catch (Exception ex)
            {
                Debug.Print(ex.Message);
            }
        }
    }
}
3dsMax-Explode-Geometry
=======================

3ds Max Explode Geometry plug-in

This sample code is in .NET for 3ds Max SDK, and is also available for download from the Autodesk App Store as a simple application.


Getting Started
============
First select the nodes that you want to explode (you have an option to maintain the original geometry if desired). From
the UI element that you assigned the plug-in action to, select it and a dialog will come up.

Select the options, and then select "Explode Selected Geometry". A progress bar will be displayed for long actions and you have the option to cancel.

You can choose to create three or four sided objects as a result of the explode operation. Select the radio button of the desired operation. 
Additionally you can toggle whether to try and convert the object’s mesh before the conversion. By default it will try to convert, and if it cannot
it will end. If it can be converted (or is already of the correct type) then each node will be exploded into the resulting individual faces.

You can also control several other options.
Add Shell Modifier -- will add the modifier to the resulting face object, and apply the given shell offset.
Add Edit Mesh Modifier -- will add the modifier to the stack resulting in edit mesh operation being immediately available.
Collapse Modifier Stack -- will collapse the stack down to become an editable mesh as the end result.
Center Pivot -- will center the pivot on each resulting face.
Delete Original -- will remove each original node that was used to create the new faces.

App Store
==============
From 3ds Max 2025 and up, adding menu entries to the main menu bar utilizes the use of GUID to uniquely identify menu entries. As such, we recommend the use of `CC18FEFC-E8A4-4B16-B519-664E8FA3B549` as App Store menu entry for 2025 and later versions for uniformity.

To add you menu etries under "App Store" main menu entry, here is a short snippet in MaxScript. See full sample for adding Explode Geometry to the App Store menu [here](Bundle2/Contents/Post-Start-Up_Scripts/ADNGeometryExplodeSetupMenu2025.ms).

```ms
-- other code here ....

-- Add the "App Store" menu before "Help" menu on main menubar
local newSubMenu = mainMenuBar.CreateSubMenu appStoreMenuId stringAppStoreDefaultMenu beforeId:helpMenuId

-- Adding your menu item
-- 647394 : MacroScript Action Table ID
newSubMenu.CreateAction <Your Menu GUID> 647394 <MacroScript Name`MacroScript Category>
```

Python Version
==============
A port of this plugin that implements the basic functionality is available in the Python folder called `explode_geometry.py`.  This
script requires the `MaxPlus` Python feature for 3ds Max *2021* or earlier. 

> Limitation: The python sample relies on `MaxPlus` which was deprecated and removed as from 3ds Max 2022 [(See Here)](https://help.autodesk.com/view/MAXDEV/2023/ENU/?guid=MAXDEV_Python_what_s_new_in_3ds_max_python_api_html). As such, the Python sample only works with 3ds Max versions earlier than 2022.

Additional Information
=================
This plug-in was written by Kevin Vandecar - Autodesk Developer Network.  
The idea was provided by Louis Marcoux - Autodesk.  
The python version was developed by Drew Avis - Autodesk to show similar functionality.  

Known Issues
===========
There are no known limitations; however it is a very process intensive program. If you select many nodes with many faces it could take a long time
to complete, or even cause an error your system if it runs out of memory.

Contact
======
For more information on developing with 3ds Max, please visit the 3ds Max Developer Center.  
http://www.autodesk.com/develop3dsmax

Version
=======
1.0 - Initial Release  
2.0 - Adds support for 3ds Max UI color scheme, and also now supports both 3ds Max and 3ds Max Design.  
2.3 - Updates the DLL binary and other aspects of the App Bundle format to be supporting 2020, 2021, 2022, and 2023.  
2.5 - Update release to support 2022. No change in version Number.  
2.6 - Update release to support 2024  
2.7 - Support for 3ds Max 2025 and the new menu system.  


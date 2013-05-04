3dsMax-Explode-Geometry
=======================

3ds Max Explode Geometry plug-in

Available for download with installer for 3ds Max 2014 at:
http://apps.exchange.autodesk.com/3DSMAX/en/Detail/Index?id=appstore.exchange.autodesk.com%3aexplodegeometryfor3dsmax%3aen

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

Additional Information
=================
This plug-in was written by Kevin Vandecar - Autodesk Developer Network.
The idea was provided by Louis Marcoux - Autodesk.

Known Issues
===========
There are no known limitations; however it is a very process intensive program. If you select many nodes with many faces it could take a long time
to complete, or even cause an error your system if it runs out of memory.

Contact
======
For more information on developing with 3ds Max, please visit the 3ds Max Developer Center.
http://www.autodesk.com/develop3dsmax

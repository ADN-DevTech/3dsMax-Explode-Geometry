================================================
Brought to you by the Autodesk Developer Network
================================================
-------------
Explode Geometry for 3ds Max
-------------


Description
-----------
This plug-in can be used to choose one or more nodes in the scene and create 
"exploded" geometry. The exploded geometry is actually 3 or 4 sided faces and 
you have the options to add modifiers to enhance the finished geometry to your
needs.

Complete sample code, including a python version, is provided at the ADN samples guthub.
See here: https://github.com/ADN-DevTech/3dsMax-Explode-Geometry/


System Requirements
-------------------
This plug-in has been tested with Autodesk 3ds Max 2014. 


Usage
-----
First select the nodes that you want to explode (you have an option to maintain
the original geometry if desired). From the UI element that you assigned the 
plug-in action to, select it and a dialog will come up. 

Select the options, and then select "Explode Selected Geometry". A progress bar 
will be displayed for long actions and you have the option to cancel. 

You can choose to create three or four sided objects as a result of the explode 
operation. Select the radio button of the desired operation. Additionally you 
can toggle whether to try and convert the object�s mesh before the conversion. 
By default it will try to convert, and if it cannot it will end. If it can be 
converted (or is already of the correct type) then each node will be exploded 
into the resulting individual faces. 

You can also control several other options.
*Add Shell Modifier -- will add the modifier to the resulting face object, and
apply the given shell offset.
*Add Edit Mesh Modifier -- will add the modifier to the stack resulting in edit
mesh operation being immediately available.
*Collapse Modifier Stack -- will collapse the stack down to become an editable
mesh as the end result.
*Center Pivot -- will center the pivot on each resulting face.
*Delete Original -- will remove each original node that was used to create 
the new faces.


Limitations:
--------------------
There are no known limitations; however it is a very process intensive 
program. If you select many nodes with many faces it could take a long 
time to complete, or even cause an error your system if it runs out of memory.


Author
------
This plug-in was written by kevin.vandecar@autodesk.com from the 
Autodesk Developer Technical Services team. 

The idea was provided by Louis Marcoux.


Further Reading
---------------
For more information on developing with 3ds Max, please visit the
3ds Max Developer Center at http://www.autodesk.com/develop3dsmax


Feedback
--------
Email us at labs.plug-ins@autodesk.com with feedback or requests for
enhancements.


Release History
---------------

1.0    Original release                     (February 1, 2013)
2.0    Update release to incude UI color matching and now suports 3ds Max (Design) 2015 and 2016. (December 1, 2015)
2.1    Update release to support 2017, and minor code changes to support bug fixing in the Autodesk.Max.DLL assembly. (July 1, 2016)
2.3    Updates the DLL binary and other aspects of the App Bundle format to be supporting 2020, 2021, 2022, and 2023.  
2.5    Updates the sample code to support Mesh changes in the 2024 SDK.  
2.6    Support for 3ds Max 2025, ported to new menu system

(C) Copyright 2012 by Autodesk, Inc. 

Permission to use, copy, modify, and distribute this software in
object code form for any purpose and without fee is hereby granted, 
provided that the above copyright notice appears in all copies and 
that both that copyright notice and the limited warranty and
restricted rights notice below appear in all supporting 
documentation.

AUTODESK PROVIDES THIS PROGRAM "AS IS" AND WITH ALL FAULTS. 
AUTODESK SPECIFICALLY DISCLAIMS ANY IMPLIED WARRANTY OF
MERCHANTABILITY OR FITNESS FOR A PARTICULAR USE.  AUTODESK, INC. 
DOES NOT WARRANT THAT THE OPERATION OF THE PROGRAM WILL BE
UNINTERRUPTED OR ERROR FREE.

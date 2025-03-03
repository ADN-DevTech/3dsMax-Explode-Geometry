macroScript ADNExplodeGeomMS category:"ADN Samples" tooltip:"Explode Selected Geometry" buttonText:"Explode Selected Geometry"
(
    -- Again a limitation in maxscript... Cannot get the actionitem from the managed assembly easily
    -- but using the IDs will allow this macroscript to execute it
    
    -- Execute the ADN Explode Geometry plugin; from a managed CuiCommandAdaptor implemented plugin,
    -- you can grab the unqiue ID from the MAXScript listener window.
    actionMan.executeAction 36784 "14536"

    -- NOTE
    -- Doc Link: https://help.autodesk.com/view/MAXDEV/2023/ENU/?guid=GUID-38CB8317-6EB2-49D1-A086-B06BA2A141AE 
    -- The `executrAction` function expects two parameters, namely:
    --      1. `Action Table ID`    Action Table ID assigned to specific action table. Systemwide action tables have
    --                              non-changing IDs and we can also create our own action tables bearing our own IDs.
    --                              If you want to check all available ActionIDs, use the script in the doc link below
    --                              https://help.autodesk.com/view/MAXDEV/2025/ENU/?guid=GUID-D33B4031-2AB2-4A84-BA96-6BA96DD5A042 
    --      2. `Persistent ID`      Generated by hashing the CuiCommandAdapter's `InternalActionText` hence should be uniform
    --                              across installs and build as long as the `InternalActionText` is unchanged.
)
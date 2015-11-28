macroScript ADNExplodeGeomMS category:"ADN Samples" tooltip:"Explode Selected Geometry" buttonText:"Explode Selected Geometry"
(
    -- AGain a limitation in maxscript... Cannot get the actionitem frmo the managed assembly easily
    -- but using the IDs will allow this macroscript to execute it
    -- This is ugly, and not sure how the values are persistent between installs. 
    -- However, it is the same between my two machines!
    
    -- Execute the ADN Explode Geometry plugin; from a amanged CuiCommandAdaptor implemented plugin,
    -- you can grab the unqiue ID from the MAXScript listener window.
    actionMan.executeAction 36784 "14536"
)

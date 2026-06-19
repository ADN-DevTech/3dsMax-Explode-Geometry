macroScript ADNExplodeGeomPyMS category:"ADN Samples" tooltip:"Explode Geometry (Python)" buttonText:"Explode Geometry (Python)"
(
    local scriptDir = getFilenamePath (getSourceFileName())
    local pyFile = scriptDir + "..\python\explode_geometry.py"
    python.ExecuteFile pyFile
)
-- setup App Store menu, and add our app to it.
function menuCallback =
(
    local stringAppStoreDefaultMenu = "App Store"
    -- ADN Explode Geometry MXS
    local stringMacroScriptName = "ADNExplodeGeomMS" 
    local stringMacroScriptCategory = "ADN Samples"

    local menuMgr = callbacks.notificationParam()
    local mainMenuBar = menuMgr.mainMenuBar

    -- Id of "Help" menu in main menu bar. Can be found in Menu editor -> right click on menu item -> copy item id
    local helpMenuId = "cee8f758-2199-411b-81e7-d3ff4a80d143"
    local newSubMenu = mainMenuBar.CreateSubMenu "CC18FEFC-E8A4-4B16-B519-664E8FA3B549" stringAppStoreDefaultMenu beforeId:helpMenuId

    local separatorId = "96FB49D4-6263-4D8E-AC95-6D304673327B"
    newSubMenu.CreateSeparator separatorId

    local permanentId = stringMacroScriptName + "`" + stringMacroScriptCategory

    -- 647394 : MacroScript Action Table ID
    -- 36784  : .NET Assembly Action Table ID    
    newSubMenu.CreateAction "9DE5BDB9-E47F-4614-BDF8-C331B9B38C70" 36784 permanentId
)

-- Register Callback to the #CuiRegisterMenus
callbacks.removeScripts id:#adnExplodeGeomMenu
callbacks.addScript #cuiRegisterMenus menuCallback id:#adnExplodeGeomMenu
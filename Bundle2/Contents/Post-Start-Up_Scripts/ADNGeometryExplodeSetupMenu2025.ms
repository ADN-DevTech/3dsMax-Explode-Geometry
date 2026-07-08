-- To generare GUID for menu actions, use the following code snippet:
-- 
-- From MAXScript
-- local uid = genGUID()
-- 
-- From Python using PyMXS
-- from pymxs import runtime as rt
-- uid = rt.genguid()
-- 
-- From C++ Using the SDK
-- auto guid = MaxSDK::MaxGuid::CreateMaxGuid();
-- 

-- Utility function to get or create the App Store menu item
-- if it does not exist. This prevents errors when the script is run multiple times.
-- The argument `menuMgr` is passed from the callback notification parameter, where:
-- menuMgr = callbacks.notificationParam()
function getAppStoreMenuItem menuMgr =
(
	local mainMenuBar = menuMgr.mainMenuBar

	-- Global ID for App Store Menu
	local appstoreMenuId = "CC18FEFC-E8A4-4B16-B519-664E8FA3B549"

	-- Find Main Menu Bar (App Store)
	-- Create App Store Submenu and instantiate it to `undefined` first
	local appStoreSubmenu = menuMgr.getMenuItemById  appstoreMenuId

	-- Create App Store submenu if it does not exist
	if appstoreSubmenu == undefined then (
		-- Id of "Help" menu in main menu bar can be found in Menu editor -> right click on menu item -> copy item id
		local helpMenuId = "cee8f758-2199-411b-81e7-d3ff4a80d143"
		appStoreSubmenu = mainMenuBar.CreateSubMenu  appstoreMenuId "App Store" beforeId:helpMenuId
	) else (
        -- If the App Store submenu already exists, we need to get its subMenu property to access the actual submenu 
        -- where we can add our menu items. This is necessary because the `getMenuItemById` method returns the menu item itself, not the submenu.     
        appStoreSubmenu = appStoreSubmenu.subMenu
    )

	return appStoreSubmenu
)

-- setup App Store menu, and add our app to it.
function menuCallback =
(
    local menuMgr = callbacks.notificationParam()

    -- Check if App Store menu exists, if not create it
	-- and return the `App Store` sub menu which we will use to add our menu items.
    local newSubMenu = getAppStoreMenuItem menuMgr

    local separatorId = "96FB49D4-6263-4D8E-AC95-6D304673327B"
    newSubMenu.CreateSeparator separatorId

    -- ADN Explode Geometry MXS
    local stringMacroScriptName = "ADNExplodeGeomMS" 
    local stringMacroScriptCategory = "ADN Samples"
    local permanentId = stringMacroScriptName + "`" + stringMacroScriptCategory

    -- 647394 : MacroScript Action Table ID
    newSubMenu.CreateAction "9DE5BDB9-E47F-4614-BDF8-C331B9B38C70" 647394 permanentId	

	-- Only add Python menu entry for 3ds Max 2027 and above, as Python support in the UI is only available from 2027 onwards.
	if (maxVersion())[1] >= 29000 then
    (
    	newSubMenu.CreateAction "85045470-A03C-45EC-A13F-538346AF077A" 647394 "ADNExplodeGeomPyMS`ADN Samples"
	)
)

-- Register Callback to the #CuiRegisterMenus
callbacks.removeScripts id:#adnExplodeGeomMenu
callbacks.addScript #cuiRegisterMenus menuCallback id:#adnExplodeGeomMenu

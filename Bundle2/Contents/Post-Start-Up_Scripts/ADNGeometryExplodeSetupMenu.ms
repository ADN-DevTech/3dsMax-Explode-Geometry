-- setup App Store menu, and add our app to it.
(
    local stringAppStoreDefaultMenu = "App Store"

    -- so this should ensure it is only one time only per user UI setup
    -- MUST keep the value the SAME for all apps
    if menuMan.registerMenuContext 0x3923df2 then
    (
        -- can take these out, but it shows that it is called only when needed...
        -- print "ADN-Explode geometry: Creating App Store Menu"

        -- Get the main menu bar
        local mainMenuBar = menuMan.getMainMenuBar()

        -- Create the menu
        local subMenu = menuMan.createMenu stringAppStoreDefaultMenu
        local menuPos = mainMenuBar.numItems()
        local submenuItem = menuMan.createSubMenuItem "test" subMenu

        mainMenuBar.addItem submenuItem menuPos
        -- redraw the menu bar with the new item
        menuMan.updateMenuBar()
    )

    -- This one will allow an app to add theirs to existing App store app.
    -- MUST use genclassid() to get this value and it should be DIFFERENT per app.
    -- This then allows only onetime setup per app, per user UI setup

    local stringMacroScriptName = "ADNExplodeGeomMS" 
    local stringMacroScriptCategory = "ADN Samples"
    if menuMan.registerMenuContext 0x7b244316 then
    (
        -- can take these out, but it shows that it is called only when needed...
        -- print "Creating ADN Explode Geometry Sub-Menu"

        -- this should always succeed because above
        local appStoreMenu = menuMan.findMenu stringAppStoreDefaultMenu

        -- create the action item    
        local actionItem1 = menuMan.createActionItem stringMacroScriptName stringMacroScriptCategory

        -- Add the action item as a menu entry
        appStoreMenu.addItem actionItem1 -1

        -- Let's also separate each app...
        local menuSepItem = menuMan.createSeparatorItem()
        appStoreMenu.addItem menuSepItem -1

        -- redraw the menu bar with the new item
        menuMan.updateMenuBar()
    )
)
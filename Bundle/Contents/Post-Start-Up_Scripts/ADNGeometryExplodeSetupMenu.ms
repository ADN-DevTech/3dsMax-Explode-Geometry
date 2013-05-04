-- setup Exchange Store menu, and add our app to it.
(
    local stringExhangeStoreDefaultMenu = "Exchange Store"

    -- so this should ensure it is only one time only per user UI setup
    -- MUST keep the value the SAME for all apps
    if menuMan.registerMenuContext 0x3923df2 then
    (
        -- probably can take these out, but it shows that it is called only when needed...
        print "ADN-Explode geomtry: Creating Exchange Store Menu"

        -- Get the main menu bar
        local mainMenuBar = menuMan.getMainMenuBar()

        -- Create the menu
        local subMenu = menuMan.createMenu stringExhangeStoreDefaultMenu
        local menuPos = mainMenuBar.numItems()
        local submenuItem = menuMan.createSubMenuItem "test" subMenu

        mainMenuBar.addItem submenuItem menuPos
        -- redraw the menu bar with the new item
        menuMan.updateMenuBar()
    )

    -- This one will allow an app to add theirs to existing exchange store app.
    -- MUST use genclassid() to get this value and it should be DIFFERENT per app.
    -- This then allows only onetime setup per app, per user UI setup

    local stringMacroScriptName = "ADNExplodeGeomMS" 
    local stringMacroScriptCategory = "ADN Samples"
    if menuMan.registerMenuContext 0x7b244316 then
    (
        -- probably can take these out, but it shows that it is called only when needed...
        print "Creating ADN Explode Geometry Sub-Menu"

        -- this should always succeed because above
        local exchangeMenu = menuMan.findMenu stringExhangeStoreDefaultMenu

        -- create the action item    
        local actionItem1 = menuMan.createActionItem stringMacroScriptName stringMacroScriptCategory

        -- Add the action item as a menu entry
        exchangeMenu.addItem actionItem1 -1

        -- Let's also seperate each app...
        local menuSepItem = menuMan.createSeparatorItem()
        exchangeMenu.addItem menuSepItem -1

        -- redraw the menu bar with the new item
        menuMan.updateMenuBar()
    )
)
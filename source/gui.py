

import wx
import wx.xrc
import wx.adv
import wx.html


class mainGui ( wx.Frame ):

	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"OCI Auditing", pos = wx.DefaultPosition, size = wx.Size( 680,630 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

		self.SetSizeHints( wx.Size( -1,-1 ), wx.Size( -1,-1 ) )
		self.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.SetBackgroundColour( wx.Colour( 250, 205, 98 ) )

		self.m_menubar = wx.MenuBar( 0|wx.TAB_TRAVERSAL )
		self.m_menubar.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )

		self.m_menu_options = wx.Menu()
		self.m_menuItem_connection = wx.MenuItem( self.m_menu_options, wx.ID_ANY, u"&Connection Check", u"Checks connection to all selected tenancies.", wx.ITEM_NORMAL )
		self.m_menuItem_connection.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_TICK_MARK, wx.ART_MENU ) )
		self.m_menu_options.Append( self.m_menuItem_connection )

		self.m_menubar.Append( self.m_menu_options, u"&Options" )

		self.m_menu_conf = wx.Menu()
		self.m_menuItem_openConfigs = wx.MenuItem( self.m_menu_conf, wx.ID_ANY, u"&Open Configurations", u"Open \"configurations/tool.ini\" file in your default editor.\n\nfor better experience associate \"ini\" file extensions in your system to advanced editors.", wx.ITEM_NORMAL )
		self.m_menuItem_openConfigs.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_FILE_OPEN, wx.ART_MENU ) )
		self.m_menu_conf.Append( self.m_menuItem_openConfigs )

		self.m_menuItem_reloadConfigs = wx.MenuItem( self.m_menu_conf, wx.ID_ANY, u"&Reload Configurations", u"If \"tool.ini\" is modified while UI is open, this will reload to update configurations.", wx.ITEM_NORMAL )
		self.m_menuItem_reloadConfigs.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_REDO, wx.ART_MENU ) )
		self.m_menu_conf.Append( self.m_menuItem_reloadConfigs )

		self.m_menuItem_tenancies = wx.MenuItem( self.m_menu_conf, wx.ID_ANY, u"&Tenancies", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItem_tenancies.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_LIST_VIEW, wx.ART_MENU ) )
		self.m_menu_conf.Append( self.m_menuItem_tenancies )
		self.m_menuItem_tenancies.Enable( False )

		self.m_menubar.Append( self.m_menu_conf, u"&Configurations" )

		self.m_menu_shortcuts = wx.Menu()
		self.m_menuItem_servicesWindow = wx.MenuItem( self.m_menu_shortcuts, wx.ID_ANY, u"&Services Window"+ u"\t" + u"Ctrl+S", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItem_servicesWindow.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_LIST_VIEW, wx.ART_MENU ) )
		self.m_menu_shortcuts.Append( self.m_menuItem_servicesWindow )

		self.m_menuItem_networkingWindow = wx.MenuItem( self.m_menu_shortcuts, wx.ID_ANY, u"&Networking Window"+ u"\t" + u"Ctrl+N", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItem_networkingWindow.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_LIST_VIEW, wx.ART_MENU ) )
		self.m_menu_shortcuts.Append( self.m_menuItem_networkingWindow )

		self.m_menuItem_startAudit = wx.MenuItem( self.m_menu_shortcuts, wx.ID_ANY, u"&Start"+ u"\t" + u"Ctrl+G", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuItem_startAudit.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_MENU ) )
		self.m_menu_shortcuts.Append( self.m_menuItem_startAudit )

		self.m_menubar.Append( self.m_menu_shortcuts, u"&Shortcuts" )

		self.m_menu_help = wx.Menu()
		self.m_menuItem_doc = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"&Document"+ u"\t" + u"Ctrl+D", u"Opens Document Page for more details of this Tool", wx.ITEM_NORMAL )
		self.m_menuItem_doc.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_HELP, wx.ART_MENU ) )
		self.m_menu_help.Append( self.m_menuItem_doc )

		self.m_menuItem_about = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"&About"+ u"\t" + u"Ctrl+A", u"Shows information about this tool", wx.ITEM_NORMAL )
		self.m_menuItem_about.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_INFORMATION, wx.ART_MENU ) )
		self.m_menu_help.Append( self.m_menuItem_about )

		self.m_menu_help.AppendSeparator()

		self.m_menuItem_credits = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"&Credits", u"Shows ideas and contributions details", wx.ITEM_NORMAL )
		self.m_menuItem_credits.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_ADD_BOOKMARK, wx.ART_MENU ) )
		self.m_menu_help.Append( self.m_menuItem_credits )

		self.m_menu_help.AppendSeparator()

		self.m_menuItem_updates = wx.MenuItem( self.m_menu_help, wx.ID_ANY, u"Check &Updates"+ u"\t" + u"Ctrl+U", u"Check for updates in recent releases", wx.ITEM_NORMAL )
		self.m_menuItem_updates.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_UP, wx.ART_MENU ) )
		self.m_menu_help.Append( self.m_menuItem_updates )

		self.m_submenu_submit = wx.Menu()
		self.m_menuItem_feedback = wx.MenuItem( self.m_submenu_submit, wx.ID_ANY, u"&Feedback", u"Submit your feedback ..", wx.ITEM_NORMAL )
		self.m_submenu_submit.Append( self.m_menuItem_feedback )

		self.m_menuItem_feature = wx.MenuItem( self.m_submenu_submit, wx.ID_ANY, u"&New Feature", u"Propose enhancements or new feature request with details ..", wx.ITEM_NORMAL )
		self.m_submenu_submit.Append( self.m_menuItem_feature )

		self.m_menuItem_defect = wx.MenuItem( self.m_submenu_submit, wx.ID_ANY, u"&Defect", u"Submit any issue that you found with details ..", wx.ITEM_NORMAL )
		self.m_submenu_submit.Append( self.m_menuItem_defect )

		self.m_menu_help.AppendSubMenu( self.m_submenu_submit, u"&Submit" )

		self.m_submenu_ref = wx.Menu()
		self.m_menuItem_guard = wx.MenuItem( self.m_submenu_ref, wx.ID_ANY, u"Cloud &Guard", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_submenu_ref.Append( self.m_menuItem_guard )

		self.m_menuItem_advisor = wx.MenuItem( self.m_submenu_ref, wx.ID_ANY, u"Cloud &Advisor", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_submenu_ref.Append( self.m_menuItem_advisor )

		self.m_menu_help.AppendSubMenu( self.m_submenu_ref, u"&References" )

		self.m_menubar.Append( self.m_menu_help, u"&Help   " )

		self.SetMenuBar( self.m_menubar )

		bSizer = wx.BoxSizer( wx.VERTICAL )

		self.m_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		self.m_panel.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_panel.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_panel.SetBackgroundColour( wx.Colour( 40, 39, 35 ) )

		SizerOuter = wx.BoxSizer( wx.VERTICAL )

		bSizerBrand = wx.BoxSizer( wx.HORIZONTAL )


		bSizerBrand.Add( ( 10, 0), 0, wx.FIXED_MINSIZE, 5 )

		self.m_logo_bitmap = wx.StaticBitmap( self.m_panel, wx.ID_ANY, wx.ArtProvider.GetBitmap( wx.ART_MISSING_IMAGE, wx.ART_FRAME_ICON ), wx.DefaultPosition, wx.Size( 75,75 ), 0 )
		bSizerBrand.Add( self.m_logo_bitmap, 0, wx.ALL, 5 )


		bSizerBrand.Add( ( 10, 0), 0, wx.EXPAND, 5 )

		self.m_staticText_oci = wx.StaticText( self.m_panel, wx.ID_ANY, u"Oracle Cloud Infrastructure", wx.DefaultPosition, wx.Size( -1,48 ), 0 )
		self.m_staticText_oci.Wrap( -1 )

		self.m_staticText_oci.SetFont( wx.Font( 20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, "Corbel" ) )
		self.m_staticText_oci.SetForegroundColour( wx.Colour( 203, 106, 53 ) )

		bSizerBrand.Add( self.m_staticText_oci, 0, wx.ALIGN_BOTTOM, 5 )


		bSizerBrand.Add( ( 10, 0), 0, wx.EXPAND, 5 )

		self.m_staticText_sub_header = wx.StaticText( self.m_panel, wx.ID_ANY, u"\nOCI Tenancies Detailed Auditing", wx.Point( -1,-1 ), wx.Size( -1,49 ), 0 )
		self.m_staticText_sub_header.Wrap( -1 )

		self.m_staticText_sub_header.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_staticText_sub_header.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizerBrand.Add( self.m_staticText_sub_header, 0, wx.ALIGN_BOTTOM, 5 )


		SizerOuter.Add( bSizerBrand, 1, wx.EXPAND, 5 )

		fgSizerInputs = wx.FlexGridSizer( 4, 4, 0, 0 )
		fgSizerInputs.SetFlexibleDirection( wx.BOTH )
		fgSizerInputs.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )


		fgSizerInputs.Add( ( 60, 0), 1, 0, 5 )

		self.m_staticText_domains = wx.StaticText( self.m_panel, wx.ID_ANY, u"Tenancies:", wx.DefaultPosition, wx.Size( 250,-1 ), 0 )
		self.m_staticText_domains.Wrap( -1 )

		self.m_staticText_domains.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText_domains.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.m_staticText_domains.SetToolTip( u"Select OCIC Domains here." )

		fgSizerInputs.Add( self.m_staticText_domains, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5 )


		fgSizerInputs.Add( ( 50, 0), 0, 0, 5 )

		self.m_staticText_audits = wx.StaticText( self.m_panel, wx.ID_ANY, u"Audits:", wx.DefaultPosition, wx.Size( 180,-1 ), 0 )
		self.m_staticText_audits.Wrap( -1 )

		self.m_staticText_audits.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText_audits.SetForegroundColour( wx.Colour( 255, 255, 255 ) )

		fgSizerInputs.Add( self.m_staticText_audits, 0, wx.ALL, 5 )


		fgSizerInputs.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		self.m_domains_listCtrl = wx.ListCtrl( self.m_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( 240,330 ), wx.LC_NO_HEADER|wx.LC_REPORT|wx.BORDER_NONE )
		self.m_domains_listCtrl.SetFont( wx.Font( 11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_domains_listCtrl.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_domains_listCtrl.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.m_domains_listCtrl.SetToolTip( u"Select OCI Tenancies here.\nUse CTRL / SHIFT for multiple selections.\nGrey Background indicates, configuration incomplete for that tenancy." )

		fgSizerInputs.Add( self.m_domains_listCtrl, 0, wx.ALL, 5 )


		fgSizerInputs.Add( ( 0, 0), 1, wx.EXPAND, 5 )

		bSizer_checkBoxes = wx.BoxSizer( wx.VERTICAL )

		self.m_panel2 = wx.Panel( self.m_panel, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		self.m_panel2.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.m_panel2.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.m_panel2.SetToolTip( u"Select Required Audits" )

		bSizer6 = wx.BoxSizer( wx.VERTICAL )

		bSizer6.SetMinSize( wx.Size( 200,-1 ) )
		self.m_staticline2 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		self.m_staticline2.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )
		self.m_staticline2.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

		bSizer6.Add( self.m_staticline2, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_staticText_mandatory_audits = wx.StaticText( self.m_panel2, wx.ID_ANY, u"default selections", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_mandatory_audits.Wrap( -1 )

		self.m_staticText_mandatory_audits.SetFont( wx.Font( 7, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_staticText_mandatory_audits.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_ACTIVEBORDER ) )

		bSizer6.Add( self.m_staticText_mandatory_audits, 0, wx.ALIGN_BOTTOM|wx.ALIGN_CENTER, 0 )

		self.m_checkBox_Tenancies = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Tenancies", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.m_checkBox_Tenancies.SetValue(True)
		self.m_checkBox_Tenancies.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_Tenancies.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_checkBox_Tenancies.Enable( False )

		bSizer6.Add( self.m_checkBox_Tenancies, 0, wx.ALL, 5 )

		self.m_checkBox_Compartments = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Compartments", wx.DefaultPosition, wx.Size( 150,-1 ), 0 )
		self.m_checkBox_Compartments.SetValue(True)
		self.m_checkBox_Compartments.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_Compartments.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_checkBox_Compartments.Enable( False )

		bSizer6.Add( self.m_checkBox_Compartments, 0, wx.ALL, 5 )

		self.m_staticline1 = wx.StaticLine( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
		bSizer6.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

		self.m_checkBox_UserGroups = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"&Users and Groups", wx.Point( 0,0 ), wx.Size( -1,-1 ), 0 )
		self.m_checkBox_UserGroups.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_UserGroups.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_checkBox_UserGroups.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )

		bSizer6.Add( self.m_checkBox_UserGroups, 0, wx.ALL, 5 )

		self.m_checkBox_serviceLimits = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Service &Limits", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_serviceLimits.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_serviceLimits.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer6.Add( self.m_checkBox_serviceLimits, 0, wx.ALL, 5 )

		self.m_checkBox_Policies = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"&Policies", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_Policies.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_Policies.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer6.Add( self.m_checkBox_Policies, 0, wx.ALL, 5 )

		bSizer62 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_checkBox_Instances = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"&Services Used", wx.DefaultPosition, wx.Size( 147,-1 ), 0 )
		self.m_checkBox_Instances.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_Instances.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer62.Add( self.m_checkBox_Instances, 0, wx.ALL, 5 )

		self.m_button_instances = wx.Button( self.m_panel2, wx.ID_ANY, u">", wx.DefaultPosition, wx.Size( 34,24 ), 0 )
		self.m_button_instances.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_button_instances.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_button_instances.SetBackgroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer62.Add( self.m_button_instances, 0, wx.ALIGN_CENTER|wx.ALL, 0 )


		bSizer6.Add( bSizer62, 0, 0, 5 )

		bSizer63 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_checkBox_Events = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"&Events", wx.DefaultPosition, wx.Size( 147,-1 ), 0 )
		self.m_checkBox_Events.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_Events.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer63.Add( self.m_checkBox_Events, 0, wx.ALL, 5 )

		self.m_button_events = wx.Button( self.m_panel2, wx.ID_ANY, u">", wx.DefaultPosition, wx.Size( 34,24 ), 0 )
		self.m_button_events.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_button_events.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_button_events.SetBackgroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer63.Add( self.m_button_events, 0, wx.ALIGN_CENTER|wx.ALL, 0 )


		bSizer6.Add( bSizer63, 0, 0, 5 )

		bSizer64 = wx.BoxSizer( wx.HORIZONTAL )

		self.m_checkBox_Networking = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"&Networking", wx.DefaultPosition, wx.Size( 147,-1 ), 0 )
		self.m_checkBox_Networking.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_Networking.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer64.Add( self.m_checkBox_Networking, 0, wx.ALL, 5 )

		self.m_button_networking = wx.Button( self.m_panel2, wx.ID_ANY, u">", wx.DefaultPosition, wx.Size( 34,24 ), 0 )
		self.m_button_networking.SetFont( wx.Font( 12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_ITALIC, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_button_networking.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.m_button_networking.SetBackgroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer64.Add( self.m_button_networking, 0, wx.ALIGN_CENTER|wx.ALL, 0 )


		bSizer6.Add( bSizer64, 0, 0, 5 )

		self.m_checkBox_CloudGuard = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Cloud &Guard", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_CloudGuard.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_CloudGuard.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer6.Add( self.m_checkBox_CloudGuard, 0, wx.ALL, 5 )

		self.m_checkBox_CloudAdvisor = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Cloud &Advisor", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_CloudAdvisor.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_CloudAdvisor.SetForegroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer6.Add( self.m_checkBox_CloudAdvisor, 0, wx.ALL, 5 )

		self.m_checkBox_Billing = wx.CheckBox( self.m_panel2, wx.ID_ANY, u"Billing", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_checkBox_Billing.SetFont( wx.Font( 12, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_checkBox_Billing.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_checkBox_Billing.Enable( False )
		self.m_checkBox_Billing.Hide()

		bSizer6.Add( self.m_checkBox_Billing, 0, wx.ALL, 5 )


		bSizer6.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		self.m_panel2.SetSizer( bSizer6 )
		self.m_panel2.Layout()
		bSizer6.Fit( self.m_panel2 )
		bSizer_checkBoxes.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 5 )


		fgSizerInputs.Add( bSizer_checkBoxes, 1, wx.EXPAND, 5 )


		SizerOuter.Add( fgSizerInputs, 1, wx.EXPAND, 5 )


		SizerOuter.Add( ( 0, 0), 1, wx.EXPAND, 2 )

		gSizer1 = wx.GridSizer( 1, 3, 0, 0 )

		self.m_staticField1 = wx.StaticText( self.m_panel, wx.ID_ANY, u"Region", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticField1.Wrap( -1 )

		self.m_staticField1.SetFont( wx.Font( 10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.m_staticField1.Hide()

		gSizer1.Add( self.m_staticField1, 0, wx.ALIGN_CENTER_VERTICAL|wx.LEFT|wx.TOP, 10 )

		self.start_button = wx.Button( self.m_panel, wx.ID_ANY, wx.EmptyString, wx.Point( -1,-1 ), wx.Size( 100,40 ), 0|wx.BORDER_RAISED )

		self.start_button.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_CMN_DIALOG ) )
		self.start_button.SetBitmapPressed( wx.NullBitmap )
		self.start_button.SetBitmapFocus( wx.NullBitmap )
		self.start_button.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.start_button.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.start_button.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.start_button.SetToolTip( u"On Click,\nOCI Auditing will be started.." )

		gSizer1.Add( self.start_button, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 0 )


		SizerOuter.Add( gSizer1, 1, wx.EXPAND, 5 )

		self.gauge = wx.Gauge( self.m_panel, wx.ID_ANY, 100, wx.Point( -1,-1 ), wx.Size( 645,20 ), wx.GA_HORIZONTAL|wx.GA_SMOOTH|wx.BORDER_RAISED )
		self.gauge.SetValue( 0 )
		self.gauge.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
		self.gauge.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )

		SizerOuter.Add( self.gauge, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 2 )


		SizerOuter.Add( ( 0, 0), 1, wx.EXPAND, 5 )


		self.m_panel.SetSizer( SizerOuter )
		self.m_panel.Layout()
		SizerOuter.Fit( self.m_panel )
		bSizer.Add( self.m_panel, 1, wx.ALL|wx.EXPAND, 5 )


		self.SetSizer( bSizer )
		self.Layout()
		self.statusBar = self.CreateStatusBar( 1, 0, wx.ID_ANY )
		self.statusBar.SetFont( wx.Font( 11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Calibri" ) )
		self.statusBar.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT ) )
		self.statusBar.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.statusBar.SetMinSize( wx.Size( -1,30 ) )
		self.statusBar.SetMaxSize( wx.Size( -1,35 ) )


		self.Centre( wx.BOTH )

		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.Bind( wx.EVT_MENU, self.TenanciesConnectionCheck, id = self.m_menuItem_connection.GetId() )
		self.Bind( wx.EVT_MENU, self.OpenConfigurations, id = self.m_menuItem_openConfigs.GetId() )
		self.Bind( wx.EVT_MENU, self.ReloadConfigurations, id = self.m_menuItem_reloadConfigs.GetId() )
		self.Bind( wx.EVT_MENU, self.OpenTenancyConfigWizard, id = self.m_menuItem_tenancies.GetId() )
		self.Bind( wx.EVT_MENU, self.openInstancesSelection, id = self.m_menuItem_servicesWindow.GetId() )
		self.Bind( wx.EVT_MENU, self.openNetworkingSelection, id = self.m_menuItem_networkingWindow.GetId() )
		self.Bind( wx.EVT_MENU, self.startConnectionAndreporting, id = self.m_menuItem_startAudit.GetId() )
		self.Bind( wx.EVT_MENU, self.OpenDocumentPage, id = self.m_menuItem_doc.GetId() )
		self.Bind( wx.EVT_MENU, self.ShowAboutMessage, id = self.m_menuItem_about.GetId() )
		self.Bind( wx.EVT_MENU, self.ShowCreditsMessage, id = self.m_menuItem_credits.GetId() )
		self.Bind( wx.EVT_MENU, self.CheckForUpdates, id = self.m_menuItem_updates.GetId() )
		self.Bind( wx.EVT_MENU, self.SubmitFeedback, id = self.m_menuItem_feedback.GetId() )
		self.Bind( wx.EVT_MENU, self.SubmitFeature, id = self.m_menuItem_feature.GetId() )
		self.Bind( wx.EVT_MENU, self.SubmitDefect, id = self.m_menuItem_defect.GetId() )
		self.Bind( wx.EVT_MENU, self.OpenCloudGuardPage, id = self.m_menuItem_guard.GetId() )
		self.Bind( wx.EVT_MENU, self.OpenCloudAdvisorPage, id = self.m_menuItem_advisor.GetId() )
		self.m_domains_listCtrl.Bind( wx.EVT_LIST_ITEM_DESELECTED, self.domainsSelectionChanged )
		self.m_domains_listCtrl.Bind( wx.EVT_LIST_ITEM_SELECTED, self.domainsSelectionChanged )
		self.m_checkBox_Tenancies.Bind( wx.EVT_CHECKBOX, self.compartmentsSelectionChanged )
		self.m_checkBox_UserGroups.Bind( wx.EVT_CHECKBOX, self.userGroupsSelectionChanged )
		self.m_checkBox_serviceLimits.Bind( wx.EVT_CHECKBOX, self.limitsSelectionChanged )
		self.m_checkBox_Policies.Bind( wx.EVT_CHECKBOX, self.policiesSelectionChanged )
		self.m_checkBox_Instances.Bind( wx.EVT_CHECKBOX, self.instancesSelectionChanged )
		self.m_button_instances.Bind( wx.EVT_BUTTON, self.openInstancesSelection )
		self.m_checkBox_Events.Bind( wx.EVT_CHECKBOX, self.eventsSelectionChanged )
		self.m_button_events.Bind( wx.EVT_BUTTON, self.openEventsSelection )
		self.m_checkBox_Networking.Bind( wx.EVT_CHECKBOX, self.networkingSelectionChanged )
		self.m_button_networking.Bind( wx.EVT_BUTTON, self.openNetworkingSelection )
		self.m_checkBox_CloudGuard.Bind( wx.EVT_CHECKBOX, self.cloudGuardSelectionChanged )
		self.m_checkBox_CloudAdvisor.Bind( wx.EVT_CHECKBOX, self.cloudAdvisorSelectionChanged )
		self.m_checkBox_Billing.Bind( wx.EVT_CHECKBOX, self.billingSelectionChanged )
		self.start_button.Bind( wx.EVT_BUTTON, self.startConnectionAndreporting )

	def __del__( self ):
		pass


	def onClose( self, event ):
		event.Skip()

	def TenanciesConnectionCheck( self, event ):
		event.Skip()

	def OpenConfigurations( self, event ):
		event.Skip()

	def ReloadConfigurations( self, event ):
		event.Skip()

	def OpenTenancyConfigWizard( self, event ):
		event.Skip()

	def openInstancesSelection( self, event ):
		event.Skip()

	def openNetworkingSelection( self, event ):
		event.Skip()

	def startConnectionAndreporting( self, event ):
		event.Skip()

	def OpenDocumentPage( self, event ):
		event.Skip()

	def ShowAboutMessage( self, event ):
		event.Skip()

	def ShowCreditsMessage( self, event ):
		event.Skip()

	def CheckForUpdates( self, event ):
		event.Skip()

	def SubmitFeedback( self, event ):
		event.Skip()

	def SubmitFeature( self, event ):
		event.Skip()

	def SubmitDefect( self, event ):
		event.Skip()

	def OpenCloudGuardPage( self, event ):
		event.Skip()

	def OpenCloudAdvisorPage( self, event ):
		event.Skip()

	def domainsSelectionChanged( self, event ):
		event.Skip()


	def compartmentsSelectionChanged( self, event ):
		event.Skip()

	def userGroupsSelectionChanged( self, event ):
		event.Skip()

	def limitsSelectionChanged( self, event ):
		event.Skip()

	def policiesSelectionChanged( self, event ):
		event.Skip()

	def instancesSelectionChanged( self, event ):
		event.Skip()


	def eventsSelectionChanged( self, event ):
		event.Skip()

	def openEventsSelection( self, event ):
		event.Skip()

	def networkingSelectionChanged( self, event ):
		event.Skip()


	def cloudGuardSelectionChanged( self, event ):
		event.Skip()

	def cloudAdvisorSelectionChanged( self, event ):
		event.Skip()

	def billingSelectionChanged( self, event ):
		event.Skip()




class instancesDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Select OCI Services", pos = wx.DefaultPosition, size = wx.Size( 400,462 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.SetBackgroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_services_listCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 380,380 ), wx.LC_NO_HEADER|wx.LC_REPORT|wx.BORDER_NONE )
		self.m_services_listCtrl.SetFont( wx.Font( 11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_services_listCtrl.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_services_listCtrl.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.m_services_listCtrl.SetToolTip( u"Select Services\n\nEvery \"Instance\" details, of selected services will be shown in the report." )

		bSizer9.Add( self.m_services_listCtrl, 0, wx.EXPAND|wx.TOP, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.Point( -1,-1 ), wx.Size( 100,40 ), 0|wx.BORDER_RAISED )

		self.ok_button.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_CMN_DIALOG ) )
		self.ok_button.SetBitmapPressed( wx.NullBitmap )
		self.ok_button.SetBitmapFocus( wx.NullBitmap )
		self.ok_button.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.ok_button.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.ok_button.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.ok_button.SetToolTip( u"OK" )

		bSizer9.Add( self.ok_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.SetSizer( bSizer9 )
		self.Layout()

		self.Centre( wx.BOTH )

		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_services_listCtrl.Bind( wx.EVT_CHAR, self.keyPressOnServicesList )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onClose )

	def __del__( self ):
		pass


	def onClose( self, event ):
		event.Skip()

	def keyPressOnServicesList( self, event ):
		event.Skip()




class eventsDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Select options for Audit Events", pos = wx.DefaultPosition, size = wx.Size( 240,231 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		m_radioBox_dateRangeChoices = [ u"Past 1 hour", u"Past 1 day", u"Past 30 days", u"All events from last run" ]
		self.m_radioBox_dateRange = wx.RadioBox( self, wx.ID_ANY, u"Date Range", wx.DefaultPosition, wx.DefaultSize, m_radioBox_dateRangeChoices, 1, wx.RA_SPECIFY_COLS )
		self.m_radioBox_dateRange.SetSelection( 2 )
		self.m_radioBox_dateRange.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOW ) )
		self.m_radioBox_dateRange.SetBackgroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer9.Add( self.m_radioBox_dateRange, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10 )

		self.ok_button = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.Point( -1,-1 ), wx.Size( 100,40 ), 0|wx.BORDER_RAISED )

		self.ok_button.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_CMN_DIALOG ) )
		self.ok_button.SetBitmapPressed( wx.NullBitmap )
		self.ok_button.SetBitmapFocus( wx.NullBitmap )
		self.ok_button.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.ok_button.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.ok_button.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.ok_button.SetToolTip( u"OK" )

		bSizer9.Add( self.ok_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.SetSizer( bSizer9 )
		self.Layout()

		self.Centre( wx.BOTH )

		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_radioBox_dateRange.Bind( wx.EVT_RADIOBOX, self.onButtonChange )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onClose )

	def __del__( self ):
		pass


	def onClose( self, event ):
		event.Skip()

	def onButtonChange( self, event ):
		event.Skip()




class networkingDialog ( wx.Dialog ):

	def __init__( self, parent ):
		wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = u"Select Network Components", pos = wx.DefaultPosition, size = wx.Size( 400,460 ), style = wx.DEFAULT_DIALOG_STYLE|wx.STAY_ON_TOP )

		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		self.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.SetBackgroundColour( wx.Colour( 250, 205, 98 ) )

		bSizer9 = wx.BoxSizer( wx.VERTICAL )

		self.m_networkComponents_listCtrl = wx.ListCtrl( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 380,370 ), wx.LC_NO_HEADER|wx.LC_REPORT|wx.BORDER_NONE )
		self.m_networkComponents_listCtrl.SetFont( wx.Font( 11, wx.FONTFAMILY_ROMAN, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "Courier New" ) )
		self.m_networkComponents_listCtrl.SetForegroundColour( wx.Colour( 250, 205, 98 ) )
		self.m_networkComponents_listCtrl.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.m_networkComponents_listCtrl.SetToolTip( u"Select Network Components\n\nDetails of selected components will be shown in the report." )

		bSizer9.Add( self.m_networkComponents_listCtrl, 0, wx.EXPAND|wx.TOP, 5 )

		self.ok_button = wx.Button( self, wx.ID_ANY, wx.EmptyString, wx.Point( -1,-1 ), wx.Size( 100,40 ), 0|wx.BORDER_RAISED )

		self.ok_button.SetBitmap( wx.ArtProvider.GetBitmap( wx.ART_GO_FORWARD, wx.ART_CMN_DIALOG ) )
		self.ok_button.SetBitmapPressed( wx.NullBitmap )
		self.ok_button.SetBitmapFocus( wx.NullBitmap )
		self.ok_button.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.ok_button.SetForegroundColour( wx.Colour( 255, 255, 255 ) )
		self.ok_button.SetBackgroundColour( wx.Colour( 32, 32, 32 ) )
		self.ok_button.SetToolTip( u"OK" )

		bSizer9.Add( self.ok_button, 0, wx.ALIGN_CENTER|wx.ALL, 5 )


		self.SetSizer( bSizer9 )
		self.Layout()

		self.Centre( wx.BOTH )

		self.Bind( wx.EVT_CLOSE, self.onClose )
		self.m_networkComponents_listCtrl.Bind( wx.EVT_CHAR, self.keyPressOnNetworksList )
		self.ok_button.Bind( wx.EVT_BUTTON, self.onClose )

	def __del__( self ):
		pass


	def onClose( self, event ):
		event.Skip()

	def keyPressOnNetworksList( self, event ):
		event.Skip()




class configWizard ( wx.adv.Wizard ):

	def __init__( self, parent ):
		wx.adv.Wizard.__init__ ( self, parent, id = wx.ID_ANY, title = u"Configurations", bitmap = wx.NullBitmap, pos = wx.DefaultPosition, style = wx.DEFAULT_DIALOG_STYLE )

		self.SetSizeHints( wx.Size( 630,460 ), wx.DefaultSize )
		self.m_pages = []

		self.m_wizPage1 = wx.adv.WizardPageSimple( self  )
		self.add_page( self.m_wizPage1 )

		self.m_wizPage1.SetMinSize( wx.Size( -630,460 ) )

		bSizer12 = wx.BoxSizer( wx.VERTICAL )

		bSizer12.SetMinSize( wx.Size( 630,460 ) )

		bSizer12.Add( ( 0, 50), 0, wx.EXPAND, 5 )

		self.m_staticText_Config1 = wx.StaticText( self.m_wizPage1, wx.ID_ANY, u"Tenancies Configuration:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_Config1.Wrap( -1 )

		self.m_staticText_Config1.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText_Config1.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		bSizer12.Add( self.m_staticText_Config1, 0, wx.ALL, 5 )


		bSizer12.Add( ( 0, 5), 0, wx.EXPAND, 5 )

		self.m_staticText8 = wx.StaticText( self.m_wizPage1, wx.ID_ANY, u"Before proceeding to next screen, make sure your tenancy/s information like,\n    tenancy name, tenancy ocid, home region\n    user ocid, key file, fingerprint\nare ready with you !\n\n", wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
		self.m_staticText8.Wrap( -1 )

		bSizer12.Add( self.m_staticText8, 0, wx.ALL, 5 )


		bSizer12.Add( ( 0, 30), 0, wx.EXPAND, 0 )

		self.m_button8 = wx.Button( self.m_wizPage1, wx.ID_ANY, u"&Help to get these information", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer12.Add( self.m_button8, 0, wx.ALL, 5 )


		self.m_wizPage1.SetSizer( bSizer12 )
		self.m_wizPage1.Layout()
		self.m_wizPage2 = wx.adv.WizardPageSimple( self  )
		self.add_page( self.m_wizPage2 )

		self.m_wizPage2.SetMinSize( wx.Size( 630,460 ) )

		bSizer13 = wx.BoxSizer( wx.VERTICAL )

		bSizer13.SetMinSize( wx.Size( 630,460 ) )

		bSizer13.Add( ( 0, 50), 0, wx.EXPAND, 5 )

		self.m_staticText_Config11 = wx.StaticText( self.m_wizPage2, wx.ID_ANY, u"Open, Update and Save Configurations:", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText_Config11.Wrap( -1 )

		self.m_staticText_Config11.SetFont( wx.Font( 15, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD, False, wx.EmptyString ) )
		self.m_staticText_Config11.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHT ) )

		bSizer13.Add( self.m_staticText_Config11, 0, wx.ALL, 5 )


		bSizer13.Add( ( 0, 5), 0, wx.EXPAND, 5 )

		self.m_staticText81 = wx.StaticText( self.m_wizPage2, wx.ID_ANY, u"1. Click below button to open configuration file.\n2. Locate this, add required OCI tenancy details here.", wx.DefaultPosition, wx.Size( 500,-1 ), 0 )
		self.m_staticText81.Wrap( -1 )

		bSizer13.Add( self.m_staticText81, 0, wx.ALL, 5 )

		self.m_htmlWin1 = wx.html.HtmlWindow( self.m_wizPage2, wx.ID_ANY, wx.DefaultPosition, wx.Size( 500,100 ), wx.html.HW_SCROLLBAR_AUTO )
		bSizer13.Add( self.m_htmlWin1, 0, wx.ALL, 5 )

		self.m_button81 = wx.Button( self.m_wizPage2, wx.ID_ANY, u"Open Configuration file in your default Text Editor", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizer13.Add( self.m_button81, 0, wx.ALL, 5 )


		bSizer13.Add( ( 0, 30), 0, wx.EXPAND, 0 )


		self.m_wizPage2.SetSizer( bSizer13 )
		self.m_wizPage2.Layout()
		self.Centre( wx.BOTH )


		self.m_button8.Bind( wx.EVT_BUTTON, self.OpenUserConfigurationsHelp )
		self.m_button81.Bind( wx.EVT_BUTTON, self.OpenUserConfigurationsHelp )
	def add_page(self, page):
		if self.m_pages:
			previous_page = self.m_pages[-1]
			page.SetPrev(previous_page)
			previous_page.SetNext(page)
		self.m_pages.append(page)

	def __del__( self ):
		pass


	def OpenUserConfigurationsHelp( self, event ):
		event.Skip()




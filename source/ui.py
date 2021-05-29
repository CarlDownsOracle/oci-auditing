import wx,sys,os,re,locale
uio=sys.modules[__name__]
from wx.lib.embeddedimage import PyEmbeddedImage
from gui import mainGui,instancesDialog,eventsDialog,networkingDialog
import the, start
the.ui=uio
threading=the.threading
conf=the.conf
log=conf.log
gaugeBreaks=the.gaugeBreaks
the.justConnectionCheck=False
app_icon = PyEmbeddedImage(
    b'iVBORw0KGgoAAAANSUhEUgAAAEsAAABLCAYAAAA4TnrqAAAAAXNSR0IArs4c6QAAAARnQU1B'
    b'AACxjwv8YQUAAAAJcEhZcwAADsEAAA7BAbiRa+0AABFjSURBVHhe7VsLeFXVlf7PPo/7SG7e'
    b'CSEQQlASJAjyqEZAEIudlra0na/VqX6dasdPx7FTx+lUO36tkdZqHcfnTB3fjKPWDlO1Bf18'
    b'ICM+QETUYDUQ3gbI+3lz3+c1a+1zbwiINgiCce5/s8+555x99t7rP2utvdY+N8giiyyyyCKL'
    b'LLLIIossssgiiyxGDiW9P+5ou/KmiWoooPsMINEXc3sH+jpOeeiWwfTlzySOG1k7fvSzyYG6'
    b'mrrg6bNhjK9A4oX11woNxRAOrIRlKaWlvzUqx2xONr6HSKr/ueqLL06kb/3M4FMl66WGBq12'
    b'wtRCtTD/22p50TdUof2FUTkWIpQH1TCgqC5cOHAc2iYcuJEozM4u+MaN+ZfB1zaGI9v3/L76'
    b'6su3KYripps8ofhUyCLJFLy3Qm97zTrPN63mb/zV4+aoxQW5ilChKA7VoG4dBYpDRFFt77wC'
    b'1yXSBF2zbdfs6oUzEF6NlLlsYHvT1gnnn9/rtX7i8KmQtfvKG04r+v7XFyr5oSu04uLJWtAv'
    b'GWQyrL4BWHv2w+7shR2OQaFzIjcApawAPtI6dUwpkSe4OtyUZdr9A3vNjq4nXGHfWDhzZr/X'
    b'w4nBMSdrW8Od43OmVD+Wt6j+DL0g31BUUpVkCsnWLoRfexupF18Dmpvh9gwAcZPIokH4NdhF'
    b'QWgnTYSxcC5yF82DXlUBze8jgh2k4vFBW8HdHR2dDTU1Ncl0V8cdx4wslrml4bZqo3bSQ8EF'
    b'9fP9ZUUqyQmrvRPR/12H+B/WwHqrCW5XJzTLIhMUZHp8I22YMUFaR+ZoF+ZDn1YL/9fOQe6S'
    b'BUTaOEBV4Vp22OrrvyO3ovwmMtkT4vyPHVmbNukdTXtuDS1Z9EMRCim2ayG1owXRe/8byade'
    b'gNLeQQSRO6K6Gjl0CUmW8L4QYXxWejRSRpEfgvq1hQj9/UUInFoDQUSaiXjUSaV+mrNx4/1i'
    b'yZLjrmE80qOG2/CS1hZNnhk4Z/4iNZQj567k1t0I3/oAUo8+CbR2kIpRRXLqKhWvW9IWWcix'
    b'cxtUGHLes2nTF4b55Gr03HQPom80wrEtqIFAjuoL/LpH+H5A/u+YjP1IcEw67JkeL9dV7Q6t'
    b'KK+OtSK1rw2R2x6C+dRqmtGiUl3Y2iR4z/bn/XmmKL+nP3xMIL8PEU1Afe4lRO5ajviuFmqH'
    b'6DX0nEBd7fnhLVsKvZrHD0dNltvQINzc3LP9U2tqoWmKbToIP7EKeGYNlIEImZ6nM26arTQX'
    b'B+Hgcx5hPB8KV6NJgMx5zQYM/OZxWP0DEHRRKyg4c3B3V8N7t95fRBpGE+rBJd3QMcdRN9x3'
    b'+/IC56zZD+fU1Sx1VAFz6w50XvwToHELBJkTiUy1uBsywaHePrrbNLVkjg7VIsoowreJM+Xk'
    b'kxC66zoULqynAwXR3a2mURD6oxYy+p2kCbs/jPgH+5Da2bK3YP6s5R2PPmVORLRTWbaM3eAx'
    b'wVGTtf/uRy8InFP/m9yTqgrMWAI9190G877fwY2nZOOe8GxgpC0ZG/u4bsn+5D2KTaZLwaov'
    b'AJxSBf93vozc85ciMGFsuppHqKxNs4ZrUYCbSlHqlIy6prkjuv6Ndres9B8rFi9okjccA4yI'
    b'rPcaGgy1cqYv1L7vJC236Iv61CoY5UVQQ34OtueLkqJvajlBRP+0DV1fvwQ6xVQO+V8WWiGH'
    b'lfZGpBAj6I5I8KJ6uq+0BFi8AKHvLUXwC9MpePVTFKGSs6drFpHJhW7hIFZopMGaxnfCdSw4'
    b'sbhlpcxnE7vbn3a6e1aWrdzWo9x3mel18skwIrL2XX3jxXr9zEuD02oLdF+gWqFBw6CnToOk'
    b'UaqKqlLoZKLvkZVIXvlzuJTnHdB9j6gDWvXxYI1hOAEN/isuQN6lF8KorIBCRBALHNVjcMO7'
    b'SG7ZiVh3NymVi0BRPvJrqqDPmAJfaSlPulRXapvtDMZi0Y2N27qeeP7Wqct//bhs/BPioyRQ'
    b'3Hs3aW1jO08j/3xz/hmzTqVpu0TTfRA6kUQVWCh+il5q4iLVH0HPL+6E+I/HKJ2T6bHXEhPF'
    b'9UZKFhc2sfpTkXf9j+CfNQ1agDS4tw/RtW8i+l8r4W7dDiVOkwebHrVua1Tf74c7vhK+xXMR'
    b'+urZ0E+ugpoXoviMdDueROSdpp3xxvevqFyf+6LyP+dxuHfEUNP7g9B774r8SKVxae60Kf8U'
    b'qJ08V8/LyxUGPVny0C7FO3ZXHxJ725Hqi9CAcrzzA4OIPL4KTvNeEtYjSmrUERAlwUTRzonE'
    b'YO1tg0ntWh3dCD/8JOL3PQb3/e1Q6ZxIJEnLSOakBS1BaVOEQpT2bihvvY/kBkqrevqglhRD'
    b'Ly2ACBjQikOFTtKat6+3ceu/r1+zw+vsyPAhKfqffrXQLg79wlde/AOjvCTIqQZ1QoMeQKpp'
    b'O2LrGoH3t0Lp64RSU4Oi666EWlqIVEs7zYJXw331nXS4wJ7HI+xIyBoyQ7pb0OzqkIkp9EDc'
    b'th7SpjhV4NmV/aDXekYE6ejpK+u99GT5eRALZiP/qosROH0GFHrY7mAcieYPHikITb9Emaak'
    b'5I1HgIOkcJ5vzOnLww2+yVWX6aFgQFEErG5S/w3vILJqNaxXNkDrJJLYJxEBxrw5KPnPW6CO'
    b'K0OypQ0dFDIorxKZLLAns8QnISsDecTpDwe28nPIoPlAViL6ZPhPyFQyyEXUn4b8f74ceQtO'
    b'J8J0mNFEP6VhPzY3NbWhqxfxtq6uXSVm49nXX2/TONMNHB5DZtj1wB9CiQLtx0ZN1U99hQU6'
    b'd5jYvRd9D65A/K4H4azdCK03DJg0oVASLKigpAT+pYuhUfJrR2OIPrcWyq59NFgeKRUi6YhM'
    b'kHBobdlSOtnmpoYXeZHGmfnKW3ktfczrZYJy0lRnNyXnNTSDl9JEoftdy/yGFjAupFn8Qn1i'
    b'xYLxC+bnRNa+efLN11y1++yxY+2HX375sLGZJMttcEVfafMloVl1y4yyYp1XLhPNO9B/+wOw'
    b'Hl0FsZ9yO5quHa7usqLzx4Xp0yHqZ0FUlMl8LrXuTdhN28ivcQTujZoHfaSQ90hpuXgE8AHv'
    b'Mo8+c9k7732TZzIXuDDJNC6HclOLAldt9nRouTnQQ7kwxpeBiIJePb5YBAOL9LKiRQmhzinJ'
    b'H5O4YtK05O1rn+tftmwZNzoESdY1t3x7vFY76SfGuNIpNH0gvnMPJcH3IrlyNfmmCM/YBO7d'
    b'28tx8LDNFGlUFBZN5zaZj7VnL9RNW4nX9INhQb1vI4dUDY8A75M+nd4eOOsVSaQs3vfMdfnh'
    b'E6x5pg27nXxeVTmMuskkD3lEGq9LPlFQiqbqhlBzgn4lGJiMgtB8N5U6K7Fj14ZbHn+0m1oe'
    b'grK14V9LQtOm3la4eP53RcivOeQEu264C9by38OhcIAXANS0qmfAA3Hl4OhsQIdSnA8xfqyc'
    b'CNTN22BbvMSQqSl3JwwZH6iQ/8KsU6AsWQQnHKMAVoU+pgD+2knw15GJFhWzicIh9TEHBx2n'
    b't//FRDh+Rdmsup0ZX6bsu+exMwNnTF+VW1dbbDs2Is+sxeBVvwT2dnOSTzVo5kmT5XXrwaOB'
    b'BsDXFUuanQON1/DovvQNQ/VOHIbIovTJ1mm8/gCFHOR3+WFT4CuKC6HW1cJ/7lnwLaqHUV1F'
    b'pNEsnEy6qQ/2PZ1s7fqH8nPP2sVtCEVV/jYwYVwRTTiwOnsRfmAFVLJxzrsEsSQ+IonnszKV'
    b'4cHQ4+D0htn9sGccTvHxR2aC4eUvhTgSgwmoCRtq3ILSm4Cyow3WM68g3PBv6L7+NkQ3bZbB'
    b'ru7TFd/Y8q8qhv9Xe+55RCak6rK777xILyiYwg58cPU6mPf8DoKSYA4NpJPmjuTWg0eSB09r'
    b'aEshhgc69v5o49Uavj1R4KEwaSyRdyJ9Mv3dIcVQkjEoe1pgNe2EO2kCfBVjoAb8Cplrjebz'
    b'vT/nK+e+J5SEeTYv2NmxOOLPvwIlHKabqWFiyItq0m2ny3BkrjN4KHJQ8oCPvHMfvutE4MA4'
    b'PjQmEkEjc1BJWUQ0Cbz+Dvp+dTeSOz6Q0gXKSgytMO+ys/LHFQs1lJPPlmb29MPauJlmimEN'
    b'jQBMmJxZ0r5hNEGaKBWXLMMFhZYOTVaU17pvNKLvsacoawnTjKlAH1tWQ3HDOYJUTbKb2v0B'
    b'wPFUBlJNR0bccA0bDTisZCwCyWwTcT5yQ9ZvVyHx5rsUM9oQfn8Jp3/C1b0ZzNpDkXeCHN4I'
    b'CToUTBjb/mjSsEMl9Y5J00gEta0TiTXrAUroBXGk+YNzhKB4g6NxrWMACtltur68URbpfw58'
    b'/hyYtNFklkNyyiMCj512FqVz1ttbYPWFpdwilFMoeCaTWhEnrWKu6K5DSZGESbMcGbzuRhkO'
    b'kY8lcFraYLZ30TeaFH1+skBiUjKnUug6cj4+9zB41gsPwGqjmJOjR41XPmQgqcAqzOEceRhf'
    b'h9eOjNbx1Y8qGRx6PNrAkb4VjpLQpFAUogmYlMeR/O64MXB0g6t4ZbRLepRgxZJul+MvdkO8'
    b'poZUijhxETipGm5e/hA/3v5gtjK+S5rtxxT+jHbICYq0Sb4okSfo0IrETNYxbWwp9CkTJRme'
    b'g+b94YUeIu3PFa7r3TLqwKsqqp9ChuJ8TnllpEBxlvEGr0TqeSH4vjSPf0sgF7kO1qn/HzgQ'
    b'7pBLV1SIoiKoFeVycYDfUYr4jtb9Di8V+3T4vjgf5qRyqstUeiXz8ejLNDa6cagkmbjQswLv'
    b'qnxdSwm1WlZI12xYkUGIZPOeZ83e3gg7MP+USfD91VLYoSCTK2/ONHpoB6MfHkGeIniyDhWW'
    b'XXVgfGEGjPw8eZaMcItIJbvWxjY3t4DUTKc8MURkiTOmAzqpIVXT0ixJDZV7r5PRjWHjZ5m8'
    b'nfyhHS9NMVupieNhLKqHCPgocbZMq6t3o6h+OW+fmuO/MhmJ7OIbfJUVyLn8e1BPqYajCUos'
    b'6SSB3f1BnYxmHFYUPkGJNGtIyI/ARX8J/7STScOIg1i01dKcmwW/yu6N978a27nrj2Yk4vLr'
    b'7uCiufBfdREUIgwG0ST9lzfDDcdoVLDhVsHfOJ5iuXiZhleLBS89L5iN0Le+BJETlO8TIm+/'
    b'G4msXtfPPKJmyZJUbNvW+5PbdjdatgktJ4D8pV9B8JrLgPqZUIIB4lwG/Z87yLiQI3TFhpOj'
    b'Qcwnoq65HBqZIf+2LNXR02OFB++IvL6mR74KY9wxY0Zv/4RJrwhDP1P4jXLV71d0mg20U2th'
    b'86+F23phxaIy2fZiKO8JyUiX96Oh8CaNjI3wqwOXV4qLCqF/8xzkX/N3yJk5DSrlglYi2W+G'
    b'B38es5MP1159dfJguyJ0Nzef7lfEg8qYsql6ICgcYp1f4cfWvI7oC+vhNm0HenrhRKIQKUqV'
    b'iLxhY/jsgwfLpkck2QEdKMwjLaqGsXgucr61GEbFWPJTZEXhCOIbN6+LheNLJ5z/ZfnfHR8i'
    b'i9G68oWFvoqynwVrJ5+m+IwSaau2BbOrD6mWVlj722ETYdpgXEa2HKEctqHPKGS4QI7bKsqF'
    b'KC+Hv6oKxoRycjc+yaUdi0f7X3qzKfHGn34xydf3nLJsmXwRelgZV6xYoS4MlpYap0y8gEKK'
    b'a43y0iI1ECDro+r8OpyXWh2veE+KyRo9dMlf2bD/oNneVTWoRJwkKWGSj+pMum7qxsjqt5a3'
    b'b36pfc599w39WvBjJdx/78qgWizmKprv+3pp8Xd8U08WetDQvJmDk2bugvvNkPVpE8b9cZG6'
    b'/gnBy9/eshS/F3U58bNsO9naYcd37n0tFY/fNW580bPKnDlDJGUwIularr11XHD2qZWWzzfD'
    b'hfndXA4pSoogDOOohv3JwGQd3UOhaFz6WpFIINXayW9xVut+Y01iw+buMT/864/8odsR9eo2'
    b'NGhbKysDJfPmyZ8boVj+jUr09Hhj72luRklra1I577wj/nFbFllkkUUWWWSRRRZZZJHF5wLA'
    b'/wGNfFLm15wfYwAAAABJRU5ErkJggg==')

locale.setlocale(locale.LC_ALL, 'C')
#inherit from the MainFrame created in wxFowmBuilder and create MainFrame
class MainFrame(mainGui):
    #constructor
    def __init__(self,parent):
        #initialize parent class
        super(MainFrame, self).__init__(parent)
        global appIcon
        appIcon = app_icon.GetIcon() # appBmp=app_icon.GetBitmap()
        self.SetIcon(appIcon)
        wx.CallLater(1, self.onActivate) # After 1ms of GUI Draw completed
        self.Show(True)
    def onActivate(self): # called after 1ms from __init__
        self.m_logo_bitmap.SetIcon(appIcon)
        self.statusBar.SetStatusText('Ready')
        self.gauge.Hide()
        fillDomainsList(self)
        if conf.uiSubHeading: self.m_staticText_sub_header.SetLabel('\n'+conf.uiSubHeading)
        global parentWindow
        parentWindow=self
        loadSelections(self)
    #wx calls this function with and 'event' object
    def startConnectionAndreporting(self,event):        
        def callback():
            disableUIwhileWorking() # UI disables once work is started
            try:
                numOfSelectedTenancies = self.m_domains_listCtrl.GetSelectedItemCount()
                # Validations for User selections
                if numOfSelectedTenancies==0:
                    wx.MessageBox("Tenancies Not Selected !!\n\nSelect required tenancy/s and try again.", 'Select Tenancies', wx.OK | wx.ICON_EXCLAMATION)
                    return
                # Initiate Gauge with initial start value
                self.gauge.SetValue(1) #the.setGauge(1)
                start.init(the)
                ret=start.start()
                if ret:
                    if ret[0]=='warn': wx.MessageBox(ret[2], ret[1], wx.OK | wx.ICON_WARNING)
                    elif ret[0]=='error': wx.MessageBox(ret[2], ret[1], wx.OK | wx.ICON_ERROR)
                    else: wx.MessageBox(ret[2], ret[1], wx.OK | wx.ICON_INFORMATION)
            except Exception as e:
                err=str(e)
                the.setError(err)
                raise   
            finally:
                the.setGauge(0)
                disableUIwhileWorking(enable=True)
        t1 = threading.Thread(target=callback)
        t1.start()

    def TenanciesConnectionCheck(self,event):
        the.setInfo('Selected Tenancies Connection Check Started ..')
        the.justConnectionCheck=True
        self.startConnectionAndreporting(event)
    def OpenConfigurations(self,event):
        the.setInfo('Opening "' + conf.configFilePath + '" ...')
        os.startfile(os.path.abspath(conf.configFilePath))
        the.setInfo('Configurations Opened in your default editor.')
    def ReloadConfigurations(self,event):
        the.setInfo('Reloading Configurations from file ...')
        conf.loadConfigs()
        conf.logConfigs()
        the.setInfo('Configurations Reloaded.')
    def ShowAboutMessage(self,event):
        details="\n\n"
        details+="Tool used for auditing Oracle Cloud Infrastructure (OCI)\n\n\n"
        msg = the.tool_name + "\nVersion " + the.version + details + the.copyright
        wx.MessageBox(msg, 'About - ' + the.tool_name, wx.OK | wx.ICON_INFORMATION)
    def ShowCreditsMessage(self,event):
        details="""\n
Thanks to Oracle University, for initiative of OCI Auditing Tool and framing audits on Users, Groups, Compartments, Policies, Limits.\n
Oracle Consulting, has helped in taking this tool to next level including wide Networking and EventLog audits.\n
Also many thanks to all users and collaborators for your suggestions and discussions in improving this tool.\n
Github is used to maintain product releases, documents and issues.\n
\n\n"""
        msg = the.tool_name + "\nVersion " + the.version + details + the.copyright
        wx.MessageBox(msg, 'Credits - ' + the.tool_name, wx.OK | wx.ICON_INFORMATION)
    def CheckForUpdates(self,event):
        the.setInfo('Checking for updates ... ..')
        import requests, webbrowser
        from distutils.version import LooseVersion
        url = requests.get('https://github.com/KsiriCreations/oci-auditing/releases/latest').url
        latestVersion = url.split('/')[-1]
        verMsg = 'Latest Stable Version ('+latestVersion+'), '+'Your Installed Version ('+the.version+')'
        the.setInfo(verMsg)
        if LooseVersion(latestVersion) > LooseVersion(the.version):
            dlg=wx.MessageDialog(None, 'Latest Stable Version ' + latestVersion + ' available !!',
                    'Updates', wx.OK | wx.CANCEL | wx.OK_DEFAULT | wx.ICON_WARNING)
            dlg.SetOKCancelLabels("Go to &Download Page", "&Cancel")
            ans=dlg.ShowModal()
            if ans==wx.ID_OK: 
                webbrowser.open_new_tab(url)
        else:
            dlg=wx.MessageDialog(None, 'Great! you are already updated.\n\n'+verMsg,
                    '-', wx.OK | wx.CANCEL | wx.CANCEL_DEFAULT | wx.ICON_INFORMATION)
            dlg.SetOKCancelLabels("&Try New Pre-Released Beta Versions", "&OK")
            ans=dlg.ShowModal()
            if ans==wx.ID_OK:
                openLinkOnBrowser('Get Stable-Releases / Pre-Released versions', 'https://github.com/KsiriCreations/oci-auditing/releases')
    def OpenDocumentPage(self,event):
        openLinkOnBrowser('OCI Auditing Tool Document', 'https://github.com/KsiriCreations/oci-auditing#oci-auditing')
    def OpenCloudGuardPage(self,event):
        openLinkOnBrowser('OCI Cloud Guard Document', 'https://docs.oracle.com/en-us/iaas/cloud-guard/using/index.htm')
    def OpenCloudAdvisorPage(self,event):
        openLinkOnBrowser('OCI Cloud Advisor Document', 'https://docs.oracle.com/en-us/iaas/Content/CloudAdvisor/Concepts/cloudadvisoroverview.htm')
    def SubmitFeedback(self,event):
        openLinkOnBrowser('Submit Feedback', 'https://github.com/KsiriCreations/oci-auditing/issues/new?title=Feedback:%20%3CReplace%20with%20Feedback%20Title%3E&body=%3CReplace%20with%20your%20expirience%20and%20feedbacks%20on%20OCI%20Auditing%20Tool%3E')
    def SubmitFeature(self,event):
        openLinkOnBrowser('Request Enhancements or New Feature', 'https://github.com/KsiriCreations/oci-auditing/issues/new?title=Request%20Feature:%20%3CReplace%20with%20Feature%20Title%3E&body=%3CReplace%20with%20your%20detailed%20comments%20of%20any%20new%20feature%20or%20enhancements%20that%20need%20to%20be%20incorporated%20in%20OCI%20Auditing%20Tool%3E')
    def SubmitDefect(self,event):
        openLinkOnBrowser('Submit a Defect with details', 'https://github.com/KsiriCreations/oci-auditing/issues/new?title=Defect:%20%3CReplace%20with%20Defect%20Title%3E&body=%3CReplace%20with%20your%20detailed%20findings,%20explanations,%20investigations%20or%20resolutions%20if%20anything%20already%20done%3E')
    def domainsSelectionChanged(self,event):
        selectedDomains = []
        for i in range(self.m_domains_listCtrl.GetItemCount()):
            if self.m_domains_listCtrl.IsSelected(i): selectedDomains.append(self.m_domains_listCtrl.GetItemText(i,0))
        the.updateSelection('domains', 'selection', selectedDomains)
    def userGroupsSelectionChanged(self,event):
        the.updateSelection('audits', 'usersAndGroups', self.m_checkBox_UserGroups.GetValue())
    def limitsSelectionChanged(self,event):
        the.updateSelection('audits', 'limits', self.m_checkBox_serviceLimits.GetValue())   
    def policiesSelectionChanged(self,event):
        the.updateSelection('audits', 'policies', self.m_checkBox_Policies.GetValue())
    def eventsSelectionChanged(self,event):
        the.updateSelection('audits', 'events', self.m_checkBox_Events.GetValue())
    def billingSelectionChanged(self,event):
        the.updateSelection('audits', 'billing', self.m_checkBox_Billing.GetValue())
    def instancesSelectionChanged(self,event,openSubUI=True):
        the.updateSelection('audits', 'instances', self.m_checkBox_Instances.GetValue())
        if self.m_checkBox_Instances.GetValue() and openSubUI: self.openInstancesSelection(event)
    def eventsSelectionChanged(self,event,openSubUI=True):
        the.updateSelection('audits', 'events', self.m_checkBox_Events.GetValue())
        if self.m_checkBox_Events.GetValue() and openSubUI: self.openEventsSelection(event)
    def networkingSelectionChanged(self,event,openSubUI=True):
        the.updateSelection('audits', 'networks', self.m_checkBox_Networking.GetValue())
        if self.m_checkBox_Networking.GetValue() and openSubUI: self.openNetworkingSelection(event)
    def cloudGuardSelectionChanged(self,event):
        the.updateSelection('audits', 'cloudGuard', self.m_checkBox_CloudGuard.GetValue())
    def cloudAdvisorSelectionChanged(self,event):
        the.updateSelection('audits', 'cloudAdvisor', self.m_checkBox_CloudAdvisor.GetValue())
    def openInstancesSelection(self,event):
        d = InstancesDialog(self)
        d.SetIcon(appIcon); d.ShowModal()
    def openEventsSelection(self,event):
        d = EventsDialog(self)
        d.SetIcon(appIcon); d.ShowModal()
    def openNetworkingSelection(self,event):
        d = NetworkingDialog(self)
        d.SetIcon(appIcon); d.ShowModal()
    def onClose(self,event):
        self.Destroy()

class wxTimedDialog(wx.Dialog):
    def __init__(self, parent=None, title='KK-Title', message='KK-Message', waitTime=2): # default 2 seconds
        log.info(message)
        wx.Dialog.__init__(self, parent, title=title, size=wx.Size(400,400), style=wx.CAPTION|wx.SYSTEM_MENU|wx.STAY_ON_TOP)
        timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.onTimer, timer)
        timer.Start(waitTime*1000)
        self.SetIcon(appIcon)
        bSizer=wx.BoxSizer(wx.VERTICAL)
        self.m_staticText=wx.StaticText(self, wx.ID_ANY, message, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.m_staticText.Wrap(-1)
        bSizer.Add(self.m_staticText, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5)
        self.ShowModal()
    def onTimer(self, event):
        self.Destroy()

class InstancesDialog(instancesDialog):
    def __init__(self, parent):
        instancesDialog.__init__(self,parent)
        # Fill services list
        self.m_services_listCtrl.InsertColumn(0, "Cloud Services")
        self.m_services_listCtrl.SetColumnWidth(0, 370)
        i=0 # Add Services to list
        for srv in the.ociServices.keys():
            self.m_services_listCtrl.InsertItem(i, srv)
            i+=1
        # Hide Main Screen
        parentWindow.m_panel.Hide()
        try: # Load last known selections from DB
            selectedServices = the.getSelection('audits', 'ociServices') # Should return array of Services
            # log.debug('InstancesDialog>the.getSelection: '+str(selectedServices))
            for i in range(self.m_services_listCtrl.GetItemCount()):
                service = self.m_services_listCtrl.GetItemText(i,0)
                if service in selectedServices:
                    self.m_services_listCtrl.Select(i)
        except: # if false is returned on no information
            pass
    def keyPressOnServicesList(self, event):
        keycode = event.GetKeyCode()
        # print(keycode)
        if keycode in [wx.WXK_NUMPAD_ENTER, wx.WXK_ESCAPE, 13, 27]: # enter=13, esc=27
            self.onClose(event)
        elif keycode==1: # Ctrl+A = 1
            for i in range(self.m_services_listCtrl.GetItemCount()):
                self.m_services_listCtrl.Select(i)
        event.Skip()
    def onClose(self, event):
        # In main window, UI selection changes are immediatly updated to db
        # however here, selection updates to db is done only while closing sub-window, and thats sufficient
        selectedServices=[]
        for i in range(self.m_services_listCtrl.GetItemCount()):
            if self.m_services_listCtrl.IsSelected(i): selectedServices.append(self.m_services_listCtrl.GetItemText(i,0))
        the.updateSelection('audits', 'ociServices', selectedServices)
        if len(selectedServices)>0:
            parentWindow.m_checkBox_Instances.SetValue(True)
            parentWindow.instancesSelectionChanged(event,openSubUI=False)
        else:
            parentWindow.m_checkBox_Instances.SetValue(False)
        parentWindow.m_panel.Show()
        self.Destroy()
class EventsDialog(eventsDialog):
    def __init__(self, parent):
        eventsDialog.__init__(self,parent)
        parentWindow.m_panel.Hide() # Hide Main Screen
        # load previous selection
        opt = the.getSelection('audits', 'eventsDateRange')
        # log.debug('EventsDialog>the.getSelection: '+str(opt)+' - '+self.m_radioBox_dateRange.GetItemLabel(opt))
        self.m_radioBox_dateRange.SetSelection(opt)
    def onButtonChange(self, event):
        if self.m_radioBox_dateRange.GetSelection()==start.EVENTSLASTRUN and not the.getSelection('audits', 'eventsLastRun'): # Returns boolean false, if audit events last run not available
            msg = 'Change Selection..\n\nAudit events last run not available !!'
            log.debug(msg)
            wx.MessageBox(msg, 'Last Run for Audit Events', wx.OK | wx.ICON_INFORMATION)
            self.m_radioBox_dateRange.SetSelection(0)
    def onClose(self, event):
        # In main window, UI selection changes are immediatly updated to db
        # however here, selection updates to db is done only while closing sub-window, and thats sufficient
        the.updateSelection('audits', 'eventsDateRange', self.m_radioBox_dateRange.GetSelection())
        parentWindow.m_checkBox_Events.SetValue(True)
        parentWindow.eventsSelectionChanged(event,openSubUI=False)
        parentWindow.m_panel.Show()
        self.Destroy()
class NetworkingDialog(networkingDialog):
    def __init__(self, parent):
        networkingDialog.__init__(self,parent)
        # Fill list
        self.m_networkComponents_listCtrl.InsertColumn(0, "Network Components")
        self.m_networkComponents_listCtrl.SetColumnWidth(0, 370)
        i=0 # Add Services to list
        for nc in the.networkComponents:
            self.m_networkComponents_listCtrl.InsertItem(i, nc)
            i+=1
        # Hide Main Screen
        parentWindow.m_panel.Hide()
        # Load last known selections from DB
        try: # for first run "the.getSelection" will return bool-false
            selectedNCs = the.getSelection('audits', 'networkComponents')
            # log.debug('NetworkComponents>the.getSelection: '+str(selectedNCs))
            for i in range(self.m_networkComponents_listCtrl.GetItemCount()):
                nc = self.m_networkComponents_listCtrl.GetItemText(i,0)
                if nc in selectedNCs:
                    self.m_networkComponents_listCtrl.Select(i)
        except TypeError: pass
    def keyPressOnNetworksList(self, event):
        keycode = event.GetKeyCode()
        # print(keycode)
        if keycode in [wx.WXK_NUMPAD_ENTER, wx.WXK_ESCAPE, 13, 27]: # enter=13, esc=27
            self.onClose(event)
        elif keycode==1: # Ctrl+A = 1
            for i in range(self.m_networkComponents_listCtrl.GetItemCount()): self.m_networkComponents_listCtrl.Select(i)
        event.Skip()
    def onClose(self, event):
        selectedNCs=[]
        for i in range(self.m_networkComponents_listCtrl.GetItemCount()):
            if self.m_networkComponents_listCtrl.IsSelected(i): selectedNCs.append(self.m_networkComponents_listCtrl.GetItemText(i,0))
        the.updateSelection('audits', 'networkComponents', selectedNCs)
        if len(selectedNCs)>0:
            parentWindow.m_checkBox_Networking.SetValue(True)
            parentWindow.networkingSelectionChanged(event,openSubUI=False)
        else:
            parentWindow.m_checkBox_Networking.SetValue(False)
        parentWindow.m_panel.Show()
        self.Destroy()

def openLinkOnBrowser(name, link):
    import webbrowser
    msg= name + '\n\n' + link[:80] + '\n(opens in your default browser)'
    dlg=wx.MessageDialog(None, msg, 'Browser Switch', wx.OK | wx.CANCEL | wx.OK_DEFAULT | wx.ICON_INFORMATION)
    dlg.SetOKCancelLabels("&Open", "&Cancel")
    ans=dlg.ShowModal()
    if ans==wx.ID_OK: 
        webbrowser.open_new_tab(link)
def fillDomainsList(pw): # parent window
    pw.m_domains_listCtrl.InsertColumn(0, "Tenancy Name")
    pw.m_domains_listCtrl.SetColumnWidth(0, 200)
    
    for i in range(len(conf.tenancyNames)):
        tenancyName = conf.tenancyNames[i]
        pw.m_domains_listCtrl.InsertItem(i, tenancyName)
        
        # fill background color, for domains not having credentials
        if not (conf.tenancyOcids[tenancyName] and conf.userOcids[tenancyName]):
            pw.m_domains_listCtrl.SetItemBackgroundColour(i, wx.Colour(170,170,170))
def loadSelections(pw): # parent window
    try: # Load last known form selections, from DB
        selectedDomains = the.getSelection('domains', 'selection') # Should return array of domain names
        for i in range(pw.m_domains_listCtrl.GetItemCount()):
            tenancyName = pw.m_domains_listCtrl.GetItemText(i,0)
            if tenancyName in selectedDomains: pw.m_domains_listCtrl.Select(i)
    except: # if false is returned on no information
        pass
    pw.m_checkBox_UserGroups.SetValue(the.getSelection('audits', 'usersAndGroups'))
    pw.m_checkBox_Compartments.SetValue(the.getSelection('audits', 'compartments'))
    pw.m_checkBox_serviceLimits.SetValue(the.getSelection('audits', 'limits'))
    pw.m_checkBox_Policies.SetValue(the.getSelection('audits', 'policies'))
    pw.m_checkBox_Billing.SetValue(the.getSelection('audits', 'billing'))
    pw.m_checkBox_Instances.SetValue(the.getSelection('audits', 'instances'))
    pw.m_checkBox_Events.SetValue(the.getSelection('audits', 'events'))
    pw.m_checkBox_Networking.SetValue(the.getSelection('audits', 'networks'))
    pw.m_checkBox_CloudGuard.SetValue(the.getSelection('audits', 'cloudGuard'))
    pw.m_checkBox_CloudAdvisor.SetValue(the.getSelection('audits', 'cloudAdvisor'))
def disableUIwhileWorking(enable=False):
    if enable:# Show / Hides
        parentWindow.start_button.Show()
        parentWindow.gauge.Hide()
    else:
        parentWindow.start_button.Hide()
        parentWindow.gauge.Show()
    # Menu Items
    parentWindow.m_menuItem_connection.Enable(enable)
    parentWindow.m_menuItem_reloadConfigs.Enable(enable)
    parentWindow.m_menuItem_servicesWindow.Enable(enable)
    parentWindow.m_menuItem_networkingWindow.Enable(enable)
    parentWindow.m_menuItem_startAudit.Enable(enable)
    # UI's
    parentWindow.m_domains_listCtrl.Enable(enable)
    parentWindow.m_checkBox_UserGroups.Enable(enable)
    # parentWindow.m_checkBox_Compartments.Enable(enable) # Now Compartments made default enabled
    parentWindow.m_checkBox_serviceLimits.Enable(enable)
    parentWindow.m_checkBox_Policies.Enable(enable)
    parentWindow.m_checkBox_Instances.Enable(enable)
    parentWindow.m_button_instances.Enable(enable)
    parentWindow.m_checkBox_Events.Enable(enable)
    parentWindow.m_button_events.Enable(enable)
    parentWindow.m_checkBox_Networking.Enable(enable)
    parentWindow.m_button_networking.Enable(enable)
    parentWindow.m_checkBox_CloudGuard.Enable(enable)
    parentWindow.m_checkBox_CloudAdvisor.Enable(enable)
    # parentWindow.m_checkBox_Billing.Enable(enable)


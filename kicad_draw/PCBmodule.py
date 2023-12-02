import numpy as np

class PCBdraw:
    """ Python module for generating traces for KiCad PCB.

    Args:
        Nlayer (int)
        net_number
        track_width
        connect_width
        Nelement
        viasize
        drillsize

    """
    def __init__(self, Nlayer, net_number, track_width = 0.2, connect_width = 0.15, Nelement = 100, viasize = 0.3, drillsize = 0.15):

        if Nlayer == 4:
            self.layers = ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]
        if Nlayer == 6:
            self.layers = ["F.Cu", "In1.Cu", "In2.Cu", "In3.Cu", "In4.Cu", "B.Cu"]
        self.track_width = track_width
        self.connect_width = connect_width
        self.net_number = net_number
        self.Nelement = Nelement
        self.viasize = viasize
        self.drillsize = drillsize 
        self.file = None

    def drawline(self, x1, y1, x2, y2, line_width, LayerString):
        """ draw linear conductive trace

        Args:
            x1 (float): x-coordinate of start point
            y1 (float): y-coordinate of start point
            x2 (float): x-coordinate of end point
            y2 (float): y-coordinate of end point
            line_width (float): width of trace
            LayerString (string): name of layer
        
        Returns:
            None
            
        """
        print("  (segment (start " + str(x1) + " " + str(y1) + ") (end " + str(x2) + " " + str(y2) + ") (width " + str(line_width) + ") (layer \"" + LayerString + "\") (net " + str(self.net_number) + ") (tstamp 0))")

    def drawpolylinearc(self, x0, y0, r1, portangle, LayerString, line_width, angleOffset=0):
        """ draw arc-shaped conductive trace

        Args:
            x0 (float): x-coordinate of arc center
            y0 (float): y-coordinate of arc center
            r1 (float): radius of arc
            portangle (float): angle of arc opening
            LayerString (string): name of layer
            line_width (float): width of trace
            angleOffset (float): offset of start angle of arc
        
        Returns:
            None
            
        """
        delta_angle = (2 * np.pi - portangle)/self.Nelement
        for i in range(self.Nelement):
            x1 = x0 + r1 * np.cos(portangle/2 + i * delta_angle + angleOffset)
            x2 = x0 + r1 * np.cos(portangle/2 + (i + 1) * delta_angle + angleOffset)
            y1 = y0 + r1 * np.sin(portangle/2 + i * delta_angle + angleOffset)
            y2 = y0 + r1 * np.sin(portangle/2 + (i + 1) * delta_angle + angleOffset)
            self.drawline(x1=x1, y1=y1, x2=x2, y2=y2, line_width=line_width, LayerString=LayerString)

    def drawvia(self, x, y, Layerstring1, Layerstring2):
        """ draw via

        Args:
            x (float): x-coordinate of via
            y (float): y-coordinate of via
            LayerString1 (string): name of via start layer
            LayerString2 (string): name of via end layer
        
        Returns:
            None
            
        """
        print("  (via (at "+ str(x) +" "+ str(y) +") (size " + str(self.viasize) + ") (drill "+ str(self.drillsize) +") (layers \""+Layerstring1+"\" \""+Layerstring2+"\") (net " + str(self.net_number) + ") (tstamp 0))")

    def drawhelix(self, x0, y0, radius, port_gap, tab_gap, angle_step, layerindexlist, tabposition = 'OUT', base_angle_offset = 0):
        """ draw helix coil pattern

        Args:
            x0 (float): x-coordinate of helix coil center
            y0 (float): y-coordinate of helix coil center
            radius (float): radius of helix coil
            portgap (float): length of port opening
            tabgap (float): TBD
            angle_step: TBD
            layerindexlist (list): list/order of layers to draw helix coil
            tabposition (string): defines position of tab for placing vias
            base_angle_offset (float): defines starting angle offset

        Returns:
            None

        """
        #angle of the port openings
        portangle = np.arcsin(port_gap/2/radius) * 2

        #list layers for coil
        layerlist = [None] * len(layerindexlist)
        for layerindex in range(len(layerindexlist)):
            layerlist[layerindex] = self.layers[layerindexlist[layerindex]]

        #draw coil patterns
        for turn in range(len(layerlist)):
            turn_angle_offset = (portangle+angle_step)*turn + base_angle_offset - (portangle+angle_step)*(len(layerlist)-1)/2
            self.drawpolylinearc(x0=x0,
                                  y0=y0,
                                  r1=radius,
                                  portangle=portangle,
                                  line_width=self.track_width,
                                  LayerString=layerlist[turn],
                                  angleOffset=turn_angle_offset)

            portangle_top = turn_angle_offset + portangle/2
            portangle_bottom = turn_angle_offset - portangle/2

            x1_top = x0 + radius * np.cos(portangle_top)
            y1_top = y0 + radius * np.sin(portangle_top)
            x2_top = x0 + (radius + tab_gap) * np.cos(portangle_top + angle_step/2)
            y2_top = y0 + (radius + tab_gap) * np.sin(portangle_top + angle_step/2)
            
            x1_bottom = x0 + radius * np.cos(portangle_bottom)
            y1_bottom = y0 + radius * np.sin(portangle_bottom)
            x2_bottom = x0 + (radius + tab_gap) * np.cos(portangle_bottom - angle_step/2)
            y2_bottom = y0 + (radius + tab_gap) * np.sin(portangle_bottom - angle_step/2)

            if turn != 0:
                self.drawline (x1=x1_bottom,
                                y1=y1_bottom,
                                x2=x2_bottom,
                                y2=y2_bottom,
                                line_width=self.connect_width,
                                LayerString=layerlist[turn])
            if turn != len(layerlist) - 1:
                self.drawline (x1=x1_top,
                                y1=y1_top,
                                x2=x2_top,
                                y2=y2_top,
                                line_width=self.connect_width,
                                LayerString=layerlist[turn])
                self.drawvia(x=x2_top,
                              y=y2_top,
                              Layerstring1=layerlist[turn],
                              Layerstring2=layerlist[turn+1])

    def open_pcbfile(self, path):
        """ open pcb file **(not used yet)**

        Args:
            path (str): path to .kicad_pcb file
        
        Returns:
            None

        Raises:
            FileNotFoundError: if file is not found
            
        """
        try:
            self.file = open(path , "r+")
        except FileNotFoundError:
            # doesn’t exist
            print('File doesn\'t exit')
        else:
            # exists
            print('opened:' + path)

    '''
    def drawspiral_2layer(self, x0, y0, rstart, rend, Nturns, Portgap, Nelement, Layerindex1, Layerindex2, TrackWidth, Connectwidth, netnumber):
        r_inc = (rend - rstart)/(Nturns-1)
        for i in range(Nturns):
            self.drawpolylinearc(x0, y0, rstart + r_inc * i, Portgap, Nelement, self.layers[Layerindex1], TrackWidth, netnumber)
            if i < Nturns -1:
                portangle1 = np.arcsin((Portgap/2)/(rstart + r_inc * i))
                portangle2 = np.arcsin((Portgap/2)/(rstart + r_inc * (i+1)))
                
                x1 = x0 + (rstart + r_inc * i) * np.cos(portangle1)
                x2 = x0 + (rstart + r_inc * (i+1)) * np.cos(portangle2)
                y1 = y0 + (rstart + r_inc * i) * np.sin(portangle1)
                y2 = y0 - ((rstart + r_inc * (i+1)) * np.sin(portangle2))
                self.drawline (x1, y1, x2, y2, Connectwidth, self.layers[Layerindex1], netnumber)
        for i in range(Nturns):
            self.drawpolylinearc(x0, y0, rstart + r_inc * i, Portgap, Nelement, self.layers[Layerindex2], TrackWidth, netnumber)
            if i < Nturns -1:
                portangle1 = np.arcsin((Portgap/2)/(rstart + r_inc * i))
                portangle2 = np.arcsin((Portgap/2)/(rstart + r_inc * (i+1)))
                
                x1 = x0 + (rstart + r_inc * i) * np.cos(portangle1)
                x2 = x0 + (rstart + r_inc * (i+1)) * np.cos(portangle2)
                y1 = y0 - (rstart + r_inc * i) * np.sin(portangle1)
                y2 = y0 + ((rstart + r_inc * (i+1)) * np.sin(portangle2))
                self.drawline (x1, y1, x2, y2, Connectwidth, self.layers[Layerindex2], netnumber)
    '''

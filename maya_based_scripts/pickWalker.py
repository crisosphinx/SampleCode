# -*- coding: utf-8 -*-
# Revised pickWalkTool

import maya.cmds as cm
import maya.mel as mm


class PickWalker:
    def __init__(self):
        # get initial selection
        self.umv = []
        self.indexed = 0
        self.selected = []
        self.selectd = cm.ls(sl=1)
        self.hilited = cm.ls(hl=1)
        self.visible = [
            cm.listRelatives(x, p=1)[0] for x in cm.ls(v=1, type="mesh")
        ]

        if len(self.visible) < 1:
            if self.selectd == 1:
                self.selected.append(self.selectd[0])

            else:
                print("Nothing visible in the scene!")
                cm.error("Nothing visible in the scene!")

        elif len(self.visible) == 1:
            if len(self.selectd) >= 1:
                if len(self.hilited) == 1:
                    self.selected.append(self.hilited[0])
                else:
                    self.selected.append(self.selectd[0])

            elif len(self.selectd) == 0:
                self.selected.append(self.visible[0])

        elif len(self.visible) > 1:
            if len(self.selectd) == 0:
                self.selected.append(self.visible[0])

            elif len(self.selectd) == 1:
                if len(self.hilited) == 1:
                    self.selected.append(self.hilited[0])
                else:
                    self.selected.append(self.selectd[0])

        self.selected = self.selected[0]
        # Create initial dictionary of all objects in the scene

        _assy = cm.ls(assemblies=1)
        cm.select(
            [
                x for x in _assy if len(cm.listRelatives(x, children=1)) > 1
            ],
            hi=1
        )

        self.dictOfSceneObjects = {}
        i = 0
        for each in cm.ls(sl=1):
            if each in [x for x in self.all_parts()]:
                self.dictOfSceneObjects[i] = each
                i += 1

        # get index of selected object
        for (index, value) in self.dictOfSceneObjects.iteritems():
            if self.selected == value:
                self.indexed = index

        # Titles for scene
        self.pickWalkVersion = ("v {}".format(self.__version__()))
        self.scriptName = 'pickWalk Python '

        # Select object
        cm.select(self.selected)

    @staticmethod
    def all_parts():
        # Get all the mesh transforms in the scene / non-shapes
        _all_shapes = cm.ls(shapes=1)
        [_all_shapes.remove(x) for x in cm.ls(cameras=1)]
        _all_models = [cm.listRelatives(x, p=1)[0] for x in _all_shapes]
        return _all_models

    @staticmethod
    def __doc__():
        doc = \
            """
        Started development in late 2015 and honed the development process
        until 2017. This tool should always be credited to Jeff Miller.
        
        PickWalker allows the user to skip though groups, going from mesh
        to mesh without ever having to pickwalk up, over or down the hierarchy.
        
        It will also display how many vertices are unmerged, which object is
        selected out of the total, isolate and fit the mesh to the viewport and,
        finally, the name of the model.
        
        
        In Maya's Hotkey Settings, append this script to the following
        recommended hotkeys:
        
        alt + `     - To go up the scene tree
        `           - To go down the scene tree
        
        
        Jeff3DAnimation@yahoo.com
        Jeff3DAnimation.com
        """

        return doc

    @staticmethod
    def __version__():
        return "1.1.0"

    def print_sel_and_info(self):
        _info = '{}{} has selected {}. This is mesh {} of {}.'.format(
            self.scriptName,
            self.pickWalkVersion,
            self.dictOfSceneObjects[self.indexed],
            self.indexed + 1,
            len(self.dictOfSceneObjects),
        )
        _umvs = '{} unmerged verts.'.format(self.umv)

        # Print the info
        print(_info)

        # Heads up message for user to visibly always see information
        cm.headsUpMessage(_info + '    ' + _umvs)

    def show_sel(self):
        # get the item
        obj = self.dictOfSceneObjects[self.indexed]

        # Hide all
        [cm.hide(x) for x in self.dictOfSceneObjects.values()]
        cm.showHidden(obj)
        cm.select(obj)
        cm.showHidden(cm.listRelatives(obj, ap=1))
        cm.viewFit('persp')

        # get number of umv for selected item
        self.umv = self.get_umvs()

        # Select item again and print info
        cm.select(obj)
        self.print_sel_and_info()

    def get_umvs(self):
        # get object selected
        obj = self.dictOfSceneObjects[self.indexed]

        # Turn into vert selection
        verts = cm.polyListComponentConversion(obj, tv=True)
        cm.select(verts)

        # Filter verts to border only
        cm.polySelectConstraint(
            m=3,
            t=1,
            w=1,
            bo=0,
            sh=0,
            cr=0,
        )

        # Count
        num_v = cm.ls(sl=1, fl=1)
        cm.polySelectConstraint(
            m=0,
            t=0,
            # w=0,  # disabled for now
        )

        return len(num_v)

    @staticmethod
    def run_check():
        # Check for keyboard modifiers
        mods = cm.getModifiers()
        return mods

    def run(self):
        # Force object selection
        mm.eval('toggleSelMode;')
        mm.eval('toggleSelMode;')
        mods = self.run_check()

        if mods == 0:

            # normal
            self.indexed += 1

        elif mods == 8:

            # alt held down
            self.indexed -= 1

        # Reset values
        if self.indexed > len(self.dictOfSceneObjects) - 1:
            self.indexed = 0

        elif self.indexed < 0:
            self.indexed = len(self.dictOfSceneObjects) - 1

        # Show the selection
        self.show_sel()


def main():
    PickWalker().run()


if __name__ == '__main__':
    main()

### THIS CODE HAS TO BE EXECUTED FROM A PYTHON SCRIPT NODE IN SOLARIS

from pxr import Usd, UsdGeom, Gf
import hou
import json

node = hou.pwd()


class blockbuild():
    def __init__(self):
        self.dictread()
    
    def dictread(self):
        self.citydict = open("P:/AndreJukebox/assets/sets/city/publish/xml/block_builder.json")
        self.cityread = json.load(self.citydict)
    
    def blockslist(self):
        for keys in self.cityread:
            blockhierarchy = keys.rsplit("_",1)[0]
            block_stage = f'P:/AndreJukebox/assets/sets/{blockhierarchy}/publish/usd/{blockhierarchy}.usd'
            self.stage = Usd.Stage.CreateNew(block_stage)
            group_prim_path = f'/{keys}'
            group_prim = self.stage.DefinePrim(group_prim_path,'Xform')
            self.createRefs(blocks=keys,refsnum=len(self.cityread[keys]['assets']))
            group_model = Usd.ModelAPI(group_prim)
            group_model.SetKind("group")
            self.stage.GetRootLayer().Save()
            # print('________DONE_________')
    
    def createRefs(self, blocks, refsnum):    
        iteration = 0
        for buildings in self.cityread[blocks]['assets']:
            xform = (self.cityread[blocks]['assets'][buildings]['xform'])
            assetname = buildings.rsplit("_",1)[0]
            new_building = f"/{blocks}/{buildings}"
            
            print(new_building)

            new_prim = self.stage.DefinePrim(new_building)
            assetabc = (self.cityread[blocks]['assets'][buildings]['abcpath'])
            new_prim.GetReferences().AddReference(assetabc)
            new_prim.SetInstanceable(True)
            building_model = Usd.ModelAPI(new_prim)
            building_model.SetKind("component")
            
            # assign the matrix to each building
            target_path = self.stage.GetPrimAtPath(new_building)
            xformable = UsdGeom.Xformable(target_path)
            transform_matrix = eval(xform)
            final_matrix = Gf.Matrix4d(transform_matrix)
            xformable.ClearXformOpOrder()
            xformable.AddTransformOp().Set(value=final_matrix)


blockbuild().blockslist()

### THIS CODE HAS TO BE EXECUTED FROM A PYTHON SCRIPT NODE IN SOLARIS

from pxr import Usd, UsdGeom, Gf
import hou
import json
node = hou.pwd()

class blockbuild():
    def __init__(self):
        self.dictread()
    
    def dictread(self):
        self.citydict = open("P:/AndreJukebox/assets/sets/city/publish/xml/city_builder.json")
        self.cityread = json.load(self.citydict)
    
    def blockslist(self):
        block_stage = f'P:/AndreJukebox/assets/sets/city/publish/usd/city.usd'
        self.stage = Usd.Stage.CreateNew(block_stage)
        city_prim = self.stage.DefinePrim("/city", "Xform")
        city_prim.SetInstanceable(True)
        city_model = Usd.ModelAPI(city_prim)
        city_model.SetKind("assembly")

        for keys in self.cityread:
            print(keys)
            self.createRefs(blocks=keys)
            
        self.stage.GetRootLayer().Save()
        
        print('________DONE_________')
    
    def createRefs(self, blocks):

        xform = (self.cityread[blocks]['xform'])
        assetname = blocks.rsplit("_",1)[0]

        block_asset = blocks.rsplit("_",1)[0]
        new_block = f"/city/{blocks}"

        groupusd = (self.cityread[blocks]['usdpath'])
        
        new_prim = self.stage.DefinePrim(new_block, "Xform")
        building_prim = f'/{block_asset}_0001'
        
        new_prim.GetReferences().AddReference(groupusd, building_prim)
        new_prim.SetInstanceable(True)
        
        # assign the matrix to each building

        target_path = self.stage.GetPrimAtPath(new_block)
        xformable = UsdGeom.Xformable(target_path)
        transform_matrix = eval(xform)
        final_matrix = Gf.Matrix4d(transform_matrix)
        xformable.ClearXformOpOrder()
        xformable.AddTransformOp().Set(value=final_matrix)


blockbuild().blockslist()

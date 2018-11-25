import bpy

import json
import os

f = open("./orion.json")
data = json.load(f)
f.close()

def hex_to_rgb(hex):
    hex = hex.lstrip("#")

    gamma = 2.2

    base = list(int(hex[i:i + len(hex) // 3], 16) for i in range(0, len(hex), len(hex) // 3))

    return list(map(lambda _: pow(_ / 255, gamma), base))

class Palette(bpy.types.Panel):
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_label = "Palette"

    def draw(self, ctx):
        cont = self.layout.box()

        for i, item in enumerate(bpy.context.scene.col):
            row = cont.row()

            row.prop(
                ctx.scene.col[i],
                "rgb",
                text = str(item.name)
            )

def register():
    class Item(bpy.types.PropertyGroup):
        name = bpy.props.StringProperty()
        rgb = bpy.props.FloatVectorProperty(
            subtype = "COLOR"
        )
    bpy.utils.register_class(Item)

    bpy.types.Scene.col = bpy.props.CollectionProperty(
        type = Item
    )

    bpy.context.scene.col.clear()
    for key, val in data.items():
        item = bpy.context.scene.col.add()
        item.name = key
        item.rgb = hex_to_rgb(val)

    bpy.utils.register_module(__name__)

def unregister():
    bpy.utils.unregister_module(__name__)

if __name__ == "__main__":
    register()

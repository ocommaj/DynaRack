bl_info = {
    "name": "DynaRack",
    "description": "Make Mini Rack Units Dynamically",
    "author": "Jim O'Connor <hello@ocommaj.com>",
    "version": (0, 0, 1),
    "blender": (2, 90, 1),
    "location": "Object",
    "warning": "",
    "category": "All"
}

moduleNames = [
    'property_groups',
    'mountpoints_operators',
    'standoff_operator',
    'dynarack_panels',
    ]

import sys
import importlib

moduleFullNames = [ f"{__name__}.{module}" for module in moduleNames ]

for module in moduleFullNames:
    if module in sys.modules:
        importlib.reload(sys.modules[module])
    else:
        globals()[module] = importlib.import_module(module)
        setattr(globals()[module], 'moduleNames', moduleFullNames)

def register():
    for module in moduleFullNames:
        if module in sys.modules:
            if hasattr(sys.modules[module], 'register'):
                sys.modules[module].register()

def unregister():
    for module in moduleFullNames:
        if module in sys.modules:
            if hasattr(sys.modules[module], 'unregister'):
                sys.modules[module].unregister()

if __name__ == "__main__":
    register()

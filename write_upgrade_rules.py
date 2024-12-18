"""
Write rules for upgrading outdated SOFA files.

Writes the following json files:
upgrade.json

For a more detailed information about the json files refer to _readme.txt
"""
# %%
import json
import os

upgrade = {
    "AnnotatedEmitterAudio": {
        "from_to": [[["0.1"], ["AnnotatedEmitterAudio_0.2"], "1"]],
        "1": {
            "move": {},
            "remove": [],
            "message": ("The data in the variable 'Response' "
                        "might have to be updated."),
            },
    },
    "AnnotatedReceiverAudio": {
        "from_to": [[["0.1"], ["AnnotatedReceiverAudio_0.2"], "1"]],
        "1": {
            "move": {},
            "remove": [],
            "message": ("The data in the variable 'Response' "
                        "might have to be updated."),
            },
    },
    "FreeFieldDirectivityTF": {
        "from_to": [[["1.0"], ["FreeFieldDirectivityTF_1.1"], "1"]],
        "1": {
            "move": {
                "EmitterPosition": {
                    "target": "EmitterPosition",
                    "moveaxis": None,
                    "deprecated_dimensions": ["IC", "MC"]},
                "EmitterDescription": {
                    "target": "EmitterDescriptions",
                    "moveaxis": None,
                    "deprecated_dimensions": ["IS"]},
            },
            "remove": [],
            "message": ("Consider to add the optional data "
                        "'GLOBAL_EmitterDescription'"
                        "introduced in convention version 1.1.\n"
                        "WARNING: Adding 'GLOBAL_EmitterDescription' is "
                        "required if 'EmitterDescriptions' is contained in "
                        "the SOFA object."),
        },
    },
    "SimpleFreeFieldHRIR": {
        "from_to": [[["0.4"], ["SimpleFreeFieldHRIR_1.0"], "1"]],
        "1": {
            "move": {},
            "remove": [],
            "message": ("Consider to add the optional data 'SourceUp', "
                        "'SourceView', 'SourceView:Type', and "
                        "'SourceView:Units' with default values that were "
                        "introduced in convention version 1.0"),
        },
    },
    "SimpleFreeFieldTF": {
        "from_to": [[["0.4", "1.0"], ["SimpleFreeFieldHRTF_1.0"], "1"]],
        "1": {
            "move": {},
            "remove": [],
            "message": None,
        },
    },
    "SimpleHeadphoneIR": {
        "from_to": [[["0.1", "0.2"], ["SimpleHeadphoneIR_1.0"], "1"]],
        "1": {
            "move": {
                "ReceiverDescription": {
                    "target": "ReceiverDescriptions",
                    "moveaxis": None,
                    "deprecated_dimensions": None},
                "EmitterDescription": {
                    "target": "EmitterDescriptions",
                    "moveaxis": None,
                    "deprecated_dimensions": None},
            },
            "remove": [],
            "message": None,
        },
    },
    "SingleRoomDRIR": {
        "from_to": [[["0.2", "0.3"], ["SingleRoomSRIR_1.0"], "1"]],
        "1": {
            "move": {},
            "remove": [],
            "message": ("Consider providing optional data that was introduced "
                        "in SingleRoomSRIR version 1.0"),
        },
    },
    "MultiSpeakerBRIR": {
        "from_to": [[["0.3"], ["SingleRoomMIMOSRIR_1.0"], "1"]],
        "1": {
            "move": {
                "Data.IR": {
                    "target": "Data.IR",
                    "moveaxis": [3, 2],
                    "deprecated_dimensions": None},
                "Data.Delay": {
                    "target": "Data.Delay",
                    "moveaxis": None,
                    "deprecated_dimensions": ["IRE"]},
            },
            "remove": [],
            "message": ("Consider providing optional data that was introduced "
                        "in SingleRoomSRIR version 1.0"),
        },
    },
    "GeneralFIRE": {
        "from_to": [[["1.0"], ["GeneralFIR-E_2.0"], "1"]],
        "1": {
            "move": {
                "Data.IR": {
                    "target": "Data.IR",
                    "moveaxis": [3, 2],
                    "deprecated_dimensions": None},
                "EmitterPosition": {
                    "target": "EmitterPosition",
                    "moveaxis": None,
                    "deprecated_dimensions": ["ECI"]},
            },
            "remove": [],
            "message": ("Consider providing optional data that was introduced "
                        "in SingleRoomSRIR version 1.0"),
        },
    },
}

json_file = os.path.join(os.path.dirname(__file__), "rules", "upgrade.json")
with open(json_file, 'w') as file:
    json.dump(upgrade, file, indent=4)

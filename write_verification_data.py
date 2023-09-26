# %%
"""Write verification data to SOFA files."""
import sofar as sf
from sofar.utils import _complete_sofa
import os
import numpy as np

rules, unit_aliases, deprecations, _ = sf.Sofa._verification_rules()


# -----------------------------------------------------------------------------
# Rules that restrict SOFA attributes to certain values
print("Write data to test SOFA attributes with restricted values")
print("---------------------------------------------------------")

# key: name of variable or attribute for testing the rule
for key in rules:
    # check if rule exists
    if "value" not in rules[key] or rules[key]["value"] is None:
        continue

    # get blank SOFA file
    key_sf = key.replace(".", "_").replace(":", "_")
    filename = f"{key_sf}=invalid-value.sofa"
    print(filename)
    sofa = _complete_sofa()

    # write invalid value
    sofa.protected = False
    setattr(sofa, key_sf, "invalid-value")
    sofa.protected = True

    # write invalid SOFA file
    sf.io._write_sofa(
        os.path.join("data", "restricted_values", filename),
        sofa, compression=4, verify=False)

del key, key_sf, sofa, filename


# -----------------------------------------------------------------------------
# Rules that require conditional Attributes or Variables to be existing
print("\nWrite data to test general dependencies")
print("---------------------------------------")

# key: name of variable or attribute for testing the rule
for key in rules:

    # check if rule applies
    if "general" not in rules[key]:
        continue

    key_sf = key.replace(".", "_").replace(":", "_")

    for sub in rules[key]["general"]:

        # get blank SOFA file
        sub_sf = sub.replace(".", "_").replace(":", "_")
        filename = f"{key_sf}.{sub_sf}=missing.sofa"
        print(filename)
        sofa = _complete_sofa()

        # delete conditional dependency
        sofa.delete(sub_sf)

        # write invalid SOFA file
        sf.io._write_sofa(os.path.join(
            "data", "general_dependencies", filename),
            sofa, compression=4, verify=False)

del key, key_sf, sub, sub_sf, sofa, filename


# -----------------------------------------------------------------------------
# Specific rules except for GLOBAL:DataType and GLOBAL:SOFAConventions.
# Specific rules require certain variables or attributes to exist depending
# on a parent variable or attribute and sometimes also restrict the value for
# the child.
print("\nWrite data to test specific dependencies")
print("----------------------------------------")

keys = [k for k in rules.keys() if "specific" in rules[k] and k not in
        ["GLOBAL:DataType", "GLOBAL:SOFAConventions"]]

# key: name of variable or attribute for testing specific dependency
for key in keys:
    key_sf = key.replace(".", "_").replace(":", "_")

    # key_value: value of the variable or attribute that triggers the
    # specific dependency
    for value_key in rules[key]["specific"]:

        # sub: name of variable or attribute for which a specific
        # dependency is checked
        for sub in rules[key]["specific"][value_key]:

            if sub.startswith("_"):
                continue

            sub_sf = sub.replace(".", "_").replace(":", "_")
            sofa = _complete_sofa()

            # set key to correct value
            sofa.protected = False
            setattr(sofa, key_sf, value_key)
            sofa.protected = False

            # test a wrong value sor sub
            value_sub = rules[key]["specific"][value_key][sub]
            if value_sub is not None:
                setattr(sofa, sub_sf, "invalid-value")
                filename = f"{key_sf}={value_key}.{sub_sf}=invalid-value.sofa"
                print(filename)
                sf.io._write_sofa(os.path.join(
                    "data", "specific_dependencies", filename),
                    sofa, compression=4, verify=False)

            # test deleting sub
            sofa.protected = False
            delattr(sofa, sub_sf)
            sofa.protected = True
            filename = f"{key_sf}={value_key}.{sub_sf}=missing.sofa"
            print(filename)
            sf.io._write_sofa(os.path.join(
                "data", "specific_dependencies", filename),
                sofa, compression=4, verify=False)

del keys, key, key_sf, value_key, sub, sub_sf, sofa, value_sub, filename


# -----------------------------------------------------------------------------
# specific rules for GLOBAL:DataType
for data_type in rules["GLOBAL:DataType"]["specific"]:

    if data_type in ["FIR", "FIR-E", "FIRE", "TF", "TF-E"]:
        convention = "General" + data_type
    elif data_type == "SOS":
        convention = "SimpleFreeFieldHRSOS"
    elif data_type == "FIRE":
        convention = "MultiSpeakerBRIR"
    elif data_type == "Audio":
        convention = "AnnotatedEmitterAudio"

    for key in rules["GLOBAL:DataType"]["specific"][data_type]:
        if key.startswith("_"):
            continue

        key_sf = key.replace(".", "_").replace(":", "_")
        sofa = sf.Sofa(convention)
        if sofa.GLOBAL_SOFAConventionsVersion.startswith('0.'):
            sofa.verify(mode="read")

        # test a wrong value
        value = rules["GLOBAL:DataType"]["specific"][data_type][key]
        if value is not None:
            setattr(sofa, key_sf, "invalid-value")
            filename = \
                f"GLOBAL_DataType={data_type}.{key_sf}=invalid-value.sofa"
            print(filename)
            sf.io._write_sofa(os.path.join(
                "data", "specific_dependencies", filename),
                sofa, compression=4, verify=False)

        # test deleting the attribute
        sofa.protected = False
        delattr(sofa, key_sf)
        sofa.protected = True
        filename = f"GLOBAL_DataType={data_type}.{key_sf}=missing.sofa"
        print(filename)
        sf.io._write_sofa(os.path.join(
                "data", "specific_dependencies", filename),
                sofa, compression=4, verify=False)

del data_type, convention, key, key_sf, sofa, value, filename


# -----------------------------------------------------------------------------
# specific rules for GLOBAL:SOFAConventions
for convention in rules["GLOBAL:SOFAConventions"]["specific"]:
    for key in rules["GLOBAL:SOFAConventions"]["specific"][convention]:
        if key.startswith("_"):
            continue

        key_sf = key.replace(".", "_").replace(":", "_")
        sofa = sf.Sofa(convention)
        if sofa.GLOBAL_SOFAConventionsVersion.startswith('0.'):
            sofa.verify(mode="read")

        # test a wrong value
        value = rules["GLOBAL:SOFAConventions"]["specific"][convention][key]
        if value is not None:
            sofa.protected = False
            setattr(sofa, key_sf, "invalid-value")
            sofa.protected = True

            filename = (f"GLOBAL_SOFAConventions={convention}."
                        f"{key_sf}=invalid-value.sofa")
            print(filename)

            sf.io._write_sofa(os.path.join(
                    "data", "specific_dependencies", filename),
                    sofa, compression=4, verify=False)

        # test deleting the attribute
        sofa.protected = False
        delattr(sofa, key_sf)
        sofa.protected = True

        filename = f"GLOBAL_SOFAConventions={convention}.{key_sf}=missing.sofa"
        print(filename)

        sf.io._write_sofa(os.path.join(
                "data", "specific_dependencies", filename),
                sofa, compression=4, verify=False)

del convention, key, key_sf, sofa, filename


# -----------------------------------------------------------------------------
# restrictions on dimensions
print("\nWrite data to test restrictions on dimensions")
print("---------------------------------------------")

# test dimensions for spherical harmonics coordinates
sofa = sf.Sofa("GeneralFIR-E")
sofa.ReceiverPosition_Type = "spherical harmonics"
sofa.ReceiverPosition_Units = "degree, degree, metre"
sofa.Data_IR = np.zeros((1, 2, 1, 1))
sofa.Data_Delay = np.zeros((1, 2, 1))

filename = "ReceiverPosition_Type=spherical harmonics.R=2.sofa"
print(filename)

sofa.verify(issue_handling="ignore")
sf.io._write_sofa(os.path.join(
    "data", "restricted_dimensions", filename),
    sofa, compression=4, verify=False)

sofa = sf.Sofa("GeneralFIR-E")
sofa.EmitterPosition_Type = "spherical harmonics"
sofa.EmitterPosition_Units = "degree, degree, metre"
sofa.Data_IR = np.zeros((1, 1, 1, 2))
sofa.Data_Delay = np.zeros((1, 1, 2))

filename = "EmitterPosition_Type=spherical harmonics.E=2.sofa"
print(filename)

sofa.verify(issue_handling="ignore")
sf.io._write_sofa(os.path.join(
    "data", "restricted_dimensions", filename),
    sofa, compression=4, verify=False)

# test dimensions for SOS data type
sofa = sf.Sofa("SimpleFreeFieldHRSOS")
sofa.Data_SOS = np.zeros((1, 2, 1))

filename = "GLOBAL_DataType_Type=SOS.N=1.sofa"
print(filename)

sofa.verify(issue_handling="ignore")
sf.io._write_sofa(os.path.join(
    "data", "restricted_dimensions", filename),
    sofa, compression=4, verify=False)

# test dimensions for SimpleFreeFieldHRIR
for convention in ["SimpleFreeFieldHRIR",
                   "SimpleFreeFieldHRTF",
                   "SimpleFreeFieldHRSOS"]:
    sofa = sf.Sofa(convention)
    sofa.EmitterPosition = [[1, 0, 0], [0, 1, 0]]

    filename = f"GLOBAL_SOFAConventions={convention}.E=2.sofa"
    print(filename)

    sofa.verify(issue_handling="ignore")
    sf.io._write_sofa(os.path.join(
        "data", "restricted_dimensions", filename),
        sofa, compression=4, verify=False)

del sofa, filename, convention


# -----------------------------------------------------------------------------
# deprecations
print("\nWrite data to test deprecations")
print("-------------------------------")

conventions = sf.utils._get_conventions("name")

for deprecated, substitute in deprecations["GLOBAL:SOFAConventions"].items():
    """
    Test if deprecations raise warnings in read mode and errors in write mode.
    """

    # check if deprecated and substitute convention exist in sofar
    if deprecated in conventions:

        if deprecated == "SingleTrackedAudio":
            # This convention was never used and does not define the dimension
            # 'R'. Thus test files can not be written in this case
            continue

        sofa = sf.Sofa(deprecated, verify=False)

        filename = f"GLOBAL_SOFAConventions={deprecated}.{substitute}.sofa"
        print(filename)

        sofa.verify(issue_handling="ignore")
        sf.io._write_sofa(os.path.join(
            "data", "deprecations", filename),
            sofa, compression=4, verify=False)

del conventions, deprecated, substitute, sofa, filename

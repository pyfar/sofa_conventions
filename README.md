# SOFA conventions

Complete definition of SOFA conventions according to AES69 are contained in the
folders *conventions* and *rules*. The conventions are intended to be used in
applications that read or write SOFA data. Test data violating the conventions
are contained in *data*. This data is intended for testing if an application
correctly verifies data against AES69 when reading it. Updating and writing
data partly requires the sofar package available from
<https://github.com/pyfar/sofar> and can be installed via

 `pip install sofar`

AES69-2022: *AES standard for file exchange - Spatial acoustic data file
format*, Audio Engineering Society, Inc., New York, NY, USA.

## 1. Conventions

This folder contains the official SOFA conventions as json and csv files. SOFA
conventions are the basis of SOFA files, a data format to store spatially
distributed acoustic data. They also contain basic information for verifying
the content inside SOFA files. The conventions are tested as part of the sofar
package.

## 2. Data

Contains SOFA files that each contain exactly one invalid entry. They are
written with

`write_verification_data.py`

and are intended for testing SOFA APIs. See the following section for more
details.

## 3. Rules

Contains Verification rules as json files that are needed for a complete
verification of SOFA files. They are written by running

`write_verification_rules.py`

### Verification of SOFA files

The following details how SOFA files must be verified to follow the SOFA
standard AES69. The verification rules make use of the SOFA conventions
and the verification rules. The verification requires the following steps:

1. Mandatory variables and attributes must be contained in the file. Such data
   has the flag "m" in the conventions.
2. All data must have the correct type (double, string, attribute) as denoted
   the field "type" in the conventions.
3. All variables must have the correct dimensions as denoted by the
   "dimemsions" in the conventions. The dimensions is determined from the
   variable that lists it with a lower case letter. E.g. if Data_IR shall have
   the dimension "mrn" the and the actual shape of Data_IR is (10, 2, 128),
   then M=10, R=2, and N=128.
4. Variable and attribute names may not contain underscores and the keywords
   'API', 'GLOBAL', and 'PRIVATE'.
   Note: AES69 uses colons to denote attributes (e.g., 'SourcePosition:Units'
   denotes the attribute 'Units' belonging to the variable 'SourcePosition')
   and dots to denote hierarchies (e.g., 'Data.Real' and 'Data.Imag' are
   variables of the group 'Data'). In addition AES69does not have a keyword to
   specify global attribute. Some APIs (API_MO and sofar) can not use dots and
   colons in the names (they use underscores instead) and require the keyword
   'GLOBAL' to highlight global attributes, e.g., 'GLOBAL_SOFAConventions'.
   The verification of this rule might thus vary across toolboxes.
5. Application specific (custom) variables and attributes can not have names
   that are used by the respective convention.
6. Some attributes can only have a limited number of entries. Examples for this
   are names of coordinate systems, units, and room types. For instance the
   used coordinate system can only be 'cartesian', 'spherical', or
   'spherical harmonics'. A special case are units, where multiple spellings
   are allowed (e.g. 'meter' and 'metre') and that can be separated either by
   commas, commas plus spaces, or spaces (e.g. 'meter, meter, degree' or
   'meter,meter degree'). All restricted values should be verified insensitive
   of the case, however, units shall be written in lowercase only.
7. All verification rules from rules.json must be checked (see below)

The json files inside this folder contain rules for verifying SOFA files.
The rules were manually extracted from the SOFA Standard AES69-2020. Note that
the json files are written with `write_verification_rules.py` where additional
comments on the rules can be found.

### rules.json

Contains all verification rules

- that can not be derived from the SOFA conventions
- that do not pertain to units and unit strings

Note that the values of units MUST always be given in reference units as
detailed for unit_aliases.json (see below)

The rules are contained in a json file with the following structure
(explanation below, examples refer to rules.json)

```python
{
   key_1: {
      "value": values
      "general": [sub_key_1, sub_key_2, ..., sub_key_N],
      "specific": {
         value_1: {
            sub_key_1: values
            .
            .
            .
            sub_key_N: values
            "_dimensions": {
               dimension_1: {
                  "value": values,
                  "value_str": value_string
               },
               .
               .
               .
               dimensions_N: {...}
            }
         }
         value_2: {...},
         .
         .
         .
         value_N: {...}
      }
   },
   key_2: {...},
   .
   .
   .
   key_N: {...}
}
```

#### Keys

`key_1`, `key_2`, ... `key_N` are the names of SOFA variables (e.g.,
'ReceiverPosition') or attributes (e.g., 'GLOBAL_DataType').

#### Values

`values` are either a list of possible values that a variable of attribute must
have or null, if the variable or attribute can have any value.
EXAMPLE: 'GLOBAL_DataType' (`key`) can be ["FIR", "FIR-E", "FIRE" "TF", "TF-E",
         "TFE", "SOS"] (`value`) and an error should be raised if
         'GLOBAL_DataType' has any other value. If `values` was null,
         'GLOBAL_DataType' could have any value.

#### Dependencies

A variable or attribute (`key`) can have two different kinds of dependencies.
general" and "specific". If there are such dependencies, a `key` is
followed by the corresponding fields.
EXAMPLE: 'GLOBAL_DataType' (`key`) has "specific" dependencies and
         'ListenerPosition_Type' (`key`) has "general" dependencies.

##### General Dependencies

General dependencies are simple. The contain an list that contains an arbitrary
number of variables and attributes (`sub_keys`), which must be contained in a
SOFA object IF `key` is contained.
EXAMPLE: 'ListenerView_Type' must be contained if 'ListenerView' is contained.

##### Specific Dependencies

Specific dependencies are more complex. They describe dependencies for a
variable or attribute (`sub_key_1`, `sub_key_2`, ..., `sub_key_N`) that only
have to be enforced if `key` has a specific value (`value_1`, `value_2`, ...
, `value_N`). There are three possible dependencies.

1. If the value of `sub_key` is null, it only has to be checked if `sub_key` is
   contained in the Sofa object
   EXAMPLE: If 'GLOBAL_DataType' is "FIR", 'Data_IR' must be contained
2. If the value is not null, `sub_key` must have on of the listed values.
   EXAMPLE: If 'GLOBAL_DataType' is "FIR", 'Data_SamplingRate_Units' must be
            "hertz"
3. If the `sub_key` is "_dimensions", the size of on or more SOFA/NetCDF
   dimensions is restricted to one or more certain values.
   EXAMPLE: If 'GLOBAL_DataType' is "SOS", the dimension 'N' must be an integer
            multiple of 6 (in this specific case provided as a list of
            possible values up to 600).
   For restrictions on the dimensions the rules also provide a verbose error
   message that can be used for feedback in case the dependency is violated.
   EXAMPLE: The error message for the case described above is "an integer
            multiple of 6 greater 0"

### unit_aliases.json

Contains a list of possible variants of unit names. The structure is as follows

{
   variant_1_unit_1: reference_unit_1
   variant_2_unit_1: reference_unit_2
   .
   .
   .
   variant_N_unit_1: reference_unit_1
   variant_1_unit_2: reference_unit_2
   .
   .
   .
   variant_N_unit_N: reference_unit_N
}

EXAMPLE: The unit "metre" (`reference_unit_1`) can also be written "metres",
         "meter", and "meters" (`variant_1_unit_1`, `variant_2_unit_1`,
         `variant_3_unit_1`).

### deprecations.json

Contains a list of deprecated conventions and the convention that replaces
them.

### upgrade.json

Contains rules for upgrading deprecated conventions. Upgrading a convention
requires the following steps

1. Replace the convention, e.g., switch from *MultiSpeakerBRIR* to
   *SingleRoomMIMOSRIR*. Note that this dot not change any data. It only
   changes what data is expected to be stored in a SOFA file.
2. Update the fields *GLOBAL:SOFAConventions*, *GLOBAL_SOFAConventionsVersion*,
   *GLOBAL_Version*, and *GLOBAL_DataType* according to the new convention.
3. Check if any data needs to be renamed and/or reshaped.
4. Check if any data needs to be removed.
5. Check if new default data needs to be specified.

Steps 1, 2, and 5 are general steps and do not require specific rules. Steps
3 and 4 are defined by the json file

```python
{
   deprecated_convention_1: {
      "from_to": [[[outdated versions],
                   [possible upgrades],
                    upgrade_key],
                  [a possible second/third/... set in analogy to the above]],
      upgrade_key_1: {
         "move": {
            source_key_1: {
               "target": target_key,
               "moveaxis: [from, to],
               "deprecated_dimensions": [dimensions_1, ..., dimensions_N]
            .
            .
            .
            source_key_N: {...}
            }
         "remove": [target_key_1, ..., target_key_N],
         "message": message to display after upgrading
         }
      },
      upgrade_key_2: {},
      .
      .
      .
      upgrade_key_N: {}
   },
   deprecated_convention_2: {...},
   .
   .
   .
   deprecated_convention_N: {...}
}
```

#### deprecated_convention

The name of the deprecated convention as a string.

#### from_to

A list with three values

1. The version numbers of the deprecated conventions that can be upgraded.
2. The conventions and version numbers to which it can be upgraded.
3. A unique key, that defines where the information for upgrading is given.

#### move

Defines data that must be moved by means of

- the *source_key*, i.e., the name of the data that needs to be moved
- the *target_key*, i.e., the new name of the data
- *moveaxis* which defines if any of the dimensions of the data must be
  reorganized. In this case *from* gives on or more dimension that are moved
  in the positions defined by *to*. Dimensions start at 0 and the procedure
  follows that of *numpy.moveaxis*
- *deprecated_dimensions* lists data dimensions that are not supported by the
  upgraded convnention.

In case no data needs to be moved, move simply is empty, i..e, `{}`.

#### remove

A list of data names that must be removed. This is empty if no data needs to
be removed, i.e., `[]`.

#### message

A message that should be printed after upgrading. `null` if no message is
required.

# OT2-SARS-CoV2
OT-2 API V2 scripts for Opentrons robot using the [TaqPath COVID-19 Combo Kit](https://www.fda.gov/media/136112/download)

This workflow enables end-to-end RT-qPCR using the OT2 liquid handling robot by OpenTrons. This includes:
- Executing magnetic beads-based RNA extraction.
- Performing qPCR assay preperation protocol in 96-well plate format.

Each folder contains the python script to run the protocol fully in the OT2 desktop application, as well as a Jupyter Notebook that allows the user to test each liquid transfer function individually.

Full setup instructions can be found [here](https://github.com/DAMPLAB/OT2-SARS-CoV2/blob/master/instructions.md)

## Software Requirements

1. [Python 3](https://www.python.org/downloads/)

2. [Jupyter Notebook](https://jupyter.org/)

3. [OT2 APP](https://opentrons.com/ot-app)

4. Clone this [repository](https://github.com/DAMPLAB/OT2-SARS-CoV2) to a local computer.

## Magnetic Beads-based RNA Extraction
**Kit**: MagMAX™ Viral/Pathogen II Nucleic Acid Isolation Kit    

**Sample Volume**: 200&mu;L

## qPCR Preperation
**Kit**: TaqPath™ COVID-19 Combo Kit

**Sample Volume**: 200&mu;L

## Authors

* **Dany Fu** - [dany-fu](https://github.com/dany-fu)
* **Rita R. Chen** - [rychen58](https://github.com/rychen58)

# Instructions for OT2-SARS-CoV2
Rita R. Chen, Dany Fu    
<p align="center">
  <img src="https://user-images.githubusercontent.com/32885235/95505810-fb33c200-097c-11eb-9cb9-3f299bb68920.png" />
</p>


## About
This document is intended to guide users through OT2 SARS CoV2 detection workflow based on [TaqPath™ COVID-19 Combo Kit](https://www.fda.gov/media/136112/download).
This workflow enables end-to-end RT-qPCR using the OT2 liquid handling robot by OpenTrons. This includes:
- Executing magnetic beads-based RNA extraction protocol
- Performing qPCR assay preparation protocol in 96-well plate format

## Materials
Below we list the materials previously used to implement OT2 SARS CoV2 detection workflow. We recommend starting with these consumables, however certain standard labwares may be altered. Labware needs to be defined carefully when working with OpenTrons OT-2 liquid handling robot and changes to labware requires the user to update the protocol scripts and the labwares used during the execution of OT2 SARS CoV2 runs. Here is a general [OpenTrons’ Guideline](https://support.opentrons.com/en/articles/3137426-what-labware-can-i-use-with-the-ot-2) for utilizing labware for users new to OT2 and additional details regarding labware can be found on [OpenTrons Labware Library](https://labware.opentrons.com/).

### Software:
- OpenTrons OT-2 App (Version 3.10.3 or later)
- Python 3
- [OT2 SARS CoV2 GitHub repository](https://github.com/DAMPLAB/OT2-SARS-CoV2)

### Hardware:
- [OpenTrons OT-2](https://opentrons.com/ot-2)
- [OpenTrons P20 Multi-Channel Generation 2 Electronic Pipette](https://opentrons.com/pipettes)
- [OpenTrons P300 Multi-Channel Generation 2 Electronic Pipette](https://opentrons.com/pipettes)
- [OpenTrons Temperature Module Generation 2](https://opentrons.com/modules#temperature)
- [OpenTrons Magnetic Module Generation 1](https://opentrons.com/modules#magnetic)
- Eppendorf ThermoMixer® C

### Consumables & Reagents:
- [OpenTrons 20 µL Filter Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-20ul-filter-tips)
- [OpenTrons 200 µL Filter Tips](https://shop.opentrons.com/collections/opentrons-tips/products/opentrons-200ul-filter-tips)
- [Bio-Rad 96-well PCR Plate](https://www.bio-rad.com/en-us/sku/hsp9601-hard-shell-96-well-pcr-plates-low-profile-thin-wall-skirted-white-clear?ID=hsp9601)
- [USA Scientific 96 Deep Well Plate 2.4 mL](https://www.usascientific.com/plateone-96-deep-well-2ml/p/PlateOne-96-Deep-Well-2mL)
- [Agilent 1 Well Reservoir 290 mL](https://www.agilent.com/store/en_US/Prod-201252-100/201252-100)
- [USA Scientific 12- well Reservoir](https://www.usascientific.com/12-channel-automation-reservoir/p/1061-8150)
- [MagMAXTM Viral/Pathogen II (MVP II) Nucleic Acid Isolation Kit](https://www.thermofisher.com/order/catalog/product/A48383#/A48383)
- [TaqPathTM COVID-19 Combo Kit](https://www.thermofisher.com/order/catalog/product/A47814#/A47814)
- [Thermo Scientific Adhesive PCR Plate Foils](https://www.thermofisher.com/order/catalog/product/A47814#/A47814)
- Additional Reagents:
    - Nuclease-free Water (not DEPC-Treated)
    - Ethanol, Absolute, Molecular Biology Grade

## Protocol
### OT-2 Preparation
Follow the Opentrons guidelines for setting up the OT-2 before executing any protocols.

### General Installation
Using any web browser, navigate to the [GitHub directory](https://github.com/DAMPLAB/OT2-SARS-CoV2) and follow the instructions provided in the **README.md** for the General Installation to install the necessary software setup.

### Prepare Fresh 80% Ethanol
Prepare fresh 80% Ethanol using Ethanol, Absolute, Molecular Biology Grade and Nuclease-free Water (not DEPC-Treated) for the required number of reactions, plus 10% overage.

### Prepare Binding Bead Mix
Before preparing binding bead mix, vortex the total nucleic acid magnetic beads to ensure that the bead mixture is homogeneous. For the number of required reactions, prepare the Binding Bead Mix according to the following ratio: 265 μL of Binding Solution with 10 μL of total nucleic acid magnetic beads, plus 10% overage. Mix well by inversion, then store at room temperature.    
**NOTE:** Prepare the required amount of Binding Bead Mix on each day of use.

### Prepare Reagents in the Proper Labware for RNA Extraction Protocol
Follow the instruction provided in the [TaqPath™ COVID-19 Combo Kit](https://www.fda.gov/media/136112/download) for preparing the necessary reagents. Refer to Figure 1B for the appropriate labware needed for protocol execution.    
**NOTE:** When prepare for reagents in the proper labware, be sure to account for 10% overage.

### Execute RNA Extraction Protocol on OT-2
1. Open up OT2 APP, and upload the *rna_extraction_magmax.py* under the Protocol the folder **rna_extraction_magmax**. [8 Minutes / Variable]
2. Once the protocol is uploaded, following the calibration instructions provided by the OT2 APP by placing the Temperature Module and an empty Bio-Rad 96 well plate (Output Plate), the Magnetic Module and a USA Scientific 96 deep well plate containing the samples (Reaction Plate), the Reagents Plate, the Reagent Trough, the Waste Reservoir, two Opentrons 20 µL Filter Tips, and four Opentrons 200 µL Filter Tips Racks onto the deck of the liquid handler. (Figure 1A and 1B). [5 Minutes / Variable]     
  **NOTE:** 200 µL tip reload will be necessary, protocol will pause in the proper places and must be resumed manually.       
3. Once the calibration process is completed, proceed to running the protocol. [2 Hours / Variable]     
  **NOTE:** Always allow the robotic liquid handler to complete the execution of a script before trying to access the deck space.    
  **NOTE:** All shaking and incubation steps are performed with benchtop Eppendorf ThermoMixer® C.  Protocol will pause in the proper places and must be resumed manually.    
4. The robotic liquid handler would automatically pause when the RNA extraction protocol is completed. Leave the output plate on the OT2 robot (Deck #8), and immediately proceed to the qPCR assay preparation protocol.    
  **NOTE:** Significant bead carry over may adversely impact RT-PCR performance.

<p align="center">
  <img src="https://user-images.githubusercontent.com/32885235/97507189-0910ad80-1953-11eb-8523-cfd40ce13af3.png" />

  **Figure 1:** Workflow for executing RNA extraction protocols on OT-2.     
  **(A)** Representative OT-2 deck layout with labwares and pipette tip boxes placement locations.     
  **(B)** Representative OT-2 deck layout for plate setup instructions
</p>

### Prepare Reagents in the Proper Labware for qPCR Assay Preparation Protocol
Follow the instruction provided in the [TaqPath™ COVID-19 Combo Kit](https://www.fda.gov/media/136112/download) for preparing the necessary reagents. Refer to Figure 2B for the appropriate labware needed for protocol execution.    
**NOTE:** When prepare for reagents in the proper labware, be sure to account for 10% overage.

### Execute qPCR Assay Preparation Protocol on OT-2
1. Open up OT2 APP, and upload the *qPCR_taqpath_multiplex.py* under the Protocol the folder **qPCR_taqpath_multiplex**. [2 Minutes / Variable]
2. Once the protocol is uploaded, following the calibration instructions provided by the OT2 APP by placing the Temperature Modules 1 and a Bio-Rad 96 well plate containing purified RNA extraction form the previous workflow (Reaction Plate), place the Temperature Modules 2 and a Bio-Rad 96 well plate containing TaqPath™ master mixes (Reagents Plate), and one Opentrons 200 µL Filter Tips Racks onto the deck of the liquid handler (Figure 2A and 2B). [2 Minutes / Variable]    
  **NOTE:** Pipette replacement might be necessary, please follow the instructions provided by OT2 App.
3. Once the calibration process is completed, proceed to running the protocol. [5 Minutes / Variable]    
  **NOTE:** Always allow the robotic liquid handler to complete the execution of a script before trying to access the deck space.
4. The robotic liquid handler would automatically pause when the qPCR assay preparation protocol is completed. Seal and store the RNA Plate from the previous protocol.

<p align="center">
  <img src="https://user-images.githubusercontent.com/32885235/97507580-d915da00-1953-11eb-88fe-4cc303e58564.png" />

  **Figure 2:** Workflow for executing qPCR assay preparation protocols on OT-2.     
  **(A)** Representative OT-2 deck layout with labwares and pipette tip boxes placement locations.     
  **(B)** Representative OT-2 deck layout for plate setup instructions
</p>

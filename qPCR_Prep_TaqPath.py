# qPCR Assay Setup Protocol
# Written By Rita Chen 2020-05-21

# Before starting the protocol, do following manual steps for prepare the RT‑PCR reactions:
# Use this procedure if you extracted sample RNA using an original sample input volume of 200 μL.
# 1. If frozen, thaw the reagents on ice.
# 2. Gently vortex the samples and reagents, then centrifuge briefly to collect liquid at the bottom of the 96-well\
# plate.
# 3. Dilute TaqPath™ COVID‑19 Control (1 × 104 copies/μL) to a working stock of 25 copies/μL:
# a. Pipette 98 μL of TaqPath™ COVID‑19 Control Dilution Buffer into a microcentrifuge tube, then add 2 μL of diluted\
# TaqPath™ COVID‑19 Control. Mix well, then centrifuge briefly.
# b. Pipet 87.5 μL of TaqPath™ COVID‑19 Control Dilution Buffer into a second microcentrifuge tube, then add 12.5 μL of\
# the dilution created in substep 3a. Mix well, then centrifuge briefly.
# Note: The TaqPath™ COVID‑19 Control does not contain the MS2 template.
# 4. Prepare the Reaction Mix:
# a. For each run, combine the following components sufficient for the number of tests plus one Positive Control and\
# one  Negative Control.
# All volumes include 10% overage for pipette error.
# IMPORTANT! The volumes in this table assume that you extracted sample RNA using an original sample input volume of\
# 200 μL.
# 5. Set up the reaction plate:
# 6. Seal the plate with MicroAmp™ Optical Adhesive Film, vortex the plate for 10 seconds to ensure proper mixing,\
# then centrifuge for 1 minute at 2000 rpm to collect the liquid at the bottom of the reaction plate.

from opentrons import labware, instruments, modules, robot

# Load hardware module and labwares
temp_deck_1 = modules.load('tempdeck', '7')
temp_deck_2 = modules.load('tempdeck', '8')
reaction_plate = labware.load('biorad-hardshell-96-PCR','8', 'Reaction Plate', share=True) #250uL/well
reagent_plate = labware.load('biorad-hardshell-96-PCR', '7', 'Reagnet Plate', share=True) #250uL/well
reagent_mix = reagent_plate.cols(0) # 15uL per sample, 198uL in the well


# Load in 3 of 20ul filter tiprack 
tr_20 = [labware.load('opentrons_96_filtertiprack_20ul', '9'),\
labware.load('opentrons_96_filtertiprack_20ul', '10'), labware.load('opentrons_96_filtertiprack_20ul', '11')]

# Load in pipettes
pipette = instruments.p20_multi_gen2(mount='left', tip_racks=tr_20)

num_cols = 12 # Number of columns
rnx_vol = 15 # Reaction volume

# qPCR Assay Preparation stats here____________________________________________________________________________________
temp_deck_1.set_temperature(4)
temp_deck_2.set_temperature(4)

# Transfer 15ul of reagent mix (reagent plate) to the pre-prepared reaction plate
for i in range(num_cols):
	pipette.pick_up_tip()
	pipette.mix(5, rnx_vol, reagent_mix.bottom(2.00))
	pipette.transfer(rnx_vol, reagent_mix.bottom(2.00), reaction_plate.cols(i), new_tip='never')
	pipette.mix(5, rnx_vol, reaction_plate.cols(i).bottom(2.00))
	pipette.blow_out()
    pipette.drop_tip()


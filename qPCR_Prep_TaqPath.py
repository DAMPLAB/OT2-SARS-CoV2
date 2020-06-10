# qPCR Assay Setup Protocol
# Written By Rita Chen 2020-05-21
# Updated by Dany Fu 2020-06-10

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

from opentrons import protocol_api
metadata = {'apiLevel': '2.2',
            'protocolName': 'RNA Extraction (MagMAX)',
            'author': 'Rita Chen, Dany Fu',
            'description': '''Distributes master mix to 96 well plate'''}

TEMP_DECK = {
    'NAME': 'Temperature Module',
    'SLOT': 7
}
P200_MULTI = {
    'NAME': 'p300_multi',
    'POSITION': 'left'
}
FILTER_TIP_20 = [{
    'NAME': 'opentrons_96_filtertiprack_200ul',
    'SLOT': 1,
    'LABEL': 'Filter Tip S-1'
}]

ASPIRATE_DEPTH_BOTTOM = 2.00 #2mm from bottle
VOL_MASTER_MIX = 15 # Reaction volume
TEMP = 4
VOL_MIX_SM = 10

def run(protocol: protocol_api.ProtocolContext):
	temp_deck = protocol.load_module(TEMP_DECK['NAME'], location=TEMP_DECK['SLOT'])
	reaction_plate = temp_deck.load_labware('biorad_96_wellplate_200ul_pcr',
											label='Reaction Plate')
	reagent_plate = protocol.load_labware('biorad_96_wellplate_200ul_pcr',
                                          location=4,
										  label='Reagent Plate')
	reagent_mix = reagent_plate.columns()[0]
	tip_20 = [protocol.load_labware(i['NAME'], location=i['SLOT'], label=i['LABEL'])
              for i in FILTER_TIP_20]
	p200 = protocol.load_instrument(P200_MULTI['NAME'], P200_MULTI['POSITION'],
								    tip_racks=tip_20)
	p200.well_bottom_clearance.aspirate = ASPIRATE_DEPTH_BOTTOM
	p200.well_bottom_clearance.dispense = ASPIRATE_DEPTH_BOTTOM

	num_cols = len(reaction_plate.columns())

	temp_deck.set_temperature(celsius=TEMP)
	add_master_mix(num_cols=num_cols, pipette=p200,
				   source=reagent_mix, dest=reaction_plate.columns())

def add_master_mix(num_cols=1, pipette=None, source=None, dest=[]):
	# Transfer 15ul of reagent mix (reagent plate) to the pre-prepared reaction plate
	for c in range(num_cols):
		pipette.pick_up_tip()
		pipette.mix(repetitions=5, volume=VOL_MIX_SM, location=source[0])
		pipette.aspirate(volume=VOL_MASTER_MIX, location=source[0])
		pipette.dispense(volume=VOL_MASTER_MIX, location=dest[c][0])
		pipette.mix(repetitions=5, volume=VOL_MIX_SM)
		pipette.blow_out()
		pipette.blow_out()
		pipette.blow_out()
		pipette.drop_tip()

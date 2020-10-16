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

import math
from opentrons import protocol_api
metadata = {'apiLevel': '2.2',
            'protocolName': 'qPCR Prep (MagMAX)',
            'author': 'Rita Chen, Dany Fu',
            'description': 'Aliquot RNA eluent and distribute master mix to 96 well plate'}

TEMP_DECK = {
    'NAME': 'Temperature Module',
    'SLOT': 7
}
QPCR_PLATE = {#200uL per well, 96 wells
    'NAME': 'biorad_96_wellplate_200ul_pcr',
    'LABEL': 'Output Plate', #no slot, sits on temp deck
}
RNA_PLATE = { #200uL per well, 96 wells
    'NAME': 'biorad_96_wellplate_200ul_pcr',
    'LABEL': 'RNA Plate',
    'SLOT': 8
}
REAGENT_PLATE = {
    'NAME': 'biorad_96_wellplate_200ul_pcr',
    'SLOT': 4,
    'LABEL': 'Reagent Plate'
}
P10_MULTI = {
    'NAME': 'p20_multi_gen2',
    'POSITION': 'right'
}
FILTER_TIP_20 = [{
    'NAME': 'opentrons_96_filtertiprack_20ul',
    'SLOT': 1,
    'LABEL': 'Filter Tip S-1'
},
{
    'NAME': 'opentrons_96_filtertiprack_20ul',
    'SLOT': 2,
    'LABEL': 'Filter Tip S-2'
}]

ASPIRATE_DEPTH_BOTTOM = 2.00 #2mm from bottle
VOL_RNA = 10
VOL_MASTER_MIX = 15 # Reaction volume
TEMP = 4
TOUCH_SPEED = 20.0
TOUCH_RADIUS_SM_SM = 1.20
TOUCH_HEIGHT_SM_SM = -2.0

def run(protocol: protocol_api.ProtocolContext):
    temp_deck = protocol.load_module(TEMP_DECK['NAME'], location=TEMP_DECK['SLOT'])
    qPCR_plate = temp_deck.load_labware(QPCR_PLATE['NAME'],
                                       label=QPCR_PLATE['LABEL'])
    rna_plate = protocol.load_labware(RNA_PLATE['NAME'],
                                      location=RNA_PLATE['SLOT'],
                                      label=RNA_PLATE['LABEL'])
    reagent_plate = protocol.load_labware(REAGENT_PLATE['NAME'],
                                          location=REAGENT_PLATE['SLOT'],
                                          label=REAGENT_PLATE['LABEL'])
    mastermix = reagent_plate.columns()[0]
    tip_20 = [protocol.load_labware(i['NAME'], location=i['SLOT'], label=i['LABEL'])
              for i in FILTER_TIP_20]
    p20 = protocol.load_instrument(P10_MULTI['NAME'], P10_MULTI['POSITION'],
								    tip_racks=tip_20)
    p20.well_bottom_clearance.aspirate = ASPIRATE_DEPTH_BOTTOM
    p20.well_bottom_clearance.dispense = ASPIRATE_DEPTH_BOTTOM

    num_cols = len(qPCR_plate.columns())

    temp_deck.set_temperature(celsius=TEMP)
    aliquot_eluent(num_cols=num_cols, pipette=p20,
                   source=rna_plate.columns(), dest=qPCR_plate.columns())
    add_master_mix(num_cols=num_cols, pipette=p20,
                   source=mastermix, dest=qPCR_plate.columns())

def aliquot_eluent(num_cols=1, pipette=None, source=None, dest=[]):
    for c in range(num_cols):
        transfer(vol=VOL_RNA, pipette=pipette,
                 source=source[c], dest=dest[c])

def add_master_mix(num_cols=1, pipette=None, source=None, dest=[]):
    # Transfer 15ul of reagent mix (reagent plate) to the pre-prepared reaction plate
    for c in range(num_cols):
        transfer(vol=VOL_MASTER_MIX, pipette=pipette,
                 source=source, dest=dest[c],
                 mix_before=(5, VOL_MASTER_MIX), mix_after=(5, VOL_MASTER_MIX),
                 touch_tip=(TOUCH_RADIUS_SM_SM, TOUCH_HEIGHT_SM_SM))

# Custom transfer function; when the volume needed
# exceeds the pipette's max volume this function will
# prioritize tip reuse by pipetting to the top of the
# wells until the last dispensation
def transfer(vol=0, pipette=None, source=[], dest=[],
             mix_before=None, mix_after=None,
             touch_tip=None, delay_time_s=None):
    n = math.ceil(vol / pipette.hw_pipette['working_volume'])
    vol_ar = [vol // n + (1 if x < vol % n else 0) for x in range(n)]
    pipette.pick_up_tip()

    # dispense to the top of the well so we can reuse the tips
    for v in vol_ar[:-1]:
        if mix_before:
            if len(mix_before) == 1:
                pipette.mix(repetitions=mix_before[0],
                            volume=v,
                            location=source[0])
            if len(mix_before) == 2:
                pipette.mix(repetitions=mix_before[0],
                            volume=mix_before[1],
                            location=source[0])
        pipette.aspirate(volume=v, location=source[0])
        if(delay_time_s):
            pipette.air_gap(volume=0)
            protocol.delay(seconds=delay_time_s)
        pipette.dispense(volume=v, location=dest[0].top())
        pipette.blow_out(location=dest[0])
        if touch_tip:
            pipette.touch_tip(radius=touch_tip[0],
                              v_offset=touch_tip[1],
                              speed=TOUCH_SPEED)

    # the final transfer
    if mix_before:
        if len(mix_before) == 1:
            pipette.mix(repetitions=mix_before[0],
                        volume=vol_ar[-1],
                        location=source[0])
        if len(mix_before) == 2:
            pipette.mix(repetitions=mix_before[0],
                        volume=mix_before[1],
                        location=source[0])
    pipette.aspirate(volume=vol_ar[-1], location=source[0])
    if(delay_time_s):
        pipette.air_gap(volume=0)
        protocol.delay(seconds=delay_time_s)
    pipette.dispense(volume=vol_ar[-1], location=dest[0])
    if mix_after:
        if len(mix_after) == 1:
            pipette.mix(repetitions=mix_after[0], volume=vol_ar[-1])
        if len(mix_after) == 2:
            pipette.mix(repetitions=mix_after[0], volume=mix_after[1])

    pipette.blow_out(location=dest[0])
    if touch_tip:
        pipette.touch_tip(radius=touch_tip[0],
                          v_offset=touch_tip[1],
                          speed=TOUCH_SPEED)
    pipette.drop_tip()

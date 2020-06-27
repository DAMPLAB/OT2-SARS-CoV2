# RNA Extraction Protocol
# Written By Rita Chen 2020-05-21
# Updated by Dany Fu 2020-05-25

# Before starting the protocol, do following manual steps for prepare binding bead mix:
# Prepare the required amount of Binding Bead Mix on each day of use.
# 1. Vortex the Total Nucleic Acid Magnetic Beads to ensure that the bead mixture is homogeneous.
# 2. For the number of required reactions, prepare the Binding Bead Mix according to the following ratio:
  # 265 μL of Binding Solution with 10 μL of Total Nucleic Acid Magnetic Beads
# Include 10% overage when making the Binding Bead Mix for use with multiple reactions.
# 3. Mix well by inversion, then store at room temperature.
import os
import sys
sys.path.append(os.getcwd())
from rna_constants import *
import math
from opentrons import protocol_api

metadata = {'apiLevel': '2.2',
            'protocolName': 'RNA Extraction (MagMAX)',
            'author': 'Rita Chen, Dany Fu',
            'description': '''Extract RNA using the MagMAXTM Viral/Pathogen II
                            Nucleic Acid Isolation Kit and 200μL sample input
                            volume'''}

def run(protocol: protocol_api.ProtocolContext):
    temp_deck = protocol.load_module(TEMP_DECK['NAME'],
                                     location=TEMP_DECK['SLOT'])
    # The output plate needs to be kept cold on the temp deck
    output_plate = temp_deck.load_labware(OUTPUT_PLATE['NAME'],
                                          label=OUTPUT_PLATE['LABEL'])

    mag_deck = protocol.load_module(MAG_DECK['NAME'],
                                    location=MAG_DECK['SLOT'])
    # The reaction plate is loaded on top of the magnetic module
    reaction_plate = mag_deck.load_labware(REACTION_PLATE['NAME'],
                                           label=REACTION_PLATE['LABEL'])

    reagent_plate = protocol.load_labware(REAGENT_PLATE['NAME'],
                                          location=REAGENT_PLATE['SLOT'],
                                          label=REAGENT_PLATE['LABEL'])

    reagent_reservior = protocol.load_labware(REAGENT_RESERVOIR['NAME'],
                                              location=REAGENT_RESERVOIR['SLOT'],
                                              label=REAGENT_RESERVOIR['LABEL'])

    waste_reservior = protocol.load_labware(WASTE_RESERVOIR['NAME'],
                                            location=WASTE_RESERVOIR['SLOT'],
                                            label=WASTE_RESERVOIR['LABEL'])

    # Load in 2 of 10ul filter tiprack
    tip_10 = [protocol.load_labware(i['NAME'], location=i['SLOT'], label=i['LABEL'])
              for i in FILTER_TIP_10]
    p10 = protocol.load_instrument(P10_MULTI['NAME'], P10_MULTI['POSITION'],
                                   tip_racks=tip_10)
    p10.well_bottom_clearance.aspirate = DEPTH_BOTTOM_MID
    p10.well_bottom_clearance.dispense = DEPTH_BOTTOM_MID

    # Load in 4 of 300ul filter tiprack
    tip_300 = [protocol.load_labware(i['NAME'], location=i['SLOT'], label=i['LABEL'])
               for i in FILTER_TIP_300]
    p300 = protocol.load_instrument(P300_MULTI['NAME'], P300_MULTI['POSITION'],
                                    tip_racks=tip_300)
    p300.well_bottom_clearance.aspirate = DEPTH_BOTTOM_MID
    p300.well_bottom_clearance.dispense = DEPTH_BOTTOM_MID

    reagent_map = make_reagent_map(reagent_plate, reagent_reservior)
    num_cols = len(reaction_plate.columns())

    """
    LYSE SAMPLE
    """
    # 1. Mix and add 5 μL of Proteinase K to each well of reaction plate
    # that already contains 200 μL of sample
    add_proteinase_k(num_cols=num_cols, pipette=p10,
                     source=reagent_map[PROTEINASE_K][0]['WELL'],
                     dest=reaction_plate.columns())

    # 2. Mix and add 275 μL of bead solution to each well
    add_beads(num_cols=num_cols, pipette=p300,
              source=reagent_map[BEADS],
              dest=reaction_plate.columns())

    # 3. Add 5 μL of MS2 Phage Control to each well
    add_ms2(num_cols=num_cols, pipette=p10,
            source=reagent_map[MS2][0]['WELL'],
            dest=reaction_plate.columns())

    # 4. Seal the plate then shake at 1,050 rpm for 2 minutes.
    # 5. Incubate at 65°C for 5 minutes, shake at 1,050 rpm for 5 minutes.
    # Step 4-5 happens outside of OT2
    protocol.pause()

    # 6. Place the sealed plate on the magnetic stand for 10 minutes or until all of the beads have collected.
    mag_deck.engage(height=MAG_DECK_HEIGHT) # Raise the Magnetic Module’s magnets.
    protocol.delay(minutes=10)

    """
    WASH BEADS
    """
    # 1. Keeping the plate on the magnet, discard the supernatant from each well.
    # IMPORTANT! Avoid disturbing the beads.
    discard_supernatant(num_cols=num_cols, pipette=p300,
                        source=reaction_plate.columns(),
                        dest=waste_reservior.columns(),
                        vol=VOL_WASTE)
    # Steps 2-7
    wash_beads(protocol, source=reagent_map[WASH_BUFFER], vol=VOL_500)

    # add more 300uL tips
    protocol.pause()
    for t in tip_300:
        t.reset()

    wash_beads(protocol, source=reagent_map[ETHANOL1], vol=VOL_500)
    wash_beads(protocol, source=reagent_map[ETHANOL2], vol=VOL_250)

    # 8. Dry the beads by shaking the plate (uncovered) at 1,050 rpm for 2 minutes
    # Happens outside of OT2
    protocol.pause()

    # add more 300uL tips
    for t in tip_300:
        t.reset()

    """
    Elute the nucleic acid
    """
    temp_deck.set_temperature(celsius=TEMP)
    # 1. Add 50 μL of Elution Solution to each sample, then seal the plate
    elute(num_cols=num_cols, pipette=p300,
          source=reagent_map[ELUTION][0],
          dest=reaction_plate.columns())
    # 2. Shake at 1,050 rpm for 5 minutes.
    # 3. Incubate at 65°C for 10 minutes.
    # 4. Shake at 1,050 rpm for 5 minutes.
    # Step 2-4 happen outside of OT-2.
    protocol.pause()

    # 5. Place the sealed plate on the magnetic stand for 3 minutes or until clear to collect the beads against the magnets.
    mag_deck.engage(height=MAG_DECK_HEIGHT)
    protocol.delay(minutes=3)

    # 6. Keeping the plate on the magnet, transfer the eluates to a fresh standard
    # (not deep-well) plate, then seal the plate with MicroAmp™ Clear Adhesive Film.
    # IMPORTANT! To prevent evaporation, seal the plate containing the eluate immediately after the transfers are complete.
    # Note: Significant bead carry over may adversely impact RT-PCR performance. Place the plate on ice for immediate use\
    # in real-time RT‑PCR.
    make_qPCR_plate(num_cols=num_cols, pipette=p300,
                    source=reaction_plate.columns(),
                    dest=output_plate.columns())


def make_reagent_map(reagent_plate, reagent_reservior):
    return {
        PROTEINASE_K: [ # 5uL per sample, 528uL in the well
            {'VOL': 528, 'WELL': reagent_plate.columns()[0]}
        ],
        MS2: [ # 5uL per sample, 52uL in the well
            {'VOL': 528, 'WELL': reagent_plate.columns()[1]}
        ],
        ELUTION: [ # 50uL per sample, 5.28mL in the well
            {'VOL': 5280, 'WELL': reagent_reservior.columns()[10]}
        ],
        BEADS: [ # 275uL per sample, 14.52mL in the well
            {'VOL': 14520, 'WELL': reagent_reservior.columns()[0]},
            {'VOL': 14520, 'WELL': reagent_reservior.columns()[1]}
        ],
        WASH_BUFFER: [ # 500uL per sample, 17.6mL in the well
            {'VOL': 17600, 'WELL': reagent_reservior.columns()[2]},
            {'VOL': 17600, 'WELL': reagent_reservior.columns()[3]},
            {'VOL': 17600, 'WELL': reagent_reservior.columns()[4]}
        ],
        ETHANOL1: [
            {'VOL': 17600, 'WELL': reagent_reservior.columns()[5]},
            {'VOL': 17600, 'WELL': reagent_reservior.columns()[6]},
            {'VOL': 17600, 'WELL': reagent_reservior.columns()[7]},
        ],
        ETHANOL2: [
            {'VOL': 13200, 'WELL': reagent_reservior.columns()[8]},
            {'VOL': 13200, 'WELL': reagent_reservior.columns()[9]}
        ]
    }

# Custom transfer function for when the volume needed
# exceeds the pipette's max volume. This function will
# prioritize tip reuse by pipetting to the top of the
# wells until the last dispensation
def transfer(vol=0, pipette=None, source=[], dest=[],
             mix_before=None, mix_after=None,
             touch_tip=None):
    # https://github.com/Opentrons/opentrons/issues/5815#issuecomment-644849879
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

def reagent_low(q_remain=0, q_transfer=0):
    return True if q_remain < q_transfer else False

def add_proteinase_k(num_cols=1, pipette=None, source=None, dest=[]):
    for c in range(num_cols):
        pipette.pick_up_tip()
        pipette.mix(repetitions=2, volume=VOL_10, location=source[0])
        pipette.aspirate(volume=VOL_PK, location=source[0])
        pipette.dispense(volume=VOL_PK, location=dest[c][0])
        pipette.blow_out(location=dest[c][0])
        pipette.touch_tip(radius=TOUCH_RADIUS_SM_LG,
                          v_offset=TOUCH_HEIGHT_SM_LG,
                          speed=TOUCH_SPEED)
        pipette.drop_tip()

def add_beads(num_cols=1, pipette=None, source=[], dest=[]):
    s = 0
    reagent_vol = source[s]['VOL']
    for c in range(num_cols):
        vol_transfer = VOL_BEAD * pipette.channels
        if reagent_low(q_remain=reagent_vol, q_transfer=vol_transfer):
            s += 1
            reagent_vol = source[s]['VOL']

        transfer(vol=VOL_BEAD, pipette=pipette,
                 source=source[s]['WELL'], dest=dest[c],
                 mix_before=(5,), mix_after=(2,),
                 touch_tip=(TOUCH_RADIUS_LG_LG, TOUCH_HEIGHT_LG_LG))

        reagent_vol -= vol_transfer

def add_ms2(num_cols=1, pipette=None, source=None, dest=[]):
    for c in range(num_cols):
        pipette.pick_up_tip()
        pipette.mix(repetitions=2, volume=VOL_10, location=source[0])
        pipette.aspirate(volume=VOL_MS2, location=source[0])
        pipette.dispense(volume=VOL_MS2, location=dest[c][0])
        pipette.mix(repetitions=3, volume=VOL_10)
        pipette.blow_out(location=dest[c][0])
        pipette.touch_tip(radius=TOUCH_RADIUS_SM_LG,
                          v_offset=TOUCH_HEIGHT_SM_LG,
                          speed=TOUCH_SPEED)
        pipette.drop_tip()

def discard_supernatant(num_cols=1, pipette=None, source=[], dest=[], vol=0):
    pipette.well_bottom_clearance.aspirate = DEPTH_BOTTOM_LOW
    for c in range(num_cols):
        transfer(vol=vol, pipette=pipette,
                 source=source[c], dest=dest[0])
    pipette.well_bottom_clearance.aspirate = DEPTH_BOTTOM_MID

def wash_beads(protocol, source=None, vol=0):
    mag_deck = protocol.loaded_modules[MAG_DECK['SLOT']]
    p300 = protocol.loaded_instruments[P300_MULTI['POSITION']]
    reaction_plate = protocol.loaded_labwares[MAG_DECK['SLOT']]
    waste_reservior = protocol.loaded_labwares[WASTE_RESERVOIR['SLOT']]
    num_cols = len(reaction_plate.columns())

    # 2. Remove the plate from the magnetic stand
    mag_deck.disengage()

    wash(num_cols=num_cols, pipette=p300,
         source=source, dest=reaction_plate.columns(),
         vol=vol)

    # 3. Reseal the plate, then shake at 1,050 rpm for 1 minute.
    # Step 3 happen outside of OT-2.
    protocol.pause()

    # 4. Place the plate back on the magnetic stand for 2 minutes, or until all the beads have collected.
    mag_deck.engage(height=MAG_DECK_HEIGHT)
    protocol.delay(minutes=2)

    # 5. Keeping the plate on the magnet, discard the supernatant from each well.
    # IMPORTANT! Avoid disturbing the beads.
    discard_supernatant(num_cols=num_cols, pipette=p300,
                        source=reaction_plate.columns(),
                        dest=waste_reservior.columns(),
                        vol=vol)

def wash(num_cols=0, pipette=None, source=None, dest=None, vol=0):
    s = 0
    reagent_vol = source[s]['VOL']
    for c in range(num_cols):
        vol_transfer = vol * pipette.channels
        if reagent_low(q_remain=reagent_vol, q_transfer=vol_transfer):
            s += 1
            reagent_vol = source[s]['VOL']

        transfer(vol=vol, pipette=pipette,
                 source=source[s]['WELL'], dest=dest[c],
                 mix_before=(3,), mix_after=(5,),
                 touch_tip=(TOUCH_RADIUS_LG_LG, TOUCH_HEIGHT_LG_LG))
        reagent_vol -= vol_transfer

def elute(num_cols=1, pipette=None, source=None, dest=[]):
    pipette.well_bottom_clearance.dispense = DEPTH_BOTTOM_LOW
    for c in range(num_cols):
        transfer(vol=VOL_ELUTE, pipette=pipette,
                 source=source['WELL'], dest=dest[c],
                 mix_before=(3, 175), mix_after=(5, 35),
                 touch_tip=(TOUCH_RADIUS_LG_LG, TOUCH_HEIGHT_LG_LG))
    pipette.well_bottom_clearance.aspirate = DEPTH_BOTTOM_MID

def make_qPCR_plate(num_cols=1, pipette=None, source=[], dest=[]):
    for c in range(num_cols):
        transfer(vol=VOL_ELUTE, pipette=pipette,
                 source=source[c], dest=dest[c],
                 touch_tip=(TOUCH_RADIUS_LG_SM, TOUCH_HEIGHT_LG_SM))

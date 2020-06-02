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
from constants import *
from opentrons import protocol_api

metadata = {'apiLevel': '2.0',
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

    # Load in 2 of 20ul filter tiprack
    tip_20 = [protocol.load_labware(i['NAME'], location=i['SLOT'], label=i['LABEL'])
              for i in FILTER_TIP_20]
    p20 = protocol.load_instrument(P20_MULTI['NAME'], P20_MULTI['POSITION'],
                                   tip_racks=tip_20)
    p20.well_bottom_clearance.aspirate = ASPIRATE_DEPTH_BOTTOM
    p20.well_bottom_clearance.dispense = ASPIRATE_DEPTH_BOTTOM

    # Load in 4 of 30ul filter tiprack
    tip_200 = [protocol.load_labware(i['NAME'], location=i['SLOT'], label=i['LABEL'])
               for i in FILTER_TIP_200]
    p200 = protocol.load_instrument(P200_MULTI['NAME'], P200_MULTI['POSITION'],
                                    tip_racks=tip_200)
    p200.well_bottom_clearance.aspirate = ASPIRATE_DEPTH_BOTTOM
    p200.well_bottom_clearance.dispense = ASPIRATE_DEPTH_BOTTOM

    reagent_map = make_reagent_map(reagent_plate, reagent_reservior)
    num_cols = len(reaction_plate.columns())

    """
    LYSE SAMPLE
    """
    # 1. Mix and add 5 μL of Proteinase K to each well of reaction plate
    # that already contains 200 μL of sample
    add_proteinase_k(num_cols=num_cols, pipette=p20,
                     source=reagent_map[PROTEINASE_K][0],
                     dest=reaction_plate.columns())

    # 2. Mix and add 275 μL of bead solution to each well
    add_beads(num_cols=num_cols, pipette=p200,
              source=reagent_map[BEADS],
              dest=reaction_plate.columns())

    # 3. Add 5 μL of MS2 Phage Control to each well
    add_ms2(num_cols=num_cols, pipette=p20,
            source=reagent_map[MS2][0],
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
    discard_supernant(num_cols=num_cols, pipette=p200,
                      source=reaction_plate.columns(),
                      dest=waste_reservior.columns())
    # Steps 2-7
    wash_beads(protocol, source=reagent_map[WASH_BUFFER], vol=VOL_500)
    wash_beads(protocol, source=reagent_map[ETHANOL], vol=VOL_500)
    wash_beads(protocol, source=reagent_map[ETHANOL], vol=VOL_250)

    # 8. Dry the beads by shaking the plate (uncovered) at 1,050 rpm for 2 minutes
    # Happens outside of OT2
    protocol.pause()

    """
    Elute the nucleic acid
    """
    temp_deck.set_temperature(TEMP)
    # 1. Add 50 μL of Elution Solution to each sample, then seal the plate
    elute(num_cols=num_cols, pipette=p20,
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
    make_qPCR_plate(num_cols=num_cols, pipette=p200,
                    source=reaction_plate.columns(),
                    dest=output_plate.columns())


def make_reagent_map(reagent_plate, reagent_reservior):
    return {
        PROTEINASE_K: [reagent_plate.columns()[0]], # 5uL per sample, 528uL in the well
        MS2: [reagent_plate.columns()[1]], # 5uL per sample, 52uL in the well
        ELUTION: [reagent_reservior.columns()[10]], # 50uL per sample, 5.28mL in the well
        BEADS: [ # 275uL per sample, 14.52mL in the well
            reagent_reservior.columns()[0],
            reagent_reservior.columns()[1]
        ],
        WASH_BUFFER: [ # 500uL per sample, 17.6mL in the well
            reagent_reservior.columns()[2],
            reagent_reservior.columns()[3],
            reagent_reservior.columns()[4]
        ],
        ETHANOL: [
            reagent_reservior.columns()[5], # 500uL per sample, 17.6mL in the well
            reagent_reservior.columns()[6], # 500uL per sample, 17.6mL in the well
            reagent_reservior.columns()[7], # 500uL per sample, 17.6mL in the well
            reagent_reservior.columns()[8], # 250uL per sample, 13.2mL in the well
            reagent_reservior.columns()[9] # 250uL per sample, 13.2mL in the well
        ]

    }

def add_proteinase_k(num_cols=1, pipette=None, source=None, dest=None):
    for c in range(num_cols):
        #pipette.pick_up_tip()
        pipette.transfer(VOL_5, source, dest[c],
                         #new_tip='never',
                         mix_before=(5, VOL_15),
                         blow_out=True)

def add_beads(num_cols=1, pipette=None, source=None, dest=None):
    s = 0
    for c in range(num_cols):
        # pipette.pick_up_tip()
        # pipette.mix(repetitions=8, volume=VOL_250,
        #             location=source[s].bottom(ASPIRATE_DEPTH_BOTTOM))
        pipette.transfer(VOL_BEAD, source[s], dest[c],
                         #new_tip='never',
                         mix_before=(8, pipette.max_volume), # repeat 8x
                         mix_after=(3, pipette.max_volume), # repeat 3x
                         blow_out=True)
        # pipette.mix(repetitions=3, volume=VOL_250,
        #             location=dest[c].bottom(ASPIRATE_DEPTH_BOTTOM))
        # pipette.blow_out()
        # pipette.drop_tip()
        if c == 5:
            s += 1

def add_ms2(num_cols=1, pipette=None, source=None, dest=None):
    for c in range(num_cols):
        # pipette.pick_up_tip()
        # pipette.mix(repetitions=5, volume=VOL_15,
        #             location=source.bottom(ASPIRATE_DEPTH_BOTTOM))
        pipette.transfer(VOL_5, source, dest[c],
                         #new_tip='never',
                         mix_before=(5, VOL_15), # repeat 5x
                         mix_after=(8, VOL_15), # repeat 8x
                         blow_out=True)
        # pipette.mix(repetitions=8, volume=VOL_15,
        #             location=source.bottom(ASPIRATE_DEPTH_BOTTOM))
        # pipette.blow_out()
        # pipette.drop_tip()

def discard_supernant(num_cols=1, pipette=None, source=None, dest=None):
    for c in range(num_cols):
        pipette.pick_up_tip()
        pipette.transfer(VOL_WASTE, source[c], dest[0][0].top,
                         new_tip='never',
                         blow_out=True)
        pipette.transfer(VOL_WASTE, source[c], dest[0][0],
                         new_tip='never')
        pipette.drop_tip()

def wash_beads(protocol, source=None, vol=0):
    mag_deck = protocol.loaded_modules[MAG_DECK['NAME']]
    p200 = protocol.loaded_instrument[P200_MULTI['NAME']]
    reaction_plate = protocol.loaded_labwares[MAG_DECK['SLOT']]
    waste_reservior = protocol.loaded_labwares[WASTE_RESERVOIR['SLOT']]
    num_cols = len(reaction_plate.columns())

    # 2. Remove the plate from the magnetic stand
    mag_deck.disengage()

    wash(vol=vol, pipette=p200, source=source, dest=reaction_plate.columns())

    # 3. Reseal the plate, then shake at 1,050 rpm for 1 minute.
    # Step 3 happen outside of OT-2.
    protocol.pause()

    # 4. Place the plate back on the magnetic stand for 2 minutes, or until all the beads have collected.
    mag_deck.engage(height=MAG_DECK_HEIGHT)
    protocol.delay(minutes=2)

    # 5. Keeping the plate on the magnet, discard the supernatant from each well.
    # IMPORTANT! Avoid disturbing the beads.
    discard_supernant(num_cols=num_cols, pipette=p200,
                      source=reaction_plate.columns(),
                      dest=waste_reservior.columns())

def wash(vol=0, pipette=None, source=None, dest=None):
    if vol == VOL_500:
        wash_500(num_cols=len(dest), pipette=pipette, source=source, dest=dest)
    if vol == VOL_250:
        wash_250(num_cols=len(dest), pipette=pipette, source=source, dest=dest)

def wash_500(num_cols=1, pipette=None, source=None, dest=None):
    s = 0
    for c in range(num_cols):
        pipette.pick_up_tip()
        # pipette.mix(repetitions=3, volume=VOL_250,
        #             location=source[s].bottom(ASPIRATE_DEPTH_BOTTOM))

        # dispense to the top of the well so we can reuse the tips
        pipette.transfer(VOL_250, source[s], dest[c][0].top,
                         new_tip='never',
                         mix_before=(3, pipette.max_volume),)

        pipette.transfer(VOL_250, source[s], dest[c],
                         new_tip='never',
                         mix_after=(5, pipette.max_volume),
                         blow_out=True)
        # pipette.mix(repetitions=5, volume=VOL_250,
        #             location=dest[c].bottom(ASPIRATE_DEPTH_BOTTOM))
        # pipette.blow_out()
        pipette.drop_tip()
        if c == 3 or c == 7:
            s += 1

def wash_250(num_cols=1, pipette=None, source=None, dest=None):
    s = 3
    for c in range(num_cols):
        pipette.pick_up_tip()
        # pipette.mix(repetitions=3, volume=VOL_250,
        #             location=source[s].bottom(ASPIRATE_DEPTH_BOTTOM))
        pipette.transfer(VOL_250, source[s], dest[c],
                         mix_before=(3, pipette.max_volume), # repeat 3x
                         mix_after=(5, pipette.max_volume), # repeat 5x
                         blow_out=True)
        # pipette.mix(repetitions=5, volume=VOL_250,
        #             location=dest[c].bottom(ASPIRATE_DEPTH_BOTTOM))
        # pipette.blow_out()
        # pipette.drop_tip()
        if c == 5:
            s += 1

def elute(num_cols=1, pipette=None, source=None, dest=None):
    for c in range(num_cols):
        pipette.pick_up_tip()
        # pipette.mix(repetitions=3, volume=VOL_250,
        #             location=source.bottom(ASPIRATE_DEPTH_BOTTOM))
        pipette.transfer(VOL_ELUTE, source, dest[c],
                         mix_before=(3, pipette.max_volume), # repeat 3x
                         mix_after=(5, 35), # repeat 5x
                         blow_out=True)
        # pipette.mix(repetitions=5, volume=35,
        #             location=dest.bottom(ASPIRATE_DEPTH_BOTTOM))
        # pipette.blow_out()
        # pipette.drop_tip()

def make_qPCR_plate(num_cols=1, pipette=None, source=None, dest=None):
    for c in range(num_cols):
        pipette.pick_up_tip()
        pipette.transfer(VOL_ELUTE, source[c], dest[c],
                         blow_out=True)
        # pipette.blow_out()
        # pipette.drop_tip()

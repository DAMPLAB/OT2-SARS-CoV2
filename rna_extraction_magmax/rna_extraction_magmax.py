"""
--------------------------------------------------------------------------------
Description: RNA Extraction Protocol

General Instructions:
Before starting the protocol, do following manual steps for prepare binding
bead mix. Prepare the required amount of Binding Bead Mix on each day of use.

1. Vortex the Total Nucleic Acid Magnetic Beads to ensure that the bead mixture
    is homogeneous.

2. For the number of required reactions, prepare the Binding Bead Mix according
    to the following ratio: 265 μL of Binding Solution with 10 μL of Total
    Nucleic Acid Magnetic Beads. Include 10% overage when making the Binding
    Bead Mix for use with multiple reactions.

3. Mix well by inversion, then store at room temperature.

Written by Rita Chen & Dany Fu, DAMP Lab 2020-10-26
--------------------------------------------------------------------------------
"""
import math
from typing import (
    Tuple,
)

from opentrons import protocol_api
from opentrons.protocol_api import InstrumentContext
from opentrons.protocol_api.labware import Labware

# ------------------------- Declaration of Constants ---------------------------
metadata = {
    "apiLevel": "2.7",
    "protocolName": "RNA Extraction (MagMAX)",
    "author": "Rita Chen, Dany Fu",
    "description": "Extract RNA using the MagMAXTM Viral/Pathogen II Nucleic "
    "Acid Isolation Kit and 200μL sample input volume",
}

# Hardware
TEMP_DECK = {"NAME": "Temperature Module GEN2", "SLOT": 7}
MAG_DECK = {"NAME": "Magnetic Module", "SLOT": 10}  # gen 1 magnets

# Labware
OUTPUT_PLATE = {  # 200uL per well, 96 wells
    "NAME": "biorad_96_wellplate_200ul_pcr",
    "LABEL": "Output Plate",  # no slot, sits on temp deck
}
REACTION_PLATE = {  # 2.4mL per well, 96 wells
    "NAME": "usascientific_96_wellplate_2.4ml_deep",
    "LABEL": "Reaction Plate",  # no slot, sits on mag deck
}
REAGENT_PLATE = {
    "NAME": "biorad_96_wellplate_200ul_pcr",
    "SLOT": 5,
    "LABEL": "Reagent Plate",
}
REAGENT_RESERVOIR = {  # 22mL per well, 12 wells
    "NAME": "usascientific_12_reservoir_22ml",
    "SLOT": 11,
    "LABEL": "Reagent Reservoir",
}
WASTE_RESERVOIR = {  # 290mL per well, 1 well
    "NAME": "agilent_1_reservoir_290ml",
    "SLOT": 8,
    "LABEL": "Waste Reservoir",
}
FILTER_TIP_20 = [
    {
        "NAME": "opentrons_96_filtertiprack_20ul",
        "SLOT": 1,
        "LABEL": "Filter Tip SM1",
    },
    {
        "NAME": "opentrons_96_filtertiprack_20ul",
        "SLOT": 4,
        "LABEL": "Filter Tip SM4",
    },
]
FILTER_TIP_200 = [
    {
        "NAME": "opentrons_96_filtertiprack_200ul",
        "SLOT": 2,
        "LABEL": "Filter Tip LG3",
    },
    {
        "NAME": "opentrons_96_filtertiprack_200ul",
        "SLOT": 3,
        "LABEL": "Filter Tip LG6",
    },
    {
        "NAME": "opentrons_96_filtertiprack_200ul",
        "SLOT": 6,
        "LABEL": "Filter Tip LG9",
    },
    {
        "NAME": "opentrons_96_filtertiprack_200ul",
        "SLOT": 9,
        "LABEL": "Filter Tip LG5",
    },
]

# Instruments
P20_MULTI = {"NAME": "p20_multi_gen2", "POSITION": "right"}
P300_MULTI = {"NAME": "p300_multi_gen2", "POSITION": "left"}

# Reagents
PROTEINASE_K = "Proteinase K"
MS2 = "MS2 Phage Control"
BEADS = "Nucleic Acid Magnetic Beads"
WASH_BUFFER = "Wash Buffer"
ETHANOL1 = "Ethanol_1"
ETHANOL2 = "Ethanol_2"
ELUTION = "Elution Solution"

DEFAULT_ASPIRATE_SPEED = 94
DEFAULT_DISPENSE_SPEED = 94
ASPIRATE_SPEED = 50
DISPENSE_SPEED = 50

DEPTH_BOTTOM_MID = 2.00  # 2mm from bottom
DEPTH_BOTTOM_LOW = 1.00
TOUCH_SPEED = 20.0  # minimum speed

# 10uL pipette with deepwell plate
TOUCH_RADIUS_SM_LG = 1.00
TOUCH_HEIGHT_SM_LG = -3.0

# 200uL pipette with deepwell plate
TOUCH_RADIUS_LG_LG = 0.75
TOUCH_HEIGHT_LG_LG = -7.0

# 200uL pipette with PCR plate
TOUCH_RADIUS_LG_SM = 0.8
TOUCH_HEIGHT_LG_SM = -1.0

VOL_10 = 10
VOL_250 = 250
VOL_500 = 500

VOL_SAMPLE = 200
VOL_MS2 = 5
VOL_PK = 5
VOL_BEAD = 275
VOL_ELUTE = 50
VOL_WASTE = 485

TEMP = 4
MAGDECK_ENGAGE_HEIGHT = 12


# ----------------------------- Utility Methods --------------------------------


def make_reagent_map(
    reagent_plate: Labware,
    reagent_reservoir: Labware,
):
    """
    Utility Method to generate static reagent map with given labware.

    Args:
        reagent_plate: 96 Well Plate for Reagents.
        reagent_reservoir: Reagent Reservoir.

    """
    return {
        PROTEINASE_K: [  # 5uL per sample, 528uL in the well
            {"VOL": 528, "WELL": reagent_plate.columns()[0]}
        ],
        MS2: [  # 5uL per sample, 528uL in the well
            {"VOL": 528, "WELL": reagent_plate.columns()[1]}
        ],
        ELUTION: [  # 50uL per sample, 5.28mL in the well
            {"VOL": 5280, "WELL": reagent_reservoir.columns()[10]}
        ],
        BEADS: [  # 275uL per sample, 14.52mL in the well
            {"VOL": 14520, "WELL": reagent_reservoir.columns()[0]},
            {"VOL": 14520, "WELL": reagent_reservoir.columns()[1]},
        ],
        WASH_BUFFER: [  # 500uL per sample, 17.6mL in the well
            {"VOL": 17600, "WELL": reagent_reservoir.columns()[2]},
            {"VOL": 17600, "WELL": reagent_reservoir.columns()[3]},
            {"VOL": 17600, "WELL": reagent_reservoir.columns()[4]},
        ],
        ETHANOL1: [
            {"VOL": 17600, "WELL": reagent_reservoir.columns()[5]},
            {"VOL": 17600, "WELL": reagent_reservoir.columns()[6]},
            {"VOL": 17600, "WELL": reagent_reservoir.columns()[7]},
        ],
        ETHANOL2: [
            {"VOL": 13200, "WELL": reagent_reservoir.columns()[8]},
            {"VOL": 13200, "WELL": reagent_reservoir.columns()[9]},
        ],
    }


def transfer(
    volume_ul: int = 0,
    dispense_all: bool = True,
    pipette: InstrumentContext = None,
    source: Labware = [],
    dest: Labware = [],
    mix_before: Tuple[int, int] = None,
    mix_after: Tuple[int, int] = None,
    touch_tip: Tuple[float, float] = None,
    delay_time_s: int = None,
    protocol: protocol_api.ProtocolContext = None,
):
    """
    Custom transfer function; when the volume needed exceeds the pipette's max
    volume this function will prioritize tip reuse by pipetting to the top of
    the wells until the last dispensation

    Args:
        volume_ul: The requested pipetting volume.
        dispense_all: To dispense the entire volume of the pipette.
        pipette: Which pipette to perform the operation with.
        source: The labware that is being aspirated from.
        dest: The labware being dispensed to.
        mix_before: Whether to perform mixing before the transfer process.
        mix_after: Whether to perform mixing after the transfer process.
        touch_tip: Whether to allow the tip to be submerged.
        delay_time_s: How long to delay while aspirating.
        protocol: The protocol context to operate on.
    """

    # must pick up tip first before proper working volume is calculated
    pipette.pick_up_tip()

    max_vol = pipette.hw_pipette["working_volume"]
    if mix_before and len(mix_before) == 2:
        mix_before_vol = max_vol if mix_before[1] > max_vol else mix_before[1]
    if mix_after and len(mix_after) == 2:
        mix_after_vol = max_vol if mix_after[1] > max_vol else mix_after[1]

    n = math.ceil(volume_ul / max_vol)
    vol_ar = [
        volume_ul // n + (1 if x < volume_ul % n else 0) for x in range(n)
    ]

    # dispense to the top of the well so we can reuse the tips
    for v in vol_ar[:-1]:
        if mix_before:
            if len(mix_before) == 1:
                pipette.mix(
                    repetitions=mix_before[0],
                    volume=v,
                    location=source[0],
                )
            if len(mix_before) == 2:
                pipette.mix(
                    repetitions=mix_before[0],
                    volume=mix_before_vol,
                    location=source[0],
                )
        pipette.aspirate(volume=v, location=source[0])
        if delay_time_s:
            pipette.air_gap(volume=0)
            protocol.delay(seconds=delay_time_s)

        dispense_vol = v if dispense_all else v - 10
        pipette.dispense(volume=dispense_vol, location=dest[0].top())
        pipette.blow_out(location=dest[0])

    # the final transfer
    if mix_before:
        if len(mix_before) == 1:
            pipette.mix(
                repetitions=mix_before[0],
                volume=vol_ar[-1],
                location=source[0],
            )
        if len(mix_before) == 2:
            pipette.mix(
                repetitions=mix_before[0],
                volume=mix_after_vol,
                location=source[0],
            )
    pipette.aspirate(volume=vol_ar[-1], location=source[0])
    if delay_time_s:
        pipette.air_gap(volume=0)
        protocol.delay(seconds=delay_time_s)

    dispense_vol = vol_ar[-1] if dispense_all else vol_ar[-1] - 10
    pipette.dispense(volume=dispense_vol, location=dest[0])

    if mix_after:
        if len(mix_after) == 1:
            pipette.mix(repetitions=mix_after[0], volume=vol_ar[-1])
        if len(mix_after) == 2:
            pipette.mix(repetitions=mix_after[0], volume=mix_after_vol)

    pipette.blow_out(location=dest[0])
    if touch_tip:
        pipette.touch_tip(
            radius=touch_tip[0],
            v_offset=touch_tip[1],
            speed=TOUCH_SPEED,
        )
    pipette.drop_tip()


def reagent_low(
    quantity_remaining: int = 0,
    quantity_to_transfer: int = 0,
) -> bool:
    """
    Checks to see if our Reagent is low.

    Args:
        quantity_remaining: The quantity remaining
        quantity_to_transfer: The quantity to transfer.

    Returns:
        True if we have enough reagent remaining, else False.
    """
    return True if quantity_remaining < quantity_to_transfer else False


def add_proteinase_k(
    num_cols: int = 0,
    pipette: InstrumentContext = None,
    source_plate: Labware = None,
    destination_plate: Labware = [],
):
    """
    Adds Proteinase K to selected columns.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.

    """
    for c in range(num_cols):
        transfer(
            volume_ul=VOL_PK,
            pipette=pipette,
            source=source_plate,
            dest=destination_plate[c],
            mix_before=(2, VOL_10),
            mix_after=(3, VOL_10),
            touch_tip=(TOUCH_RADIUS_SM_LG, TOUCH_HEIGHT_SM_LG),
        )


def add_beads(
    num_cols: int = 0,
    pipette: InstrumentContext = None,
    source_plate: Labware = [],
    destination_plate: Labware = [],
    protocol: protocol_api.ProtocolContext = None,
):
    """
    Adds Magnetic Beads to selected columns.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.
        protocol: The protocol context to operate on.
    """
    s = 0
    reagent_vol = source_plate[s]["VOL"]
    for c in range(num_cols):
        vol_transfer = VOL_BEAD * pipette.channels
        if reagent_low(
            quantity_remaining=reagent_vol,
            quantity_to_transfer=vol_transfer,
        ):
            s += 1
            reagent_vol = source_plate[s]["VOL"]

        transfer(
            volume_ul=VOL_BEAD,
            pipette=pipette,
            source=source_plate[s]["WELL"],
            dest=destination_plate[c],
            mix_before=(5,),
            mix_after=(2,),
            touch_tip=(TOUCH_RADIUS_LG_LG, TOUCH_HEIGHT_LG_LG),
            delay_time_s=5,
            protocol=protocol,
        )

        reagent_vol -= vol_transfer


def add_ms2(
    num_cols: int = 0,
    pipette: InstrumentContext = None,
    source_plate: Labware = None,
    destination_plate: Labware = [],
):
    """
    Adds MS2 to selected columns.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.
    """
    for c in range(num_cols):
        transfer(
            volume_ul=VOL_PK,
            pipette=pipette,
            source=source_plate,
            dest=destination_plate[c],
            mix_before=(2, VOL_10),
            mix_after=(3, VOL_10),
            touch_tip=(TOUCH_RADIUS_SM_LG, TOUCH_HEIGHT_SM_LG),
        )


def discard_supernatant(
    num_cols: int = 0,
    pipette: InstrumentContext = None,
    source_plate: Labware = [],
    destination_plate: Labware = [],
):
    """
    Discared Supernatant.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.
    """
    pipette.well_bottom_clearance.aspirate = DEPTH_BOTTOM_LOW
    pipette.flow_rate.aspirate = ASPIRATE_SPEED
    pipette.flow_rate.dispense = DISPENSE_SPEED
    for c in range(num_cols):
        transfer(
            volume_ul=VOL_WASTE,
            dispense_all=False,
            pipette=pipette,
            source=source_plate[c],
            dest=destination_plate[0],
        )
    reset_pipette_depth(pipette)


def wash_beads(
    protocol: protocol_api.ProtocolContext,
    source_plate: Labware = None,
    volume_ul: int = 0,
):
    """
    Perform a Bead Wash.

    Args:
        protocol: The protocol context to operate on.
        source_plate: The plate to perform the wash on.
        volume_ul: What volume of liquid to use for the wash, in uL.

    """
    mag_deck = protocol.loaded_modules[MAG_DECK["SLOT"]]
    p300 = protocol.loaded_instruments[P300_MULTI["POSITION"]]
    reaction_plate = protocol.loaded_labwares[MAG_DECK["SLOT"]]
    waste_reservior = protocol.loaded_labwares[WASTE_RESERVOIR["SLOT"]]
    num_cols = len(reaction_plate.columns())

    # 2. Remove the plate from the magnetic stand
    mag_deck.disengage()

    wash(
        num_cols=num_cols,
        pipette=p300,
        source_plate=source_plate,
        destination_plate=reaction_plate.columns(),
        volume_ul=volume_ul,
    )

    # 3. Reseal the plate, then shake at 1,050 rpm for 1 minute.
    # Step 3 happen outside of OT-2.
    protocol.pause()

    # 4. Place the plate back on the magnetic stand for 2 minutes, or until all the beads have collected.
    mag_deck.engage(height=MAGDECK_ENGAGE_HEIGHT)
    protocol.delay(minutes=2)

    # 5. Keeping the plate on the magnet, discard the supernatant from each well.
    # IMPORTANT! Avoid disturbing the beads.
    discard_supernatant(
        num_cols=num_cols,
        pipette=p300,
        source_plate=reaction_plate.columns(),
        destination_plate=waste_reservior.columns(),
    )


def wash(
    num_cols: int = 0,
    pipette: InstrumentContext = None,
    source_plate: Labware = None,
    destination_plate: Labware = None,
    volume_ul: int = 0,
):
    """
    Performs a Wash, aspirating from the selected source plate to the
    destination plate.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.
        volume_ul: What volume of liquid to use for the wash, in uL.
    """
    s = 0
    reagent_vol = source_plate[s]["VOL"]
    for c in range(num_cols):
        vol_transfer = volume_ul * pipette.channels
        if reagent_low(
            quantity_remaining=reagent_vol,
            quantity_to_transfer=vol_transfer,
        ):
            s += 1
            reagent_vol = source_plate[s]["VOL"]

        transfer(
            volume_ul=volume_ul,
            pipette=pipette,
            source=source_plate[s]["WELL"],
            dest=destination_plate[c],
            mix_before=(3,),
            mix_after=(5,),
            touch_tip=(TOUCH_RADIUS_LG_LG, TOUCH_HEIGHT_LG_LG),
        )
        reagent_vol -= vol_transfer


def elute(
    num_cols: int = 0,
    pipette: InstrumentContext = None,
    source_plate: Labware = None,
    destination_plate: Labware = [],
):
    """
    Performs an Elution on the passed in destination plate aspirating from the
    source plate.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.
    """
    pipette.well_bottom_clearance.aspirate = DEPTH_BOTTOM_LOW
    for c in range(num_cols):
        transfer(
            volume_ul=VOL_ELUTE,
            pipette=pipette,
            source=source_plate["WELL"],
            dest=destination_plate[c],
            mix_before=(3, 175),
            mix_after=(5, 35),
            touch_tip=(TOUCH_RADIUS_LG_LG, TOUCH_HEIGHT_LG_LG),
        )
    reset_pipette_depth(pipette)


def make_qPCR_plate(
    num_cols: int = 0,
    pipette: InstrumentContext = None,
    source_plate: Labware = [],
    destination_plate: Labware = [],
):
    """
    Makes a qPCR (quantitative polymerase chain reaction) plate.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.

    """
    pipette.well_bottom_clearance.aspirate = DEPTH_BOTTOM_LOW
    for c in range(num_cols):
        transfer(
            volume_ul=VOL_ELUTE,
            pipette=pipette,
            source=source_plate[c],
            dest=destination_plate[c],
            touch_tip=(TOUCH_RADIUS_LG_SM, TOUCH_HEIGHT_LG_SM),
        )
    reset_pipette_depth(pipette)


def reset_pipette_depth(pipette: InstrumentContext):
    """
    Resets the selected Pipette's Depth

    Args:
        pipette: Which Opentrons Pipette the operation will use.
    """
    pipette.well_bottom_clearance.aspirate = DEPTH_BOTTOM_MID
    pipette.well_bottom_clearance.dispense = DEPTH_BOTTOM_MID


def reset_pipette_speed(pipette: InstrumentContext):
    """
    Resets the selected Pipette's Speed

    Args:
        pipette: Which Opentrons Pipette the operation will use.
    """
    pipette.flow_rate.aspirate = DEFAULT_ASPIRATE_SPEED
    pipette.flow_rate.dispense = DEFAULT_DISPENSE_SPEED


def run(protocol: protocol_api.ProtocolContext):
    """
    Run the RNA Extraction.

    Args:
        protocol: The Opentrons Protocol Context controlling the execution of
            the protocol.

    """
    temp_deck = protocol.load_module(
        TEMP_DECK["NAME"], location=TEMP_DECK["SLOT"]
    )
    # The output plate needs to be kept cold on the temp deck
    output_plate = temp_deck.load_labware(
        OUTPUT_PLATE["NAME"], label=OUTPUT_PLATE["LABEL"]
    )

    mag_deck = protocol.load_module(MAG_DECK["NAME"], location=MAG_DECK["SLOT"])
    # The reaction plate is loaded on top of the magnetic module
    reaction_plate = mag_deck.load_labware(
        REACTION_PLATE["NAME"], label=REACTION_PLATE["LABEL"]
    )

    reagent_plate = protocol.load_labware(
        REAGENT_PLATE["NAME"],
        location=REAGENT_PLATE["SLOT"],
        label=REAGENT_PLATE["LABEL"],
    )

    reagent_reservior = protocol.load_labware(
        REAGENT_RESERVOIR["NAME"],
        location=REAGENT_RESERVOIR["SLOT"],
        label=REAGENT_RESERVOIR["LABEL"],
    )

    waste_reservior = protocol.load_labware(
        WASTE_RESERVOIR["NAME"],
        location=WASTE_RESERVOIR["SLOT"],
        label=WASTE_RESERVOIR["LABEL"],
    )

    # Load in 2 of 20ul filter tiprack
    tip_20 = [
        protocol.load_labware(i["NAME"], location=i["SLOT"], label=i["LABEL"])
        for i in FILTER_TIP_20
    ]
    p20 = protocol.load_instrument(
        P20_MULTI["NAME"], P20_MULTI["POSITION"], tip_racks=tip_20
    )
    reset_pipette_depth(p20)

    # Load in 4 of 200ul filter tiprack
    tip_200 = [
        protocol.load_labware(i["NAME"], location=i["SLOT"], label=i["LABEL"])
        for i in FILTER_TIP_200
    ]
    p300 = protocol.load_instrument(
        P300_MULTI["NAME"], P300_MULTI["POSITION"], tip_racks=tip_200
    )
    reset_pipette_depth(p300)

    reagent_map = make_reagent_map(reagent_plate, reagent_reservior)
    num_cols = len(reaction_plate.columns())

    # ------------------------------ Lyse Sample -------------------------------


    # 1. Mix and add 5 μL of Proteinase K to each well of reaction plate that
    # already contains 200 μL of sample.
    add_proteinase_k(
        num_cols=num_cols,
        pipette=p20,
        source_plate=reagent_map[PROTEINASE_K][0]["WELL"],
        destination_plate=reaction_plate.columns(),
    )

    # 2. Mix and add 275 μL of bead solution to each well
    add_beads(
        num_cols=num_cols,
        pipette=p300,
        source_plate=reagent_map[BEADS],
        destination_plate=reaction_plate.columns(),
        protocol=protocol,
    )

    # 3. Add 5 μL of MS2 Phage Control to each well
    add_ms2(
        num_cols=num_cols,
        pipette=p20,
        source_plate=reagent_map[MS2][0]["WELL"],
        destination_plate=reaction_plate.columns(),
    )

    # 4. Seal the plate then shake at 1,050 rpm for 2 minutes.
    # 5. Incubate at 65°C for 5 minutes, shake at 1,050 rpm for 5 minutes.
    # Step 4-5 happens outside of OT2
    protocol.pause()

    # 6. Place the sealed plate on the magnetic stand for 10 minutes or until
    # all of the beads have collected.
    mag_deck.engage(
        height=MAGDECK_ENGAGE_HEIGHT
    )  # Raise the Magnetic Module’s magnets.
    protocol.delay(minutes=10)

    """
    WASH BEADS
    """
    # 1. Keeping the plate on the magnet, discard the supernatant from each well.
    # IMPORTANT! Avoid disturbing the beads.
    discard_supernatant(
        num_cols=num_cols,
        pipette=p300,
        source_plate=reaction_plate.columns(),
        destination_plate=waste_reservior.columns(),
    )
    # Steps 2-7
    wash_beads(
        protocol, source_plate=reagent_map[WASH_BUFFER], volume_ul=VOL_500
    )

    # add more 300uL tips
    protocol.pause()
    for t in tip_200:
        t.reset()

    wash_beads(protocol, source_plate=reagent_map[ETHANOL1], volume_ul=VOL_500)
    wash_beads(protocol, source_plate=reagent_map[ETHANOL2], volume_ul=VOL_250)

    # 8. Dry the beads by shaking the plate (uncovered) at 1,050 rpm for 2
    # minutes. This happens outside of OT2
    protocol.pause()

    # add more 300uL tips
    for t in tip_200:
        t.reset()

    # ------------------------ Elute the Nucleic Acid --------------------------

    temp_deck.set_temperature(celsius=TEMP)
    # 1. Add 50 μL of Elution Solution to each sample, then seal the plate
    mag_deck.disengage()
    elute(
        num_cols=num_cols,
        pipette=p300,
        source_plate=reagent_map[ELUTION][0],
        destination_plate=reaction_plate.columns(),
    )
    # 2. Shake at 1,050 rpm for 5 minutes.
    # 3. Incubate at 65°C for 10 minutes.
    # 4. Shake at 1,050 rpm for 5 minutes.
    # Step 2-4 happen outside of OT-2.
    protocol.pause()

    # 5. Place the sealed plate on the magnetic stand for 3 minutes or until
    # clear to collect the beads against the magnets.
    mag_deck.engage(height=MAGDECK_ENGAGE_HEIGHT)
    protocol.delay(minutes=3)

    # 6. Keeping the plate on the magnet, transfer the eluates to a fresh
    # standard (not deep-well) plate, then seal the plate with MicroAmp™ Clear
    # Adhesive Film. Note: Significant bead carry over may adversely impact
    # RT-PCR performance. Leave the output plate on the Temperature Module, and
    # immediately proceed to the qPCR assay preparation protocol.
    make_qPCR_plate(
        num_cols=num_cols,
        pipette=p300,
        source_plate=reaction_plate.columns(),
        destination_plate=output_plate.columns(),
    )

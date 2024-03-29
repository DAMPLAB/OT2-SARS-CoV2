﻿"""
--------------------------------------------------------------------------------
Description: qPCR Assay Setup Protocol

General Instructions:
Before starting the protocol, do following manual steps for prepare the RT‑PCR
reactions. Use this procedure if you extracted sample RNA using an original
sample input volume of 200 μL.

1. If frozen, thaw the reagents on ice.

2. Gently vortex the samples and reagents, then centrifuge briefly to collect
    liquid at the bottom of the 96-well plate.

3. Dilute TaqPath™ COVID‑19 Control (1 × 104 copies/μL) to a working stock of
    25 copies/μL:
    a. Pipette 98 μL of TaqPath™ COVID‑19 Control Dilution Buffer into a
        microcentrifuge tube, then add 2 μL of diluted TaqPath™ COVID‑19
        Control. Mix well, then centrifuge briefly.
    b. Pipette 87.5 μL of TaqPath™ COVID‑19 Control Dilution Buffer into a
        second microcentrifuge tube, then add 12.5 μL of the dilution created in
        substep 3a. Mix well, then centrifuge briefly.
        Note: The TaqPath™ COVID‑19 Control does not contain the MS2 template.

4. Prepare the Reaction Mix:
    a. For each run, combine the following components sufficient for the number
        of tests plus one Positive Control and one  Negative Control.
        All volumes include 10% overage for pipette error.
        IMPORTANT! The volumes in this table assume that you extracted sample
        RNA using an original sample input volume of 200 μL.

5. Set up the reaction plate.

6. Seal the plate with MicroAmp™ Optical Adhesive Film, vortex the plate for
    10 seconds to ensure proper mixing,then centrifuge for 1 minute at 2000
    rpm to collect the liquid at the bottom of the reaction plate.

Written by Rita Chen & Dany Fu, DAMP Lab 2020-03-22
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
    "protocolName": "qPCR Prep (MagMAX)",
    "author": "Rita Chen, Dany Fu",
    "description": "Aliquot RNA eluent and distribute master mix to 96 "
    "well plate",
}

TEMP_DECK_1 = {"NAME": "Temperature Module GEN2", "SLOT": 7}
TEMP_DECK_2 = {"NAME": "Temperature Module", "SLOT": 4}
QPCR_PLATE = {  # 200uL per well, 96 wells
    "NAME": "biorad_96_wellplate_200ul_pcr",
    "LABEL": "Output Plate",  # no slot, sits on temp deck
}
RNA_PLATE = {  # 200uL per well, 96 wells
    "NAME": "biorad_96_wellplate_200ul_pcr",
    "LABEL": "RNA Plate",
    "SLOT": 8,
}
REAGENT_PLATE = {  # 200uL per well, 96 wells
    "NAME": "biorad_96_wellplate_200ul_pcr",
    "LABEL": "Reagent Plate",
}
P10_MULTI = {"NAME": "p20_multi_gen2", "POSITION": "right"}
FILTER_TIP_20 = [
    {
        "NAME": "opentrons_96_filtertiprack_20ul",
        "SLOT": 1,
        "LABEL": "Filter Tip S-1",
    },
    {
        "NAME": "opentrons_96_filtertiprack_20ul",
        "SLOT": 2,
        "LABEL": "Filter Tip S-2",
    },
]

ASPIRATE_DEPTH_BOTTOM = 2.00  # 2mm from bottle
VOL_RNA = 10
VOL_MASTER_MIX = 15  # Reaction volume
TEMP = 4
TOUCH_SPEED = 20.0
TOUCH_RADIUS_SM_SM = 1.0
TOUCH_HEIGHT_SM_SM = -1.0


# ----------------------------- Utility Methods --------------------------------
def aliquot_eluent(
    num_cols: int = 1,
    pipette: InstrumentContext = None,
    source_plate: Labware = None,
    destination_plate: Labware = [],
):
    """
    Aliquot 10 µL of the purified RNA extract to an empty Bio-Rad 96 well plate
    at the beginning of the qPCR assay preparation protocol.

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.
    """
    for column in range(num_cols):
        transfer(
            volume_ul=VOL_RNA,
            pipette=pipette,
            source=source_plate[column],
            dest=destination_plate[column],
        )


def add_master_mix(
    num_cols: int = 1,
    pipette: InstrumentContext = None,
    source_plate: Labware = None,
    destination_plate: Labware = [],
):
    """
    Transfer 15ul of reagent mix (reagent plate) to the aliquoted reaction
    plate (aliquot_eluent)

    Args:
        num_cols: Number of columns to operate on.
        pipette: Which Opentrons Pipette the operation will use.
        source_plate: The plate to aspirate from.
        destination_plate: The plate being dispensed to.
    """
    for c in range(num_cols):
        transfer(
            volume_ul=VOL_MASTER_MIX,
            pipette=pipette,
            source=source_plate,
            dest=destination_plate[c],
            mix_before=(5, VOL_MASTER_MIX),
            mix_after=(5, VOL_MASTER_MIX),
            touch_tip=(TOUCH_RADIUS_SM_SM, TOUCH_HEIGHT_SM_SM),
        )


def transfer(
    volume_ul: int = 0,
    dispense_all: bool = True,
    pipette: InstrumentContext = None,
    source: Labware = [],
    dest: Labware = [],
    mix_before: Tuple[int] = None,
    mix_after: Tuple[int] = None,
    touch_tip: Tuple[int] = None,
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


# ------------------------------ Primary Method --------------------------------


def run(protocol: protocol_api.ProtocolContext):
    """
    Run the qPCR Assay.

    Args:
        protocol: The Opentrons Protocol Context controlling the execution of
            the protocol.


    """
    temp_deck_1 = protocol.load_module(
        TEMP_DECK_1["NAME"],
        location=TEMP_DECK_1["SLOT"],
    )
    temp_deck_2 = protocol.load_module(
        TEMP_DECK_2["NAME"],
        location=TEMP_DECK_2["SLOT"],
    )
    qPCR_plate = temp_deck_1.load_labware(
        QPCR_PLATE["NAME"],
        label=QPCR_PLATE["LABEL"],
    )
    rna_plate = protocol.load_labware(
        RNA_PLATE["NAME"],
        location=RNA_PLATE["SLOT"],
        label=RNA_PLATE["LABEL"],
    )
    reagent_plate = temp_deck_2.load_labware(
        REAGENT_PLATE["NAME"],
        label=REAGENT_PLATE["LABEL"],
    )
    mastermix = reagent_plate.columns()[0]
    tip_20 = [
        protocol.load_labware(i["NAME"], location=i["SLOT"], label=i["LABEL"])
        for i in FILTER_TIP_20
    ]
    p20 = protocol.load_instrument(
        P10_MULTI["NAME"], P10_MULTI["POSITION"], tip_racks=tip_20
    )
    p20.well_bottom_clearance.aspirate = ASPIRATE_DEPTH_BOTTOM
    p20.well_bottom_clearance.dispense = ASPIRATE_DEPTH_BOTTOM

    num_cols = len(qPCR_plate.columns())

    temp_deck_1.set_temperature(celsius=TEMP)
    temp_deck_2.set_temperature(celsius=TEMP)

    aliquot_eluent(
        num_cols=num_cols,
        pipette=p20,
        source_plate=rna_plate.columns(),
        destination_plate=qPCR_plate.columns(),
    )
    add_master_mix(
        num_cols=num_cols,
        pipette=p20,
        source_plate=mastermix,
        destination_plate=qPCR_plate.columns(),
    )

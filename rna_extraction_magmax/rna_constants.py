# Hardware
TEMP_DECK = {
    'NAME': 'Temperature Module',
    'SLOT': 7
}
MAG_DECK = {
    'NAME': 'Magnetic Module',
    'SLOT': 10
}

# Labware
OUTPUT_PLATE = { #200uL per well, 96 wells
    'NAME': 'biorad_96_wellplate_200ul_pcr',
    'LABEL': 'Output Plate' #no slot, sits on temp deck
}
REACTION_PLATE = { #2.4mL per well, 96 wells
    'NAME': 'usascientific_96_wellplate_2.4ml_deep',
    'LABEL': 'Reaction Plate', #no slot, sits on mag deck
}
REAGENT_PLATE = {
    'NAME': 'biorad_96_wellplate_200ul_pcr',
    'SLOT': 2,
    'LABEL': 'Reagent Plate'
}
REAGENT_RESERVOIR = { #22mL per well, 12 wells
    'NAME': 'usascientific_12_reservoir_22ml',
    'SLOT': 5,
    'LABEL': 'Reagent Reservoir'
}
WASTE_RESERVOIR = { #290mL per well, 1 well
    'NAME': 'agilent_1_reservoir_290ml',
    'SLOT': 8,
    'LABEL': 'Waste Reservoir'
}
FILTER_TIP_10 = [{
    'NAME': 'opentrons_96_filtertiprack_10ul',
    'SLOT': 1,
    'LABEL': 'Filter Tip SM1'
}, {
    'NAME': 'opentrons_96_filtertiprack_10ul',
    'SLOT': 4,
    'LABEL': 'Filter Tip SM4'
}]
FILTER_TIP_300 = [{
    'NAME': 'opentrons_96_tiprack_300ul',
    'SLOT': 3,
    'LABEL': 'Filter Tip LG3'
}, {
    'NAME': 'opentrons_96_tiprack_300ul',
    'SLOT': 6,
    'LABEL': 'Filter Tip LG6'
}, {
    'NAME': 'opentrons_96_tiprack_300ul',
    'SLOT': 9,
    'LABEL': 'Filter Tip LG7'
}, {
    'NAME': 'opentrons_96_tiprack_300ul',
    'SLOT': 11,
    'LABEL': 'Filter Tip LG9'
}]

# Instruments
P10_MULTI = {
    'NAME': 'p10_multi',
    'POSITION': 'right'
}
P300_MULTI = {
    'NAME': 'p300_multi_gen2',
    'POSITION': 'left'
}

# Reagents
PROTEINASE_K = 'Proteinase K'
MS2 = 'MS2 Phage Control'
BEADS = 'Nucleic Acid Magnetic Beads'
WASH_BUFFER = 'Wash Buffer'
ETHANOL1 = 'Ethanol_1'
ETHANOL2 = 'Ethanol_2'
ELUTION = 'Elution Solution'

DEPTH_BOTTOM_HIGH = 2.50 #2mm from bottom
DEPTH_BOTTOM_MID = 2.00 #2mm from bottom
DEPTH_BOTTOM_LOW = 1.00
MAG_DECK_HEIGHT = 12 #12mm
TOUCH_SPEED = 20.0 #minimum speed

# 10uL pipette with deepwell plate
TOUCH_RADIUS_SM_LG = 1.00
TOUCH_HEIGHT_SM_LG = -3.0

# 200uL pipette with deepwell plate
TOUCH_RADIUS_LG_LG = 0.75
TOUCH_HEIGHT_LG_LG = -7.0

# 200uL pipette with PCR plate
TOUCH_RADIUS_LG_SM = 1.00
TOUCH_HEIGHT_LG_SM = -2.0

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

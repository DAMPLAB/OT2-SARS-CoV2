
# Hardware
TEMP_DECK = {
    'NAME': 'Temperature Module',
    'SLOT': 1
}
MAG_DECK = {
    'NAME': 'Magnetic Module',
    'SLOT': 5
}

# Labware
OUTPUT_PLATE = { #200uL per well, 96 wells
    'NAME': 'biorad_96_wellplate_200ul_pcr',
    'LABEL': 'Output Plate' #no slot, sits on temp deck
}
REACTION_PLATE = { #2.4mL per well, 96 wells
    'NAME': 'usascientific_96_wellplate_2.4ml_deep',
    'LABEL': 'Reaction Plate', #no slot, sits on mag deck
    'DEPTH': 14.81
}
REAGENT_PLATE = {
    'NAME': 'biorad_96_wellplate_200ul_pcr',
    'SLOT': 8,
    'LABEL': 'Reagent Plate'
}
REAGENT_RESERVOIR = { #22mL per well, 12 wells
    'NAME': 'usascientific_12_reservoir_22ml',
    'SLOT': 4,
    'LABEL': 'Reagent Reservoir'
}
WASTE_RESERVOIR = { #290mL per well, 1 well
    'NAME': 'agilent_1_reservoir_290ml',
    'SLOT': 2,
    'LABEL': 'Waste Reservoir'
}
FILTER_TIP_20 = [{
    'NAME': 'opentrons_96_filtertiprack_20ul',
    'SLOT': 10,
    'LABEL': 'Filter Tip S-10'
}, {
    'NAME': 'opentrons_96_filtertiprack_20ul',
    'SLOT': 11,
    'LABEL': 'Filter Tip S-11'
}]
FILTER_TIP_200 = [{
    'NAME': 'opentrons_96_filtertiprack_200ul',
    'SLOT': 3,
    'LABEL': 'Filter Tip S-3'
}, {
    'NAME': 'opentrons_96_filtertiprack_200ul',
    'SLOT': 6,
    'LABEL': 'Filter Tip S-6'
}, {
    'NAME': 'opentrons_96_filtertiprack_200ul',
    'SLOT': 7,
    'LABEL': 'Filter Tip S-7'
}, {
    'NAME': 'opentrons_96_filtertiprack_200ul',
    'SLOT': 9,
    'LABEL': 'Filter Tip S-9'
}]

# Instruments
P20_MULTI = {
    'NAME': 'p20_multi_gen2',
    'POSITION': 'left'
}
P200_MULTI = {
    'NAME': 'p300_multi_gen2',
    'POSITION': 'right'
}

# Reagents
PROTEINASE_K = 'Proteinase K'
MS2 = 'MS2 Phage Control'
BEADS = 'Nucleic Acid Magnetic Beads'
WASH_BUFFER = 'Wash Buffer'
ETHANOL = 'Ethanol'
ELUTION = 'Elution Solution'

ASPIRATE_DEPTH_BOTTOM = 2.00 #2mm from bottle
MAG_DECK_HEIGHT = 12 #12mm

VOL_5 = 5 #sm rxn vol
VOL_15 = 15
VOL_250 = 250 #large rxn vol
VOL_500 = 500
VOL_BEAD = 275
VOL_ELUTE = 50
VOL_WASTE = 243

TEMP = 4

# RNA Extraction Protocol
# Written By Rita Chen 2020-05-21

# Before starting the protocol, do following manual steps for prepare binding bead Mmix:
# Prepare the required amount of Binding Bead Mix on each day of use.
# 1. Vortex the Total Nucleic Acid Magnetic Beads to ensure that the bead mixture is homogeneous.
# 2. For the number of required reactions, prepare the Binding Bead Mix according to the following ratio:
  # 265 μL of Binding Solution with 10 μL of Total Nucleic Acid Magnetic Beads
# Include 10% overage when making the Binding Bead Mix for use with multiple reactions.
# 3. Mix well by inversion, then store at room temperature.

from opentrons import labware, instruments, modules, robot

# Load hardware module and labwares
temp_deck = modules.load('tempdeck', '1', 'Temp Deck')
output_plate = labware.load('biorad-hardshell-96-PCR', '1', 'Output Plate', share=True) #250uL/well
mag_deck = modules.load('magdeck', '5', 'Mag Deck')
reaction_plate = labware.load('usascientific_96_wellplate_2.4ml_deep','5', 'Reaction Plate', share=True) #2.4mL/well

reagent_plate = labware.load('biorad-hardshell-96-PCR', '8', 'Reagnet Plate') #250uL/well
proteinase_k = reagent_plate.cols(0) # 5uL per sample, 528uL in the well
ms2_phage_control = reagent_plate.cols(1) # 5uL per sample, 52umL in the well

reagent_reservior = labware.load('usascientific_12_reservoir_22ml', '4', 'Reagnet Reservior') #22mL/well
magbead_mix_1 = reagent_reservior.cols(0) # 275uL per sample, 14.52mL in the well
magbead_mix_2 = reagent_reservior.cols(1) # 275uL per sample, 14.52mL in the well
wash_buffer_1 = reagent_reservior.cols(2) # 500uL per sample, 17.6mL in the well
wash_buffer_2 = reagent_reservior.cols(3) # 500uL per sample, 17.6mL in the well
wash_buffer_3 = reagent_reservior.cols(4) # 500uL per sample, 17.6mL in the well
ethanol_wash_1_1 = reagent_reservior.cols(5) # 500uL per sample, 17.6mL in the well
ethanol_wash_1_2 = reagent_reservior.cols(6) # 500uL per sample, 17.6mL in the well
ethanol_wash_1_3 = reagent_reservior.cols(7) # 500uL per sample, 17.6mL in the well
ethanol_wash_2_1 = reagent_reservior.cols(8) # 250uL per sample, 13.2mL in the well
ethanol_wash_2_2 = reagent_reservior.cols(9) # 250uL per sample, 13.2mL in the well
elution_solution = reagent_reservior.cols(10) # 50uL per sample, 5.28mL in the well

waste_reservior = labware.load('agilent_1_reservoir_290ml', '2', 'Waste Reservior') #290mL/well

# Load in 2 of 20ul filter tiprack 
tr_20 = [labware.load('opentrons_96_filtertiprack_20ul', '10'), labware.load('opentrons_96_filtertiprack_20ul', '11')]

# Load in 4 of 30ul filter tiprack 
tr_200 = [labware.load('opentrons_96_filtertiprack_200ul', '3'), labware.load('opentrons_96_filtertiprack_200ul', '6'),
labware.load('opentrons_96_filtertiprack_200ul', '9'), labware.load('opentrons_96_filtertiprack_200ul', '7')]

# Load in pipettes
p20 = instruments.p20_multi_gen2(mount='left', tip_racks=tr_20)
p300 = instruments.p300_multi_gen2(mount='right', tip_racks=tr_200)

num_cols = 12 # Number of columns
bead_vol = 275 # Reagent volume of binding bead mixture
small_rxn_vol = 5 # Small reagent volume
large_rxn_vol = 250 # Large reagent volume
elute_vol = 50 # Elution volume
waste_vol = 250 # Volume of waste 
waste_vol_left = 235 # Additional waste volume

# RNA Extraction here__________________________________________________________________________________________________

# Digest with Proteinase K_____________________________________________________________________________________________
# 1. Add 5 μL of Proteinase K to each well of reagent plate with 200 μL of sample in each sample well
for i in range(num_cols):
  p20.pick_up_tip()
  p20.mix(5, 15, ms2_phage_control.bottom(2.00))
  p20.transfer(small_rxn_vol, ms2_phage_control.bottom(2.00), reaction_plate.cols(i), new_tip='never')
  p20.blow_out()
  p20.drop_tip()

# 2. Invert the Binding Bead Mix 5 times gently to mix, then add 275 μL to each sample well and Negative Control well.
# Note: Remix the Binding Bead Mix by inversion frequently during pipetting to ensure even distribution of beads to all\
# samples or wells. The Binding Bead Mix is viscous, so pipet slowly to ensure that the correct amount is added.\
# DO NOT reuse pipette tips to add Binding Bead Mix to the samples, as the high viscosity will cause variations in\
# the volumes added.
for i in range(num_cols):
  if i < 6: 
    p300.pick_up_tip()
    p300.mix(8, large_rxn_vol, magbead_mix_1.bottom(2.00))
    p300.transfer(bead_vol, magbead_mix_1.bottom(2.00), reaction_plate.cols(i), new_tip='never')
    p300.mix(3, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()
  else:
    p300.pick_up_tip()
    p300.mix(8, large_rxn_vol, magbead_mix_1.bottom(2.00))
    p300.transfer(bead_vol, magbead_mix_1.bottom(2.00), reaction_plate.cols(i), new_tip='never')
    p300.mix(3, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()

# 3. Add 5 μL of MS2 Phage Control to each sample well and to the Negative Control well.
# !!! Does the order of adding MS2 Phage matters?
for i in range(num_cols):
  p20.pick_up_tip()
  p20.mix(5, 15, ms2_phage_control.bottom(2.00))
  p20.transfer(small_rxn_vol, ms2_phage_control.bottom(2.00), reaction_plate.cols(i), new_tip='never')
  p20.mix(8, 15, ms2_phage_control.bottom(2.00))
  p20.blow_out()
  p20.drop_tip()

# 4. Seal the plate with MicroAmp™ Clear Adhesive Film, then shake the sealed plate at 1,050 rpm for 2 minutes.
# 5. Incubate the sealed plate at 65°C for 5 minutes (ensure the bottom of the plate is uncovered), then shake\
# the plate at 1,050 rpm for 5 minutes.
# Step 4-5 happen outside of OT-2.
robot.pause()

# 6. Place the sealed plate on the magnetic stand for 10 minutes or until all of the beads have collected.
mag_deck.engage(height=12)
p20.delay(minutes=10)

# Wash the beads_______________________________________________________________________________________________________
# 1. Keeping the plate on the magnet, carefully remove the cover, then discard the supernatant from each well.
# IMPORTANT! Avoid disturbing the beads.
for i in range(num_cols):
    p300.pick_up_tip()
    p300.transfer(waste_vol_left, reaction_plate.cols(i).bottom(2.00), waste_reservior.cols(i).top(), new_tip='never')
    p300.blow_out()
    p300.transfer(waste_vol, reaction_plate.cols(i).bottom(2.00), waste_reservior.cols(i), new_tip='never')
    p300.drop_tip()

# 2. Remove the plate from the magnetic stand, then add 500 μL of Wash Buffer to each sample.
mag_deck.disengage()
for i in range(num_cols):
  if i < 4: 
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, wash_buffer_1.bottom(2.00))
    p300.transfer(large_rxn_vol, wash_buffer_1.bottom(2.00), reaction_plate.cols(i).top(), new_tip='never')
    p300.transfer(large_rxn_vol, wash_buffer_1.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()
  elif i in range(4,8): 
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, wash_buffer_2.bottom(2.00))
    p300.transfer(large_rxn_vol, wash_buffer_2.bottom(2.00), reaction_plate.cols(i).top(), new_tip='never')
    p300.transfer(large_rxn_vol, wash_buffer_2.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()
  else:
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, wash_buffer_3.bottom(2.00))
    p300.transfer(large_rxn_vol, wash_buffer_3.bottom(2.00), reaction_plate.cols(i).top(), new_tip='never')
    p300.transfer(large_rxn_vol, wash_buffer_3.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()

# 3. Reseal the plate, then shake at 1,050 rpm for 1 minute.
# Step 3 happen outside of OT-2.
robot.pause()

# 4. Place the plate back on the magnetic stand for 2 minutes, or until all the beads have collected.
mag_deck.engage(height=12)
p20.delay(minutes=2)

# 5. Keeping the plate on the magnet, carefully remove the cover, then discard the supernatant from each well.
# IMPORTANT! Avoid disturbing the beads.
for i in range(num_cols):
    p300.pick_up_tip()
    p300.transfer(waste_vol, reaction_plate.cols(i).bottom(2.00), waste_reservior.cols(i).top(), new_tip='never')
    p300.blow_out()
    p300.transfer(waste_vol, reaction_plate.cols(i).bottom(2.00), waste_reservior.cols(i), new_tip='never')
    p300.drop_tip()

# 6. Repeat step 2 to step 5 using 500 μL of 80% Ethanol.
mag_deck.disengage()
for i in range(num_cols):
  if i < 4: 
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, ethanol_wash_1_1.bottom(2.00))
    p300.transfer(large_rxn_vol, ethanol_wash_1_1.bottom(2.00), reaction_plate.cols(i).top(), new_tip='never')
    p300.transfer(large_rxn_vol, ethanol_wash_1_1.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()
  elif i in range(4,8): 
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, ethanol_wash_1_2.bottom(2.00))
    p300.transfer(large_rxn_vol, ethanol_wash_1_2.bottom(2.00), reaction_plate.cols(i).top(), new_tip='never')
    p300.transfer(large_rxn_vol, ethanol_wash_1_2.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()
  else:
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, ethanol_wash_1_3.bottom(2.00))
    p300.transfer(large_rxn_vol, ethanol_wash_1_3.bottom(2.00), reaction_plate.cols(i).top(), new_tip='never')
    p300.transfer(large_rxn_vol, ethanol_wash_1_3.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()

  # 6b. Reseal the plate, then shake at 1,050 rpm for 1 minute.
  # Step 6b happen outside of OT-2.
robot.pause()

  # 6c. Place the plate back on the magnetic stand for 2 minutes, or until all the beads have collected.
mag_deck.engage(height=12)
p20.delay(minutes=2)

  # 6d. Keeping the plate on the magnet, carefully remove the cover, then discard the supernatant from each well.
  # IMPORTANT! Avoid disturbing the beads.
for i in range(num_cols):
    p300.pick_up_tip()
    p300.transfer(waste_vol, reaction_plate.cols(i).bottom(2.00), waste_reservior.cols(i).top(), new_tip='never')
    p300.blow_out()
    p300.transfer(waste_vol, reaction_plate.cols(i).bottom(2.00), waste_reservior.cols(i), new_tip='never')
    p300.drop_tip()

# 7. Repeat step 2 to step 5 using 250 μL of 80% Ethanol.
mag_deck.disengage()
for i in range(num_cols):
  if i < 6: 
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, ethanol_wash_2_1.bottom(2.00))
    p300.transfer(large_rxn_vol, ethanol_wash_2_1.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()
  else:
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, ethanol_wash_2_2.bottom(2.00))
    p300.transfer(large_rxn_vol, ethanol_wash_2_2.bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, large_rxn_vol, reaction_plate.cols(i).bottom(2.00))
    p300.blow_out()
    p300.drop_tip()

  # 7b. Reseal the plate, then shake at 1,050 rpm for 1 minute.
  # Step 6b happen outside of OT-2.
robot.pause()

  # 7c. Place the plate back on the magnetic stand for 2 minutes, or until all the beads have collected.
mag_deck.engage(height=12)
p20.delay(minutes=2)

  # 7d. Keeping the plate on the magnet, carefully remove the cover, then discard the supernatant from each well.
  # IMPORTANT! Avoid disturbing the beads.
for i in range(num_cols):
    p300.pick_up_tip()
    p300.transfer(waste_vol, reaction_plate.cols(i).bottom(2.00), waste_reservior.cols(i), new_tip='never')
    p300.blow_out()
    p300.drop_tip()

mag_deck.disengage()

# 8. Dry the beads by shaking the plate (uncovered) at 1,050 rpm for 2 minutes.
# Step 8 happen outside of OT-2.
robot.pause()

# Elute the nucleic acid_______________________________________________________________________________________________
# 1. Add 50 μL of Elution Solution to each sample, then seal the plate with MicroAmp™ Clear Adhesive Film.
temp_deck.set_temperature(4)
for i in range(num_cols):
    p300.pick_up_tip()
    p300.mix(3, large_rxn_vol, elution_solution.bottom(2.00))
    p300.transfer(elute_vol, elution_solution.cols(i).bottom(2.00), reaction_plate.cols(i).bottom(2.00), new_tip='never')
    p300.mix(5, 35, elution_solution.bottom(2.00))
    p300.blow_out()
    p300.drop_tip()

# 2. Shake the sealed plate at 1,050 rpm for 5 minutes.
# 3. Place the plate in an incubator at 65°C for 10 minutes.
# 4. Remove the plate from the incubator, then shake the plate at 1,050 rpm for 5 minutes.
# Step 2-4 happen outside of OT-2.
robot.pause()

# 5. Place the sealed plate on the magnetic stand for 3 minutes or until clear to collect the beads against the magnets.
mag_deck.engage(height=12)
p20.delay(minutes=3)

# 6. Keeping the plate on the magnet, carefully remove the seal, transfer the eluates to a fresh standard\
# (not deep-well) plate, then seal the plate with MicroAmp™ Clear Adhesive Film.
# IMPORTANT! To prevent evaporation, seal the plate containing the eluate immediately after the transfers are complete.
# Note: Significant bead carry over may adversely impact RT-PCR performance. Place the plate on ice for immediate use\
# in real-time RT‑PCR.
for i in range(num_cols):
    p300.pick_up_tip()
    p300.transfer(elute_vol, reaction_plate.cols(i).bottom(2.00), output_plate.cols(i), new_tip='never')
    p300.blow_out()
    p300.drop_tip()




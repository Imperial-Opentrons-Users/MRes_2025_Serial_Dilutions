from opentrons import protocol_api
#from opentrons import simulate
##This is code for single channel pippete
metadata = {
# double check which api version Geoff's OT2 is using and change the code accordingly
    "protocolName": "iGEM Fluorescin Serial Dilution",
    "description": """This protocol is the outcome of following the
                   Python Protocol API Tutorial located at
                   https://docs.opentrons.com/v2/tutorial.html. It takes a
                   solution and progressively dilutes it by transferring it
                   stepwise across a plate.""",
    "author": "Team2"}

#protocol = simulate.get_protocol_api('2.15')

requirements = {"robotType": "OT-2", "apiLevel": "2.15"}

##Adjusted for multichannel pippete using partial channels
##make sure to adjust loops in case only 4 rows/rows are used
def run(protocol: protocol_api.ProtocolContext):
    tips = protocol.load_labware("opentrons_96_tiprack_300ul", 7)
    #tips = protocol.load_labware("opentrons_96_tiprack_300ul", 1)
    reservoir = protocol.load_labware("4ti0136_96_wellplate_2200ul", 8)
    #reservoir = protocol.load_labware("nest_12_reservoir_15ml", 2)
    plate = protocol.load_labware("costar96flatbottomtransparent_96_wellplate_200ul", 9)
    #plate = protocol.load_labware("nest_96_wellplate_200ul_flat", 3)
    left_pipette = protocol.load_instrument("p300_multi_gen2", "left", tip_racks=[tips])
    # Set pipette parameters bottom clearances and flow rates
    left_pipette.well_bottom_clearance.aspirate = 1  # mm
    left_pipette.well_bottom_clearance.dispense = 1  # mm

    left_pipette.flow_rate.aspirate = 100  # ul/s
    left_pipette.flow_rate.dispense = 70  # ul/s
    left_pipette.flow_rate.blow_out = 200  # ul/s

    # defining rates which can be used to modify flow rates
    high = 1.5
    normal = 1.0
    slow = 0.5
    vslow = 0.25
    ### example of how to aspirate with rates
    # left_pipette.aspirate(100, reservoir["A1"], rate=slow)

    ### how to add delay to let things settle
    # protocol.delay(seconds=2)  # wait for 2 seconds

    #Using block commands and loops
    ##Adding 100 uL of PBS from reservoir to well 2 to 12 in every row in plate
    left_pipette.pick_up_tip(tips.columns()[2][0]) 
    for i in range(11):
        left_pipette.aspirate(100, reservoir["A1"])
        left_pipette.dispense(100, plate.rows()[0][i+1].bottom(1))
    left_pipette.drop_tip()

    ##Adding 200 uL of solution from reservoir to first well in each row
    for i in range(1):
        left_pipette.pick_up_tip(tips.columns()[4][0])
        left_pipette.aspirate(200, reservoir["A2"])
        left_pipette.dispense(200, plate.rows()[i][0])
        #mixing after dispensing, with block commnands
        #left_pipette.aspirate(100, plate.rows()[i][0].bottom(1))
        #left_pipette.dispense(100, plate.rows()[i][0].bottom(1))
        #left_pipette.aspirate(100, plate.rows()[i][0].bottom(1))
        #left_pipette.dispense(100, plate.rows()[i][0].bottom(1))
        #left_pipette.aspirate(100, plate.rows()[i][0].bottom(1))
        #left_pipette.dispense(100, plate.rows()[i][0].bottom(1))
        ##Trashing the tip after each row
        left_pipette.drop_tip()
    
    ## Transferring 100 uL from each well to the next in the row
    for i in range(1):
        left_pipette.pick_up_tip(tips.columns()[5][0])
        for j in range(10):
            
            left_pipette.aspirate(100, plate.rows()[i][j])
            left_pipette.dispense(100, plate.rows()[i][j+1])
            
            #mixing after dispensing, with block commands
            left_pipette.aspirate(100, plate.rows()[i][j+1].bottom(1))
            left_pipette.dispense(100, plate.rows()[i][j+1].bottom(1), rate=high)
            left_pipette.aspirate(100, plate.rows()[i][j+1].bottom(1))
            left_pipette.dispense(100, plate.rows()[i][j+1].bottom(1), rate=high)
            left_pipette.aspirate(100, plate.rows()[i][j+1].bottom(1))
            left_pipette.dispense(100, plate.rows()[i][j+1].bottom(1))
            
            
            ##Discarding 100 uL from last well in each row into trash
            if j == 9:
                left_pipette.aspirate(100, plate.rows()[i][j+1])
                #left_pipette.dispense(100, fixed_trash['A1'])
            
            ##Trashing the tip after each transfer
        left_pipette.drop_tip()

    for line in protocol.commands(): 
        print(line)


#run(protocol)

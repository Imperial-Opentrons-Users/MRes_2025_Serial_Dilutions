from opentrons import protocol_api
from opentrons import simulate

metadata = {
    'apiLevel': '2.19', #the version updated for group4 opentron
    'protocolName': 'Team4_Serial_Dilution_2025_multi',
    'description': 'iGEM practice for serial dilution',
}

#for simulation only
protocol = simulate.get_protocol_api('2.19')


def run(protocol: protocol_api.ProtocolContext):

    #labware
    source_plate = protocol.load_labware('4ti0131_12_reservoir_21000ul', 1)   
    dest_plate = protocol.load_labware('costar3370flatbottomtransparent_96_wellplate_200ul', 4)   
    tiprack_1 = protocol.load_labware('opentrons_96_tiprack_300ul', 2)

    #pipette
    p300 = protocol.load_instrument('p300_multi_gen2',mount='left',tip_racks=[tiprack_1])

    #flow
    p300.flow_rate.aspirate = 50
    p300.flow_rate.dispense = 150
    p300.flow_rate.blow_out = 300

    #sources
    fluo_source = source_plate.wells_by_name()['A1']  
    PBS_source  = source_plate.wells_by_name()['A2']   

    #add 100 µL PBS
    dest_columns = dest_plate.columns()

    p300.pick_up_tip()

    for col_idx in range(1, 12):
        dest_col_top = dest_columns[col_idx][0]
        p300.aspirate(100, PBS_source)    
        p300.dispense(100, dest_col_top)

    p300.drop_tip()
    protocol.comment('PBS added')

    #add 200 µL fluorescein
    dest_col_fluo = dest_plate.wells_by_name()['A1']

    p300.pick_up_tip()
    p300.aspirate(200, fluo_source)     
    p300.dispense(200, dest_col_fluo)    
    p300.drop_tip()
    p300.pick_up_tip()
    #serial dilution
    for i in range(0,10):
        source_col = dest_columns[i][0]   
        dest_col   = dest_columns[i+1][0]     
        p300.aspirate(100, source_col)      
        p300.dispense(100, dest_col)          
        p300.mix(3, 50, dest_col)         
        p300.blow_out(dest_col.top())
        
    p300.aspirate(100, dest_columns[10][0])      
    p300.drop_tip()
    for line in protocol.commands():
        print(line)

#for simulation only
run(protocol)

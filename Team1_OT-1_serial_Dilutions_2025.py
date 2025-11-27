from opentrons.protocol_api import ProtocolContext

metadata = {
    'protocolName': 'Serial dilution for iGEM reference standard',
    'author': 'Team X',
    'description': 'Make a serial dilution plate using multi-channel pipette',
    'apiLevel': '2.14'
}

def run(ctx: ProtocolContext):

    tiprack1 = ctx.load_labware('opentrons_96_tiprack_300ul', '1')
    tiprack2 = ctx.load_labware('opentrons_96_tiprack_300ul', '4')
    trough = ctx.load_labware('nest_12_reservoir_15ml', '2')
    plate = ctx.load_labware('corning_96_wellplate_360ul_flat', '3')

    p300 = ctx.load_instrument('p300_multi', 'left', tip_racks=[tiprack1, tiprack2])

    p300.flow_rate.aspirate = 100
    p300.flow_rate.dispense = 150
    p300.flow_rate.blow_out = 200

    transfer_vol = 100
    mix_reps = 5
    mix_vol = 100

    stock = trough.wells_by_name()['A2']
    diluent = trough.wells_by_name()['A1']

    p300.pick_up_tip()
    for col in plate.columns()[1:]:
        p300.aspirate(transfer_vol , diluent.bottom())
        p300.dispense(transfer_vol , col[0].top(-2))
        #p300.mix(mix_reps, mix_vol, col[0].bottom(1))
        p300.blow_out(col[0].top())
    p300.drop_tip()		

    p300.pick_up_tip()
    first_col = plate.columns()[0][0]
    p300.aspirate(transfer_vol * 2, stock.bottom())
    p300.dispense(transfer_vol * 2, first_col)
    p300.mix(mix_reps, mix_vol, first_col.bottom(1))
    p300.blow_out(first_col.top())
    #p300.drop_tip()

    #p300.pick_up_tip()

    for i in range(10):  # 0→1, 1→2, ... 10→11
        src = plate.columns()[i][0]
        dest = plate.columns()[i + 1][0]

        p300.aspirate(transfer_vol, src.bottom(1))
        p300.dispense(transfer_vol, dest.bottom(1))
        p300.mix(mix_reps, mix_vol, dest.bottom(1))
        p300.blow_out(dest.top())


    final_col = plate.columns()[10][0]
    p300.aspirate(transfer_vol, final_col.bottom(1))
    p300.drop_tip()

    ctx.comment("Serial dilution complete (final column normalized).")

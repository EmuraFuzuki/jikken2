def main1():
    import pyvisa

    rm = pyvisa.ResourceManager()
    vis_list = rm.list_resources()
    print("接続可能な機器:")
    for vis in vis_list:
        print(vis)

    inst = rm.open_resource("USB0::6833::1100::DHO9A270600106::0::INSTR")

    print(inst.query("*IDN?"))  # 機器のIDを取得

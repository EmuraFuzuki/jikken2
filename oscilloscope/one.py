def main1():
    import pyvisa

    rm = pyvisa.ResourceManager()
    vis_list = rm.list_resources()
    print("接続可能な機器:")
    for vis in vis_list:
        print(vis)

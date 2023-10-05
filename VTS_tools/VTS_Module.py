from VTS_tools.examples.vts_tools import Hotkeyrequire, send_hotkey_request, set_parameter_value
import pyvts
import threading

hotkey = 0
#asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS_threading(hotkey)))
#asyncio_VTS_thread.start()

def VTS_motion_MODE(mode):
    if mode == 'happy':
        motion = -1
        expression = [5, 6]
    else:
        motion = -1
        expression = -1       
    return motion, expression

# Vtube Studio Function Module
async def VTS_module(emotion, status):

    End_VTS = False
    plugin_info = {
        "plugin_name": "trigger hotkey",
        "developer": "OverHome",
        "authentication_token_path": "./VTS_tools/examples/pyvts_token.txt",
    }
    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    #await myvts.request_authenticate_token()  # get token
    await myvts.read_token() 
    await myvts.request_authenticate()  # use token

    motion, expression_list = VTS_motion_MODE(emotion)
    
    hotkeyname_list = ['Scene1.motion3.json', 'rotation.motion3.json', 'yun.exp3.json', 
                       'kongbai.exp3.json', 'lei.exp3.json', 'lianhei.exp3.json', 
                       'lianhong.exp3.json', 'lianqing.exp3.json', 'xie.exp3.json', 
                       'xingxingyan.exp3.json', 'yuanquanyan.exp3.json', 'yun.exp3.json', 
                       'han.exp3.json', 'duzui.exp3.json', 'guzui.exp3.json', 
                       '', 'xianhua.exp3.json', 'jiantou.exp3.json', 
                       'Scene1.exp3.json', 'aixinyan.exp3.json', 'huatong.exp3.json']
                            
    hotkey_list = ['cd5e3fa233cf4e69ad7e84d8f5bcd455', 'b2510ff2d8c246d68a8177aed5a1b057', '05589e7e73e74df5b384fe19df522ce3', 
                   'fcd2408f3a3747d2b3846bdffb7f1f0a', '9d522b99d018434d810e675bddadb811', '246ccfb8078f4a09895383a03d5be1b5', 
                   '50e7df6cb3864e288127d145e09107be', 'b921ee641ef142c2a2093a53b045fa7c', 'ca45ed4ae7a640e4b5cb3f364853535b', 
                   '8d7315ded7e9481380271f99b6c8d1b2', '0c7b86c3db1645709735585623c4a7be', 'ff668ae9bc3a493fb911e66d74358457', 
                   '62e29735a8fd419991cc00e4450c5073', 'a80cc371c668486ab253507977321129', '81179c41ddc8417596d86ae31dd00598', 
                   '7ee3db7432d14e4a97bd4ec10a30221a', 'e3b4ab4ce89c4d01bac5f884b64b8a04', 'e5e9b2c720df4335afe5db6fc56a4481', 
                   '1eb4c74f16fa483eb07128ec058a3230', 'd0ffd701889645cd88106546a5eab26b', 'ff9ad1e8db774ab1aacb0bd4488e2144']

    print('Vtuber Move Now!')
    if status == True:
        #motion mode
        if motion != -1:
            send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[motion])
            await myvts.request(send_hotkey_request) 
    
    #expression mode
    if expression_list != -1:
        for i in range(expression_list):
            send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[i])
            await myvts.request(send_hotkey_request) 

    await myvts.close()

# Vtube Studio Function Module
async def VTS_threading(hotkey):

    End_VTS = False
    plugin_info = {
        "plugin_name": "trigger hotkey",
        "developer": "OverHome",
        "authentication_token_path": "./VTS_tools/examples/pyvts_token.txt",
    }
    myvts = pyvts.vts(plugin_info=plugin_info)
    await myvts.connect()
    #await myvts.request_authenticate_token()  # get token
    await myvts.read_token() 
    await myvts.request_authenticate()  # use token

    
    hotkeyname_list = ['Scene1.motion3.json', 'rotation.motion3.json', 'yun.exp3.json', 
                       'kongbai.exp3.json', 'lei.exp3.json', 'lianhei.exp3.json', 
                       'lianhong.exp3.json', 'lianqing.exp3.json', 'xie.exp3.json', 
                       'xingxingyan.exp3.json', 'yuanquanyan.exp3.json', 'yun.exp3.json', 
                       'han.exp3.json', 'duzui.exp3.json', 'guzui.exp3.json', 
                       '', 'xianhua.exp3.json', 'jiantou.exp3.json', 
                       'Scene1.exp3.json', 'aixinyan.exp3.json', 'huatong.exp3.json']
                            
    hotkey_list = ['cd5e3fa233cf4e69ad7e84d8f5bcd455', 'b2510ff2d8c246d68a8177aed5a1b057', '05589e7e73e74df5b384fe19df522ce3', 
                   'fcd2408f3a3747d2b3846bdffb7f1f0a', '9d522b99d018434d810e675bddadb811', '246ccfb8078f4a09895383a03d5be1b5', 
                   '50e7df6cb3864e288127d145e09107be', 'b921ee641ef142c2a2093a53b045fa7c', 'ca45ed4ae7a640e4b5cb3f364853535b', 
                   '8d7315ded7e9481380271f99b6c8d1b2', '0c7b86c3db1645709735585623c4a7be', 'ff668ae9bc3a493fb911e66d74358457', 
                   '62e29735a8fd419991cc00e4450c5073', 'a80cc371c668486ab253507977321129', '81179c41ddc8417596d86ae31dd00598', 
                   '7ee3db7432d14e4a97bd4ec10a30221a', 'e3b4ab4ce89c4d01bac5f884b64b8a04', 'e5e9b2c720df4335afe5db6fc56a4481', 
                   '1eb4c74f16fa483eb07128ec058a3230', 'd0ffd701889645cd88106546a5eab26b', 'ff9ad1e8db774ab1aacb0bd4488e2144']
    
    print('Vtuber Move Now!')
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[hotkey])
    await myvts.request(send_hotkey_request)
    await myvts.close()
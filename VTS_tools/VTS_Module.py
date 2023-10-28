from VTS_tools.examples.vts_tools import Hotkeyrequire, send_hotkey_request, set_parameter_value
import pyvts
import threading

hotkeyname_list = ['OO眼.exp3.json', 'Scene1.exp3.json', '压扁.exp3.json', '堵嘴.exp3.json', '屑.exp3.json', 
 '恐怕.exp3.json', '星星眼.exp3.json', '汗.exp3.json', '爱心眼.exp3.json', '生气皱眉.exp3.json', 
 '箭头眼.exp3.json', '累.exp3.json', '脸红.exp3.json', '脸青.exp3.json', '脸黑.exp3.json', 
 '话筒.exp3.json', '鼓嘴.exp3.json', '@@眼.exp3.json', '上下摇摆10.motion3.json', 
 '快速眨眼5.motion3.json', '惊讶55.motion3.json']
hotkey_list = ['83a2d987f7064642b7a9d3640274333b', '06826505889b40678302597311c79911', '12ca15e78fe7421483691b167fe7482d', 'b1cd02db9cfa4b04bddb1ee48c326dae', '47a8088c7b6a415b8158c2f42b0485e2', 'edb893b80c294871b6635ae0b42d44e6', '0a7bf45151324c6d82ccdda5f34e4115', 'bee0edc6cf65491f9cc2e2bcd768ee2b', '7b849ad686b94e328a4c3748e19be7c6', 'bf102f7962dc47cd81de8c8366d39147', 'edfc753b78024779ad5bca0bf7f73f8e', 'e379e9d6b94d4ffe98d1e89dd7673843', 'a18ce5e4d0a144ac9b4a0805241048c8', '70f8c48382634faba50555b76940cd72', 'd2894537a77a43238df478324cd55a55', 'c292a2b25b424c48bf177e64db22cdc7', 'b6157183d1d94b1eaecfa8dd28522abe', '8ee59d635dd041ccb2335280cf7fff9d', 'e217ac7c24b540ebb72fdfe11d42479c', 'da76c120eb0745a9a2621a8c0ea4fde7', 'cf9269def5be447ea9b6c44a2ef34ef8']


hotkey = 0
#asyncio_VTS_thread = threading.Thread(target=lambda: asyncio.run(VTS_threading(hotkey)))
#asyncio_VTS_thread.start()

def VTS_motion_MODE(mode):
    # mode: happy / fear / anger / disgust / normal / love / sad  
    if mode == 'happy':
        motion = -1
        expression = [3] # xianhua
    elif mode == 'fear':
        motion = -1
        expression = [3] #kongbai
    elif mode == 'anger':
        motion = -1
        expression = [14]  # guzui
    elif mode == 'disgust':
        motion = -1
        expression = [5] # lianhei
    elif mode == 'normal':
        motion = 19 # rotation
        expression = -1 
    elif mode == 'love':
        motion = 19
        expression = [6, 18] #aixinyan lianhong
    elif mode == 'sad':
        motion = -1
        expression = [4] #lianlei liuhan
    else:
        motion = 19 # rotation
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
    print('motion:', motion, 'expression:', expression_list)
    
    print('Vtuber Move Now!')
    
    if expression_list != -1:
        #expression mode
        for i in range(len(expression_list)):
            send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[expression_list[i]])
            await myvts.request(send_hotkey_request)

    if status == True:
        #motion mode
        if motion != -1:
            send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[motion])
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
    
    print('Vtuber Move Now!')
    send_hotkey_request = myvts.vts_request.requestTriggerHotKey(hotkey_list[hotkey])
    await myvts.request(send_hotkey_request)
    await myvts.close()
import asyncio, pyvts
import time
import threading
import math
import random
import numpy as np

plugin_info = {
    "plugin_name": "trigger hotkey",
    "developer": "OverHome",
    "authentication_token_path": "./pyvts_token.txt",
}

global blick
# 0 normal 1 sleep 2 awake
global status
global trigger



#fit curve function
def order3curve(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0):
    t = t - t0
    y = y1 + (y1 - y0) * (t - T) ** 3 / T ** 3
    return y

def cos_fit_half(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0):
    t = t - t0
    y = (y0 + y1)/2 + ((y0 - y1)/2) * math.cos( math.pi * (t - t0) / T )
    return y

def cos_fit_full(t0 = 0, T = 1, y0 = 0, y1 = 0, t = 0, N = 1):
    t = t - t0
    y = (y0 + y1)/2 + ((y0 - y1)/2) * math.cos( 2 * N * math.pi * (t - t0) / T )
    return y

def cos_fun01(T0 = 0, T = 2, N = 5, t = 0):
    value = math.cos( 2 * N * math.pi * (t - T0) / T ) + 0.5
    return value

# main control data initial
def param_initia():
    parameter = {
        "parameterValues": [
            #{"id": "FaceAngleY", "weight": 1, "value": value*30}
        ]
    }
    data = {
        "faceFound": False,
        "mode": "set",
        "parameterValues": parameter["parameterValues"],
    }
    return data


def Eye_blick(t):
    # awake
    T = 0.3
    if t < T:
        value = cos_fun01(T0 = 0, T = T, N = 3, t = t)
    else:
        value = 1
    return value    
def Eye_normalmode(t0 = 0, T = 1, y0 = 0, y1 = 1, t = 0, N = 2):
    # normal
    if t < T:
        value = cos_fit_full(t0 = t0, T = T, y0 = y0, y1 = y1, t = t, N = N)
    else:
        value = y1
    return value    
        
# control param
def EyeOpenMotion(data, T, y1, y0, t, N):
    if status == 2:
        # awake
        value = Eye_blick(t)
    else:    
        # normal
        value = Eye_normalmode(T = T, y0 = y0, y1 = y1, t = t, N = N)

    data["parameterValues"].append({ "id": "EyeOpenRight", "weight": 1, "value": value })
    data["parameterValues"].append({ "id": "EyeOpenLeft", "weight": 1, "value": value })
    return data, value

def body_awake(param, data, T, y1, y0, t):
    # awake
    if param == "FaceAngleX":
        T = 0.5
        if t < T:
            value = (cos_fun01(T0 = 0, T = T, N = 3, t = t) - 0.5)*15
        else:
            value = 1
    else:
        if t < T:
            value = cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
        else:
            value = y1
    return value 

def BodyMotion(param, data, T, y1, y0, t):
    if status == 2:
        # awake
        value = body_awake(param, data, T, y1, y0, t)
    else:
        if t < T:
            value = cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
        else:
            value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value

def EyeBallMotion(param, data, T, y1, y0, t):
    if t < T:
        value = cos_fit_half(T = T, y0 = y0, y1 = y1, t = t)
    else:
        value = y1
    data["parameterValues"].append({ "id": param, "weight": 1, "value": value })
    return data, value


# consider value
def consider_body_motion(y1 = 0, max = 30, direction = 1):

    global status
    if status == 1:
        #sleep mode
        if direction > 0:
            y1_new = np.random.normal(max/2, 3)
        else:
            y1_new = np.random.normal(-max/2, 3)
    else:
        # nomral mode
        if y1 >= 0 : 
            y1_new = np.random.normal(-max/2, 10)
        elif y1 < 0:
            y1_new = np.random.normal(max/2, 10) #random.randint(0, 30)
        else:
            y1_new = np.random.normal(0, 10)
    return y1_new

def consider_EyeOpen_motion(mean = 0.75, bis = 1):
    global status
    if status == 1:
        EyeOpen1 = np.random.normal(0, 0.05)
    else:
        # nomral    
        EyeOpen1 = np.random.normal(mean, bis)
    return EyeOpen1

def SetParam_Normal_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]

    Xmax = 10
    Ymax = 10
    Zmax = 10

    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], max = Xmax)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], max = Ymax)
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], max = Zmax)

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)

    return param_list, T, blick_num

def Normal_Mode(param_list, T, blick_num, t):
        T_body = T
        FaceAngleX0 = param_list[0][0]
        FaceAngleX1 = param_list[0][1]
        FaceAngleY0 = param_list[1][0]
        FaceAngleY1 = param_list[1][1]
        FaceAngleZ0 = param_list[2][0]
        FaceAngleZ1 = param_list[2][1]
        EyeX0 = param_list[3][0]
        EyeX1 = param_list[3][1]
        EyeY0 = param_list[4][0]
        EyeY1 = param_list[4][1]
        EyeOpen0 = param_list[5][0] 
        EyeOpen1 = param_list[5][1]                    
        current_status = status
        T_eye = 1
        # Get the value of "start_parameter"
        data = param_initia()
        #control param
        #body
        data, param_list[0][3] = BodyMotion("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
        data, param_list[1][3] = BodyMotion("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
        data, param_list[2][3] = BodyMotion("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
        #Eye ball
        data, param_list[3][3] = EyeBallMotion("EyeRightX", data, T_body, EyeX1, EyeX0, t)
        data, param_list[4][3] = EyeBallMotion("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
        #Eye Open
        data, param_list[5][3] = EyeOpenMotion(data, T_eye, EyeOpen1, EyeOpen0, t, blick_num)
        return param_list, data, current_status

def SetParam_Sleep_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]
    
    Xmax = 0
    Ymax = 0
    Zmax = 30

    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], max = Xmax)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], max = Ymax)
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], max = Zmax)

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)

    return param_list, T, blick_num   

def Sleep_Mode(param_list, T, blick_num, t):
    T_body = T
    FaceAngleX0 = param_list[0][0]
    FaceAngleX1 = param_list[0][1]
    FaceAngleY0 = param_list[1][0]
    FaceAngleY1 = param_list[1][1]
    FaceAngleZ0 = param_list[2][0]
    FaceAngleZ1 = param_list[2][1]
    EyeX0 = param_list[3][0]
    EyeX1 = param_list[3][1]
    EyeY0 = param_list[4][0]
    EyeY1 = param_list[4][1]
    EyeOpen0 = param_list[5][0] 
    EyeOpen1 = param_list[5][1]                    
    current_status = status
    T_eye = 1
    # Get the value of "start_parameter"
    data = param_initia()
    #control param
    #body
    data, param_list[0][3] = BodyMotion("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
    data, param_list[1][3] = BodyMotion("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
    data, param_list[2][3] = BodyMotion("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
    #Eye ball
    data, param_list[3][3] = EyeBallMotion("EyeRightX", data, T_body, EyeX1, EyeX0, t)
    data, param_list[4][3] = EyeBallMotion("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
    #Eye Open
    data, param_list[5][3] = EyeOpenMotion(data, T_eye, EyeOpen1, EyeOpen0, t, blick_num)
    return param_list, data, current_status

def SetParam_Awake_Mode(param_list):

    # consider param
    param_list[5][0] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][1] = consider_EyeOpen_motion(mean = 0.75, bis = 0.3)
    param_list[5][0] = param_list[6][0]
    param_list[5][1] = param_list[6][1]

    param_list[0][0] = param_list[0][2]
    param_list[1][0] = param_list[1][2]
    param_list[2][0] = param_list[2][2]
    
    Xmax = 0
    Ymax = 0
    Zmax = 30

    param_list[0][1] = consider_body_motion(y1 = param_list[0][2], max = Xmax)
    param_list[1][1] = consider_body_motion(y1 = param_list[1][2], max = Ymax)
    param_list[2][1] = consider_body_motion(y1 = param_list[2][2], max = Zmax)

    param_list[3][0] = param_list[0][0]/30
    param_list[3][1] = param_list[0][1]/30
    param_list[4][0] = -param_list[1][0]/30
    param_list[4][1] = -param_list[1][1]/30

    blick_num = random.randint(0, 2)

    return param_list, T, blick_num   

def Awake_Mode(param_list, T, blick_num, t):
    T_body = T
    FaceAngleX0 = param_list[0][0]
    FaceAngleX1 = param_list[0][1]
    FaceAngleY0 = param_list[1][0]
    FaceAngleY1 = param_list[1][1]
    FaceAngleZ0 = param_list[2][0]
    FaceAngleZ1 = param_list[2][1]
    EyeX0 = param_list[3][0]
    EyeX1 = param_list[3][1]
    EyeY0 = param_list[4][0]
    EyeY1 = param_list[4][1]
    EyeOpen0 = param_list[5][0] 
    EyeOpen1 = param_list[5][1]                    
    current_status = status
    T_eye = 1
    # Get the value of "start_parameter"
    data = param_initia()
    #control param
    #body
    data, param_list[0][3] = BodyMotion("FaceAngleX", data, T_body, FaceAngleX1, FaceAngleX0, t)
    data, param_list[1][3] = BodyMotion("FaceAngleY", data, T_body, FaceAngleY1, FaceAngleY0, t)
    data, param_list[2][3] = BodyMotion("FaceAngleZ", data, T_body, FaceAngleZ1, FaceAngleZ0, t)
    #Eye ball
    data, param_list[3][3] = EyeBallMotion("EyeRightX", data, T_body, EyeX1, EyeX0, t)
    data, param_list[4][3] = EyeBallMotion("EyeRightY", data, T_body, EyeY1, EyeY0, t)     
    #Eye Open
    data, param_list[5][3] = EyeOpenMotion(data, T_eye, EyeOpen1, EyeOpen0, t, blick_num)
    return param_list, data, current_status


# main control function
async def send_info():
    global status
    global trigger
    global blick
    global T
    status = 0
    trigger = False
    blick = False

    param_list = np.zeros((7, 3))  #body 3, eyeball 2, eyeOpen 2, 

    # init vts object
    vts = pyvts.vts(plugin_info=plugin_info)

    # Connect
    await vts.connect()
    await vts.read_token()
    await vts.request_authenticate()  # use token

    #init value
    FaceAngleX_now = 0
    FaceAngleY_now = 0
    FaceAngleZ_now = 0

    T = 2
    T_body = 2

    while True:
        print('status:', status)
        t = 0

        if status == 0:
            param_list, T, blick_num = SetParam_Normal_Mode(param_list)
        if status == 1:
            param_list, T, blick_num = SetParam_Sleep_Mode(param_list)
        if status == 2:
            param_list, T, blick_num = SetParam_Awake_Mode(param_list)

        while t <= T:
            if status == 0:
                param_list, data, current_status = Normal_Mode(param_list, T, blick_num, t)  
            if status == 1:
                param_list, data, current_status = Sleep_Mode(param_list, T, blick_num, t)                       
            if status == 2:
                param_list, data, current_status = Awake_Mode(param_list, T, blick_num, t)  

            set_paraemter_value = await vts.request(
                vts.vts_request.BaseRequest("InjectParameterDataRequest", data=data)
            )  
            t += 0.015
            time.sleep(0.015)

            if trigger == True:
                trigger = False
                print('trigger')
                break
        if current_status == 2:
            status = 0
        


async def Trigger_time():
    global status
    global trigger

    time.sleep(5)
    print("sleep start")
    status = 1
    trigger = True
    time.sleep(5)
    print("sleep end")
    status = 2
    trigger = True



if __name__ == "__main__":

    sleep = threading.Thread(target=lambda: asyncio.run(Trigger_time()))
    controlMotionY = threading.Thread(target=lambda: asyncio.run(send_info()))
    controlMotionY.start()    
    sleep.start()    
    sleep.join()

    controlMotionY.join()
# Robótica Industrial
# Proyecto de Curso
# Ricardo Varas - Gabriel Ortiz
# PAO I - 2025 



# SETUP

import threading
import DobotDllType as dType
import math
import ast
import json
from time import sleep

#se crean definiciones para determinar errores en la comunicacion
CON_STR = {
    dType.DobotConnect.DobotConnect_NoError:  "DobotConnect_NoError",
    dType.DobotConnect.DobotConnect_NotFound: "DobotConnect_NotFound",
    dType.DobotConnect.DobotConnect_Occupied: "DobotConnect_Occupied"
    }

#Load Dll and get the CDLL object
api = dType.load()
#Connect Dobot
state = dType.ConnectDobot(api, "", 115200)
print("datos de retorno de conexion ",[state])
print("Id Robot ",[state[1]])
print("Connect status:",CON_STR[state[0]])

# Establecer posición HOME (de inicio)
dType.SetHOMEParams(api, 190, 0, 65, 0)  # Coordenadas (X, Y, Z, R)
dType.SetHOMECmd(api, temp=0, isQueued=1)
dType.SetQueuedCmdStartExec(api)
print("Robot configurado y en posición inicial.")

# Obtener variables articulares de la posición actual
dType.GetPose(api)

# verificar linear rail 

dType.GetDeviceWithL(api)

# CONVERTIR TRAYECTORIA DE .dobot 
# CORREGIDA
# LETRA "a"

trajectory_string = "[1.5, 542.5, 522.5, [539.5, 184.5, 10.774999999999972, 17.025, [[[539.5, 186.375], [539.925, 185.95], [541.175, 185.125], [542.0749999999999, 184.75], [543.175, 184.525], [544.475, 184.5], [545.975, 184.775], [548.4, 185.725], [549.6999999999999, 186.675], [550.1999999999999, 187.4], [550.275, 187.7], [550.275, 201.525]], [[550.15, 193.125], [543.8, 193.125], [543.225, 193.125], [541.875, 193.475], [541.15, 193.9], [540.4499999999999, 194.55], [539.9, 195.5], [539.5749999999999, 196.775], [539.525, 198.1], [539.75, 199.2], [540.175, 200.05], [540.75, 200.725], [542.125, 201.425], [543.4, 201.45], [545.3, 201.175], [547.025, 200.475], [550.15, 198.675]]]]]"
data = json.loads(trajectory_string)

original_strokes = data[3][4]
r_start = data[3][3]
studio_start_point = data[3][0:2]
real_anchor_point = [240.0, 0.0]

recalculated_strokes = []
for original_stroke in original_strokes:
    new_stroke = []
    for point in original_stroke:
        offset_x = point[0] - studio_start_point[0]
        offset_y = point[1] - studio_start_point[1]
        
        # Mantiene la rotación de 90°
        new_x = real_anchor_point[0] + offset_y
        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN FINAL! (signo cambiado a '+') ---
        new_y = real_anchor_point[1] + offset_x
        new_stroke.append([new_x, new_y])
    recalculated_strokes.append(new_stroke)
print("Trayectoria recalculada (ESTA SÍ 100%)")

# CONVERTIR TRAYECTORIA DE .dobot 

# "hola mundo"


trajectory_string = "[1.5, 767.5, 522.5, [705.5, 185.5, 125.75999999999996, 17.249999999999996, [[[705.5, 185.5], [705.5, 201.685]], [[705.5, 193.66], [705.785, 193.09], [706.58, 191.85999999999999], [707.165, 191.185], [707.855, 190.615], [708.65, 190.21], [709.55, 190.045], [710.405, 190.35999999999999], [711.08, 190.615], [711.59, 191.185], [711.98, 191.85999999999999], [712.4, 193.09], [712.505, 193.66], [712.505, 201.685]], [[721.505, 191.5], [720.95, 191.62], [719.72, 192.1], [719.06, 192.52], [718.475, 193.075], [718.055, 193.78], [717.875, 194.665], [717.845, 197.635], [717.875, 198.64], [717.905, 199.045], [718.28, 199.99], [718.7, 200.53], [719.36, 201.055], [720.275, 201.505], [721.505, 201.82], [722.78, 201.85], [723.8149999999999, 201.55], [724.64, 201.025], [725.255, 200.35], [726.005, 199.03], [726.2, 198.4], [726.2, 195.97], [726.14, 195.28], [725.96, 194.56], [725.615, 193.73499999999999], [725.06, 192.91], [724.22, 192.205], [723.05, 191.695], [721.505, 191.5]], [[732.86, 202.75], [732.86, 186.835]], [[738.86, 191.5], [739.115, 191.245], [739.865, 190.75], [740.405, 190.525], [741.0649999999999, 190.39], [741.845, 190.375], [742.745, 190.54], [744.2, 191.10999999999999], [744.98, 191.68], [745.28, 192.115], [745.325, 192.295], [745.325, 200.59]], [[745.25, 195.55], [741.4399999999999, 195.55], [741.095, 195.55], [740.285, 195.76], [739.85, 196.015], [739.43, 196.405], [739.1, 196.975], [738.905, 197.74], [738.875, 198.535], [739.01, 199.195], [739.265, 199.70499999999998], [739.61, 200.10999999999999], [740.435, 200.53], [741.2, 200.545], [742.34, 200.38], [743.375, 199.96], [745.25, 198.88]], [[763.325, 191.5], [763.325, 202.64499999999998]], [[763.325, 194.95], [764.885, 193.225], [766.265, 192.025], [766.9399999999999, 191.635], [767.54, 191.5], [768.095, 191.575], [768.65, 191.815], [769.64, 192.64], [770.015, 193.195], [770.27, 193.81], [770.375, 194.45499999999998], [770.3149999999999, 195.1], [770.06, 197.02], [769.925, 199.525], [769.88, 202.64499999999998]], [[770.3149999999999, 195.1], [770.75, 194.48499999999999], [771.8299999999999, 193.135], [772.52, 192.46], [773.225, 191.89], [773.9449999999999, 191.545], [774.605, 191.53], [775.76, 192.04], [776.66, 192.85], [777.275, 193.885], [777.545, 195.1], [777.575, 199.525], [777.545, 202.64499999999998]], [[783.575, 191.5], [783.575, 198.88], [783.8, 199.45], [784.535, 200.605], [785.105, 201.14499999999998], [785.84, 201.49], [786.74, 201.565], [787.8199999999999, 201.265], [789.62, 200.23], [790.535, 199.345], [790.88, 198.715], [790.925, 198.49]], [[790.88, 191.5], [790.9549999999999, 202.3]], [[796.9549999999999, 191.5], [796.9549999999999, 202.66]], [[796.9549999999999, 195.505], [797.435, 194.77], [798.635, 193.21], [799.385, 192.43], [800.165, 191.83], [800.9449999999999, 191.515], [801.305, 191.515], [801.65, 191.62], [802.79, 192.25], [803.615, 192.91], [803.915, 193.345], [804.125, 193.885], [804.335, 195.505], [804.365, 200.095], [804.335, 202.66]], [[816.365, 185.5], [816.365, 200.935]], [[816.365, 193.32999999999998], [815.99, 192.895], [815.015, 191.95], [813.68, 191.005], [812.9449999999999, 190.72], [812.1949999999999, 190.615], [811.505, 190.75], [810.92, 191.065], [810.05, 191.995], [809.525, 192.91], [809.36, 193.32999999999998], [809.225, 194.635], [809.165, 195.95499999999998], [809.225, 197.44], [809.48, 198.89499999999998], [810.005, 200.07999999999998], [810.395, 200.515], [810.89, 200.815], [811.475, 200.935], [812.1949999999999, 200.85999999999999], [813.605, 200.47], [814.61, 200.01999999999998], [815.345, 199.54], [815.8399999999999, 199.075], [816.305, 198.295], [816.365, 197.98]], [[826.5649999999999, 191.5], [826.01, 191.62], [824.78, 192.1], [824.12, 192.52], [823.535, 193.075], [823.115, 193.78], [822.935, 194.665], [822.905, 197.635], [822.935, 198.64], [822.9649999999999, 199.045], [823.3399999999999, 199.99], [823.76, 200.53], [824.42, 201.055], [825.3349999999999, 201.505], [826.5649999999999, 201.82], [827.8399999999999, 201.85], [828.875, 201.55], [829.6999999999999, 201.025], [830.3149999999999, 200.35], [831.0649999999999, 199.03], [831.26, 198.4], [831.26, 195.97], [831.1999999999999, 195.28], [831.02, 194.56], [830.675, 193.73499999999999], [830.12, 192.91], [829.28, 192.205], [828.11, 191.695], [826.5649999999999, 191.5]]]]]"
data = json.loads(trajectory_string)

original_strokes = data[3][4]
r_start = data[3][3]
studio_start_point = data[3][0:2]
real_anchor_point = [240.0, 0.0]

recalculated_strokes = []
for original_stroke in original_strokes:
    new_stroke = []
    for point in original_stroke:
        offset_x = point[0] - studio_start_point[0]
        offset_y = point[1] - studio_start_point[1]
        
        # Mantiene la rotación de 90°
        new_x = real_anchor_point[0] + offset_y
        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN FINAL! (signo cambiado a '+') ---
        new_y = real_anchor_point[1] + offset_x
        new_stroke.append([new_x, new_y])
    recalculated_strokes.append(new_stroke)
print("Trayectoria recalculada (ESTA SÍ 100%)")

# Seguir trayectoria 
hover_z = 20.0
#drawing_z = 0.0
drawing_z = -53.84

dType.SetPTPCommonParams(api, 80.0, 80.0, isQueued=1)

# Usar los trazos recalculados para el dibujo
for stroke in recalculated_strokes:
    start_point = stroke[0]
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVJXYZMode, start_point[0], start_point[1], hover_z, r_start, isQueued=1)
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, start_point[0], start_point[1], drawing_z, r_start, isQueued=1)

    for point in stroke[1:]:
        dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, point[0], point[1], drawing_z, r_start, isQueued=1)

    end_point = stroke[-1]
    dType.SetPTPCmd(api, dType.PTPMode.PTPMOVLXYZMode, end_point[0], end_point[1], hover_z, r_start, isQueued=1)

dType.SetQueuedCmdStartExec(api)
print("Ejecutando la secuencia de dibujo recalculada...")

last_index = dType.GetQueuedCmdCurrentIndex(api)[0]
while dType.GetQueuedCmdCurrentIndex(api)[0] < last_index:
    sleep(0.5)
print("¡Dibujo completado!")



#Desconeta el robot
dType.DisconnectDobot(api)

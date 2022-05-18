import os
from PyLTSpice.LTSpiceBatch import SimCommander
import numpy as np

celerite = 342
frequence = 300
longueurOnde = celerite/frequence
distanceEntreAntennes = longueurOnde/2
print(longueurOnde)

pointSource = [1000, 0/7] # polaire
pointsAntennes = [
    [distanceEntreAntennes/(np.sqrt(3)), 0],
    [distanceEntreAntennes/(np.sqrt(3)), 2*np.pi/3],
    [distanceEntreAntennes/(np.sqrt(3)), 4*np.pi/3],
]

def cylVersCart(point):
    return np.array([point[0]*np.cos(point[1]), point[0]*np.sin(point[1])])


phase1 = ((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[0]))) % longueurOnde) * (360/longueurOnde)
phase2 = ((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[1]))) % longueurOnde) * (360/longueurOnde)
phase3 = ((np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[2]))) % longueurOnde) * (360/longueurOnde)

# phase2 = (np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[1]))*360/longueurOnde) % 360
# phase3 = (np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[2]))*360/longueurOnde) % 360
print(phase1, phase2, phase3)

print('distances')
print(np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[0])))
print(np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[1])))
print(np.linalg.norm(cylVersCart(pointSource) - cylVersCart(pointsAntennes[2])))

LTC = SimCommander('SimuSonore.asc')
LTC.add_instructions(
    '.meas TRAN Amplitude1 PARAM (V(SortieCrete1))',
    '.meas TRAN Amplitude2 PARAM (V(SortieCrete2))',
    '.meas TRAN Amplitude3 PARAM (V(SortieCrete3))',
    '.meas TRAN AmplitudeFondMult1 PARAM (V(SortiePB1))',
    '.meas TRAN AmplitudeFondMult2 PARAM (V(SortiePB2))',

    '.meas TRAN dephasage1O PARAM arccos(2*AmplitudeFondMult1*1.13 / (Amplitude2*Amplitude1))',
    '.meas TRAN dephasage2O PARAM arccos(2*AmplitudeFondMult2*1.13 / (Amplitude3*Amplitude1))',
    f'.meas TRAN direction11O PARAM arcsin(-dephasage1O*{longueurOnde/distanceEntreAntennes}/(360))+60',
    f'.meas TRAN direction12O PARAM -(arcsin(-dephasage1O*{longueurOnde/distanceEntreAntennes}/(360)))+60',
    f'.meas TRAN direction21O PARAM arcsin(-dephasage2O*{longueurOnde/distanceEntreAntennes}/(360))-60',
    f'.meas TRAN direction22O PARAM -(arcsin(-dephasage2O*{longueurOnde/distanceEntreAntennes}/(360)))-60'
)

# LTC.set_parameter('Phase1', f'{{{phase1}}}')
# LTC.set_parameter('Phase2', f'{{{phase2}}}')
# LTC.set_parameter('Phase3', f'{{{phase3}}}')
# LTC.set_parameter('Frequence', f'{{{frequence}}}')

# LTC.add_instruction('.tran 0.3')

# LTC.run(run_filename='heh.net')
# LTC.wait_completion()
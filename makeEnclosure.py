from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

import math

IS_LABELED = True

MATERIAL_THICKNESS = 0.25 * inch
TAB_LENGTH = 0.75 * inch

VENTILATION_START = 1.0 * inch
VENTILATION_END = 7.0 * inch
VENTILATION_FREQ = 0.5 * inch
VENTILATION_WIDTH = 0.1 * inch
VENTILATION_DEPTH = 1.0 * inch
VENTILATION_IN = 0.45 * inch

def resetFont(c):
    c.setFont("Helvetica", 36)
    c.setFillColor((1.0, 0.0, 0.0))

def drawLabel(c, x, y, s):
    if IS_LABELED:
        resetFont(c)
        c.drawString(x, y, s)

def makeBoxJointCutouts(c, x1, y1, x2, y2, isRight, offset = 0):
    c.saveState()

    c.translate(x1, y1)
    deltaY = y2 - y1
    deltaX = x2 - x1

    angleRad = math.atan2(deltaY, deltaX)
    angleDeg = angleRad * 180.0 / math.pi
    c.rotate(angleDeg)
    dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)

    mul = 1
    if isRight:
        mul = -1
    
    elapsed = -(offset * 2 * TAB_LENGTH)
    while elapsed < dist:
        if elapsed + TAB_LENGTH >= dist:
            break
        if elapsed + 2 * TAB_LENGTH < 0:
            elapsed += 2 * TAB_LENGTH
            continue
        
        p = c.beginPath()
        ne = max(0, min(dist, elapsed + TAB_LENGTH))
        p.moveTo(ne, 0)
        ne = max(0, min(dist, elapsed + TAB_LENGTH))
        p.lineTo(ne, MATERIAL_THICKNESS * mul)
        ne = max(0, min(dist, elapsed + 2 * TAB_LENGTH))
        p.lineTo(ne, MATERIAL_THICKNESS * mul)
        p.lineTo(ne, 0)
        c.drawPath(p, stroke = 1)
        elapsed += 2 * TAB_LENGTH
        
    c.restoreState()

def makeVentilationCutouts(c, x1, y1, x2, y2, isRight, depth):
    c.saveState()

    c.translate(x1, y1)
    deltaY = y2 - y1
    deltaX = x2 - x1

    angleRad = math.atan2(deltaY, deltaX)
    angleDeg = angleRad * 180.0 / math.pi
    c.rotate(angleDeg)
    dist = math.sqrt(deltaX * deltaX + deltaY * deltaY)

    mul = 1
    if isRight:
        mul = -1
    
    elapsed = 0
    while elapsed < VENTILATION_END:
        if elapsed + VENTILATION_FREQ >= VENTILATION_END:
            break
        if elapsed + VENTILATION_FREQ < VENTILATION_START:
            elapsed += VENTILATION_FREQ
            continue
        
        p = c.beginPath()
        ne = max(VENTILATION_START, min(VENTILATION_END, elapsed))
        p.moveTo(ne, 0)
        p.lineTo(ne, depth * mul)
        ne = max(VENTILATION_START, min(VENTILATION_END, elapsed + VENTILATION_WIDTH))
        p.lineTo(ne, depth * mul)
        p.lineTo(ne, 0)
        c.drawPath(p, stroke = 1)
        elapsed += VENTILATION_FREQ
        
    c.restoreState()

    

def rightSidePanel(c):
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, 4*inch)
    p.lineTo(8.5 * inch, 4 * inch)
    dx = 8.5 * inch
    dy = 2 * inch
    dh = math.sqrt(dx * dx + dy * dy)
    ux = dx / dh
    uy = dy / dh
    nx = 17 * inch - 2 * TAB_LENGTH * ux
    ny = 2 * inch + 2 * TAB_LENGTH * uy
    p.lineTo(nx, ny)
    p.moveTo(17 * inch, 2 * inch)
    p.lineTo(15 * inch, 0)
    p.lineTo(0, 0)
    c.drawPath(p, stroke=1)
    makeBoxJointCutouts(c, 0, 0, 0, 4 * inch, True, 0.5) # back
    makeBoxJointCutouts(c, 0, 4 * inch, 8.5 * inch, 4 * inch, True, 0.5) # top
    makeBoxJointCutouts(c, 17 * inch, 2 * inch, 8.5 * inch, 4 * inch, False, 0.5) # kb
    makeBoxJointCutouts(c, 17 * inch, 2 * inch, nx, ny, True, 0) # wrist rest
    makeBoxJointCutouts(c, 15 * inch, 0, 17 * inch, 2 * inch, False, 0.75) # chin
    makeBoxJointCutouts(c, 0, 0, 15 * inch, 0, False) # bottom
    makeVentilationCutouts(c, 0, 4 * inch, 8.5 * inch, 4 * inch, True, VENTILATION_DEPTH) 
    drawLabel(c, 0.5 * inch, 0.5* inch, "right panel --> f")

def leftSidePanel(c):
    p = c.beginPath()
    p.moveTo(0, 0)
    p.lineTo(0, 4*inch)
    p.lineTo(15 * inch, 4 * inch)
    p.lineTo(17 * inch, 2 * inch)
    dx = 8.5 * inch
    dy = 2 * inch
    dh = math.sqrt(dx * dx + dy * dy)
    ux = dx / dh
    uy = dy / dh
    nx = 17 * inch - 2 * TAB_LENGTH * ux
    ny = 2 * inch - 2 * TAB_LENGTH * uy
    p.moveTo(nx, ny)
    p.lineTo(8.5 * inch, 0)
    p.lineTo(0, 0)
    c.drawPath(p, stroke=1)
    makeBoxJointCutouts(c, 0, 4 * inch, 0, 0, False, 0.5) # back
    makeBoxJointCutouts(c, 15 * inch, 4*inch, 17 * inch, 2 * inch, True, 0.75) # chin
    makeBoxJointCutouts(c, 17 * inch, 2 * inch, nx, ny, False, 0) # wrist rest
    makeBoxJointCutouts(c, 17 * inch, 2 * inch, 8.5 * inch, 0, True, 0.5) # kb
    makeBoxJointCutouts(c, 0, 0, 8.5 * inch, 0, False, 0.5) # top
    makeBoxJointCutouts(c, 0, 4 * inch, 15 * inch, 4 * inch, True) # bottom
    makeVentilationCutouts(c, 0, 0, 8.5 * inch, 0, False, VENTILATION_DEPTH) 
    drawLabel(c, 0.5 * inch, 2.5* inch, "left panel --> f")

def lid(c):
    # 15 inches wide x 8.5 inches high
    c.rect(0, 0, 15 * inch, 8.5*inch)
    drawLabel(c, 0.5 * inch, 0.5* inch, "lid  V f")
    height = 8.5 * inch
    makeVentilationCutouts(c, 0, height, 0, 0, False, VENTILATION_IN)
    makeVentilationCutouts(c, 15 * inch, height, 15 * inch, 0, True, VENTILATION_IN)

def accessPanel(c):
    # 15 inches wide x 8.5 inches high,
    # minus one material width

    height = 8.5 * inch - MATERIAL_THICKNESS
    
    c.rect(0, 0, 15 * inch, height)
    # hole inset from outside
    c.roundRect(1*inch, 1*inch, 13 * inch, height - 2 * inch, 1*inch, stroke=True)

    makeBoxJointCutouts(c, 0, height, 0, 0, False)
    makeBoxJointCutouts(c, 15 * inch, height, 15 * inch, 0, True)
    makeBoxJointCutouts(c, 15 * inch, height, 0, height, False, 0.25) # back
    makeVentilationCutouts(c, 0, height, 0, 0, False, VENTILATION_IN)
    makeVentilationCutouts(c, 15 * inch, height, 15 * inch, 0, True, VENTILATION_IN)
    drawLabel(c, 2.5 * inch, 0.5* inch, "access panel  v f")

def wristRest(c):
    # 15 inches wide x 2 inch high
    c.rect(0, 0, 15 * inch, 2 * inch)
    makeBoxJointCutouts(c, 0, 0, 0, 2*inch, True)
    makeBoxJointCutouts(c, 15 * inch, 0, 15 * inch, 2*inch, False)
    drawLabel(c, 0.5 * inch, 0.5* inch, "wrist rest  V f")

def chin(c):
    # 15 inches wide x 2 * sqrt(2) inch high,
    # less two thicknesses of the material, for the front lip
    high = 2.0 * inch * math.sqrt(2.0) - 2 * MATERIAL_THICKNESS
    c.rect(0, 0, 15 * inch, high)

    handle_width = 6 * inch
    handle_height = 1.0 * inch
    handle_center_x = 15 * inch / 2.0
    handle_center_y = high / 2.0
    c.roundRect(handle_center_x - handle_width / 2, handle_center_y - handle_height / 2,
                handle_width, handle_height,
                handle_height / 2.0, stroke = 1)
    
    makeBoxJointCutouts(c, 0, 0, 0, high, True, 0.25)
    makeBoxJointCutouts(c, 15 * inch, 0, 15*inch, high, False, 0.25)
    drawLabel(c, 0.5 * inch, 0.5* inch, "chin  ^ u")

def keyboardTray(c):
    # 15 inches wide x sqrt(2^2 + 8.5^2) inch high
    high = math.sqrt(2.0 * 2.0 + 8.5 * 8.5) * inch
    c.rect(0, 0, 15 * inch, high)
    makeBoxJointCutouts(c, 0, 0, 0, high, True, 0)
    makeBoxJointCutouts(c, 15 * inch, 0, 15 * inch, high, False, 0)
    #drawLabel(c, 0.5 * inch, 0.5* inch, "keyboard tray  v f")
    # TODO make logo
    drawLabel(c, 5.5 * inch, high -1.5* inch, "logo goes here-ish")

def backPanel(c):
    # 15 inches wide x 4 inch high
    c.rect(0, 0, 15 * inch, 4 * inch)
    makeBoxJointCutouts(c, 0, 0, 0, 4 * inch, True)
    makeBoxJointCutouts(c, 15 * inch, 0, 15 * inch, 4 * inch, False)
    makeBoxJointCutouts(c, 0, 4 * inch, 15 * inch, 4 * inch, True, 0.75)
    makeBoxJointCutouts(c, 0, 0, 15 * inch, 0, False, 0.25)

    inset_x = 1.0 * inch
    horz_width = 1.5 * inch
    inset_top = 0.75 * inch
    slot_width = 0.75 * inch
    
    c.roundRect(inset_x, 4 * inch - inset_top - slot_width, horz_width, slot_width, slot_width / 2, stroke = 1)
    c.roundRect(15 * inch - inset_x - horz_width, 4 * inch - inset_top - slot_width, horz_width, slot_width, slot_width / 2, stroke = 1)

    inter_slot_width = 0.5 * inch
    slot_start = 2.75 * inch

    for i in range(8):
        x = slot_start + i * (slot_width + inter_slot_width)
        c.roundRect(x, inset_top, slot_width, 4 * inch - (2 * inset_top), slot_width / 2, stroke = 1)
        
    
    drawLabel(c, 0.5 * inch, 0.5* inch, "back panel  ^ u")

def rearBottom(c):
    # 15 inches wide x 10 inch high
    c.rect(0, 0, 15 * inch, 10 * inch)
    makeBoxJointCutouts(c, 0, 0, 0, 10 * inch, True, 0.5)
    makeBoxJointCutouts(c, 15 * inch, 0, 15 * inch, 10 * inch, False, 0.5)
    makeBoxJointCutouts(c, 0, 0, 15 * inch, 0, False, 0.75)
    drawLabel(c, 0.5 * inch, 0.5 * inch, "rear bottom  ^ f")
    
def frontBottom(c):
    # 15 inches wide x 5 inch high
    # minus one material thickness
    height = 5 * inch - MATERIAL_THICKNESS
    c.rect(0, 0, 15 * inch, height)

    # this is tricky. 10 inches were already used for the rear bottom,
    # so account for that.
    offset = 10 * inch / (2 * TAB_LENGTH) - 0.5
    makeBoxJointCutouts(c, 0, 0, 0, height, True, offset)
    makeBoxJointCutouts(c, 15 * inch, 0, 15 * inch, height, False, offset)
    drawLabel(c, 0.5 * inch, 0.5* inch, "front bottom  ^ f")

def allInOneGo():
    c = canvas.Canvas("appleIIenclosureComplete.pdf",
                      pagesize=(20*inch, 12*inch))

    #c.setStrokeColorRGB(0.9, 0.1, 0.1)
    c.setFont('Helvetica', 36)

    c.saveState()
    c.translate(0.5 * inch, 0.5 * inch)
    leftSidePanel(c)
    c.translate(0, 4.5 * inch)
    rightSidePanel(c)
    c.restoreState()
    c.showPage()

    c.saveState()
    c.translate(0.5 * inch, 0.5 * inch)
    lid(c)
    c.translate(0, 9 * inch)
    wristRest(c)
    c.restoreState()
    c.showPage()

    c.saveState()
    c.translate(0.5 * inch, 0.25 * inch)
    accessPanel(c)
    c.translate(0, 8.7 * inch)
    chin(c)
    c.restoreState()
    c.showPage()

    c.saveState()
    c.translate(0.5 * inch, 0.25 * inch)
    keyboardTray(c)
    c.restoreState()
    c.showPage()

    c.saveState()
    c.translate(0.5 * inch, 0.25 * inch)
    backPanel(c)
    c.translate(0, 4.5*inch)
    frontBottom(c)
    c.restoreState()
    c.showPage()

    c.saveState()
    c.translate(0.5 * inch, 0.25 * inch)
    rearBottom(c)
    c.restoreState()
    c.showPage()
    
    c.save()


if __name__ == "__main__":
    allInOneGo()
    
    

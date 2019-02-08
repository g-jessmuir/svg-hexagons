from PIL import Image
import math
im = Image.open("sample_image.jpg")
circumRadius = 17
cr = circumRadius
oR = round(cr / math.cos(math.radians(30)))

f = open("sample_image.svg", "w+")
f.truncate()
f.write('<?xml version="1.0" standalone="yes"?>' + '\n')
f.write('<parent xmlns="http://example.org" xmlns:svg="http://www.w3.org/2000/svg">' + '\n')
f.write('<svg:svg width="' + str(im.size[0]) + '" height="' + str(im.size[1]) + '" version="1.1">' + '\n')

def paintHexShape(cX, cY, cr, colour):
    points = [
        str(round(cX - cr / 2)) + ',' + str(cY - cr),
        str(round(cX + cr / 2)) + ',' + str(cY - cr),
        str(cX + oR) + ',' + str(cY),
        str(round(cX + cr / 2)) + ',' + str(cY + cr),
        str(round(cX - cr / 2)) + ',' + str(cY + cr),
        str(cX - oR) + ',' + str(cY)
    ]
    s = ' '
    pointsString = s.join(points)
    f.write('<svg:polygon fill="'  + colour + '" points="' + pointsString + '" />' + '\n')

def getAvgHexColour(x, y, cr):
    widthsTopHalf = [j * cr for j in range(1, cr + 1)]
    for i in range(cr):
        widthsTopHalf[i] += i
    widthsBotHalf = widthsTopHalf[::-1]
    allWidths = widthsTopHalf + widthsBotHalf
    colours = list()
    for i in range(cr * 2):
        tX = x - allWidths[i] / 2
        tY = y - cr + i
        ti = im.crop((tX, tY, tX + allWidths[i], tY + 1)).resize((1, 1))
        colours.append(ti.getpixel((0,0)))
    widthWeight = [i / allWidths[cr] for i in allWidths]
    returnColour = [0, 0, 0]
    for j in range(3):
        returnColour[j] = round(sum([colours[i][j] * widthWeight[i] for i in range(len(colours))]) / (cr * 2))
    tuple(returnColour)
    return '#{:02x}{:02x}{:02x}'.format(*returnColour)

def hexShapes(im, cr):
    startPointsX = [i for i in range(0, im.size[0] +  cr, round(oR + (cr / 2)) - 1)]
    startPointsY = [j for j in range(0, im.size[1] +  cr, 2 * cr - 1)]

    oddRow = True
    for i in startPointsX:
        for j in startPointsY:
            colour = getAvgHexColour(i, j, cr)
            if(oddRow):
                paintHexShape(i, j, cr, colour)
            else:
                paintHexShape(i, j - cr, cr, colour)
            print("Hexagon at " + str(i) + ',' + str(j) + " created")
        oddRow = not oddRow

hexShapes(im, cr)

f.write('</svg:svg>' + '\n')
f.write('</parent>')
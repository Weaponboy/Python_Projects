import cv2
import numpy as np
import math

image = cv2.imread("images/CameraV.jpg")
resized = cv2.resize(image, (600, 600))  

hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

lower_bound = np.array([10, 100, 130])  
upper_bound = np.array([35, 255, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)

kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

def find_intersection_2(line1, line2):

    (x1, y1), (x2, y2) = line1
    (x3, y3), (x4, y4) = line2

    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return None 

    px = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)) / denominator
    py = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)) / denominator

    return px, py


def find_slope(x1, y1, x2, y2):
    if x1 == x2:
        raise ValueError("Slope is undefined for vertical lines (x1 == x2).")
    return (y2 - y1) / (x2 - x1)

def returnExpectedSideLength(x1, y1, x2, y2):
    if x1 == x2:
        raise ValueError("Slope is undefined for vertical lines (x1 == x2).")
    return (y2 - y1) / (x2 - x1)

def find_intersection(p1, p2, p3, p4):
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    x4, y4 = p4

    # Compute determinants
    denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

    if denominator == 0:
        return None  # Lines are parallel or coincident

    # Compute intersection point
    x_numerator = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
    y_numerator = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)

    x = x_numerator / denominator
    y = y_numerator / denominator

    return (x, y)

def distance(point1: tuple, point2: tuple) -> float:
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

countourBig = []

for contour in contours:
    area = cv2.contourArea(contour)
    contour_length = len(contour)

    M = cv2.moments(contour)
    if M["m00"] != 0:
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
    else:
        cX, cY = 0, 0 

    # points = [tuple(pt[0]) for pt in contour]

    # cv2.circle(resized, points[0], 5, (0,0,255), -1)
    
    if cY > 300 and area > 1200:
        # Display contour area and length
        # cv2.putText(resized, f"A:{int(area)} L:{contour_length}", (cX, cY), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if area < 3500:
            # cv2.drawContours(resized, [contour], -1, (0, 255, 0), 2)
            test = 10
        else:
            cv2.drawContours(resized, [contour], -1, (255, 255, 0), 2)
            countourBig.append(contour)

    elif cY < 300 and area > 1000:
        # Display contour area and length
        # cv2.putText(resized, f"A:{int(area)} L:{contour_length}", (cX, cY), 
        #             cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        if area < 2500:
            # cv2.drawContours(resized, [contour], -1, (0, 255, 0), 2)
            test = 10
        else:
            cv2.drawContours(resized, [contour], -1, (255, 255, 0), 2)
            countourBig.append(contour)


contourProcess = countourBig[0]

points = [tuple(pt[0]) for pt in contourProcess]

GoingPositive = True
GoingNegitive = True

highestPoint = points[0]
# cv2.circle(resized, highestPoint, 2, (0,0,0), -1)
intercept1 = points[0]
intercept2 = points[0]

counter = 0

Slopes1Real = []
SlopeTotal1Real = 0
Slopes1 = []
SlopeTotal1 = 0
endPoint1 = 0

Slopes2Real = []
SlopeTotal2Real = 0
Slopes2 = []
SlopeTotal2 = 0
endPoint2 = 0

while (GoingPositive or GoingNegitive):

    print(counter)

    if GoingPositive:
        x1, y1 = points[counter]
        x2, y2 = points[counter+2]

        slopeInIf1 = (find_slope(x1, y1, x2, y2))

        # cv2.line(resized, (x2, y2), (x1, y1), (0, 255, 0), 2)

        SlopeTotal1 += slopeInIf1
        Slopes1.append(slopeInIf1)

        if abs(math.degrees(math.atan(SlopeTotal1/len(Slopes1))) - math.degrees(math.atan(slopeInIf1))) > 5 and counter > 5:
            GoingPositive = False
            endPoint1 = points[counter]
            print(abs(math.degrees(math.atan(SlopeTotal1/len(Slopes1))) - math.degrees(math.atan(slopeInIf1))))
        elif abs(math.degrees(math.atan(SlopeTotal1/len(Slopes1))) - math.degrees(math.atan(slopeInIf1))) < 5:
            SlopeTotal1Real += slopeInIf1
            Slopes1Real.append(slopeInIf1)

    if GoingNegitive:
        x1, y1 = points[len(points) - (counter+1)]
        x2, y2 = points[len(points) - (counter+3)]

        slopeInIf2 = (find_slope(x1, y1, x2, y2))

        # cv2.line(resized, (x2, y2), (x1, y1), (0, 255, 0), 2)

        SlopeTotal2 += slopeInIf2
        Slopes2.append(slopeInIf2)

        if abs(math.degrees(math.atan(SlopeTotal2/len(Slopes2))) - math.degrees(math.atan(slopeInIf2))) > 5 and counter > 5: 
            GoingNegitive = False
            endPoint2 = points[len(points) - (counter+1)]
            print(abs(math.degrees(math.atan(SlopeTotal2/len(Slopes2))) - math.degrees(math.atan(slopeInIf2))))
        elif abs(math.degrees(math.atan(SlopeTotal2/len(Slopes2))) - math.degrees(math.atan(slopeInIf2))) < 5:
            SlopeTotal2Real += slopeInIf2
            Slopes2Real.append(slopeInIf2)

    counter += 1

CounterSaved = counter

slope1 = -(SlopeTotal1Real/len(Slopes1Real))
slope2 = -(SlopeTotal2Real/len(Slopes2Real))

intercept1 = points[int(CounterSaved/2)]
intercept2 = points[len(points) - int(CounterSaved/2)]

x1 = int(intercept1[0] - (100))
x2 = int(intercept1[0] + (100))

y1 = int(intercept1[1] + (100 * slope1))
y2 = int(intercept1[1] - (100 * slope1))

# cv2.line(resized, (x2, y2), (x1, y1), (0, 255, 0), 2)

x3 = int(intercept2[0] - (100))
x4 = int(intercept2[0] + (100))

y3 = int(intercept2[1] + (100 * slope2))
y4 = int(intercept2[1] - (100 * slope2))

# cv2.line(resized, (x3, y3), (x4, y4), (0, 0, 255), 2)

line1 = ((x1, y1), (x2, y2))
line2 = ((x3, y3), (x4, y4))

intersection = find_intersection_2(line1, line2)

GoingPositive = True
GoingNegitive = True

highestPoint = points[0]

counter = 5

while (GoingPositive or GoingNegitive):

    print(counter)

    if GoingPositive:
        x1, y1 = intersection
        x2, y2 = points[counter]

        slopeInIf1 = (find_slope(x1, y1, x2, y2))

        if abs(math.degrees(math.atan(SlopeTotal1Real/len(Slopes1Real))) - math.degrees(math.atan(slopeInIf1))) > 5 and counter > 5:
            GoingPositive = False
            endPoint1 = points[counter]

    if GoingNegitive:
        x1, y1 = intersection
        x2, y2 = points[len(points) - (counter)]

        slopeInIf2 = (find_slope(x1, y1, x2, y2))

        print(abs(math.degrees(math.atan(SlopeTotal2Real/len(Slopes2Real))) - math.degrees(math.atan(slopeInIf2))))

        if abs(math.degrees(math.atan(SlopeTotal2Real/len(Slopes2Real))) - math.degrees(math.atan(slopeInIf2))) > 3 and counter > 5 and distance((x2, y2), intersection) > 30: 
            GoingNegitive = False
            endPoint2 = points[len(points) - (counter-2)]

    counter += 1

# cv2.circle(resized, (int(intersection[0]), int(intersection[1])), 4, (0,0,0), -1)

Side1X = (intersection[0] - endPoint1[0])*0.4
Side1Y = (endPoint1[1] - intersection[1])*0.4

Side2X = (intersection[0] - endPoint2[0])*0.4
Side2Y = (endPoint2[1] - intersection[1])*0.4

# Side1X = (intersection[0] - endPoint1[0])
# Side1Y = (endPoint1[1] - intersection[1])

# Side2X = (intersection[0] - endPoint2[0])
# Side2Y = (endPoint2[1] - intersection[1])

centerPoint1 = (int(intersection[0] - Side1X), int(intersection[1] + Side1Y))
centerPoint2 = (int(intersection[0] - Side2X), int(intersection[1] + Side2Y))

centerPoint = (int(intersection[0] - Side2X - Side1X), int(intersection[1] + Side2Y + Side1Y))

# cv2.circle(resized, (centerPoint1), 4, (0,0,0), -1)
# cv2.circle(resized, (centerPoint2), 4, (0,0,0), -1)

cv2.circle(resized, (centerPoint), 4, (255,0,255), -1)


# if intersection:

cv2.imshow("Detected Rectangles", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

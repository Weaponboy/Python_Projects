import cv2
import numpy as np
import math

# Load image
image = cv2.imread("images/CameraV.jpg")
resized = cv2.resize(image, (600, 600))  

hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

# Adjusted HSV range
lower_bound = np.array([10, 100, 130])  
upper_bound = np.array([35, 255, 255])

mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Morphological operations to clean up mask
kernel = np.ones((5, 5), np.uint8)
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

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


contourProcess = countourBig[2]

points = [tuple(pt[0]) for pt in contourProcess]

GoingPositive = True
cv2.circle(resized, points[0], 2, (0,0,0), -1)

highestPoint = points[0]
intercept = highestPoint[1]

counter = 1

Slopes = []
SlopeTotal = 0

while (GoingPositive):

    counter += 1
    print(counter)

    x1, y1 = points[counter]
    x2, y2 = points[counter+2]

    x3, y3 = points[len(points) - (counter+2)]
    x4, y4 = points[len(points) - counter]

    slope1 = (find_slope(x1, y1, x2, y2))
    slope2 = (find_slope(x3, y3, x4, y4))

    SlopeTotal += slope1
    Slopes.append(slope1)

    print("slope1: " + str(math.degrees(math.atan(slope1))))
    print("slope2: " + str(math.degrees(math.atan(slope2))))

    cv2.circle(resized, points[counter], 2, (0,0,255), -1)
    cv2.circle(resized, points[len(points) - counter], 2, (255,0,255), -1)

    if counter > 20:
        GoingPositive = False


# slope = SlopeTotal/len(Slopes)
# x1, x2 = 0, 499

# y1 = int(slope * x1 + intercept)
# y2 = int(slope * x2 + intercept)

# cv2.line(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)

cv2.imshow("Detected Rectangles", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

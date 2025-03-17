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
    """
    Finds the intersection point of two lines given their endpoints.
    
    Parameters:
    p1, p2 - (x, y) coordinates of the first line
    p3, p4 - (x, y) coordinates of the second line

    Returns:
    (x, y) intersection point as a tuple, or None if lines are parallel.
    """
    
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

countourBig = []

for contour in contours:
    area = cv2.contourArea(contour)
    contour_length = len(contour)  # Get the number of points in the contour

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


contourProcess = countourBig[5]

points = [tuple(pt[0]) for pt in contourProcess]

# for point in points:
#     cv2.circle(resized, point, 1, (0,0,255), -1)


GoingPositive = True
counter = 0

x1, y1 = points[counter]

cv2.circle(resized, points[counter], 2, (0,0,0), -1)

counter += 2
cv2.circle(resized, points[counter], 2, (0,0,255), -1)
x2, y2 = points[counter]

counter += 2
cv2.circle(resized, points[counter], 2, (0,255,255), -1)
x3, y3 = points[counter]

slope = math.degrees(math.atan(find_slope(x1, y1, x2, y2)))
slope2 = math.degrees(math.atan(find_slope(x1, y1, x3, y3)))

print(slope)
print(slope2)
print(abs(slope - slope2))

if abs(slope - slope2) > 3:
    counter = 2
    x1, y1 = points[counter]
    slope = slope2

p3 = points[counter]

failCounter = 0

lastValidCounter = counter

while (GoingPositive):
    counter += 2
    print(counter)
    cv2.circle(resized, points[counter], 2, (0,0,255), -1)
    x3, y3 = points[counter]

    slopeIncrement = math.degrees(math.atan(find_slope(x1, y1, x3, y3)))
    print(slopeIncrement)
    print(abs(slope - slopeIncrement))

    if abs(slope - slopeIncrement) > 3 and abs(slope - slopeIncrement) < 15 and failCounter <= 3:
        failCounter += 1
    elif abs(slope - slopeIncrement) > 3:
        if abs(slope - slopeIncrement) > 5:
            counter = lastValidCounter
            x3, y3 = points[counter]

            slopeIncrement = math.degrees(math.atan(find_slope(x1, y1, x3, y3)))
            cv2.circle(resized, points[counter], 2, (0,0,255), -1)
        GoingPositive = False
        p4 = points[counter]
        cv2.line(resized, (x1, y1), (x3, y3), (0, 255, 0), 2)
        cv2.circle(resized, points[counter], 2, (0,0,255), -1)
    else:
        lastValidCounter = counter

# GoingPositive = True
# counter = 0
# counter += 4
# x1, y1 = points[len(points) - counter]
# cv2.circle(resized, points[len(points) - counter], 2, (0,0,255), -1)

# counter += 2
# x2, y2 = points[len(points) - counter]

# slope = math.degrees(math.atan(find_slope(x1, y1, x2, y2)))

# print(counter)
# print(slope)

# p1 = points[len(points) - counter]
# failCounter = 0

# while (GoingPositive):
#     counter += 2
#     print(counter)
#     # cv2.circle(resized, points[counter], 5, (0,0,255), -1)
#     x3, y3 = points[len(points) - counter]

#     slopeIncrement = math.degrees(math.atan(find_slope(x1, y1, x3, y3)))
#     cv2.circle(resized, points[len(points) - counter], 2, (0,0,255), -1)
#     print(slopeIncrement)

#     if abs(slope - slopeIncrement) > 2 and abs(slope - slopeIncrement) < 6  and failCounter <= 1:
#         failCounter += 1
#     elif abs(slope - slopeIncrement) > 2:
#         if abs(slope - slopeIncrement) > 5:
#             counter -= 2
#             x3, y3 = points[len(points) - counter]

#             slopeIncrement = math.degrees(math.atan(find_slope(x1, y1, x3, y3)))
#             cv2.circle(resized, points[len(points) - counter], 2, (0,0,255), -1)

#         p2 = points[len(points) - counter]
#         GoingPositive = False
#         cv2.line(resized, (x1, y1), (x3, y3), (0, 255, 0), 2)
#         cv2.circle(resized, points[len(points) - counter], 2, (0,0,255), -1)

# # Find intersection
# intersection = find_intersection(p1, p2, p3, p4)

# if intersection:
#     # cv2.circle(resized, (int(intersection[0]), int(intersection[1])), 5, (255, 0, 255), -1)  # Red dot
#     newPoint1X = int((intersection[0] - p2[0])/2)
#     newPoint1Y = int((intersection[1] - p2[1])/2)
#     newPoint2 = (int(intersection[0] - (intersection[0] - p4[0])/2) - newPoint1X, int(intersection[1] - (intersection[1] - p4[1])/2) - newPoint1Y)
#     # cv2.circle(resized, newPoint1, 5, (255, 0, 0), -1)
#     cv2.circle(resized, newPoint2, 5, (255, 0, 255), -1)



# x3, y3 = points[len(points) - 6]

# cv2.line(resized, (x1, y1), (x2, y2), (0, 255, 0), 2)
# cv2.line(resized, (x1, y1), (x3, y3), (0, 255, 0), 2)

# slope = find_slope(x1, y1, x2, y2)

# print(slope)
# cv2.drawContours(resized, [contourProcess], -1, (255, 0, 0), 2)

cv2.imshow("Detected Rectangles", resized)
cv2.waitKey(0)
cv2.destroyAllWindows()

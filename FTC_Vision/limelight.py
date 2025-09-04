import cv2
import numpy as np
import math
import time

isScanning = True
AlColor = True
finished = True
YVelo = 0
XVelo= 0
start = 0
start_time = 0
elapsed_ms = 0

x = 0
y = 0
w = 0
h = 0

detections = []

llrobotLocal = [0, 0, 0, 0, 0, 0, 0, 0]

def runPipeline(image, llrobot):

    global detections
    detections.clear() 
    global finished
    global XVelo
    global YVelo
    global elapsed, AlColor, x, y, w, h, start_time, elapsed_ms
    
    llrobot = [0, 1, 82.5, 100, 0, 22, 0, 0]

    global llrobotLocal
    llrobotLocal = llrobot
    
    isScanning = True
    AlColor = llrobot[1] > 0
    Red = llrobot[6] > 0

    llpython = [0, 0, 0, 0, 0, 0, 0, 0]

    img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    x, y, w, h = 140, 120, 360, 340 
    roiImage = img_hsv[y:y+h, x:x+w]

    if (AlColor):

        if Red: 
            lower_bound_red = (140, 80, 140) 
            upper_bound_red = (180, 255, 255)

            img_threshold = cv2.inRange(roiImage, lower_bound_red, upper_bound_red)

            contours, _ = cv2.findContours(img_threshold, 
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        else:
            lower_bound_blue = (30, 120, 100) 
            upper_bound_blue = (150, 255, 255)

            img_threshold = cv2.inRange(roiImage, lower_bound_blue, upper_bound_blue)

            contours, _ = cv2.findContours(img_threshold, 
                                cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
    contours, _ = cv2.findContours(img_threshold, 
                                    cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        # Scale each point in the contour
        area = cv2.contourArea(contour)

        adjusted = contour.astype(float)  # Convert to float for scaling
        # adjusted[:, :, 0] *= scale_x  # Scale x coordinates
        # adjusted[:, :, 1] *= scale_y  # Scale y coordinates
        # Shift by the ROI offset (x, y)
        adjusted[:, :, 0] += x
        adjusted[:, :, 1] += y
        # adjusted_contours.append(adjusted.astype(np.int32))
        if area > 300:
            cv2.drawContours(image, adjusted.astype(np.int32), -1, (0, 255, 0), 2)  # Green contours with thickness 2

    largestContour = np.array([[]])

    XVelo = llrobot[0] 
    YVelo = llrobot[7] 

    if isScanning:
        finished = False
        global start
        start = time.time()
        
        llpython = [0, 0, 0, 0, 0, 0, 0, 0]

        if len(contours) > 0:
    
            drawRotatedBoundingBoxes(image, contours)

            sorted_array = []

            sorted_array = sort_close(detections)

            fieldPositions = convert_positions_to_field_positions(llrobot[5], sorted_array, (640, 480), 87.5)

            if len(fieldPositions) > 0:
                sorted_objects = fieldPositions
                
                # print(len(fieldPositions))

                # for x in fieldPositions:
                #     print(x.target_point)

                if len(sorted_objects) > 1:
                    llpython = [(sorted_objects[0].target_point[0]), (sorted_objects[0].target_point[1]), (sorted_objects[0].angle), (sorted_objects[1].target_point[0]), (sorted_objects[1].target_point[1]), (sorted_objects[1].angle), 0, 0]
                elif len(sorted_objects) > 0:
                    llpython = [(sorted_objects[0].target_point[0]), (sorted_objects[0].target_point[1]), (sorted_objects[0].angle), 0, 0, 0, 0, 0]
                
    return largestContour, image, llpython
    

def sort_far(detection_data_array):
    sorted_array = sorted(detection_data_array, key=lambda data: data.target_point[1])
    return sorted_array

def sort_close(detection_data_array):
    sorted_array = sorted(detection_data_array, key=lambda data: data.target_point[1], reverse = True)
    return sorted_array


def drawRotatedBoundingBoxes(image, contours):
    for contour in contours:
        area = cv2.contourArea(contour)
        
        M = cv2.moments(contour)

        if M["m00"] != 0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            # if area > 500:
            #     cv2.putText(image, f"Value: {area:.2f}", (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)
                
        if area > 400 and cY > 0 and cY < 85 and area < 1400:

            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            angle = rect[2]

            is_width_longer = rect[1][0] > rect[1][1]
            angle = rect[2]

            if not is_width_longer:
                angle += 90

            if angle > 90:
                angle -= 180

            xadj = int(calculate_adjustment(cY + y, 480, 0, 0, 15));

            obj2 = DetectionData(0, (cX + x, cY-xadj + y), angle)

            # print((cX, cY+xadj))

            detections.append(obj2)

            cv2.circle(image, (cX  + x, (cY-xadj  + y)), 5, (255, 255, 0), -1)
            # cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

        elif area > 600 and cY > 84 and cY < 190 and area < 2900:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            angle = rect[2]

            is_width_longer = rect[1][0] > rect[1][1] 
            angle = rect[2]

            if not is_width_longer:
                angle += 90

            if angle > 90:
                angle -= 180

            xadj = int(calculate_adjustment(cY + y, 480, 0, 0, 15));

            obj2 = DetectionData(0, (cX + x, cY-xadj + y), angle)

            # print((cX, cY+xadj))

            detections.append(obj2)

            cv2.circle(image, (cX  + x, (cY-xadj  + y)), 5, (255, 255, 0), -1)
            # cv2.drawContours(image, [box], 0, (0, 255, 0), 2) 

        elif area > 1100 and cY > 189 and cY < 275 and area < 3650:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            angle = rect[2]

            is_width_longer = rect[1][0] > rect[1][1] 
            angle = rect[2]

            if not is_width_longer:
                angle += 90

            if angle > 90:
                angle -= 180

            xadj = int(calculate_adjustment(cY + y, 480, 0, 0, 15));

            obj2 = DetectionData(0, (cX + x, cY-xadj + y), angle)

            # print((cX, cY+xadj))

            detections.append(obj2)

            cv2.circle(image, (cX  + x, (cY-xadj  + y)), 5, (255, 0, 255), -1)
            # cv2.drawContours(image, [box], 0, (0, 255, 0), 2) 
        elif area > 1300 and cY > 274 and cY < h and area < 3900:
            rect = cv2.minAreaRect(contour)
            box = cv2.boxPoints(rect)
            box = np.int0(box)

            angle = rect[2]

            is_width_longer = rect[1][0] > rect[1][1] 
            angle = rect[2]

            if not is_width_longer:
                angle += 90

            if angle > 90:
                angle -= 180

            xadj = int(calculate_adjustment(cY + y, 480, 0, 0, 15));

            obj2 = DetectionData(0, (cX + x, cY-xadj + y), angle)

            # print((cX, cY+xadj))

            detections.append(obj2)

            cv2.circle(image, (cX  + x, (cY-xadj  + y)), 5, (255, 0, 0), -1)
            # cv2.drawContours(image, [box], 0, (0, 255, 0), 2) 
     
    return image

class DetectionData:
    def __init__(self, read_time, target_point, angle):
        self.read_time = read_time
        self.target_point = target_point
        self.angle = angle

def convert_positions_to_field_positions(slide_position, detections, ROI, view_size_cm_y_axis):

    global Ydist, Xdist

    #constants
    FovAngle = 42.8
    belowAngle = 32.2
    angleAtBottom = 58

    smallerDualAngle = (180 - FovAngle) / 2

    pivot_height = slide_position + 42.5 - 13.5
    bottomSide = math.tan(math.radians(belowAngle)) * pivot_height
    first_hypot = math.sqrt((pivot_height * pivot_height) + (bottomSide * bottomSide))

    detectionConeCloseBottomAngle = 180  - angleAtBottom 

    # detectionLength = (first_hypot * math.sin(math.radians(FovAngle))) / math.sin(math.radians(180 - FovAngle - detectionConeCloseBottomAngle))+15
    pixelDetectionLength = (first_hypot * (math.sin(math.radians(FovAngle))) / math.sin(math.radians(smallerDualAngle)))

    field_detections = []

    Counter = 0

    for detection in detections:

        if Counter > 5:
            break

        # print(Counter)

        46
        61

        if len(llrobotLocal) > 4:
            center_point = 320

            y_extra = calculate_adjustment(detection.target_point[1], 480, 0.565, 0, 1.565)

            pixels_to_cm_rel_x = pixelDetectionLength / ROI[1]
            pixels_to_cm_rel_y = view_size_cm_y_axis / ROI[0]

            rel_y_position = 0

            if detection.target_point[0] > center_point:
                rel_y_position = (((detection.target_point[0]) - center_point) * pixels_to_cm_rel_y) * y_extra
            elif detection.target_point[0] < center_point:
                rel_y_position = (((detection.target_point[0]) - center_point) * pixels_to_cm_rel_y) * y_extra

            rel_y_position += 2.5

            rel_x_position = ((480 - detection.target_point[1]) * pixels_to_cm_rel_x)
            target_point = rel_x_position

            angleInDetectionCone = math.degrees(math.asin((target_point * math.sin(math.radians(smallerDualAngle))) / first_hypot))
            intersectionAngle = 180 - smallerDualAngle - angleInDetectionCone

            topAngleSmallDetectionTri = 180 - intersectionAngle
            other_inside_angle = 180 - smallerDualAngle - angleAtBottom

            real_world_position = target_point * (math.sin(math.radians(topAngleSmallDetectionTri)) / math.sin(math.radians(180 - other_inside_angle - topAngleSmallDetectionTri)))

            rel_x_position = real_world_position + (bottomSide - 8)

            global_x = rel_x_position * math.cos(math.radians(llrobotLocal[4])) - rel_y_position * math.sin(math.radians(llrobotLocal[4]))
            global_y = rel_x_position * math.sin(math.radians(llrobotLocal[4])) + rel_y_position * math.cos(math.radians(llrobotLocal[4]))
            
            elapsed = (25) / 1000

            if YVelo > 0:
                Ydist = (YVelo * elapsed) + ((0.5 * (-280)) * (elapsed * elapsed))
            else:
                Ydist = (YVelo * elapsed) + ((0.5 * (280)) * (elapsed * elapsed))

            if YVelo > 0:
                Xdist = (XVelo * elapsed) + ((0.5 * (-225)) * (elapsed * elapsed))
            else:
                Xdist = (XVelo * elapsed) + ((0.5 * (225)) * (elapsed * elapsed))


            globalX = llrobotLocal[2] + global_x 
            globalY = llrobotLocal[3] + global_y

            obj2 = DetectionData(detection.read_time, (globalX, globalY), detection.angle)

            if abs(detection.angle) > 60:
                yCloserExclude = 203
            else:
                yCloserExclude = 192

            if 17.8 > rel_y_position > -17.8 and 5 < real_world_position < 65 and globalY < yCloserExclude:
                if globalX > 190:
                    field_detections.append(obj2)
                elif globalX < 185 and globalY > 175:
                    field_detections.append(obj2)    

                     
        # field_detections.append(DetectionData(detection.read_time, (llrobotLocal[2] + global_x, llrobotLocal[3] + global_y), detection.angle))


    return field_detections
    finished = True

def calculate_adjustment(d, d1, x1, d2, x2):
    m = (x2 - x1) / (d2 - d1)
    return m * (d - d1) + x1
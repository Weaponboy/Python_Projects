import cv2
import numpy as np

# Load and resize the image
image = cv2.imread("images/CameraV.jpg")
resized = cv2.resize(image, (600, 600))

# Convert to HSV
hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)

# Define color range and create mask
lower_bound = np.array([10, 100, 130])  
upper_bound = np.array([35, 255, 255])
mask = cv2.inRange(hsv, lower_bound, upper_bound)

# Get original colors where the mask is white
result = cv2.bitwise_and(resized, resized, mask=mask)

# Convert the result to grayscale for edge detection
gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

# Apply Canny edge detection
edges = cv2.Canny(gray, 50, 150)  # Adjust thresholds as needed

# # Dilate the edges to make them thicker
# kernel = np.ones((3, 3), np.uint8)  # Kernel size can be adjusted
# dilated = cv2.dilate(edges, kernel, iterations=1)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Draw contours on a copy of the original image
contour_image = resized.copy()
cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 2)

# Print the number of detected contours
print(f"Number of contours detected: {len(contours)}")

# Display images
cv2.imshow("Dilated Edges", edges)
cv2.imshow("Contours", contour_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

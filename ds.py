import cv2
import numpy as np

def detect_similar_objects(image_path, threshold_area=500, threshold_similarity=0.8):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to create a binary image
    _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

    # Find contours in the binary image
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Filter contours based on area
    filtered_contours = [contour for contour in contours if cv2.contourArea(contour) > threshold_area]

    # Store the contours as arrays
    shape_arrays = []
    for contour in filtered_contours:
        contour_array = contour.squeeze(axis=1)  # Remove redundant axis
        shape_arrays.append(contour_array)

    # Draw the filtered contours on the image
    cv2.drawContours(img, filtered_contours, -1, (0, 255, 0), 2)

    # Show the image with the detected contours
    cv2.imshow('Similar Objects', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return shape_arrays

# Set the path to your image
image_path = 'output.jpg'

# Detect similar objects based on shape and get the contour arrays
contour_arrays = detect_similar_objects(image_path)

# Save the contour arrays to a text file
file_path = 'contour_arrays.txt'
with open(file_path, 'w') as file:
    for i, contour_array in enumerate(contour_arrays):
        file.write(f"Contour {i+1}:\n")
        np.savetxt(file, contour_array, delimiter=',', fmt='%d')
        file.write('\n')
import cv2
import numpy as np

def detect_similar_objects(image_path, threshold_area=500, threshold_similarity=0.8):
    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding to create a binary image
    # _, binary = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)
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

    # Draw the filtered contours and add text numbers
    for i, contour in enumerate(filtered_contours):
        cv2.drawContours(img, [contour], -1, (0, 255, 0), 2)
        # Find the center of the contour
        M = cv2.moments(contour)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # Add text number at the center
        cv2.putText(img, str(i+1), (cX, cY), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show the image with the detected contours and text numbers
    cv2.imshow('Similar Objects', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return shape_arrays

def check_similarity(shape_arrays, threshold_similarity=0.55):
    similar_shapes = []
    for i in range(len(shape_arrays)):
        similar_indices = [i]
        for j in range(i + 1, len(shape_arrays)):
            if compare_shapes(shape_arrays[i], shape_arrays[j], threshold_similarity):
                similar_indices.append(j)
        if len(similar_indices) > 1:
            similar_shapes.append(similar_indices)
    return similar_shapes

def compare_shapes(shape1, shape2, threshold_similarity=0.25):
    similarity = cv2.matchShapes(shape1, shape2, cv2.CONTOURS_MATCH_I1, 0)
    return similarity < threshold_similarity

# Set the path to your image
image_path = 'output.jpg'

# Detect similar objects based on shape and get the contour arrays
contour_arrays = detect_similar_objects(image_path)

# Check similarity between shape arrays
similar_shapes = check_similarity(contour_arrays)

# Write shape arrays to a file
file_path = 'shape_arrays.txt'
with open(file_path, 'w') as file:
    for i, shape_array in enumerate(contour_arrays):
        file.write(f"Shape {i+1}:\n")
        np.savetxt(file, shape_array, delimiter=',', fmt='%d')
        file.write('\n')

# Write similar shapes to a file
file_path = 'similar_shapes.txt'
with open(file_path, 'w') as file:
    for indices in similar_shapes:
        file.write('Similar Shapes: ')
        for index in indices:
            file.write(f'Shape {index + 1} ')
        file.write('\n')

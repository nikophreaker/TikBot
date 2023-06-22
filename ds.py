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

# Load the sliced captcha image: inner circle and outer circle
inner_circle_image = cv2.imread('inner_image.png', cv2.IMREAD_GRAYSCALE)
outer_circle_image = cv2.imread('outer_image.png', cv2.IMREAD_GRAYSCALE)

# Determine the maximum dimensions
max_height = max(inner_circle_image.shape[0], outer_circle_image.shape[0])
max_width = max(inner_circle_image.shape[1], outer_circle_image.shape[1])

# Resize the images to a common size
resized_inner_circle = cv2.resize(inner_circle_image, (max_width, max_height))
resized_outer_circle = cv2.resize(outer_circle_image, (max_width, max_height))

# Pad the smaller image to match the dimensions of the larger image
padded_inner_circle = cv2.copyMakeBorder(resized_inner_circle, 0, max_height - resized_inner_circle.shape[0], 0, max_width - resized_inner_circle.shape[1], cv2.BORDER_CONSTANT, value=0)
padded_outer_circle = cv2.copyMakeBorder(resized_outer_circle, 0, max_height - resized_outer_circle.shape[0], 0, max_width - resized_outer_circle.shape[1], cv2.BORDER_CONSTANT, value=0)

# Find the rotation angle of each piece using image moments
inner_moments = cv2.moments(padded_inner_circle)
inner_angle = np.degrees(np.arctan2(inner_moments['mu11'], inner_moments['mu20'] - inner_moments['mu02']) / 2)

outer_moments = cv2.moments(padded_outer_circle)
outer_angle = np.degrees(np.arctan2(outer_moments['mu11'], outer_moments['mu20'] - outer_moments['mu02']) / 2)

# Calculate the angle difference between the two pieces
angle_diff = inner_angle - outer_angle

# Rotate the outer circle piece to match the rotation of the inner circle piece
rotation_matrix = cv2.getRotationMatrix2D((max_width // 2, max_height // 2), angle_diff, 1)
synchronized_outer_circle = cv2.warpAffine(padded_outer_circle, rotation_matrix, (max_width, max_height))

# Display the synchronized captcha image
synchronized_image = cv2.addWeighted(padded_inner_circle, 0.5, synchronized_outer_circle, 0.5, 0)
cv2.imshow('Synchronized Captcha', synchronized_image)
cv2.waitKey(0)
cv2.destroyAllWindows()




# # Detect similar objects based on shape and get the contour arrays
# contour_arrays = detect_similar_objects(image_path)

# # Set the path to your image
# image_path = 'output.jpg'

# # Save the contour arrays to a text file
# file_path = 'contour_arrays.txt'
# with open(file_path, 'w') as file:
#     for i, contour_array in enumerate(contour_arrays):
#         file.write(f"Contour {i+1}:\n")
#         np.savetxt(file, contour_array, delimiter=',', fmt='%d')
#         file.write('\n')
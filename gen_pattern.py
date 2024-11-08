import numpy as np
import cv2
import os

# Create output directory if it doesn't exist
output_dir = 'calibration_images'
os.makedirs(output_dir, exist_ok=True)

# Parameters for the checkerboard pattern
checkerboard_size = (8, 8)  # Number of inner corners per row and column
square_size = 200  # Size of squares in pixels
board_width, board_height = checkerboard_size[0] * square_size, checkerboard_size[1] * square_size

# Generate a clearer checkerboard pattern
checkerboard = np.zeros((board_height, board_width), dtype=np.uint8)

# Fill with alternating black and white squares
for i in range(checkerboard_size[1]):
    for j in range(checkerboard_size[0]):
        if (i + j) % 2 == 0:
            checkerboard[i * square_size: (i + 1) * square_size,
                         j * square_size: (j + 1) * square_size] = 255

# Save the original checkerboard image for testing
cv2.imwrite(os.path.join(output_dir, 'checkerboard_test.png'), checkerboard)

# Generate 50 calibration images with slight variations
for img_num in range(50):
    # Create a copy of the checkerboard to apply transformations
    transformed_checkerboard = checkerboard.copy()

    # Apply random rotation between -30 and +30 degrees
    angle = np.random.uniform(-30, 30)
    M = cv2.getRotationMatrix2D((board_width // 2, board_height // 2), angle, 1.0)
    transformed_checkerboard = cv2.warpAffine(transformed_checkerboard, M, (board_width, board_height))

    # Add random scaling between 90% and 110%
    scale_factor = np.random.uniform(0.9, 1.1)
    scaled_width = int(board_width * scale_factor)
    scaled_height = int(board_height * scale_factor)
    transformed_checkerboard = cv2.resize(transformed_checkerboard, (scaled_width, scaled_height))

    # Crop or pad the image back to original size if needed
    if scale_factor > 1.0:
        # Crop the image to the original size
        start_x = (scaled_width - board_width) // 2
        start_y = (scaled_height - board_height) // 2
        transformed_checkerboard = transformed_checkerboard[start_y:start_y + board_height, start_x:start_x + board_width]
    else:
        # Pad the image to the original size
        pad_x = (board_width - scaled_width) // 2
        pad_y = (board_height - scaled_height) // 2
        transformed_checkerboard = cv2.copyMakeBorder(
            transformed_checkerboard, pad_y, pad_y, pad_x, pad_x, cv2.BORDER_CONSTANT, value=0
        )

    # Optionally, add some random noise to simulate imperfections
    noise = np.random.normal(0, 20, transformed_checkerboard.shape).astype(np.uint8)
    transformed_checkerboard = cv2.add(transformed_checkerboard, noise)

    # Save the generated image
    image_path = os.path.join(output_dir, f'calibration_image_{img_num + 1:02d}.png')
    cv2.imwrite(image_path, transformed_checkerboard)

    print(f'Generated: {image_path}')

print('50 calibration images generated and stored in the calibration_images/ folder.')

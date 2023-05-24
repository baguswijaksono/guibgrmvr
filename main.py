import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

def browse_file():
    filename = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg")])
    if filename:
        process_image(filename)

def process_image(filename):
    # Load image using OpenCV
    image = cv2.imread(filename)

    # Create a mask with the same size as the image
    mask = np.zeros(image.shape[:2], np.uint8)

    # Define the background and foreground models
    background_model = np.zeros((1, 65), np.float64)
    foreground_model = np.zeros((1, 65), np.float64)

    # Define the region of interest (ROI) for GrabCut
    # You can modify the values here to adjust the ROI
    rect = (50, 50, image.shape[1] - 50, image.shape[0] - 50)

    # Run GrabCut algorithm to segment the foreground and background
    cv2.grabCut(image, mask, rect, background_model, foreground_model, 5, cv2.GC_INIT_WITH_RECT)

    # Create a mask where the foreground pixels are set to 1 (sure foreground) or 3 (possible foreground)
    mask_2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')

    # Apply the mask to the original image to remove the background
    image = image * mask_2[:, :, np.newaxis]

    # Display the processed image
    cv2.imshow("Processed Image", image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def save_image():
    # Get the processed image and save it
    # TODO: Implement the saving logic using OpenCV

    print("Image saved!")

# Create the GUI window
window = tk.Tk()

# Create the Browse button
browse_button = tk.Button(window, text="Browse", command=browse_file)
browse_button.pack()

# Create the Save button
save_button = tk.Button(window, text="Save", command=save_image)
save_button.pack()

# Run the GUI window
window.mainloop()


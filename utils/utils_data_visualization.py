import matplotlib.pyplot as plt
from .utils_data_loading import *
# from ipywidgets import widgets, interactive_output, display
from ipywidgets import widgets, interactive_output
from IPython.display import display
import numpy as np
from matplotlib.colors import ListedColormap

def visualize_dbb_t1_scan(im_data=None, im_path=None, axis=0):
    """
    Visualizes slices of a T1 image interactively, either from image data or a file path.
    
    Parameters:
    - im_data: 3D numpy array of the image data. (optional)
    - im_path: Path to the image file. (optional)
    - axis: The axis along which to take slices (0, 1, or 2).
    - subject_num: The subject number (for display purposes).
    """
    # Load data from path if provided
    if im_path is not None:
        im_data = load_nifti_data(im_path)
    elif im_data is None:
        raise ValueError("Either im_data or im_path must be provided.")
    
    # Determine the number of slices along the specified axis
    num_slices = im_data.shape[axis]
    
    def plot_slice(slice_idx):
        """
        Plots a specific slice from the image data.

        Parameters:
        - slice_idx: The index of the slice to plot.
        """
        if im_path is not None:
            subject_num = get_subject_num_from_path(im_path)
        else:
            subject_num = "Unknown"
        # Select the appropriate slice based on the axis
        if axis == 0:
            slice_im = im_data[slice_idx, :, :]
        elif axis == 1:
            slice_im = im_data[:, slice_idx, :]
        else:  # axis == 2
            slice_im = im_data[:, :, slice_idx]
            

        
        # Set the figure size
        plt.figure(figsize=(10, 8))
        
        # Display the image slice
        plt.imshow(slice_im, cmap='gray')
        plt.title(f'Subject {subject_num} T1 Image Slice {slice_idx}')
        plt.axis('off') # Hide the axis to focus on the image
        plt.show()

    
    # Create a slider widget for slice selection
    slice_slider = widgets.IntSlider(min=0, max=num_slices-1, step=1, value=num_slices//2, description='Slice Index')
    
    # Use `interactive_output` to create interactive visualization without the need for a callback function
    interactive_plot = widgets.interactive_output(plot_slice, {'slice_idx': slice_slider})
    
    # Display the slider and the output together
    display(slice_slider, interactive_plot)

def visualize_minbboggle_triplet(im_data1=None, im_path1=None, im_data2=None, im_path2=None, im_data3=None, im_path3=None, axis=0):
    """
    Visualizes slices of up to three images interactively, including input data, segmentation data, and optionally ground truth data.
    """
    # Assuming a function load_nifti_data is defined elsewhere to load image data
    
    # Create a custom colormap for the segmentation data
    colors = [(0, 0, 0), (0.5, 0.5, 0.5), (1, 1, 1), (1, 0.647, 0), (1, 0, 0)]  # black, grey, white, orange, red
    cmap = ListedColormap(colors)
    
    images = [(im_data1, 'Input Data'), (im_data2, 'Segmentation Data'), (im_data3, 'Ground Truth Data')]
    images = [(data, title) for data, title in images if data is not None]  # Filter out None data

    if not images:
        raise ValueError("At least one image data must be provided.")
    
    num_slices = images[0][0].shape[axis]
    
    def plot_slices(slice_idx):
        n_images = len(images)
        fig, axes = plt.subplots(1, n_images, figsize=(6 * n_images, 6))
        if n_images == 1:
            axes = [axes]  # Make axes iterable
        
        for ax, (im_data, title) in zip(axes, images):
            if axis == 0:
                slice_im = im_data[slice_idx, :, :]
            elif axis == 1:
                slice_im = im_data[:, slice_idx, :]
            else:
                slice_im = im_data[:, :, slice_idx]
            
            if 'Segmentation' in title:  # Apply custom colormap for segmentation data
                ax.imshow(slice_im, cmap=cmap, vmin=0, vmax=len(colors)-1)
            else:
                ax.imshow(slice_im, cmap='gray')
            
            ax.set_title(title)
            ax.axis('off')
        
        plt.tight_layout()
        plt.show()
    
    slice_slider = widgets.IntSlider(min=0, max=num_slices-1, step=1, value=num_slices//2, description='Slice Index')
    interactive_plot = interactive_output(plot_slices, {'slice_idx': slice_slider})
    
    display(slice_slider, interactive_plot)
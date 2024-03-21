import matplotlib.pyplot as plt

from .data_loading import *
# from ipywidgets import widgets, interactive_output, display
from ipywidgets import widgets, interactive_output
from IPython.display import display



def visualize_t1_scan(im_data=None, im_path=None, axis=0):
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
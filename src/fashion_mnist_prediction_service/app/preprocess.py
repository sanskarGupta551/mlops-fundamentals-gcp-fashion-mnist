import numpy as np
from PIL import Image
import io

def preprocess_image(file_stream):
    """
    Preprocess an image for Fashion MNIST prediction.
    
    Args:
        file_stream: An image file object
    
    Returns:
        Normalized list ready for prediction
    """
    # Read image from file stream
    img = Image.open(file_stream).convert('L')  # Convert to grayscale
    
    # Resize to 28x28 (Fashion MNIST size)
    img = img.resize((28, 28))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Normalize pixel values to [0, 1] range
    img_array = img_array.astype('float32') / 255.0
    
    # Flatten the array to a 1D list (784 elements)
    flattened = img_array.flatten().tolist()
    
    # Ensure we're not exceeding size limits
    print(f"Processed image size: {len(str(flattened))} characters")
    
    return flattened

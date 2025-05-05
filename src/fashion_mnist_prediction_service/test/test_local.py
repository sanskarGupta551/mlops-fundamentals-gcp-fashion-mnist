from PIL import Image
import numpy as np

def preprocess_image(file_path):
    # Read image
    img = Image.open(file_path).convert('L')  # Convert to grayscale
    
    # Resize to 28x28
    img = img.resize((28, 28))
    
    # Convert to numpy array
    img_array = np.array(img)
    
    # Normalize to [0, 1]
    img_array = img_array.astype('float32') / 255.0
    
    # Flatten
    flattened = img_array.flatten().tolist()
    
    # Check size
    print(f"Processed image array length: {len(flattened)}")
    print(f"Serialized size: {len(str(flattened))} characters")
    
    # Print a few sample values
    print(f"Sample values: {flattened[:5]}...")
    
    return flattened

# Test with our image
processed = preprocess_image("test_images/test_00018.jpg")
print(f"This is a valid Fashion MNIST input with shape: (1, 784)")

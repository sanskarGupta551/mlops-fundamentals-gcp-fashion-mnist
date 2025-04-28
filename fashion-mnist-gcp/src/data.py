"""
Fashion MNIST Data Processor Module

This module provides classes for handling Fashion MNIST data processing,
including loading, normalization, augmentation, and batch generation.
"""

import numpy as np
import tensorflow as tf
from tensorflow.keras.datasets import fashion_mnist
from sklearn.model_selection import train_test_split
from scipy.ndimage import rotate, shift, zoom
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, 
                   format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class FashionMNISTDataset:
    """Handles loading and processing of Fashion MNIST dataset."""
    
    # Class names for the Fashion MNIST dataset
    CLASS_NAMES = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat',
                  'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
    
    def __init__(self, val_split=0.2, random_state=42, normalize=True):
        """
        Initialize the Fashion MNIST dataset manager.
        
        Args:
            val_split (float): Proportion of training data to use for validation
            random_state (int): Random seed for reproducibility
            normalize (bool): Whether to normalize the data
        """
        self.val_split = val_split
        self.random_state = random_state
        self.normalize = normalize
        
        # Set random seeds for reproducibility
        np.random.seed(self.random_state)
        tf.random.set_seed(self.random_state)
        
        # Load data immediately
        self._load_data()
        
    def _load_data(self):
        """Load Fashion MNIST dataset and prepare train/val/test splits."""
        logger.info("Loading Fashion MNIST dataset...")
        try:
            # Load the raw dataset
            (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()
            
            # Create validation split
            X_train, X_val, y_train, y_val = train_test_split(
                X_train_full, y_train_full, 
                test_size=self.val_split, 
                random_state=self.random_state, 
                stratify=y_train_full
            )
            
            # Apply normalization if requested
            if self.normalize:
                self.X_train = X_train.astype('float32') / 255.0
                self.X_val = X_val.astype('float32') / 255.0
                self.X_test = X_test.astype('float32') / 255.0
            else:
                self.X_train = X_train
                self.X_val = X_val
                self.X_test = X_test
                
            # Keep labels as they are
            self.y_train = y_train
            self.y_val = y_val
            self.y_test = y_test
                
            logger.info(f"Data loaded successfully. Training: {self.X_train.shape}, "
                        f"Validation: {self.X_val.shape}, Test: {self.X_test.shape}")
        
        except Exception as e:
            logger.error(f"Error loading Fashion MNIST dataset: {e}")
            raise
    
    def save_to_npz(self, output_path):
        """
        Save the processed dataset to NPZ format.
        
        Args:
            output_path (str): Directory path to save the dataset
        """
        os.makedirs(output_path, exist_ok=True)
        file_path = os.path.join(output_path, 'fashion_mnist_processed.npz')
        
        np.savez_compressed(
            file_path,
            X_train=self.X_train,
            y_train=self.y_train,
            X_val=self.X_val,
            y_val=self.y_val,
            X_test=self.X_test,
            y_test=self.y_test
        )
        
        logger.info(f"Dataset saved to {file_path}")


class ImageAugmenter:
    """Provides image augmentation functionality for Fashion MNIST dataset."""
    
    def __init__(self, 
                rotation_range=(-15, 15),
                brightness_range=(0.8, 1.2),
                contrast_range=(0.7, 1.3),
                shift_range=(-2, 3),
                zoom_range=(0.9, 1.1),
                horizontal_flip_prob=0.5,
                random_state=None):
        """
        Initialize the image augmenter with customizable parameters.
        
        Args:
            rotation_range (tuple): Min and max rotation angles in degrees
            brightness_range (tuple): Min and max brightness factors
            contrast_range (tuple): Min and max contrast factors
            shift_range (tuple): Min and max pixel shifts
            zoom_range (tuple): Min and max zoom factors
            horizontal_flip_prob (float): Probability of horizontal flip
            random_state (int): Random seed for reproducibility
        """
        self.rotation_range = rotation_range
        self.brightness_range = brightness_range
        self.contrast_range = contrast_range
        self.shift_range = shift_range
        self.zoom_range = zoom_range
        self.horizontal_flip_prob = horizontal_flip_prob
        
        if random_state is not None:
            np.random.seed(random_state)
    
    def augment_image(self, image):
        """
        Apply random augmentations to an image.
        
        Args:
            image (numpy.ndarray): Input image to augment
            
        Returns:
            numpy.ndarray: Augmented image
        """
        # Convert to float if needed
        img = image.astype('float32') if image.dtype != 'float32' else image.copy()
        
        # Random horizontal flip
        if np.random.random() < self.horizontal_flip_prob:
            img = np.fliplr(img)
        
        # Random rotation
        if np.random.random() > 0.4:
            angle = np.random.uniform(*self.rotation_range)
            img = rotate(img, angle, reshape=False, mode='nearest')
        
        # Random brightness adjustment
        if np.random.random() > 0.3:
            factor = np.random.uniform(*self.brightness_range)
            img = img * factor
            img = np.clip(img, 0, 1)
        
        # Random contrast adjustment
        if np.random.random() > 0.4:
            mean = np.mean(img)
            factor = np.random.uniform(*self.contrast_range)
            img = (img - mean) * factor + mean
            img = np.clip(img, 0, 1)
        
        # Random shift
        if np.random.random() > 0.5:
            dx = np.random.randint(*self.shift_range)
            dy = np.random.randint(*self.shift_range)
            img = shift(img, (dy, dx), mode='constant', cval=0)
        
        # Random zoom
        if np.random.random() > 0.6:
            h, w = img.shape
            zoom_factor = np.random.uniform(*self.zoom_range)
            
            # Zoom in and crop or zoom out and pad
            if zoom_factor > 1:  # Zoom in
                zoomed = zoom(img, zoom_factor, mode='nearest')
                start_h = int((zoomed.shape[0] - h) / 2)
                start_w = int((zoomed.shape[1] - w) / 2)
                img = zoomed[start_h:start_h+h, start_w:start_w+w]
            else:  # Zoom out
                zoomed = zoom(img, zoom_factor, mode='nearest')
                new_h, new_w = zoomed.shape
                pad_h = int((h - new_h) / 2)
                pad_w = int((w - new_w) / 2)
                result = np.zeros_like(img)
                result[pad_h:pad_h+new_h, pad_w:pad_w+new_w] = zoomed
                img = result
            
        return img


class DataGenerator:
    """Generates batches of data with optional augmentation for model training."""
    
    def __init__(self, X, y, batch_size=32, augmenter=None, shuffle=True, random_state=None):
        """
        Initialize the data generator.
        
        Args:
            X (numpy.ndarray): Input image data
            y (numpy.ndarray): Target labels
            batch_size (int): Size of batches to generate
            augmenter (ImageAugmenter): Optional augmenter for data augmentation
            shuffle (bool): Whether to shuffle data before batching
            random_state (int): Random seed for reproducibility
        """
        self.X = X
        self.y = y
        self.batch_size = batch_size
        self.augmenter = augmenter
        self.shuffle = shuffle
        
        if random_state is not None:
            np.random.seed(random_state)
    
    def __len__(self):
        """Return the number of batches in the dataset."""
        return int(np.ceil(len(self.X) / self.batch_size))
    
    def __iter__(self):
        """Make the generator iterable."""
        self.current_index = 0
        self.indices = np.arange(len(self.X))
        if self.shuffle:
            np.random.shuffle(self.indices)
        return self
    
    def __next__(self):
        """Get the next batch of data."""
        if self.current_index >= len(self.X):
            raise StopIteration
        
        batch_indices = self.indices[self.current_index:self.current_index + self.batch_size]
        self.current_index += self.batch_size
        
        batch_X = self.X[batch_indices].copy()
        batch_y = self.y[batch_indices].copy()
        
        # Apply augmentation if available
        if self.augmenter:
            for i in range(len(batch_X)):
                batch_X[i] = self.augmenter.augment_image(batch_X[i])
        
        return batch_X, batch_y
    
    def generate(self):
        """Generator function to yield batches of data indefinitely."""
        while True:
            # Reset the iterator
            self.current_index = 0
            if self.shuffle:
                np.random.shuffle(self.indices)
                
            # Yield batches until data is exhausted
            while self.current_index < len(self.X):
                yield next(self)


def load_fashion_mnist_dataset(val_split=0.2, random_state=42, normalize=True):
    """
    Utility function to quickly load and process Fashion MNIST dataset.
    
    Args:
        val_split (float): Proportion of training data to use for validation
        random_state (int): Random seed for reproducibility
        normalize (bool): Whether to normalize the data
        
    Returns:
        tuple: Processed data splits (X_train, y_train, X_val, y_val, X_test, y_test)
    """
    dataset = FashionMNISTDataset(val_split=val_split, 
                                 random_state=random_state, 
                                 normalize=normalize)
    
    return (dataset.X_train, dataset.y_train, 
            dataset.X_val, dataset.y_val, 
            dataset.X_test, dataset.y_test)


def create_train_generator(X_train, y_train, batch_size=32, augment=True, random_state=None):
    """
    Create a data generator for training.
    
    Args:
        X_train (numpy.ndarray): Training data
        y_train (numpy.ndarray): Training labels
        batch_size (int): Batch size
        augment (bool): Whether to apply augmentation
        random_state (int): Random seed for reproducibility
        
    Returns:
        DataGenerator: Generator for training data
    """
    augmenter = None
    if augment:
        augmenter = ImageAugmenter(random_state=random_state)
    
    return DataGenerator(X_train, y_train, batch_size=batch_size, 
                        augmenter=augmenter, shuffle=True, 
                        random_state=random_state)


def create_val_generator(X_val, y_val, batch_size=32, random_state=None):
    """
    Create a data generator for validation.
    
    Args:
        X_val (numpy.ndarray): Validation data
        y_val (numpy.ndarray): Validation labels
        batch_size (int): Batch size
        random_state (int): Random seed for reproducibility
        
    Returns:
        DataGenerator: Generator for validation data
    """
    # No augmentation for validation data
    return DataGenerator(X_val, y_val, batch_size=batch_size, 
                        augmenter=None, shuffle=False, 
                        random_state=random_state)
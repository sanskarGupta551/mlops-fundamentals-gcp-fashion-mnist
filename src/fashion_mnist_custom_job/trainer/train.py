#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fashion MNIST Custom Training Job for Vertex AI
"""

import os
import argparse
import time
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.preprocessing.image import ImageDataGenerator

# Define argument parser
def parse_args():
    parser = argparse.ArgumentParser(description='Train a CNN model on Fashion MNIST dataset')
    parser.add_argument('--epochs', type=int, default=100, help='Number of epochs')
    parser.add_argument('--batch-size', type=int, default=32, help='Batch size')
    parser.add_argument('--learning-rate', type=float, default=0.001, help='Learning rate')
    parser.add_argument('--dropout-rate', type=float, default=0.25, help='Dropout rate for convolutional layers')
    parser.add_argument('--dense-dropout-rate', type=float, default=0.5, help='Dropout rate for dense layer')
    parser.add_argument('--model-dir', type=str, 
                  default=os.environ.get('AIP_MODEL_DIR', 'gs://fashion-mnist-dev/custom-model'),
                  help='Directory for saving the model')

    return parser.parse_args()

# Load and preprocess data
def load_data():
    print("Loading Fashion MNIST dataset...")
    fashion_mnist = keras.datasets.fashion_mnist
    (X_train_full, y_train_full), (X_test, y_test) = fashion_mnist.load_data()
    
    # Reshape data to include channel dimension
    X_train_full = X_train_full.reshape((60000, 28, 28, 1))
    X_test = X_test.reshape((10000, 28, 28, 1))
    
    # Split into train and validation sets
    X_valid, X_train = X_train_full[:5000], X_train_full[5000:]
    y_valid, y_train = y_train_full[:5000], y_train_full[5000:]
    
    print(f"Training data: {X_train.shape}, Validation data: {X_valid.shape}, Test data: {X_test.shape}")
    
    return X_train, y_train, X_valid, y_valid, X_test, y_test

# Create data generators with augmentation
def create_data_generators(X_train, y_train, X_valid, y_valid, batch_size):
    print("Creating data generators with augmentation...")
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.15,
        height_shift_range=0.15,
        shear_range=0.15,
        zoom_range=0.15,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    validation_datagen = ImageDataGenerator(rescale=1./255)
    
    train_generator = train_datagen.flow(X_train, y_train, batch_size=batch_size)
    validation_generator = validation_datagen.flow(X_valid, y_valid, batch_size=batch_size)
    
    return train_generator, validation_generator

# Build model
def build_model(conv_dropout_rate, dense_dropout_rate, learning_rate):
    print("Building CNN model...")
    model = keras.models.Sequential()
    model.add(Conv2D(filters=32, kernel_size=(3,3), strides=1, padding="same", 
                     activation="relu", input_shape=(28,28,1)))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(conv_dropout_rate))
    model.add(Conv2D(filters=64, kernel_size=(3,3), strides=1, padding="same", 
                     activation="relu"))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(conv_dropout_rate))
    model.add(Conv2D(filters=128, kernel_size=(3,3), strides=1, padding="same", 
                     activation="relu"))
    model.add(MaxPooling2D((2,2)))
    model.add(Dropout(conv_dropout_rate))
    
    model.add(Flatten())
    model.add(Dense(512, activation="relu"))
    model.add(Dropout(dense_dropout_rate))
    model.add(Dense(10, activation="softmax"))
    
    # Compile model
    model.compile(
        loss="sparse_categorical_crossentropy",
        optimizer=keras.optimizers.Adam(learning_rate=learning_rate),
        metrics=["accuracy"]
    )
    
    model.summary()
    return model

# Setup callbacks
def create_callbacks(model_dir):
    print("Setting up training callbacks...")
    # Make sure the model directory exists
    if model_dir.startswith('gs://'):
        checkpoint_path = os.path.join(model_dir, 'best_model.h5')
    else:
        os.makedirs(model_dir, exist_ok=True)
        checkpoint_path = os.path.join(model_dir, 'best_model.h5')
    
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=10,
            verbose=1,
            restore_best_weights=True,
            mode='max'
        ),
        ModelCheckpoint(
            filepath=checkpoint_path,
            save_best_only=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.2,
            patience=3,
            verbose=1,
            min_delta=0.001,
            min_lr=1e-6
        )
    ]
    
    # Only add TensorBoard if not using GCS path
    if not model_dir.startswith('gs://'):
        log_dir = os.path.join(model_dir, 'logs')
        os.makedirs(log_dir, exist_ok=True)
        callbacks.append(TensorBoard(log_dir=log_dir))
    
    return callbacks

# Train model
def train_model(model, train_generator, validation_generator, epochs, callbacks, batch_size,
                X_train, X_valid):
    print(f"Training model for {epochs} epochs...")
    steps_per_epoch = len(X_train) // batch_size
    validation_steps = len(X_valid) // batch_size
    
    start_time = time.time()
    
    history = model.fit(
        train_generator,
        epochs=epochs,
        steps_per_epoch=steps_per_epoch,
        validation_data=validation_generator,
        validation_steps=validation_steps,
        callbacks=callbacks,
        verbose=2  # Use verbose=2 for more compact logging
    )
    
    training_time = time.time() - start_time
    print(f"Training completed in {training_time:.2f} seconds")
    
    return history

# Evaluate model
def evaluate_model(model, X_test, y_test):
    print("Evaluating model on test data...")
    # Normalize test data
    X_test = X_test.astype('float32') / 255.0
    
    test_loss, test_accuracy = model.evaluate(X_test, y_test, verbose=0)
    print(f"Test accuracy: {test_accuracy:.4f}")
    print(f"Test loss: {test_loss:.4f}")
    
    return test_accuracy, test_loss

# Save final model
def save_model(model, model_dir, test_accuracy):
    print(f"Saving model to {model_dir}...")
    
    # Define class names for metadata
    class_names = ["T-shirt/top", "Trouser", "Pullover", "Dress", "Coat",
                   "Sandal", "Shirt", "Sneaker", "Bag", "Ankle Boot"]
    
    # Save model in SavedModel format
    model_path = os.path.join(model_dir, 'model')
    model.save(model_path)
    
    # Save model metadata
    metadata = {
        "framework": "tensorflow",
        "accuracy": float(test_accuracy),
        "classes": class_names
    }
    
    # Write metadata to file
    try:
        import json
        metadata_path = os.path.join(model_dir, 'metadata.json')
        
        if model_dir.startswith('gs://'):
            with tf.io.gfile.GFile(metadata_path, 'w') as f:
                json.dump(metadata, f)
        else:
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f)
                
        print(f"Model metadata saved to {metadata_path}")
    except Exception as e:
        print(f"Warning: Could not save metadata: {e}")

# Main function
def main():
    # Parse arguments
    args = parse_args()
    
    # Set seeds for reproducibility
    np.random.seed(42)
    tf.random.set_seed(42)
    
    # Load data
    X_train, y_train, X_valid, y_valid, X_test, y_test = load_data()
    
    # Create data generators
    train_generator, validation_generator = create_data_generators(
        X_train, y_train, X_valid, y_valid, args.batch_size
    )
    
    # Build model
    model = build_model(
        conv_dropout_rate=args.dropout_rate,
        dense_dropout_rate=args.dense_dropout_rate,
        learning_rate=args.learning_rate
    )
    
    # Create callbacks
    callbacks = create_callbacks(args.model_dir)
    
    # Train model
    history = train_model(
        model, 
        train_generator, 
        validation_generator, 
        args.epochs, 
        callbacks, 
        args.batch_size,
        X_train,
        X_valid
    )
    
    # Evaluate model
    test_accuracy, test_loss = evaluate_model(model, X_test, y_test)
    
    # Save model
    save_model(model, args.model_dir, test_accuracy)
    
    print("Training job completed successfully")

if __name__ == "__main__":
    main()
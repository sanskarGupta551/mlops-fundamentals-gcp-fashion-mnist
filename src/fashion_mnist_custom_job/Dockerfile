FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-3

WORKDIR /

# Copy the trainer module
COPY trainer /trainer

# Make sure the Python module is importable
RUN touch /trainer/__init__.py

# Set the entrypoint
ENTRYPOINT ["python", "-m", "trainer.train"]
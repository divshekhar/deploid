FROM ubuntu:22.04

# Install Python and other dependencies
RUN apt-get update && \
    apt-get install -y python3 python3-pip sudo curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user for testing
RUN useradd -m -s /bin/bash testuser && \
    echo "testuser ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/testuser

WORKDIR /deploid

# Copy the project files
COPY . .

# Make scripts executable
RUN chmod +x *.sh *.py && \
    find . -name "*.sh" -type f -exec chmod +x {} \; && \
    find . -name "*.py" -type f -exec chmod +x {} \;

# Install Python packages globally
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Set ownership of the project directory to testuser
RUN chown -R testuser:testuser /deploid

# Switch to testuser
USER testuser

# Start with bash
CMD ["/bin/bash"]

echo "Updating package list and upgrading packages..."
pkg update -y && pkg upgrade -y

echo "Installing Python and pip..."
pkg install -y python

echo "Installing FFmpeg..."
pkg install -y ffmpeg

echo "Installing lz4 Python module..."
pip install lz4

echo "Verifying installations..."
echo "Python version:"
python --version

echo "FFmpeg version:"
ffmpeg -version

echo "Required Python modules:"
pip show lz4

echo "Setup complete! You can now run your FLVC converter"

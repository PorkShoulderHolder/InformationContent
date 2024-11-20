import os
import sys
import tempfile
import subprocess
from tqdm import tqdm

def estimate_true_information(path, temp_dir=None):
    """
    Estimate true information content using zstd compression.
    Returns compressed size in bytes.
    """
    if temp_dir is None:
        temp_dir = tempfile.gettempdir()
    
    temp_archive = os.path.join(temp_dir, 'temp_archive.zst')
    
    try:
        if os.path.exists(temp_archive):
            os.remove(temp_archive)
        
        print("Compressing data...")
        # Compress the directory/file using zstd with maximum compression
        if os.path.isdir(path):
            cmd = f'tar -cf - -C "{os.path.dirname(path)}" "{os.path.basename(path)}" | zstd -22 --force -o "{temp_archive}"'
            print(f"Running command: {cmd}")
            subprocess.run(cmd, shell=True, check=True, stderr=subprocess.PIPE)
        else:
            subprocess.run(
                ['zstd', '-22', '--force', '-o', temp_archive, path],
                check=True,
                stderr=subprocess.PIPE,
                text=True
            )
        
        compressed_size = os.path.getsize(temp_archive)
        return compressed_size
    
    except subprocess.CalledProcessError as e:
        print(f"Compression error: {e.stderr}")
        raise
    finally:
        if os.path.exists(temp_archive):
            os.remove(temp_archive)

def process_path(path):
    """
    Process a file or directory and estimate true information content.
    """
    if not os.path.exists(path):
        raise ValueError(f"Path {path} does not exist")

    # Calculate original size with progress bar for directories
    if os.path.isfile(path):
        size = os.path.getsize(path)
    else:
        print("Calculating total size...")
        size = 0
        for root, _, files in os.walk(path):
            for file in files:
                try:
                    size += os.path.getsize(os.path.join(root, file))
                except (OSError, PermissionError) as e:
                    print(f"Warning: Couldn't access {file}: {e}")

    print(f"\nAnalyzing: {path}")
    print(f"Original size: {size / 1000000:.2f} MB")
    
    print("Computing true information content...")
    compressed_size = estimate_true_information(path)
    
    print(f"Compressed size: {compressed_size / 1000000:.2f} MB")
    print(f"True information content (est.): {compressed_size * 8 / 1000000000:.2f} GB")
    
    if size > 0:
        compression_ratio = (size - compressed_size) / size * 100
        print(f"Compression ratio: {compression_ratio:.1f}%")

def main():
    try:
        if len(sys.argv) < 2:
            print("Usage: python entropy.py <file_or_directory_path>")
            sys.exit(1)
            
        path = sys.argv[1]
        process_path(path)
        
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()

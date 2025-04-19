import io
from PIL import Image

def is_valid_image(image_bytes):
    """
    Validates if the bytes represent a valid image by attempting to open it with PIL.
    
    Args:
        image_bytes: Binary content of the image file
        
    Returns:
        bool: True if valid image, False otherwise
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.verify()  # Verify image integrity
        return True
    except Exception:
        return False

def encrypt_image(image_bytes, key):
    """
    Encrypts an image using XOR encryption with the provided key.
    
    Args:
        image_bytes: Binary content of the image file
        key: Integer key for XOR encryption (0-255)
        
    Returns:
        tuple: (encrypted_data, already_encrypted) where already_encrypted is a boolean
    """
    # Validate key is an integer
    if not isinstance(key, int):
        try:
            key = int(key)
        except ValueError:
            raise ValueError("Key must be an integer value between 0 and 255")
    
    # Ensure key is in range 0-255
    if not (0 <= key <= 255):
        raise ValueError("Key must be in range 0-255")
        
    # Convert to bytearray for in-place modification
    data = bytearray(image_bytes)
    already_encrypted = True
    
    # Apply XOR with key to each byte
    for i, v in enumerate(data):
        nv = v ^ key
        if nv != v:
            already_encrypted = False
        data[i] = nv
    
    return bytes(data), already_encrypted

def decrypt_image(encrypted_bytes, key):
    """
    Decrypts an image using XOR decryption with the provided key.
    
    Args:
        encrypted_bytes: Binary content of the encrypted image file
        key: Integer key for XOR decryption (0-255)
        
    Returns:
        bytes: Decrypted image data
    """
    # Validate key is an integer
    if not isinstance(key, int):
        try:
            key = int(key)
        except ValueError:
            raise ValueError("Key must be an integer value between 0 and 255")
    
    # Ensure key is in range 0-255
    if not (0 <= key <= 255):
        raise ValueError("Key must be in range 0-255")
    
    # Convert to bytearray for in-place modification
    data = bytearray(encrypted_bytes)
    
    # Apply XOR with key to each byte (XOR is its own inverse)
    for i in range(len(data)):
        data[i] ^= key
    
    return bytes(data)

def get_image_preview(image_bytes, size=(200, 200)):
    """
    Creates a thumbnail preview of the image.
    
    Args:
        image_bytes: Binary content of the image file
        size: Tuple of (width, height) for the thumbnail
        
    Returns:
        PIL.Image: Thumbnail image or None if not valid
    """
    try:
        img = Image.open(io.BytesIO(image_bytes))
        img.thumbnail(size)
        return img
    except Exception:
        return None

def is_encrypted(image_bytes, threshold=0.9):
    """
    Attempts to determine if an image might already be encrypted by checking
    entropy characteristics. This is a heuristic approach, not foolproof.
    
    Args:
        image_bytes: Binary content of the image file
        threshold: Entropy threshold for considering encrypted
        
    Returns:
        bool: True if likely encrypted, False otherwise
    """
    # This is a simplified implementation. A more sophisticated version
    # would analyze byte distribution and entropy.
    try:
        img = Image.open(io.BytesIO(image_bytes))
        return False  # If we can open it, it's probably not encrypted
    except:
        return True  # If we can't open it, it might be encrypted
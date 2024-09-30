from PIL import Image
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import numpy as np
def pad(data):
    """ Pads the data to be a multiple of the block size. """
    padding_length = AES.block_size - (len(data) % AES.block_size)
    return data + bytes([padding_length] * padding_length)

def unpad(data):
    """ Removes padding from the data. """
    padding_length = data[-1]
    return data[:-padding_length]

def encrypt_image(image_path, output_encrypted_path, key):
    """ Encrypts the image using AES and save it to a file. """
    # Load the image
    img = Image.open(image_path)
    img_data = np.array(img)

    # Convert image data to bytes
    image_bytes = img_data.tobytes()

    # Pad the image bytes
    padded_data = pad(image_bytes)
    
    # Generate a random initialization vector
    iv = get_random_bytes(AES.block_size)

    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Encrypt the data
    encrypted_data = cipher.encrypt(padded_data)
    pixels = len(encrypted_data)//3
    bytes = img_data.shape[1]*img_data.shape[0]*3
    
    encrypted_img_d =  encrypted_data[:bytes]
    encrypted_img = np.frombuffer(encrypted_img_d,dtype=np.uint8).reshape((img_data.shape[0],img_data.shape[1],3))
    encrypted_image = Image.fromarray(encrypted_img)
    encrypted_image.save("encrypted_image.png")
    # Save the encrypted data along with the IV
    with open(output_encrypted_path, 'wb') as file:
        file.write(iv + encrypted_data)

    print(f"Image encrypted and saved to {output_encrypted_path}")

def decrypt_image(encrypted_path, output_decrypted_path, key):
    """ Decrypt the encrypted image and save it to a file. """
    # Read the encrypted data
    with open(encrypted_path, 'rb') as file:
        iv = file.read(16)  # Read the first 16 bytes as IV
        encrypted_data = file.read()

    # Create AES cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)

    # Decrypt the data
    padded_data = cipher.decrypt(encrypted_data)

    # Unpad the data
    image_bytes = unpad(padded_data)

    # Get the original dimensions of the image
    img_shape = (height, width, RGB)  # Specify the original dimensions
    image_array = np.frombuffer(image_bytes, dtype=np.uint8).reshape(img_shape)

    # Save the decrypted image
    decrypted_image = Image.fromarray(image_array)
    decrypted_image.save(output_decrypted_path)

    print(f"Image decrypted and saved to {output_decrypted_path}")


image_path = "input.png"  
output_encrypted_path = "encrypted_image.bin"  
output_decrypted_path = "decrypted_image.png"  

# Generate a random AES key (16 bytes for AES-128)
key = get_random_bytes(16)
img = Image.open("input.png")
height = img.size[1]  #  image's height
width = img.size[0]   #  image's width
RGB = 3  
# Encrypt the image
encrypt_image(image_path, output_encrypted_path, key)

# Specify the dimensions of the original image (must be known for decryption)
# Update these values according to your image

# Decrypt the image
decrypt_image(output_encrypted_path, output_decrypted_path, key)

from PIL import Image
import numpy as np
import secrets

def xor_encrypt_decrypt(image_path, key):
    # Load the image
    image = Image.open(image_path)
    image_data = np.array(image)

    # Flatten the image data to 1D array
    flattened_data = image_data.flatten()

    # Create an array for the encrypted/decrypted data
    key_length = len(key)
    encrypted_data = np.zeros(flattened_data.shape, dtype=np.uint8)
    print(len(flattened_data),"f")
    # Perform XOR operation
    for i in range(len(flattened_data)):
        encrypted_data[i] = flattened_data[i] ^ key[i]

    # Reshape the data back to the original image shape
    encrypted_image = encrypted_data.reshape(image_data.shape)

    return Image.fromarray(encrypted_image)



img = Image.open("input.png")

key_len = img.size[0]*img.size[1]*3*8
# generate random stream of bytes
key = secrets.token_bytes((key_len+7)//8)

# Encrypt an image
encrypted_image = xor_encrypt_decrypt('input.png', key)

encrypted_image.save('encrypted_image.png')


# decrypt the image using same key.

decrypted_image = xor_encrypt_decrypt('encrypted_image.png', key)
decrypted_image.save('decrypted_image.png')

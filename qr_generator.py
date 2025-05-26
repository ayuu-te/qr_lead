import segno
from PIL import Image
import shutil

def generate_basic_qr(data, filename='qr_basic.png'):
    qr = segno.make_qr(data)
    qr.save(filename)
    print(f"Basic QR code saved as {filename}")

def generate_custom_qr(data, filename='qr_custom.png', scale=10, dark='black', light='white', error='H'):
    qr = segno.make_qr(data, error=error)
    qr.save(filename, scale=scale, dark=dark, light=light)
    print(f"Custom QR code saved as {filename}")

def generate_qr_with_logo(data, filename='qr_logo.png', scale=10, dark='black', light='white', error='H', logo_path=None):
    qr = segno.make_qr(data, error=error)
    temp_file = 'temp_qr.png'
    qr.save(temp_file, scale=scale, dark=dark, light=light)
    if logo_path:
        qr_img = Image.open(temp_file)
        logo = Image.open(logo_path)
        qr_width, qr_height = qr_img.size
        logo_size = int(qr_width * 0.2)
        logo = logo.resize((logo_size, logo_size), Image.ANTIALIAS)
        pos = ((qr_width - logo_size) // 2, (qr_height - logo_size) // 2)
        qr_img.paste(logo, pos, mask=logo if logo.mode == 'RGBA' else None)
        qr_img.save(filename)
        print(f"QR code with logo saved as {filename}")
    else:
        shutil.move(temp_file, filename)
        print(f"QR code saved as {filename} (no logo)")

if __name__ == "__main__":
    print("Welcome to the Dynamic QR Code Generator!")
    data = input("Enter the data/text/URL to encode in the QR code: ")
    
    print("\nChoose QR code type:")
    print("1. Basic")
    print("2. Custom (color/size)")
    print("3. With Logo")
    choice = input("Enter your choice (1/2/3): ")

    if choice == "1":
        filename = input("Enter filename to save (e.g., qr_basic.png): ") or "qr_basic.png"
        generate_basic_qr(data, filename)
    elif choice == "2":
        filename = input("Enter filename to save (e.g., qr_custom.png): ")
        if not (filename.lower().endswith('.png') or filename.lower().endswith('.jpg') or filename.lower().endswith('.svg')):
            filename += '.png'  # Default to PNG if no valid extension

        scale = int(input("Enter scale (e.g., 10): ") or "10")
        dark = input("Enter foreground color (e.g., black, navy, #0000FF): ") or "black"
        light = input("Enter background color (e.g., white, #FFFFFF): ") or "white"
        error = input("Enter error correction level (L/M/Q/H): ") or "H"
        generate_custom_qr(data, filename, scale, dark, light, error)
    elif choice == "3":
        filename = input("Enter filename to save (e.g., qr_logo.png): ") or "qr_logo.png"
        scale = int(input("Enter scale (e.g., 10): ") or "10")
        dark = input("Enter foreground color (e.g., black, navy, #0000FF): ") or "black"
        light = input("Enter background color (e.g., white, #FFFFFF): ") or "white"
        error = input("Enter error correction level (L/M/Q/H): ") or "H"
        logo_path = input("Enter path to logo image (e.g., logo.png): ")
        generate_qr_with_logo(data, filename, scale, dark, light, error, logo_path)
    else:
        print("Invalid choice. Exiting.")

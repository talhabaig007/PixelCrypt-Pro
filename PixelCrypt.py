import os
import sys
import numpy as np
from PIL import Image
import random

class PixelCrypt:
    def __init__(self):
        self.tool_name = "PixelCrypt Pro"
        self.version = "2.0"
        self.author = "Secure Imaging Labs"
        
    def display_banner(self):
        banner = f"""
        ╔══════════════════════════════════════════════════════════════════╗
        ║                                                                  ║
        ║   ██████╗ ██╗██╗  ██╗███████╗██╗     ██████╗ ██████╗ ██████╗     ║
        ║   ██╔══██╗██║╚██╗██╔╝██╔════╝██║    ██╔════╝██╔═══██╗██╔══██╗    ║
        ║   ██████╔╝██║ ╚███╔╝ █████╗  ██║    ██║     ██║   ██║██████╔╝    ║
        ║   ██╔═══╝ ██║ ██╔██╗ ██╔══╝  ██║    ██║     ██║   ██║██╔══██╗    ║
        ║   ██║     ██║██╔╝ ██╗███████╗███████╗╚██████╗╚██████╔╝██║  ██║   ║
        ║   ╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝   ║
        ║                                                                  ║
        ║                 🖼️  IMAGE ENCRYPTION TOOL 🖼️                    ║
        ║                   Version {self.version} | {self.author}         ║
        ║                    Developed By Talha Baig                       ║
        ╚══════════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def load_image(self, image_path):
        """Load image and convert to numpy array"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            return img, img_array
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            return None, None
    
    def save_image(self, image_array, output_path):
        """Save numpy array as image"""
        try:
            img = Image.fromarray(image_array.astype('uint8'))
            img.save(output_path)
            print(f"✅ Image saved successfully: {output_path}")
            return True
        except Exception as e:
            print(f"❌ Error saving image: {e}")
            return False
    
    def xor_encrypt(self, image_array, key):
        """Encrypt image using XOR operation with key"""
        encrypted_array = image_array.copy()
        np.random.seed(key)
        key_matrix = np.random.randint(0, 256, image_array.shape, dtype=np.uint8)
        encrypted_array = np.bitwise_xor(encrypted_array, key_matrix)
        return encrypted_array
    
    def pixel_swap_encrypt(self, image_array, key):
        """Encrypt image by swapping pixel blocks"""
        encrypted_array = image_array.copy()
        np.random.seed(key)
        
        height, width = image_array.shape[:2]
        
        # Swap random pixel blocks
        for _ in range(min(1000, height * width // 100)):
            x1, y1 = np.random.randint(0, height), np.random.randint(0, width)
            x2, y2 = np.random.randint(0, height), np.random.randint(0, width)
            
            # Swap pixels
            encrypted_array[x1, y1], encrypted_array[x2, y2] = \
                encrypted_array[x2, y2].copy(), encrypted_array[x1, y1].copy()
        
        return encrypted_array
    
    def value_shift_encrypt(self, image_array, key):
        """Encrypt by shifting pixel values"""
        encrypted_array = image_array.copy()
        np.random.seed(key)
        shift_value = key % 256
        
        # Apply different shifts to RGB channels
        if len(image_array.shape) == 3:  # Color image
            for channel in range(3):
                encrypted_array[:, :, channel] = \
                    (encrypted_array[:, :, channel] + shift_value + channel * 50) % 256
        else:  # Grayscale
            encrypted_array = (encrypted_array + shift_value) % 256
        
        return encrypted_array
    
    def advanced_encrypt(self, image_array, key):
        """Combine multiple encryption techniques"""
        encrypted_array = image_array.copy()
        
        # Step 1: XOR encryption
        encrypted_array = self.xor_encrypt(encrypted_array, key)
        
        # Step 2: Value shifting
        encrypted_array = self.value_shift_encrypt(encrypted_array, key + 1)
        
        # Step 3: Pixel swapping
        encrypted_array = self.pixel_swap_encrypt(encrypted_array, key + 2)
        
        return encrypted_array
    
    def encrypt_image(self):
        """Main encryption function"""
        print("\n" + "═" * 60)
        print("🔒 ENCRYPT IMAGE")
        print("═" * 60)
        
        image_path = input("Enter image path to encrypt: ").strip()
        
        if not os.path.exists(image_path):
            print("❌ Image file not found!")
            return
        
        # Load image
        original_img, img_array = self.load_image(image_path)
        if img_array is None:
            return
        
        print(f"📊 Image loaded: {img_array.shape}")
        
        # Get encryption key
        try:
            key = int(input("Enter encryption key (integer): "))
        except ValueError:
            print("❌ Please enter a valid integer key!")
            return
        
        # Choose encryption method
        print("\n🔧 Encryption Methods:")
        print("1. XOR Encryption (Fast)")
        print("2. Pixel Swapping")
        print("3. Value Shifting")
        print("4. Advanced (All methods combined)")
        
        method = input("Choose method (1-4): ").strip()
        
        # Encrypt image
        print("\n🔄 Encrypting image...")
        
        if method == '1':
            encrypted_array = self.xor_encrypt(img_array, key)
            method_name = "XOR"
        elif method == '2':
            encrypted_array = self.pixel_swap_encrypt(img_array, key)
            method_name = "Pixel Swapping"
        elif method == '3':
            encrypted_array = self.value_shift_encrypt(img_array, key)
            method_name = "Value Shifting"
        elif method == '4':
            encrypted_array = self.advanced_encrypt(img_array, key)
            method_name = "Advanced"
        else:
            print("❌ Invalid method selected!")
            return
        
        # Save encrypted image
        base_name = os.path.splitext(image_path)[0]
        output_path = f"{base_name}_encrypted.png"
        
        if self.save_image(encrypted_array, output_path):
            print(f"\n🎯 ENCRYPTION SUCCESSFUL!")
            print(f"Method: {method_name}")
            print(f"Key: {key}")
            print(f"Original: {image_path}")
            print(f"Encrypted: {output_path}")
        
        return encrypted_array, key, method_name
    
    def decrypt_image(self):
        """Main decryption function"""
        print("\n" + "═" * 60)
        print("🔓 DECRYPT IMAGE")
        print("═" * 60)
        
        image_path = input("Enter encrypted image path: ").strip()
        
        if not os.path.exists(image_path):
            print("❌ Image file not found!")
            return
        
        # Load encrypted image
        encrypted_img, encrypted_array = self.load_image(image_path)
        if encrypted_array is None:
            return
        
        print(f"📊 Encrypted image loaded: {encrypted_array.shape}")
        
        # Get decryption key
        try:
            key = int(input("Enter decryption key (integer): "))
        except ValueError:
            print("❌ Please enter a valid integer key!")
            return
        
        # Choose decryption method
        print("\n🔧 Decryption Methods:")
        print("1. XOR Decryption")
        print("2. Pixel Swapping Reverse")
        print("3. Value Shifting Reverse")
        print("4. Advanced Reverse")
        
        method = input("Choose method (1-4): ").strip()
        
        # Decrypt image
        print("\n🔄 Decrypting image...")
        
        if method == '1':
            # XOR is symmetric - same operation for decryption
            decrypted_array = self.xor_encrypt(encrypted_array, key)
        elif method == '2':
            # Pixel swapping is symmetric
            decrypted_array = self.pixel_swap_encrypt(encrypted_array, key)
        elif method == '3':
            # Reverse value shifting
            decrypted_array = encrypted_array.copy()
            np.random.seed(key)
            shift_value = key % 256
            
            if len(encrypted_array.shape) == 3:
                for channel in range(3):
                    decrypted_array[:, :, channel] = \
                        (decrypted_array[:, :, channel] - shift_value - channel * 50) % 256
            else:
                decrypted_array = (decrypted_array - shift_value) % 256
        elif method == '4':
            # Reverse advanced encryption
            decrypted_array = self.pixel_swap_encrypt(encrypted_array, key + 2)
            decrypted_array = self.value_shift_encrypt(decrypted_array, key + 1)
            decrypted_array = self.xor_encrypt(decrypted_array, key)
        else:
            print("❌ Invalid method selected!")
            return
        
        # Save decrypted image
        base_name = os.path.splitext(image_path)[0]
        if "_encrypted" in base_name:
            base_name = base_name.replace("_encrypted", "_decrypted")
        else:
            base_name = base_name + "_decrypted"
        
        output_path = f"{base_name}.png"
        
        if self.save_image(decrypted_array, output_path):
            print(f"\n🎯 DECRYPTION SUCCESSFUL!")
            print(f"Key: {key}")
            print(f"Encrypted: {image_path}")
            print(f"Decrypted: {output_path}")
        
        return decrypted_array
    
    def preview_encryption(self):
        """Show different encryption methods on sample data"""
        print("\n" + "═" * 60)
        print("👀 ENCRYPTION METHODS PREVIEW")
        print("═" * 60)
        
        # Create a sample image
        sample_array = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Add some patterns
        sample_array[20:40, 20:80] = [255, 0, 0]    # Red rectangle
        sample_array[60:80, 20:80] = [0, 255, 0]    # Green rectangle
        sample_array[40:60, 40:60] = [0, 0, 255]    # Blue square
        
        key = 12345
        
        print("Sample image patterns created for demonstration.")
        print("Available encryption techniques:")
        print("• XOR: Fast bit-level encryption")
        print("• Pixel Swapping: Changes pixel positions")
        print("• Value Shifting: Modifies pixel values")
        print("• Advanced: Combines all methods")
        print(f"Demo Key: {key}")
        
        input("\nPress Enter to continue...")
    
    def display_help(self):
        """Display help information"""
        print("\n" + "═" * 60)
        print("📖 PIXELCRYPT PRO - HELP")
        print("═" * 60)
        
        help_text = """
        🔐 How PixelCrypt Pro Works:
        
        Pixel Manipulation Techniques:
        1. XOR Encryption
           • Each pixel is XORed with random values generated from key
           • Fast and reversible
           • Same operation for encryption and decryption
        
        2. Pixel Swapping
           • Randomly swaps pixel positions in the image
           • Changes spatial arrangement of pixels
           • Uses seed from key for reproducible swaps
        
        3. Value Shifting
           • Shifts pixel values by a fixed amount
           • Different shifts for RGB channels
           • Uses modulo 256 to stay in valid range
        
        4. Advanced Encryption
           • Combines all three methods for maximum security
           • Multiple layers of encryption
        
        📝 Usage Tips:
        • Use the same key for encryption and decryption
        • Save your encryption keys securely
        • PNG format recommended for lossless saving
        • Test with small images first
        
        🔒 Security Notes:
        • This is educational software
        • Not suitable for highly sensitive data
        • Demonstrates basic cryptography concepts
        """
        print(help_text)
    
    def main_menu(self):
        """Main menu interface"""
        while True:
            self.clear_screen()
            self.display_banner()
            
            print("\n" + "═" * 60)
            print("🎮 MAIN MENU")
            print("═" * 60)
            print("1. 🔒 Encrypt Image")
            print("2. 🔓 Decrypt Image")
            print("3. 👀 Encryption Methods Preview")
            print("4. 📖 Help & Information")
            print("5. 🚪 Exit")
            print("═" * 60)
            
            choice = input("\nSelect an option (1-5): ").strip()
            
            if choice == '1':
                self.clear_screen()
                self.display_banner()
                self.encrypt_image()
                input("\nPress Enter to continue...")
            
            elif choice == '2':
                self.clear_screen()
                self.display_banner()
                self.decrypt_image()
                input("\nPress Enter to continue...")
            
            elif choice == '3':
                self.clear_screen()
                self.display_banner()
                self.preview_encryption()
                input("\nPress Enter to continue...")
            
            elif choice == '4':
                self.clear_screen()
                self.display_banner()
                self.display_help()
                input("\nPress Enter to continue...")
            
            elif choice == '5':
                print("\n" + "═" * 60)
                print("👋 Thank you for using PixelCrypt Pro!")
                print("🖼️  Keep Your Images Secure! 🖼️")
                print("═" * 60)
                break
            
            else:
                print("❌ Invalid choice! Please select 1-5.")
                input("Press Enter to continue...")

def main():
    """Main function"""
    try:
        # Check if required packages are installed
        try:
            import numpy as np
            from PIL import Image
        except ImportError as e:
            print("❌ Required packages not installed!")
            print("Please install using:")
            print("pip install numpy pillow")
            return
        
        tool = PixelCrypt()
        tool.main_menu()
    
    except KeyboardInterrupt:
        print("\n\n⚠️  Program interrupted by user.")
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    main()
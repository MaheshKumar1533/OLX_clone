from django.core.management.base import BaseCommand
import base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend


class Command(BaseCommand):
    help = 'Generate VAPID keys for Web Push notifications'

    def handle(self, *args, **options):
        try:
            # Generate private key
            private_key = ec.generate_private_key(
                ec.SECP256R1(),
                default_backend()
            )
            
            # Get public key
            public_key = private_key.public_key()
            
            # Serialize private key to PEM format
            private_pem = private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ).decode('utf-8')
            
            # Serialize public key to uncompressed point format
            public_numbers = public_key.public_numbers()
            x = public_numbers.x.to_bytes(32, byteorder='big')
            y = public_numbers.y.to_bytes(32, byteorder='big')
            public_bytes = b'\x04' + x + y
            
            # Convert to base64url format (without padding)
            public_b64 = base64.urlsafe_b64encode(public_bytes).decode('utf-8').rstrip('=')
            
            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS('VAPID Keys Generated Successfully'))
            self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
            
            self.stdout.write(self.style.WARNING('Add these to your .env file:\n'))
            self.stdout.write(f'VAPID_PRIVATE_KEY="{private_pem.strip()}"')
            self.stdout.write(f'\nVAPID_PUBLIC_KEY="{public_b64}"')
            self.stdout.write(f'\nVAPID_ADMIN_EMAIL="mailto:studiswap@gmail.com"\n')
            
            self.stdout.write(self.style.SUCCESS('\n' + '='*60))
            self.stdout.write(self.style.SUCCESS('IMPORTANT: Keep the private key secure!'))
            self.stdout.write(self.style.SUCCESS('Never commit .env file to version control!'))
            self.stdout.write(self.style.SUCCESS('='*60 + '\n'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error generating VAPID keys: {str(e)}'))
            import traceback
            self.stdout.write(traceback.format_exc())

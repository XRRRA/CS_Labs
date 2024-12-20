import subprocess
import os
import argparse

# Directories and Files
ROOT_CA_DIR = "rootCA"
SERVER_DIR = "server"
CLIENT_DIR = "client"
CA_KEY = os.path.join(ROOT_CA_DIR, "ca-key.pem")
CA_CERT = os.path.join(ROOT_CA_DIR, "ca-cert.pem")
SERVER_KEY = os.path.join(SERVER_DIR, "server-key.pem")
SERVER_CERT = os.path.join(SERVER_DIR, "server-cert.pem")
SERVER_CSR = os.path.join(SERVER_DIR, "server-req.pem")
CLIENT_KEY = os.path.join(CLIENT_DIR, "client-key.pem")
CLIENT_CERT = os.path.join(CLIENT_DIR, "client-cert.pem")
CLIENT_CSR = os.path.join(CLIENT_DIR, "client-req.pem")
FILE_TO_SIGN = "test_file.txt"
SIGNATURE_FILE = "file.sig"


# Utility Function
def run_command(command, description):
    try:
        subprocess.run(command, shell=True, check=True, text=True)
        print(f"[SUCCESS] {description}")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description}\n{e}")


# Step 1: Generate the CA's Private Key and Certificate
def setup_ca():
    os.makedirs(ROOT_CA_DIR, exist_ok=True)
    print("Creating CA private key...")
    run_command(f"openssl genrsa -out {CA_KEY} 2048", "Generating CA private key")

    print("Creating CA certificate...")
    run_command(
        f"openssl req -new -x509 -nodes -days 3650 -key {CA_KEY} -out {CA_CERT} "
        f'-subj "/C=MD/ST=Chisinau/L=Chisinau/O=IordanLiviu/CN=IordanLiviu_CA"',
        "Generating CA certificate",
    )


# Step 2: Generate the Server's Private Key and Certificate
def setup_server():
    os.makedirs(SERVER_DIR, exist_ok=True)

    print("Creating server private key...")
    run_command(f"openssl genrsa -out {SERVER_KEY} 2048", "Generating server private key")

    print("Creating server certificate request...")
    run_command(
        f"openssl req -new -key {SERVER_KEY} -out {SERVER_CSR} "
        f'-subj "/C=MD/ST=Chisinau/L=Chisinau/O=IordanLiviu/CN=Server"',
        "Generating server CSR",
    )

    print("Signing server certificate with CA...")
    run_command(
        f"openssl x509 -req -days 365 -set_serial 01 -in {SERVER_CSR} -out {SERVER_CERT} "
        f"-CA {CA_CERT} -CAkey {CA_KEY}",
        "Signing server certificate",
    )


# Step 3: Generate the Client's Private Key and Certificate
def setup_client():
    os.makedirs(CLIENT_DIR, exist_ok=True)

    print("Creating client private key...")
    run_command(f"openssl genrsa -out {CLIENT_KEY} 2048", "Generating client private key")

    print("Creating client certificate request...")
    run_command(
        f"openssl req -new -key {CLIENT_KEY} -out {CLIENT_CSR} "
        f'-subj "/C=MD/ST=Chisinau/L=Chisinau/O=IordanLiviu/CN=Client"',
        "Generating client CSR",
    )

    print("Signing client certificate with CA...")
    run_command(
        f"openssl x509 -req -days 365 -set_serial 02 -in {CLIENT_CSR} -out {CLIENT_CERT} "
        f"-CA {CA_CERT} -CAkey {CA_KEY}",
        "Signing client certificate",
    )


# Step 4: Verify Certificates
def verify_certificates():
    print("Verifying server certificate...")
    run_command(
        f"openssl verify -CAfile {CA_CERT} {SERVER_CERT}",
        "Verifying server certificate",
    )

    print("Verifying client certificate...")
    run_command(
        f"openssl verify -CAfile {CA_CERT} {CLIENT_CERT}",
        "Verifying client certificate",
    )


# Step 5: Sign a File
def sign_file():
    print(f"Signing file {FILE_TO_SIGN} with client private key...")
    run_command(
        f"openssl dgst -sha256 -sign {CLIENT_KEY} -out {SIGNATURE_FILE} {FILE_TO_SIGN}",
        f"Signing file {FILE_TO_SIGN}",
    )


# Step 6: Verify a File's Signature
def verify_file_signature():
    print(f"Verifying signature for file {FILE_TO_SIGN}...")

    # Extract public key from the client certificate
    public_key_file = "temp_pubkey.pem"
    try:
        run_command(
            f"openssl x509 -in {CLIENT_CERT} -pubkey -noout -out {public_key_file}",
            "Extracting public key from client certificate",
        )

        # Verify the file's signature using the extracted public key
        run_command(
            f"openssl dgst -sha256 -verify {public_key_file} -signature {SIGNATURE_FILE} {FILE_TO_SIGN}",
            f"Verifying signature of file {FILE_TO_SIGN}",
        )
    finally:
        # Clean up the temporary public key file
        if os.path.exists(public_key_file):
            os.remove(public_key_file)


# Main Functionality
parser = argparse.ArgumentParser(description="PKI Setup with OpenSSL")
parser.add_argument("action", choices=["setup-ca", "setup-server", "setup-client", "verify", "sign-file", "verify-file"], help="Action to perform")
args = parser.parse_args()

if args.action == "setup-ca":
    setup_ca()
elif args.action == "setup-server":
    setup_server()
elif args.action == "setup-client":
    setup_client()
elif args.action == "verify":
    verify_certificates()
elif args.action == "sign-file":
    sign_file()
elif args.action == "verify-file":
    verify_file_signature()
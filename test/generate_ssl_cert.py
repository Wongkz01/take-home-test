from OpenSSL import crypto

def generate_self_signed_cert(cert_file, key_file):
    # Generate a new key pair
    key = crypto.PKey()
    key.generate_key(crypto.TYPE_RSA, 2048)

    # Create a self-signed certificate
    cert = crypto.X509()
    cert.get_subject().CN = "localhost"  # Common Name (CN) for the certificate
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(365 * 24 * 60 * 60)  # Valid for one year
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(key)
    cert.sign(key, "sha256")

    # Save the certificate and private key to files
    with open(cert_file, "wb") as f:
        f.write(crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    with open(key_file, "wb") as f:
        f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, key))

# Generate the self-signed certificate and private key files
generate_self_signed_cert(r"/test/certificate.crt", r"C:\Users\R O G\PycharmProjects\Test\private_key.key")


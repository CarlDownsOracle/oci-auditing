# RSA key pair generation

Use any one of these:
* bash console on Linux
* git bash or cygwin or ubuntu console on Windows-10


Navigate to home directory, and create ".oci" directory to store the credentials:
    
    mkdir ~/.oci

Generate the private key with no passphrase:

    openssl genrsa -out ~/.oci/oci_api_key.pem 2048

Ensure that only you can read the private key file:

    chmod go-rwx ~/.oci/oci_api_key.pem

Generate the public key:

    openssl rsa -pubout -in ~/.oci/oci_api_key.pem -out ~/.oci/oci_api_key_public.pem
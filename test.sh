sudo podman build --tag test .
sudo podman run -p 50004:50000 test
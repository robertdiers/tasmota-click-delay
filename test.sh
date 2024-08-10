sudo podman build --tag test .
sudo podman run -p 50005:50000 test
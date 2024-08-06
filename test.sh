sudo podman build --tag test .
sudo podman run -p 50001:50000 test
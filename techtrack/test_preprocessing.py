from modules.inference.preprocessing import capture_udp_stream

if __name__ == "__main__":
    stream_url = 'udp://127.0.0.1:23000'
    print(f"Starting to capture video from {stream_url}...")
    capture_udp_stream(stream_url)
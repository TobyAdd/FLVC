import qoi
import subprocess

def decode_qoi_frame(compressed_data):
    return qoi.decode(compressed_data)

def read_video_metadata(flvc_file_path):
    with open(flvc_file_path, 'rb') as f:
        width = int.from_bytes(f.read(2), 'little')
        height = int.from_bytes(f.read(2), 'little')
        fps = int.from_bytes(f.read(2), 'little')
        frame_count = int.from_bytes(f.read(8), 'little')

        print(f"Video: width={width}, height={height}, FPS={fps}, frames={frame_count}")
        return width, height, fps, frame_count

def process_flvc_to_mp4(flvc_file_path, mp4_file_path):
    width, height, fps, frame_count = read_video_metadata(flvc_file_path)

    ffmpeg_command = [
        'ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-pix_fmt', 'rgb24',
        '-s', f'{width}x{height}',
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-b:v', '0',
        '-pix_fmt', 'yuv420p',
        '-preset', 'ultrafast',
        '-vf', 'vflip',
        '-an',
        mp4_file_path
    ]

    with open(flvc_file_path, 'rb') as f:
        f.seek(2 + 2 + 2 + 8)

        with subprocess.Popen(ffmpeg_command, stdin=subprocess.PIPE) as proc:
            for _ in range(frame_count):
                qoi_size = int.from_bytes(f.read(4), 'little')
                qoi_data = f.read(qoi_size)
                raw_rgb_data = decode_qoi_frame(qoi_data)
                
                if raw_rgb_data.size > 0:
                    proc.stdin.write(raw_rgb_data)

            proc.stdin.close()
            proc.wait()

    print(f"Done! Video saved as {mp4_file_path}")


flvc_file_path = input("Enter the path for the input file (example input.flvc): ")
mp4_file_path = input("Enter the path for the output file (example output.mp4): ")

process_flvc_to_mp4(flvc_file_path, mp4_file_path)

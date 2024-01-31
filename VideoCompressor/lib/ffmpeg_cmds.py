def get_vide_info(input_video_path):
    cmd = [
        'ffprobe', '-v', 'error', '-select_streams', 'v:0',
        '-show_entries', 'stream=width,height,bit_rate',
        '-of', 'json', input_video_path
    ]
    return cmd

def compress(input_file_path, output_file_path, bitrate):
    cmd = [
    'ffmpeg', '-i', input_file_path, '-b:v', bitrate,
    '-vcodec', 'libx264', '-preset', 'medium', output_file_path
    ]
    return cmd

def change_resolution(input_file_path, width, height, output_vide_path):
    cmd = [
        'ffmpeg', '-i', input_file_path, '-vf', f'scale={width}:{height}',
        '-c:a', 'copy', 
        output_vide_path
    ]
    return cmd

def change_aspect_ratio(input_file_path, bit_rate, ratio, output_vide_path):
    cmd = [
    'ffmpeg', '-i', input_file_path, '-b:v', bit_rate,
    '-vcodec', 'libx264', '-preset', 'medium', '-aspect', ratio, output_vide_path
        ] 
    return cmd
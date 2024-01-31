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

def extract_mp3(input_file_path, output_vide_path):
    cmd = [
        'ffmpeg', '-i', input_file_path, '-q:a', '0', '-map', 'a?', output_vide_path,       
        ]
    return cmd

def convert_to_gif(input_file_path, time_range, output_vide_path):
    cmd = [
        'ffmpeg',
        '-ss', str(time_range[0]),            
        '-t', str(int(time_range[1]) - int(time_range[0])),          
        '-i', input_file_path,                     
        '-vf', 'fps=10,scale=320:-1:flags=lanczos',  
        '-c:v', 'gif',                        
        '-f', 'gif',                          
        output_vide_path                       
        ]
    return cmd

def convert_to_webm(input_file_path, time_range, output_vide_path):
    cmd = [
        'ffmpeg',
        '-ss', str(time_range[0]),                
        '-t', str(int(time_range[1]) - int(time_range[0])),              
        '-i', input_file_path,                         
        '-c:v', 'libvpx-vp9',                     
        '-c:a', 'libvorbis',                      
        '-b:v', '1M',                             
        '-b:a', '128k',                           
        output_vide_path                          
        ]
    return cmd
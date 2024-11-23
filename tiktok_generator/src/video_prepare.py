import multiprocessing
import os
import subprocess
import random

from utils import *

HOME = Path.cwd()


def prepare_background(background_mp4: str, filename_mp3: str, filename_srt: str, verbose: bool = False) -> str:
    video_info = get_info(background_mp4, kind='video')
    video_duration = int(round(video_info.get('duration'), 0))

    audio_info = get_info(filename_mp3, kind='audio')
    audio_duration_int = int(round(audio_info.get('duration'), 0))

    ss = random.randint(0, (video_duration-audio_duration_int))
    audio_duration = convert_time(audio_duration_int)
    if ss < 0:
        ss = 0

    srt_raw = filename_srt
    srt_filename = filename_srt.name
    srt_path = filename_srt.parent.absolute()

    directory = HOME / 'output'
    if not directory.exists():
        directory.mkdir()

    outfile = f"{HOME}{os.sep}output{os.sep}output_{ss}.mp4"

    if verbose:
        rich_print(
            f"{filename_srt = }\n{background_mp4 = }\n{filename_mp3 = }\n", style='bold green')

    args = [
        "ffmpeg",
        "-ss", str(ss),
        "-t", str(audio_duration),
        "-i", background_mp4,
        "-i", filename_mp3,
        "-i", Path("./background_music/sample_background.mp3").absolute(),
        "-map", "0:v",
        "-map", "1:a",
        "-map", "2:a",
        "-filter_complex", f"[1:a]volume=2[a1];[2:a]afade=t=out:st={audio_duration_int-2}:d={2}[a2];[a1][a2]amerge=inputs=2",
        "-vf", f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=lanczos, gblur=sigma=2, ass='{srt_raw.absolute()}'",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-ac", "2",
        "-b:a", "192K",
        "-shortest",
        f"{outfile}",
        "-y",
        "-threads", f"{multiprocessing.cpu_count()}"]

    if verbose:
        rich_print('[i] FFMPEG Command:\n'+' '.join(args)+'\n', style='yellow')

    with KeepDir() as keep_dir:
        keep_dir.chdir(srt_path)
        subprocess.run(args, check=True)

    return outfile


def create_video_with_ffmpeg(image_dir, output_file, duration):
    # Generate the input file pattern
    input_pattern = os.path.join(image_dir, "image%d.png")  # Adjust naming as needed

    file_num = len([name for name in os.listdir(image_dir)])

    if file_num == 0:
        raise Exception("Need to have at least one file")

    
    # Build the FFmpeg command
    command = [
        "ffmpeg",
        "-y",  # Overwrite output file if it exists
        "-r", str(file_num/duration),
        "-t", str(duration),
        "-i", input_pattern,
        "-vcodec", "libx264",
        "-crf", "25",
        "-pix_fmt", "yuv420p",
        "-filter_complex", "fps=30",
        output_file
    ]

    # Run the command
    subprocess.run(command, check=True)

   
    return  Path(output_file).absolute()

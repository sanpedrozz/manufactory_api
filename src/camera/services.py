import os
import re
import hashlib
import subprocess
import msgpack

from aiohttp import ClientSession
from datetime import datetime, timedelta
from typing import Dict, List

from src.camera.schemas import CameraModel
from src.config import settings

__all__ = ['get_video']

HEADERS = {'Content-Type': 'application/x-msgpack'}
VERSION = 57


async def get_video(camera: CameraModel) -> str:
    file_name = await _get_h265(camera)
    file_name = _convert_h265_to_mp4(file_name)
    return file_name


def _get_digest_headers(www_authenticate: str, method: str, url: str, username: str, password: str) -> Dict[str, str]:
    pattern = re.compile(r'(\w+)=["]?([^",]+)["]?,?')
    auth_values = {k: v for k, v in pattern.findall(www_authenticate)}
    realm = auth_values.get('realm', '')
    nonce = auth_values.get('nonce', '')
    qop = auth_values.get('qop', 'auth')
    opaque = auth_values.get('opaque', '')
    nc = '00000001'
    cnonce = hashlib.md5(os.urandom(8)).hexdigest()
    ha1 = hashlib.md5(f"{username}:{realm}:{password}".encode()).hexdigest()
    ha2 = hashlib.md5(f"{method}:{url}".encode()).hexdigest()
    response_digest = hashlib.md5(
        f"{ha1}:{nonce}:{nc}:{cnonce}:{qop}:{ha2}".encode()
    ).hexdigest()
    authorization_header = (
        f'Digest username="{username}", realm="{realm}", nonce="{nonce}", uri="{url}", '
        f'response="{response_digest}", qop={qop}, nc={nc}, cnonce="{cnonce}", opaque="{opaque}"'
    )
    return {'Authorization': authorization_header}


async def _fetch_with_digest_auth(session: ClientSession, url: str, method: str = "POST", **kwargs) -> bytes:
    headers = kwargs.pop('headers', {})
    async with session.request(method, url, headers=headers, **kwargs) as response:
        if response.status == 401:
            www_authenticate = response.headers.get('WWW-Authenticate', '')
            auth_headers = _get_digest_headers(www_authenticate, method, url, settings.CAMERAS_LOGIN,
                                               settings.CAMERAS_PASSWORD)
            headers.update(auth_headers)
            async with session.request(method, url, headers=headers, **kwargs) as auth_response:
                return await auth_response.read()
        return await response.read()


async def _get_h265(camera: CameraModel, delta_start: int = 15, delta_end: int = 0) -> str:
    async with ClientSession() as session:
        current_time = datetime.now()

        def format_time_delta(delta: timedelta) -> List[int]:
            return list(map(int, (current_time + delta).strftime("%Y, %m, %d, %H, %M, %S").split(", ")))

        start_time = format_time_delta(-timedelta(seconds=delta_start))
        end_time = format_time_delta(timedelta(seconds=delta_end))

        file_name = f'media/m{current_time.strftime("%Y_%m_%d_%H_%M_%S")}'
        full_name = f'{file_name}.h265'

        frames_request_data = msgpack.packb({
            "method": "archive.get_frames_list",
            "params": {
                "channel": camera.cameraId,
                "stream": "video",
                "start_time": start_time,
                "end_time": end_time
            },
            "version": VERSION
        })

        frames_response_data = await _fetch_with_digest_auth(session, camera.cameraURL, data=frames_request_data,
                                                             headers=HEADERS)
        frames_list = msgpack.unpackb(frames_response_data)

        frames_id_list: List[List[str]] = []
        key_frame = 0
        for frame in frames_list.get("result", {}).get("frames_list", []):
            if frame['gop_index'] == 0:
                key_frame += 1
                frames_id_list.append([])
            elif key_frame == 0:
                continue
            frames_id_list[key_frame - 1].append(frame['id'])

        frame_request_args = [{"method": "archive.get_frame",
                               "params": {"channel": camera.cameraId,
                                          "stream": "video",
                                          "id": frame_id},
                               "version": VERSION} for frame_keys in frames_id_list for frame_id in frame_keys]
        frame_request_data = msgpack.packb(frame_request_args)

        frames_response_data = await _fetch_with_digest_auth(session, camera.cameraURL, data=frame_request_data,
                                                             headers=HEADERS)
        frames = msgpack.unpackb(frames_response_data, raw=True)

        os.makedirs(os.path.dirname(full_name), exist_ok=True)
        with open(full_name, 'wb') as result_file:
            for frame in frames:
                result_file.write(frame[b'result'][b'frame'][b'data'])
        return file_name


def _convert_h265_to_mp4(file_name: str) -> str:
    ffmpeg = r'C:\ffmpeg\bin\ffmpeg.exe' if os.name == 'nt' else 'ffmpeg'
    command = [ffmpeg, '-loglevel', 'quiet', '-i', f'{file_name}.h265', '-preset', 'ultrafast', '-y',
               f'{file_name}.mp4']
    try:
        subprocess.run(command, check=True, stderr=subprocess.STDOUT)
        os.remove(f'{file_name}.h265')
    except subprocess.CalledProcessError as e:
        print(f"Error converting file {file_name}: {e}")
    return f'{file_name}.mp4'

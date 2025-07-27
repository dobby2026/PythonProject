"""
pip install opencv-python

"""

import cv2
import numpy as np
from PIL import Image


def extract_n_frames(input_video, target_frame_count, remove_white=True, white_threshold=240):
    cap = cv2.VideoCapture(input_video)

    # 전체 프레임 수 계산
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print(f"전체 프레임 수: {total_frames}")

    # 추출할 프레임 인덱스 계산
    if target_frame_count >= total_frames:
        frame_indices = list(range(total_frames))
    else:
        # 균등하게 분배
        step = total_frames / target_frame_count
        frame_indices = [int(i * step) for i in range(target_frame_count)]

    print(f"추출할 프레임 수: {len(frame_indices)}")

    extracted_count = 0

    for frame_idx in frame_indices:
        # 특정 프레임으로 이동
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
        ret, frame = cap.read()

        if not ret:
            continue

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if remove_white:
            # 흰 배경 제거
            hsv = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2HSV)
            lower_white = np.array([0, 0, white_threshold])
            upper_white = np.array([180, 30, 255])
            mask = cv2.inRange(hsv, lower_white, upper_white)

            # RGBA 이미지 생성
            rgba_frame = cv2.cvtColor(frame_rgb, cv2.COLOR_RGB2RGBA)
            rgba_frame[:, :, 3] = 255 - mask

            img = Image.fromarray(rgba_frame, 'RGBA')
        else:
            img = Image.fromarray(frame_rgb, 'RGB')

        img.save(f'grim_reaper_frame_{extracted_count:04d}.png')
        extracted_count += 1
        print(f"추출 완료: {extracted_count}/{len(frame_indices)}")

    cap.release()
    print(f"총 {extracted_count}개 프레임 추출 완료!")


# 사용 예시
extract_n_frames('input.mp4', target_frame_count=10, remove_white=True)
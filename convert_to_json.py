import os
import json

# 텍스트 파일이 저장된 디렉토리 경로
directory_path = './outputs/'
# JSON 파일이 저장될 디렉토리 경로
output_directory = './json/'
# JSON 파일 경로
json_file_path = os.path.join(output_directory, "youtube.json")

# JSON 파일 저장 디렉토리 생성
os.makedirs(output_directory, exist_ok=True)

# 기존 JSON 파일이 있다면 로드
if os.path.exists(json_file_path):
    with open(json_file_path, 'r', encoding='utf-8') as json_file:
        data_list = json.load(json_file)
else:
    data_list = []

# 현재 JSON 파일에 있는 제목 리스트
existing_titles = [data['title'] for data in data_list]

# 디렉토리 내 모든 텍스트 파일을 처리
for filename in os.listdir(directory_path):
    if filename.endswith('.txt'):
        file_path = os.path.join(directory_path, filename)
        
        # 파일 읽기
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # 제목과 내용 분리
        title = filename.replace('.txt', '')
        body = content

        # 제목이 이미 존재하지 않는 경우에만 추가
        if title not in existing_titles:
            data = {
                "title": title,
                "body": body
            }
            data_list.append(data)
            existing_titles.append(title)

# 하나의 JSON 파일로 저장
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(data_list, json_file, ensure_ascii=False, indent=4)

print(f"모든 텍스트 파일이 JSON 파일에 저장되었습니다: {json_file_path}")

import os
import shutil
import subprocess
import sys
import time
import platform

import cv2
import numpy as np
import requests
from PIL import Image
from sentence_transformers import util

API_ENDPOINT = os.environ.get("API_ENDPOINT", "http://127.0.0.1:8000/api")


def piecewise_function(x: float, k: float = 0.24) -> float:
    # Apply the sigmoid function for x > 80
    sigmoid_part = 100 / (1 + np.exp(-k * (x - 78)))
    # Apply the linear function for x <= 80
    slope = (100 / (1 + np.exp(-k * (80 - 78)))) / 80
    linear_part = slope * x

    # Combine the two parts using numpy's where function
    if x > 80:
        return sigmoid_part
    else:
        return linear_part


def get_word_count(file_path: str) -> int:
    with open(file_path, "r") as file:
        content = file.read()
        words = content.split()
        return len(words)


def linear_normalize(value, min_value, max_value):
    return (value - min_value) / (max_value - min_value)


def convert_ps_to_png(ps_file: str, png_file: str) -> str:
    # Ensure the output directory exists
    # Open the PostScript file and convert it to a PNG file
    img = Image.open(ps_file)
    img.save(png_file)


def extract_object(image_path: str):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    x, y, w, h = cv2.boundingRect(contours[0])

    object_img = image[y: y + h, x: x + w]
    return object_img


def calculate_pixel_difference_similarity(image1_path, image2_path):
    # Extract objects from the images
    img1 = cv2.imread(image1_path)
    img2 = cv2.imread(image2_path)
    # Convert images to grayscale
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY).astype(np.int16)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY).astype(np.int16)
    # Ensure the images have the same size for comparison
    img1 = cv2.resize(img1, (500, 500))
    img2 = cv2.resize(img2, (500, 500))

    # Create a mask to ignore white pixels (value 255)
    mask = (img2 == 255).astype(
        np.uint8
    )  # create mask with 1 where img2 is white(255), and 0 otherwise

    valid_pixel = 0
    similar_pixel = 0
    THRESHOLD = 10
    # total_pixel = 0
    for i in range(500):
        for j in range(500):
            if mask[i][j] == 1:  # if mask is 1, ignore this pixel
                continue
            valid_pixel += 1
            if abs(img1[i][j] - img2[i][j]) <= THRESHOLD:
                similar_pixel += 1
    # print("similar_pixel: ", similar_pixel)
    pixel_similarity = similar_pixel / valid_pixel
    return pixel_similarity


def calculate_clip_similarity(model, image1_path: str, image2_path: str):
    # Encode the images
    original_image = Image.open(image1_path)
    drawn_image = Image.open(image2_path)

    encoded_images = model.encode(
        [original_image, drawn_image], batch_size=2, convert_to_tensor=True
    )

    # Compute cosine similarity
    #  = model.similarity(encoded_images[0], encoded_images[1])
    similarity = util.cos_sim(encoded_images[0], encoded_images[1]).item()
    print(f"############### Similarity: {similarity}")
    # Normalize similarity score to a range of -1 to 1
    # similarity = linear_normalize(similarity, -1, 1)

    return similarity


def judge_logic(image_url: str, result_path: str, word_count: int, execution_time: float):
    pixel_similarity = calculate_pixel_difference_similarity(image_url, result_path)
    print("origin pixel_similarity: ", pixel_similarity)
    pixel_similarity = min(1, linear_normalize(pixel_similarity, 0, 0.025))
    product = 1.1
    data = {"image1_path": image_url, "image2_path": result_path}
    res = requests.post(f"{API_ENDPOINT}/clip/", json=data)
    # print(f'res: {res.json()}')
    if res.status_code == 200:
        print("===Similarity request success !===")
    clip_similarity = float(res.json()["similarity"])
    # model = SentenceTransformer('clip-ViT-B-32')
    # clip_similarity = calculate_clip_similarity(model, image_url, result_path)
    print("origin clip_similarity: ", clip_similarity)
    clip_similarity = max(0, linear_normalize(clip_similarity, 0.7, 1.0))
    # Normalize percentage difference to a similarity score (0 to 1)
    # Combine the similarity scores with equal weight

    # combined_similarity = min(1, 0.7 * pixel_similarity + 0.3 * clip_similarity)
    # print('pixel_similarity: ', pixel_similarity)
    print("clip_similarity: ", clip_similarity)
    # print('combined_similarity: ', combined_similarity)

    # word_count_score = 25 * (1 - max(0, linear_normalize(word_count, min_word_count, max_word_count)))
    # word_count_score = max(0, min(25, word_count_score))

    similarity_score = min(100 * clip_similarity * product, 100)
    if similarity_score > 10:
        total_score = similarity_score
    else:
        total_score = 0
    # print(f"Percentage Difference: {percentage_diff}%")
    print(f"Similarity score: {similarity_score}\n\n")
    print(f"Original total score: {total_score}")
    # total_score = round(piecewise_function(total_score), 2) # limit sigmoid value to 2 decimal places
    # print(f'Adjusted total score: {total_score}')
    return total_score, similarity_score


if __name__ == "__main__":
    start_time = time.time()
    # ps_file = sys.argv[1]  # Accept output path as a command-line argument
    submission_id = sys.argv[2]
    code_path = sys.argv[3]
    drawing_path = sys.argv[0]
    result_path = sys.argv[5]
    image_url = sys.argv[6]
    ps_src = "media/result/output.ps"
    ps_dest = f"media/result/ps/{submission_id}.ps"
    template_revise_path = sys.argv[4]
    # ps_dest = sys.argv[7]
    start_time = time.time()

    # 檢查作業系統
    python_runner = "python3"
    if platform.system() == "Windows":
        python_runner = "python"
    # 回傳資料
    data = {
        "score": 0,
        "fitness": 0,
        "word_count": 0,
        "execution_time": 0,
        "stdout": "",
        "stderr": "",
        "status": "fail",
    }
    try:
        print('##%%$$ Running code template')
        result = subprocess.run(
            [python_runner, template_revise_path],
            check=True,
            capture_output=True,
            text=True,
            timeout=30,
        )

    except subprocess.CalledProcessError as e:
        data["stderr"] = "Process crashed with the following error message :\n\n" + str(e)
        data["status"] = "fail"
        res = requests.post(
            f"{API_ENDPOINT}/submission/store/{submission_id}/",
            json=data,
        )

        print(f"Error: {e}")
        print(f'OUTPUT: {e.stdout}')
        print(f'ERROR: {e.stderr}')
        exit()
    except subprocess.TimeoutExpired as e:
        data["stderr"] = "Time Limit Exceeded"
        data["status"] = "fail"
        res = requests.post(
            f"{API_ENDPOINT}/submission/store/{submission_id}/",
            json=data,
        )

        print(f"Error: {e}")
        exit()

    print("### Subprocess executing finish")
    # Get stdout and stderr
    stdout = result.stdout
    stderr = result.stderr
    # Check if there were any errors
    if result.returncode != 0:
        print("Error occurred:", stderr)
    else:
        print("Output:", stdout)

    end_time = time.time()
    word_count = get_word_count(code_path)
    # turtle.done() # Uncomment this lin    e if you want to keep the turtle graphics window open

    execution_time = end_time - start_time
    shutil.copy(ps_src, ps_dest)
    data["stdout"] = stdout
    data["stderr"] = stderr
    data["status"] = "success"
    data["word_count"] = int(word_count)
    data["execution_time"] = int(execution_time)
    # check if the PostScript file was created
    if not os.path.exists(ps_dest):
        pass
    else:
        convert_ps_to_png(ps_dest, result_path)
        score, similarity_score = judge_logic(
            image_url, result_path, word_count, execution_time
        )
        # similarity_score = (similarity_score * 4) / 3
        print(f"Weighted similarity score: {similarity_score}")
        data["score"] = int(score)
        data["fitness"] = int(similarity_score)
    res = requests.post(
        f"{API_ENDPOINT}/submission/store/{submission_id}/",
        json=data,
    )

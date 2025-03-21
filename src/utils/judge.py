import subprocess
import os
import requests
import platform

API_ENDPOINT = os.environ.get("API_ENDPOINT", "http://127.0.0.1:8000/api")


# 修改 Template
def copy_and_modify_template(judge_template_path, template_revise_path, code_path):
    code_filename = os.path.basename(code_path)
    # Construct the import line
    import_line = f"from {code_filename.replace('.py', '')} import drawing\n"

    # Read the original template
    with open(judge_template_path, "r") as template_file:
        template_content = template_file.read()

    # Create the new content with the import line at the beginning
    new_content = import_line + template_content
    # new_content = template_content
    # Write the new content to the destination path
    with open(template_revise_path, "w") as new_template_file:
        new_template_file.write(new_content)


# At here, change the main_template code and drawing template code


def run_code(
        code_path,
        image_url,
        result_path,
        team_id,
        drawing_template_path,
        main_drawing_path,
        template_revise_path,
        submission_id,
):
    result_dir = os.path.dirname(result_path)
    ps_file = f"media/result/ps/{submission_id}.ps"
    if os.path.isfile(ps_file):
        # Remove the file
        os.remove(ps_file)
    # png_file = f"{result_dir}/{output_filename}.png"
    # Ensure the result directory exists
    os.makedirs(result_dir, exist_ok=True)
    os.makedirs("media/result/ps", exist_ok=True)

    copy_and_modify_template(drawing_template_path, template_revise_path, code_path)
    # 檢查作業系統
    python_runner = "python3"
    if platform.system() == "Windows":
        python_runner = "python"

    # Run the provided Python script to generate the PostScript file
    # Use check to raise an exception if the script fails
    try:
        subprocess.Popen(
            [
                python_runner,
                str(main_drawing_path),
                str(ps_file),
                str(submission_id),
                str(code_path),
                str(template_revise_path),
                str(result_path),
                str(image_url),
            ]
        )
    # 執行錯誤
    except subprocess.CalledProcessError as e:
        error_data = {
            "score": 0,
            "fitness": 0,
            "word_count": 0,
            "execute_time": 0,
            "stdout": e.stdout,
            "stderr": e.stderr,
            "status": "fail",
        }
        requests.post(
            f"{API_ENDPOINT}/submission/store/{submission_id}/",
            json=error_data,
        )


def judge_submission(
        code_path,
        image_url,
        result_path,
        team_id,
        drawing_template_path,
        main_drawing_path,
        template_revise_path,
        submission_id,
):
    image_url = f".{image_url}"

    run_code(
        code_path,
        image_url,
        result_path,
        team_id,
        drawing_template_path,
        main_drawing_path,
        template_revise_path,
        submission_id,
    )

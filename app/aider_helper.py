import subprocess
import os
import shutil
import subprocess
import tempfile
import uuid
import openai
from aider.coders import Coder
from dotenv import find_dotenv, dotenv_values
config = dotenv_values(find_dotenv())
client = openai.OpenAI(api_key=config["OPENAI_API_KEY"])


def clone_repo_and_run_aider(repo_url, file_to_change, instruction, area_to_focus):
    # Create a temporary directory
    temp_dir = tempfile.mkdtemp()

    try:
        # Clone the repository
        subprocess.run(['git', 'clone', repo_url, temp_dir], check=True)

        # Change directory to the cloned repository
        os.chdir(temp_dir)

        # Generate a unique UUID
        branch_name = 'oncal-fix-' + str(uuid.uuid4())

        # Checkout a new branch with the UUID as the branch name
        subprocess.run(['git', 'checkout', '-b', branch_name], check=True)
        # Call the run_aider function
        run_aider(file_to_change, instruction, area_to_focus, auto_commit=True)
        subprocess.run(['git', 'push', 'origin', branch_name], check=True)

    finally:
        # Change directory back to the original directory
        os.chdir(os.path.dirname(os.path.abspath(__file__)))

        # Remove the temporary directory
        shutil.rmtree(temp_dir)


def run_aider(file_to_change, instruction, area_to_focus, auto_commit=False):

    coder = Coder.create(client=client, fnames=[file_to_change], auto_commits=auto_commit)
    command = f"Fix the file according to instruction: {instruction} and you can focus on the area: {area_to_focus}\n"
    coder.run(command)

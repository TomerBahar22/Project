import sys
from python_terraform import Terraform, IsFlagged
from modules.input_user import InputUser
from modules.terraform_renderer import TerraformRenderer
import subprocess

def check_terraform_installed():
    try:
        result = subprocess.run(["terraform", "version"], capture_output=True, text=True)
        if result.returncode != 0:
            print("Terraform is not installed or not in PATH.")
            sys.exit(1)
        print(f"\nTerraform detected: {result.stdout.splitlines()[0]}")
    except FileNotFoundError:
        print("Terraform is not installed.")
        sys.exit(1)

def run_terraform():
    tf = Terraform(working_dir='terraform')

    print("\n=== Running terraform init ===")
    rc, out, err = tf.init(capture_output=False)
    if err and err.strip() != "":
        print(f" Init failed:\n{err}")
        sys.exit(1)

    print("\n=== Running terraform plan ===")
    rc, out, err = tf.plan(capture_output=False)
    if err and err.strip() != "":
        print(f" Plan failed:\n{err}")
        sys.exit(1)

    print("\n=== Running terraform apply ===")
    rc, out, err = tf.apply(
        skip_plan=True,
        capture_output=False,
        auto_approve=True,
        no_color=IsFlagged,
        lock=False 
    )
    if err and err.strip() != "":
        print(f" Apply failed:\n{err}")
        sys.exit(1)

    print("\n Terraform apply completed successfully.")

def destroy_infrastructure():
    print("\n Destroying infrastructure...")
    tf = Terraform(working_dir='terraform')
    return_code, stdout, stderr = tf.destroy(auto_approve=True)
    print(stdout)
    if stderr:
        print("stderr from destroy:")
        print(stderr)
    print("\n Destroy completed.")
    sys.exit(1)
    
def get_outputs():
    try:
        tf = Terraform(working_dir='terraform')
        outputs = tf.output()
        parsed_outputs = {}

        print("\n=== Terraform Outputs ===")
        for key, val in outputs.items():
            value = val.get("value", "N/A")
            parsed_outputs[key] = value
            print(f"{key}: {value}")

        destroy = input("\nDo you want to destroy the infrastructure? (yes/no): ").strip().lower()
        if destroy in ["yes", "y"]:
            destroy_infrastructure()

        return parsed_outputs

    except Exception as e:
        print(f"\n Failed to fetch outputs: {str(e)}")


if __name__ == "__main__":
    try:
        check_terraform_installed()

        # Step 1: Collect user input
        user = InputUser()
        context = user.get_user_input()

        # Step 2: Render .tf file
        renderer = TerraformRenderer()
        renderer.render(context)

        # Step 3: Run Terraform workflow
        run_terraform()

        # Step 4: Fetch and display outputs
        get_outputs()

    except Exception as e:
        print(f"\n Unexpected error: {str(e)}")
        sys.exit(1)

# AWS Automation with Terraform, Jinja2, and Boto3

This project automates the provisioning and validation of AWS infrastructure using:

- **Terraform** for declarative resource creation  
- **Jinja2** for dynamic Terraform config generation via Python  
- **Boto3** for post-deployment validation  
- **Python** to tie it all together into a clean, modular tool

---

## 📸 screen shot 

<img width="552" height="228" alt="Screenshot 2025-07-13 202547" src="https://github.com/user-attachments/assets/06b640f1-7d6f-4afb-af9a-1953be3cd722" />


---
I use the class `InputUser` to get the input of the machine, and I put it in the class `TerraformRenderer` using a Jinja2 template to generate Terraform configuration for AWS.

---
## 📦 Project Structure

```
project/
├── main.py
├── validature.py
├── aws_validation.json
├── terraform/
│   └── generated.tf
└── modules/
    ├── input_user.py
    └── terraform_renderer.py
```

---

## 🚀 How It Works

### 1. `main.py`
- Collects user input (AMI, instance type, region, LB name)
- Generates a Terraform configuration using Jinja2
- Runs `terraform init`, `plan`, `apply`
- Captures Terraform outputs (e.g., instance ID, DNS)

### 2. `validature.py`
Uses `boto3` to:
- Fetch the EC2 instance by ID  
- Verify it is running  
- Get the public IP  
- Retrieve the ALB DNS  
- Output result to `aws_validation.json`

**Example Output:**
```json
{
  "instance_id": "i-014c78c8124d22438",
  "instance_state": "running",
  "public_ip": "3.92.102.45",
  "load_balancer_dns": "tomer-lb-123456.elb.amazonaws.com"
}
```

---

## ✅ Benefits

- Full automation from input to provisioning to verification  
- Dynamic Terraform templating using Python & Jinja2  
- Resource validation with `boto3` and JSON output  
- Clear separation of logic via modules  
- Easy to expand with more AWS services

---

## ⚙️ Setup & Requirements

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt** should contain:
```
boto3
python-terraform
jinja2
```

### 2. Run the project

```bash
python3 main.py
python3 validature.py
```

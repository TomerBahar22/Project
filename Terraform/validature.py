import boto3
import json

def validate_with_boto3(instance_id: str, alb_dns: str, region: str = "us-east-2"):
    print("Starting AWS resource validation...")

    ec2 = boto3.client("ec2", region_name=region)
    elbv2 = boto3.client("elbv2", region_name=region)

    # Validate EC2 instance
    try:
        ec2_response = ec2.describe_instances(InstanceIds=[instance_id])
        instance = ec2_response['Reservations'][0]['Instances'][0]
        instance_state = instance['State']['Name']
        public_ip = instance.get('PublicIpAddress', 'N/A')
    except Exception as e:
        print(f"[ERROR] EC2 instance validation failed: {e}")
        return

    # Validate ALB
    try:
        lb_response = elbv2.describe_load_balancers()
        matched_dns = None
        for lb in lb_response['LoadBalancers']:
            print(f"Checking ALB DNS: {lb['DNSName']}")
            if alb_dns == lb['DNSName']:
                matched_dns = lb['DNSName']
                break

        if not matched_dns:
            print(f"[ERROR] ALB DNS '{alb_dns}' not found.")
            return

    except Exception as e:
        print(f"[ERROR] ALB validation failed: {e}")
        return

    # Write to JSON
    validation_data = {
        "instance_id": instance_id,
        "instance_state": instance_state,
        "public_ip": public_ip,
        "load_balancer_dns": matched_dns
    }

    with open("aws_validation.json", "w") as f:
        json.dump(validation_data, f, indent=4)

    print(" AWS resource validation complete. Output written to aws_validation.json")


# Example usage
if __name__ == "__main__":
    validate_with_boto3(
        instance_id="i-06cc60713e9060283",
        alb_dns="lb1305-1415260001.us-east-2.elb.amazonaws.com"
    )

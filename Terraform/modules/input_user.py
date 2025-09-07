class InputUser:
    def __init__(self):
        self.avilable_regions = ["us-east-2"]
        self.avilable_instance_types = ["t3.small", "t3.medium"]
        self.ami_choices = {
            "1": ("Ubuntu", "ami-0bb220fc4bffd88dd"),
            "2": ("Amazon Linux", "ami-02bf8ce06a8ed6092")
        }

    def get_user_input(self):
        ami = self._choose_ami()
        instance_type = self._choose_instance_type()
        region = self._choose_region()
        alb_name = self._choose_alb_name()
        az = region + "a"

        return {
            "ami_id": ami[1],
            "instance_type": instance_type,
            "region": region,
            "availability_zone": az,
            "load_balancer_name": alb_name
        }

    def _choose_ami(self):
        print("Choose AMI:")
        for key, (name, ami_id) in self.ami_choices.items():
            print(f"{key}. {name} ({ami_id})")
        while True:
            choice = input("Enter choice (1/2): ").strip()
            if choice in self.ami_choices:
                return self.ami_choices[choice]
            print("Invalid choice. Try again.")

    def _choose_instance_type(self):
        while True:
            instance = input("Enter instance type (t3.small or t3.medium): ").strip()
            if instance in self.avilable_instance_types:
                return instance
            print("Invalid instance type.")

    def _choose_region(self):
        region = input("Enter region (only us-east-2 is allowed): ").strip()
        if region not in self.avilable_regions:
            print("Invalid region. Defaulting to us-east-2.")
            return "us-east-2"
        return region

    def _choose_alb_name(self):
        return input("Enter Load Balancer name: ").strip() or "default-alb"

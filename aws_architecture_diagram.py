from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import EC2, AutoScaling
from diagrams.aws.database import RDS, RDSInstance
from diagrams.aws.network import ELB, InternetGateway, VPC, PublicSubnet, PrivateSubnet
from diagrams.aws.security import SecurityGroup
from diagrams.aws.general import Users
from diagrams.aws.storage import S3

with Diagram("FastAPI Multi-AZ Architecture", show=False, direction="TB"):
    users = Users("Users")
    
    with Cluster("VPC"):
        igw = InternetGateway("Internet Gateway")
        
        with Cluster("Availability Zone A"):
            with Cluster("Public Subnet A"):
                alb_a = ELB("ALB")
            
            with Cluster("Private Subnet A"):
                ec2_a = EC2("EC2 Instance A")
                
            with Cluster("DB Subnet A"):
                db_a = RDSInstance("RDS Primary")
        
        with Cluster("Availability Zone B"):
            with Cluster("Public Subnet B"):
                alb_b = ELB("ALB Standby")
            
            with Cluster("Private Subnet B"):
                ec2_b = EC2("EC2 Instance B")
                
            with Cluster("DB Subnet B"):
                db_b = RDSInstance("RDS Standby")
        
        # Auto Scaling Group
        asg = AutoScaling("Auto Scaling Group")
        
        # Security Groups
        alb_sg = SecurityGroup("ALB Security Group")
        ec2_sg = SecurityGroup("EC2 Security Group")
        rds_sg = SecurityGroup("RDS Security Group")
    
    # Connections
    users >> igw >> alb_a
    alb_a >> [ec2_a, ec2_b]
    asg >> [ec2_a, ec2_b]
    [ec2_a, ec2_b] >> db_a
    db_a >> db_b  # Multi-AZ replication
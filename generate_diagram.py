#!/usr/bin/env python3
"""
Generate AWS Architecture Diagram for FastAPI Multi-AZ Setup
Run: python generate_diagram.py
"""

try:
    from diagrams import Diagram, Cluster, Edge
    from diagrams.aws.compute import EC2, AutoScaling
    from diagrams.aws.database import RDS
    from diagrams.aws.network import ELB, InternetGateway
    from diagrams.aws.security import SecurityGroup
    from diagrams.aws.general import Users
    
    print("Generating AWS Architecture Diagram...")
    
    with Diagram("FastAPI Multi-AZ Architecture", show=False, direction="TB", filename="fastapi_aws_architecture"):
        users = Users("Users")
        
        with Cluster("AWS VPC (10.0.0.0/16)"):
            igw = InternetGateway("Internet Gateway")
            
            # Application Load Balancer in public subnets
            with Cluster("Public Subnets (Multi-AZ)"):
                alb = ELB("Application Load Balancer")
                alb_sg = SecurityGroup("ALB Security Group\n(HTTP/HTTPS)")
            
            # EC2 instances in private subnets
            with Cluster("Private Subnets (Multi-AZ)"):
                with Cluster("Auto Scaling Group"):
                    ec2_instances = [
                        EC2("EC2 Instance A\n(AZ-1a)"),
                        EC2("EC2 Instance B\n(AZ-1b)")
                    ]
                ec2_sg = SecurityGroup("EC2 Security Group\n(Port 8000)")
            
            # RDS in database subnets
            with Cluster("Database Subnets (Multi-AZ)"):
                rds = RDS("RDS PostgreSQL\n(Multi-AZ)")
                rds_sg = SecurityGroup("RDS Security Group\n(Port 5432)")
        
        # Traffic flow
        users >> Edge(label="HTTPS/HTTP") >> igw
        igw >> Edge(label="Internet Traffic") >> alb
        alb >> Edge(label="Health Checks\n& Load Balance") >> ec2_instances
        ec2_instances >> Edge(label="Database\nConnections") >> rds
    
    print("✅ Diagram generated successfully!")
    print("📁 File saved as: fastapi_aws_architecture.png")
    print("\n🏗️  Architecture includes:")
    print("   • VPC with public, private, and database subnets across 2 AZs")
    print("   • Internet Gateway for public access")
    print("   • Application Load Balancer in public subnets")
    print("   • Auto Scaling Group with EC2 instances in private subnets")
    print("   • Multi-AZ RDS PostgreSQL database")
    print("   • Security Groups with least privilege access")
    
except ImportError as e:
    print("❌ Missing dependencies. Install with:")
    print("   pip install -r requirements_diagram.txt")
    print(f"   Error: {e}")
except Exception as e:
    print(f"❌ Error generating diagram: {e}")
    print("Make sure Graphviz is installed on your system")
provider "aws" {
  region = "us-east-1"
}

resource "aws_key_pair" "deployer" {
  key_name   = "deployer-key"
  public_key = file("D:\\semester 6\\uni projects in D\\devops proj\\.ssh\\id_rsa.pub")# change path as needed
}

resource "aws_security_group" "allow_ssh_web" {
  name        = "allow_ssh_web"
  description = "Allow SSH and HTTP/HTTPS"

  ingress {
    description = "SSH"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_instance" "event_app" {
  ami           = "ami-0c02fb55956c7d316"  # Amazon Linux 2 AMI (us-east-1)
  instance_type = "t2.micro"
  key_name      = aws_key_pair.deployer.key_name
  security_groups = [aws_security_group.allow_ssh_web.name]

  user_data = file("${path.module}/ec2-user-data.sh")

  tags = {
    Name = "EventAppServer"
  }
}

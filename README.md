# AWS Cloud Co-Op Projects 🌩️

Welcome to the repository showcasing the projects completed during my AWS cloud co-op at Alnylam Pharmaceuticals. This repository includes a collection of innovative solutions designed to enhance cloud operations, automate resource management, and improve security within the AWS environment.

![AWS](https://img.shields.io/badge/AWS-Cloud-orange) ![Automation](https://img.shields.io/badge/Automation-Success-brightgreen)

---

## Table of Contents 📚

1. [Introduction](#introduction)
2. [About Me](#about-me)
3. [Contact](#contact)
4. [Navigating the Repository](#navigating-the-repository)
5. [Project Highlights](#project-highlights)
    - [CostCenter Autotag](#costcenter-autotag)
    - [Dynamic AWS Resource Tagging](#dynamic-aws-resource-tagging)
    - [Quilt CI/CD](#quilt-cicd)
    - [CDN Setup](#cdn-setup)
6. [Technologies Used](#technologies-used)
7. [Learning Outcomes](#learning-outcomes)
8. [Acknowledgments](#acknowledgments)

---

## Introduction 🌟

As a part of my co-op at Alnylam Pharmaceuticals, I had the opportunity to work on several critical projects aimed at streamlining AWS resource management, automating tagging processes, and implementing robust CI/CD pipelines. This repository is organized into four main projects, each detailed in its own folder:

- **CostCenter Autotag**
- **Dynamic AWS Resource Tagging**
- **Quilt CI/CD**
- **CDN Setup**

Each project reflects a commitment to excellence and innovation in cloud computing, leveraging AWS technologies to deliver scalable and efficient solutions.

---

## About Me 👨‍💻

I am Shardul Deshmukh, currently pursuing a Master’s in Information Systems from Northeastern University, expected to graduate in May 2024. I have a Bachelor of Technology in Computer Science from GITAM University, India.

### Professional Experience
- **AWS Cloud Co-op at Alnylam Pharmaceuticals (Jan 2024 – Jun 2024)**:
  - Automated AWS resource tagging using Lambda Functions and Python, significantly increasing efficiency in infrastructure management.
  - Designed and implemented CI/CD pipelines using Docker and AWS CodePipeline, automating deployments and enhancing release quality.
  - Implemented a CDN setup for optimized content delivery and reduced latency for global users using AWS CloudFront and Lambda.
  - Developed a comprehensive Configuration Management Database (CMDB) using AWS Config, enabling streamlined asset tracking, configuration compliance, and enhanced visibility across a multi-account AWS environment. 
  
- **Associate Software Engineer at Hexaware Technologies (Jun 2021 – Aug 2022)**:
  - Established a demand-based, dynamically scaling AWS infrastructure using Terraform and Ansible, optimizing resource utilization.
  - Enhanced REST API performance by implementing caching mechanisms, reducing average response times.
  - Transitioned a monolithic application to microservices architecture, improving scalability and maintainability.

### Skills
- **Languages:** Java, Python, SQL, HTML, YAML, Bash, JavaScript
- **Cloud:** AWS, Microsoft Azure, Google Cloud Platform (GCP)
- **DevOps:** Linux, Terraform, Ansible, CI/CD, Docker, Kubernetes, Jenkins, Git
- **Database:** MySQL, PostgreSQL, MongoDB, DynamoDB, S3
- **Frameworks:** Express.js, Node.js
- **Certifications:** 
  - AWS Solutions Architect – Associate
  - Terraform Associate
  - Microsoft Azure Fundamentals
  - AWS Cloud Practitioner

---

### Resume 📄

For a detailed overview of my skills and experiences, you can view my resume [here](./Shardul-Deshmukh-Resume.pdf).

---

## Contact 📧

For more details, you can reach out to me at [deshmukh.shard@northeastern.edu](mailto:deshmukh.shard@northeastern.edu). You can also connect with me on [LinkedIn](https://www.linkedin.com/in/shardul-deshmukh).

---

## Navigating the Repository 🗂️

This repository is structured to help you easily find detailed information about each project:

- **[CostCenter Autotag](./CostCenter_Autotag/README.md)**: Navigate to the `CostCenter_Autotag` folder for details on the automated cost center tagging solution.
- **[Dynamic AWS Resource Tagging](./Dynamic_AWS_Resource_Tagging/README.md)**: Go to the `Dynamic_AWS_Resource_Tagging` folder for insights into automatic resource tagging at creation.
- **[Quilt CI/CD](./Quilt_CICD/README.md)**: Explore the `Quilt_CICD` folder for information on the CI/CD pipeline setup for Quilt releases.
- **[CDN Setup](./CDN_Setup/README.md)**: Check the `CDN_Setup` folder for information on setting up a CDN with AWS CloudFront and S3.

Each folder contains a dedicated README file with in-depth information about the project's objectives, approach, challenges, and future scope. Feel free to explore and delve into the technical details.

---

### Project Highlights 🌐

---

### 🎯 **CostCenter Autotag**

**Objective:** Automatically tag AWS resources across multiple accounts with a custom cost center tag.

**Key Features:**
- Utilizes AWS Resource Explorer for indexing and searching resources without a cost center tag.
- Employs AWS Resource Groups Tagging API for tagging resources and DynamoDB for logging failed resource ARNs.
- Schedules tagging processes with AWS EventBridge to ensure ongoing compliance with cost center tagging policies.

**Challenges:**
- Limited to tagging up to 1000 resources at a time due to API constraints.

**Future Scope:** The solution can be expanded to cover more resource types and additional custom tags as needed.

---

### 🔧 **Dynamic AWS Resource Tagging**

**Objective:** Automatically tag AWS resources at the time of creation with the user’s email or name.

**Key Features:**
- Integrates AWS CloudTrail and Custom Event Bus to capture and forward resource creation events.
- Utilizes Lambda functions to extract user details from events and tags resources via AWS Resource Groups Tagging API.

**Challenges:**
- Requires manual updates to include and parse creation events for each desired AWS resource type.

**Future Scope:** The system can be expanded to automate tagging for a broader range of AWS resources and tags.

---

### 🚀 **Quilt CI/CD**

**Objective:** Automate the deployment of Quilt releases in AWS, minimizing manual intervention.

**Key Features:**
- Implements an end-to-end CI/CD pipeline using AWS CodePipeline.
- Leverages AWS CodeCommit, CodeBuild, SNS, and Lambda for orchestrating build and deployment processes.
- Adopts a principle of least privilege for dynamic permissions configuration.

**Challenges:**
- Ensuring secure and efficient pipeline configuration while maintaining flexibility for future enhancements.

**Future Scope:** Further refinement of the pipeline to support more complex deployment scenarios and additional AWS services.

---

### 🌐 **CDN Setup**

**Objective:** Set up a Content Delivery Network (CDN) using Amazon CloudFront and S3 for optimized content delivery.

**Key Features:**
- Configures S3 buckets to store and retrieve content efficiently.
- Sets up CloudFront distributions for fast content delivery with low latency.
- Implements logging and monitoring to track CDN performance and usage.

**Challenges:**
- Managing permissions and ensuring secure access to the CDN.

**Future Scope:** Expanding the CDN setup to include additional AWS services and enhance security measures.

---

## Technologies Used 🛠️

- **AWS Services:** CloudTrail, EventBridge, Lambda, DynamoDB, Resource Explorer, Resource Groups Tagging API, CodePipeline, CodeCommit, CodeBuild, SNS, CloudFront, S3
- **Programming Languages:** Python, YAML
- **Tools:** Terraform, AWS CLI, Git

---

## Learning Outcomes 🎓

During this co-op, I gained extensive experience with AWS services and cloud automation. Some key takeaways include:

- **Cloud Security:** Understanding the principles of cloud security and data protection.
- **Automation:** Proficiency in automating cloud operations and resource management.
- **CI/CD:** Expertise in setting up CI/CD pipelines using AWS native tools.
- **Tagging Strategies:** Developing strategies for effective resource tagging and cost management in AWS.

---

## Acknowledgments 🙏

A special thanks to Perminder Sandhu and the entire IT team at Alnylam Pharmaceuticals for their continuous support, guidance, and encouragement throughout this journey. Their mentorship was instrumental in the successful completion of these projects.

---

**Explore the projects to discover how cloud automation can transform enterprise operations and drive efficiency!** 🌟

---

Feel free to contribute or provide feedback to help improve these solutions. Happy coding! 🎉

---

This README file provides an overview of the significant projects and learnings from my AWS co-op experience, reflecting a commitment to leveraging cloud technologies for organizational excellence.

---

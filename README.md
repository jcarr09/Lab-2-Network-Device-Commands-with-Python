# Lab 2 — Network Device Commands with Python

**Course:** Software Defined Networking  
**Module:** Network Automation Fundamentals • **Lab #:** 2  
**Estimated Time:** 90-120 Minutes

## Repository structure

```text
Lab-2-Network-Device-Commands-with-Python
├── .devcontainer
│   ├── devcontainer.json
│   ├── health_check.py
│   ├── post_create.sh
│   └── post_start.sh
├── .gitignore
├── .markdownlint.json
├── .markdownlintignore
├── .pettierrc.yml
├── INSTRUCTIONS.backup.md
├── INSTRUCTIONS.md
├── LICENSE
├── README.backup.md
├── README.md
├── data
│   └── inventory.example.yml
├── lab.yml
├── prettierrc.yml
├── requirements.txt
└── src
    ├── __init__.py
    └── main.py
```

## Lab Topics

- Virtual Environments
- Managing the `requirments.txt` file
- Netmiko
- Error Handling
- Establishing a connection with Netmiko
- Sending show and configuration commands
- Pretty Printing
- NTC-templates
- F-strings for Reporting

## Grading

Your labs will be automatically graded when you upload the completed lab to GitHub Classroom. Your script will be
checked for guarenteed lines of code that must be there as they are predefined and/or built in syntax for either
python or the module you have to use to complete the Lab.

### Logging

You will need to impliment logging in your code with specific log messages after certain tasks have been completed.

### IMPORTANT

**IF YOU LOG FILE DOESN'T HAVE THE CORRECT MESSAGE IT DID NOT HAPPEN! CODING REQUIRES CAREFUL ATTENTION TO DETAIL. IT IS**
**EXPECTED OF YOU AT A SENIOR LEVEL TO BE ATTENTIVE TO WHAT YOU SUBMIT.**

## DO NOT ALTER

- Anything in the .devcontainer directory or your devcontainer won't work and will negatively effect your grade
- Anyting in the .github directory **(AUTOMATIC GRADE OF 0 IF ANYTHING IN THIS DIRECTORY IS ALTERED)**
- The .markdownlint.json file
- The .markdownlintignore file

Altering other files will result in abnormal behavior of the lab. If you feel you have altered it beyond repair simply
clone another fresh copy

## License

© 2025 Sheldon Swanson — Classroom use.

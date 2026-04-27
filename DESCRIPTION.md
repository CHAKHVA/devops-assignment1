# Project: CI/CD Pipeline Automation & Deployment Strategies

## Objective

The goal of this project is to master DevOps workflows. You will focus on automating the lifecycle of an application—from code commit to production—and managing release risks using industry-standard strategies.

## Core Requirements

* **Application Source:** You may use any existing code, a starter template, or a previous project. You are not graded on the complexity of the code, but on the automation of its delivery.
* **Hosting:** You must use a free-tier cloud provider (e.g., Render, Vercel, Netlify, or similar).
* **Automation:** The deployment must be triggered via your CI/CD pipeline only after automated tests pass.

## Part 1: Continuous Integration (CI) – The Quality Gate

### 1. Repository & Testing

* Host your application in a GitHub repository.
* Ensure the repository includes a testing suite (e.g., Jest, PyTest, Mocha).

### 2. GitHub Actions Configuration

* Create a workflow file (e.g., `.github/workflows/main.yml`).
* The workflow must automatically install dependencies and run your tests on every push or `pull_request`.
* **The Rule:** If the tests fail, the pipeline must stop and prevent the deployment.

## Part 2: Continuous Deployment (CD) – Release Strategies

### 1. Automated Deployment

* Configure your pipeline to deploy the application to your chosen cloud provider.
* The deployment should only occur if the CI stage (Part 1) succeeds.

### 2. Deployment Strategy (Student’s Choice)

* Implement or describe a specific update strategy (e.g., Canary, Blue-Green, Rolling Update, or Recreate).
* You are free to choose the strategy that best fits your platform's free-tier capabilities.

### 3. Rollback Protocol

* Define the exact steps required to revert the live application to the previous stable version if a bug is discovered in production.

## Deliverables (To be documented in your README.md)

Your GitHub repository must have a comprehensive `README.md` file containing:

* **Live Application Link:** The URL where your app is hosted.
* **Screenshots:** Clear screenshots of the hosted application and your successful GitHub Actions run.
* **Pipeline Description:** A brief explanation of how your CI/CD flow is structured.
* **Strategy Explanation:**
  * Which Update Strategy did you choose?
  * Explain the steps you took to implement or simulate this strategy for safety.
* **Rollback Guide:** A step-by-step instruction on how to perform a Rollback on your specific hosting platform.

## Evaluation Criteria

* **Automation:** Does the pipeline work without manual intervention?
* **Reliability:** Does the CI correctly block "broken" code from being deployed?
* **Documentation:** Is the README clear, professional, and supported by screenshots?
* **Strategic Thinking:** Is the chosen update and rollback strategy logical for the project?

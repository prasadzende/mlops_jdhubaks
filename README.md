# MLOps: Build ML lifecycle from the scratch
Mlops use case using jenkins, dockerhub and AKS

## Architecture
![Architecture](https://blogger.googleusercontent.com/img/a/AVvXsEjSwB0C9WRKDwl4dP5GRYe5sAI0O2J-H8BPR5f8koDgb_sr2eMybGc6UfDvn5kdyoa96QqMPKSBJFoSOrc511WMW2Lrj_oZqqLJWQjzKCQq5_jD6oOzUpK2YMM989CxPx_6bi8l_tIzplDMuxG8k-MBwjIjfXaFCWC0Edg5Omodvf-a5qo0Z5OYkw4_tg)

In this use case, We will use DVC for data versioning and data pipeline, MLflow for experiment tracking, flask for model serving and Jenkins for CI/CD pipeline. 

We are going to deploy our model on managed Kubernetes service by Azure, But in theory you could also use AWS, GCP or any Kubernetes service provider. 

All these tools are used here to demonstrate End-to-End ML lifecycle. You could also try other alternatives to build ML pipeline based on your requirement.

### Tools used:
* [Flask](https://flask.palletsprojects.com/en/2.0.x/) - for model serving
* [MLFlow](https://www.mlflow.org/) - for experiment tracking
* [DVC](https://dvc.org/) - for data versioning
* [Jenkins](https://www.jenkins.io/) - for the CI/CD
* [AKS](https://azure.microsoft.com/en-us/services/kubernetes-service/) - for kubernetes


For more details, please visit [Blog Post](https://datarubrics.blogspot.com/2021/12/httpsray.html)

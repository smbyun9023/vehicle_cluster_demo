# Vehicle Data Cluster Demo

이 리포지토리는 **Kubernetes 기반 차량 데이터 수집 및 분석 워크플로우 시스템**을 로컬 개발 환경(예: Minikube)을 통해 구현하는 예시 프로젝트입니다.  
프로젝트는 Django 기반 백엔드, Airflow 데이터 파이프라인, Mosquitto MQTT 브로커, PostgreSQL, MongoDB, Grafana 등을 포함합니다.

> **참고:**  
> 본 가이드는 macOS에서 Docker 드라이버를 사용하는 Minikube 환경을 기준으로 작성되었습니다. Windows 사용자는 WSL2 또는 Docker Desktop의 Kubernetes 기능을 활용하시기 바랍니다.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Directory Structure](#directory-structure)
- [Local Development Setup](#local-development-setup)
  - [1. Clone Repository](#1-clone-repository)
  - [2. Install Prerequisites](#2-install-prerequisites)
  - [3. Build Docker Images](#3-build-docker-images)
  - [4. Start Minikube & Set Docker Environment](#4-start-minikube--set-docker-environment)
  - [5. Deploy Kubernetes Manifests (Bring Up)](#5-deploy-kubernetes-manifests-bring-up)
- [Service Configuration](#service-configuration)
  - [Django Backend](#django-backend)
  - [Airflow](#airflow)
  - [Mosquitto (MQTT Broker)](#mosquitto-mqtt-broker)
  - [PostgreSQL](#postgresql)
  - [MongoDB](#mongodb)
  - [Grafana](#grafana)
- [Accessing Services](#accessing-services)
- [Tearing Down the Environment](#tearing-down-the-environment)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

본 프로젝트는 차량 데이터의 수집, 분석, 시각화까지 전 과정을 포함하는 시스템을 구축하기 위한 예제입니다.  
주요 기능은 다음과 같습니다.

- **Kubernetes**를 이용한 컨테이너 오케스트레이션 및 배포 자동화
- **Django**를 이용한 RESTful API 서버 및 Admin UI 제공
- **Airflow**를 통한 데이터 파이프라인 관리 및 DAG 스케줄링
- **Mosquitto** MQTT 브로커를 통한 센서 데이터 수집
- **PostgreSQL** (StatefulSet) 및 **MongoDB**를 이용한 데이터 저장
- **Grafana**를 이용한 시각화 및 모니터링

---

## Architecture

```plaintext
           +-----------------+
           |     Client      |
           +-----------------+
                    │
                    ▼
       +--------------------------+
       | Ingress Controller (NGINX)|
       +--------------------------+
                    │
                    ▼
       +--------------------------+
       | Backend Service (Django) |
       +--------------------------+
                    │
                    ▼
       +--------------------------+
       | Airflow Scheduler &      |
       |       Worker             |
       +--------------------------+
                    │
        ┌───────────┼───────────┐
        │                       │
        ▼                       ▼
+---------------+       +-------------------------+
| AWS S3        |       | PostgreSQL on K8s       |
| (비정형 데이터)  |       | (정형 데이터 저장소)         |
+---------------+       +-------------------------+
                    │
                    ▼
         +--------------------------+
         | MQTT 브로커 (Mosquitto)  |
         +--------------------------+
                    │
                    ▼
         +--------------------------+
         | MongoDB / Grafana        |
         | (반정형 데이터 및        |
         |  시각화/모니터링)         |
         +--------------------------+
```

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/)
- [Minikube](https://minikube.sigs.k8s.io/docs/start/)
- [kubectl](https://kubernetes.io/docs/tasks/tools/)
- [Python 3.8+](https://www.python.org/downloads/)
- Git (선택사항)

> 각 도구가 정상 설치되었는지 터미널에서 아래와 같이 확인하세요:
> ```bash
> docker --version
> minikube version
> kubectl version --client
> python --version
> ```

---

## Directory Structure

```plaintext
vehicle-data-project/
├── backend/        # Django 백엔드 소스 및 Dockerfile
├── airflow/        # Airflow 관련 설정, DAGs 및 Dockerfile
├── mqtt/           # Mosquitto 설정 파일 (mosquitto.conf 등)
└── kubernetes/     # Kubernetes 매니페스트 (Deployment, Service, ConfigMap 등)
```

---

## Local Development Setup

다음 단계에 따라 로컬 개발 환경을 구축하세요.

### 1. Clone Repository

```bash
git clone <repository-url>
cd vehicle-data-project
```

### 2. Install Prerequisites

설치한 Docker, Minikube, kubectl 등이 정상 동작하는지 확인합니다.

```bash
docker --version
minikube version
kubectl version --client
```

### 3. Build Docker Images

#### Django Backend

1. **가상환경 생성 및 패키지 설치**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate
   pip install --upgrade pip
   pip install Django djangorestframework paho-mqtt
   pip freeze > requirements.txt
   ```

2. **Django 프로젝트 생성 (이미 생성된 경우 생략)**

   ```bash
   django-admin startproject vehicle_backend .
   ```

3. **Docker 이미지 빌드**

   ```bash
   docker build -t backend:latest .
   cd ..
   ```

#### Airflow

1. **Airflow 디렉토리 내 Dockerfile과 DAGs 설정 확인**

   ```bash
   cd airflow
   mkdir -p dags
   # example_dag.py 등 필요한 DAG 파일을 dags/ 디렉토리에 추가합니다.
   docker build -t airflow:latest .
   cd ..
   ```

> **참고:** Mosquitto, PostgreSQL, MongoDB, Grafana는 공식 이미지를 사용하므로 별도 빌드하지 않습니다.

### 4. Start Minikube & Set Docker Environment

1. **Minikube 클러스터 시작**

   ```bash
   minikube start
   ```

2. **Minikube의 Docker 데몬 사용**

   ```bash
   eval $(minikube docker-env)
   ```

   _이제 로컬에서 빌드한 Docker 이미지가 Minikube 클러스터 내에서 사용됩니다._

### 5. Deploy Kubernetes Manifests (Bring Up)

`kubernetes` 디렉토리로 이동하여 YAML 파일들을 순차적으로 적용합니다.

```bash
cd kubernetes

# Django 백엔드 배포
kubectl apply -f backend-deployment.yaml
kubectl apply -f backend-service.yaml

# Airflow 배포
kubectl apply -f airflow-deployment.yaml
kubectl apply -f airflow-service.yaml

# Mosquitto (MQTT 브로커) 배포
kubectl apply -f mqtt-configmap.yaml
kubectl apply -f mqtt-deployment.yaml
kubectl apply -f mqtt-service.yaml

# PostgreSQL 배포
kubectl apply -f postgres-statefulset.yaml
kubectl apply -f postgres-service.yaml

# MongoDB 배포
kubectl apply -f mongodb-deployment.yaml
kubectl apply -f mongodb-service.yaml

# Grafana 배포
kubectl apply -f grafana-deployment.yaml
kubectl apply -f grafana-service.yaml

# (옵션) Ingress 배포
kubectl apply -f ingress.yaml
```

각 리소스가 올바르게 생성되었는지 다음 명령어로 확인합니다:

```bash
kubectl get pods
kubectl get services
```

---

## Service Configuration

### Django Backend

- **마이그레이션 및 슈퍼유저 생성**

  1. **마이그레이션 적용:**

     ```bash
     kubectl exec -it <backend-pod-name> -- python manage.py migrate
     ```

  2. **슈퍼유저 생성:**

     ```bash
     kubectl exec -it <backend-pod-name> -- python manage.py createsuperuser
     ```

  3. **Admin UI 접속:**  
     터미널에서 `minikube service backend-service --url` 명령어로 URL을 확인한 후 브라우저에서 접속  
     (예: `http://127.0.0.1:XXXXX/admin`)

### Airflow

- **관리자 계정 생성**

  ```bash
  kubectl exec -it <airflow-pod-name> -- airflow users create \
    --username admin \
    --firstname Admin \
    --lastname User \
    --role Admin \
    --email admin@example.com \
    --password admin
  ```

  > 만약 이미 생성된 경우, 삭제 후 재생성하거나 `--update` 옵션(지원되는 버전일 경우)을 확인하세요.

- **Airflow UI 접속:**  
  `minikube service airflow-service --url` 명령어를 사용합니다.

### Mosquitto (MQTT Broker)

- **설정:**  
  `mqtt/mosquitto.conf` 파일에 설정되어 있으며, ConfigMap을 통해 마운트됩니다.

- **접속:**  
  `minikube service mqtt-service --url` 명령어를 사용하여 연결 테스트

### PostgreSQL

- **기본 사용자:** `postgres`  
- **비밀번호:** `yourpassword` (매니페스트에서 설정한 값)  
- **접속:**  
  Kubernetes 내부에서는 서비스 이름 `postgres-service`를 사용하고, 외부 접근이 필요한 경우 NodePort를 활용

### MongoDB

- **기본 설정:**  
  인증 없이 실행됨 (보안 강화 필요 시 별도 설정)

- **접속:**  
  `minikube service mongodb-service --url` 명령어 활용

### Grafana

- **기본 계정:**  
  - Username: `admin`  
  - Password: `admin` (최초 로그인 후 비밀번호 변경 권장)

- **접속:**  
  `minikube service grafana-service --url` 명령어로 Grafana UI 확인

---

## Accessing Services

Minikube 터널을 통해 각 서비스에 접근할 수 있습니다. 예를 들어:

```bash
minikube service backend-service
minikube service airflow-service
minikube service mqtt-service
minikube service grafana-service
```

macOS Docker 드라이버를 사용하는 경우 터널 주소(예: `127.0.0.1:58838`)를 사용하면 정상적으로 접속할 수 있습니다.

---

## Tearing Down the Environment

개발 환경을 종료하거나 클린업(clean up)하려면, 아래 명령어들을 순차적으로 실행하여 Kubernetes 리소스를 삭제하고 Minikube 클러스터를 정리할 수 있습니다.

### 1. Kubernetes 리소스 삭제

`kubernetes` 디렉토리 내의 모든 YAML 파일을 이용해 배포한 리소스를 삭제합니다. 예를 들어:

```bash
cd kubernetes

# (옵션) Ingress 삭제
kubectl delete -f ingress.yaml

# Grafana 삭제
kubectl delete -f grafana-service.yaml
kubectl delete -f grafana-deployment.yaml

# MongoDB 삭제
kubectl delete -f mongodb-service.yaml
kubectl delete -f mongodb-deployment.yaml

# PostgreSQL 삭제
kubectl delete -f postgres-service.yaml
kubectl delete -f postgres-statefulset.yaml

# Mosquitto 삭제
kubectl delete -f mqtt-service.yaml
kubectl delete -f mqtt-deployment.yaml
kubectl delete -f mqtt-configmap.yaml

# Airflow 삭제
kubectl delete -f airflow-service.yaml
kubectl delete -f airflow-deployment.yaml

# Django 백엔드 삭제
kubectl delete -f backend-service.yaml
kubectl delete -f backend-deployment.yaml
```

또는, 현재 네임스페이스의 모든 리소스를 삭제하려면 다음 명령어를 사용할 수 있습니다:

```bash
kubectl delete all --all
```

> **주의:**  
> 삭제 후, 만약 Persistent Volume Claim(PVC) 등이 남아 있다면 추가로 삭제해야 할 수 있습니다.

### 2. Minikube 클러스터 종료

개발 환경 전체를 중단하려면 아래 명령어를 사용하세요:

- **클러스터 일시 중지 (Stop):**

  ```bash
  minikube stop
  ```

- **클러스터 삭제 (Complete Tear Down):**

  ```bash
  minikube delete
  ```

---

## Troubleshooting

- **Pod 상태 확인:**

  ```bash
  kubectl get pods
  kubectl logs <pod-name>
  ```

- **서비스 접근 문제:**  
  NodePort 번호 확인 및 `minikube service <service-name> --url` 명령어 사용  
  macOS 환경에서는 내부 IP(예: `192.168.49.2:30002`)로 직접 접근이 어려울 수 있으므로 터널 주소를 사용

- **Django 마이그레이션 오류:**  
  반드시 `python manage.py migrate`를 실행하여 데이터베이스 테이블을 생성하세요.

- **Airflow 관리자 비밀번호 문제:**  
  기존 사용자가 있다면 삭제 후 재생성하거나 `--update` 옵션(지원되는 경우) 사용

---

## Contributing

- Jake Byun

---

## License

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.
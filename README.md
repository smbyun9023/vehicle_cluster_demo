# Kubernetes 기반 차량 데이터 수집 및 분석 워크플로우 시스템

## 프로젝트 개요

이 프로젝트는 **Kubernetes**를 활용하여 실시간 차량 데이터 수집, 분석, 시각화 시스템을 구축하는 것을 목표로 합니다. 차량에서 수집된 데이터를 효율적으로 처리하고 분석할 수 있는 데이터 파이프라인을 구현하며, AWS 클라우드 서비스를 연동하여 확장성 있는 환경을 제공합니다.

주요 구성 요소로는 **Airflow**, **Docker**, **AWS S3**, **PostgreSQL**, **MongoDB**, **Grafana** 등이 있으며, 차량의 GPS 데이터를 기반으로 경로 최적화, 이상 감지 등의 기능도 포함됩니다.

## 주요 기능

1. **실시간 데이터 수집**:
    - MQTT 프로토콜을 사용하여 차량 센서 데이터를 실시간으로 수집
    - 수집된 데이터는 MongoDB에 전처리 후 저장

2. **분석 및 리포트 생성**:
    - MongoDB에서 데이터를 로드하여 분석 후 Postgres에 저장
    - 주간 리포트를 생성하고, 이를 AWS S3에 저장

## 기술 스택

- **Python**: 데이터 파이프라인, RESTful API 서버 구현 (Django, Paho-MQTT)
- **Airflow**: 데이터 워크플로우 자동화 및 관리 (KubernetesExecutor 사용)
- **Kubernetes**: 컨테이너 오케스트레이션, 클러스터 관리
- **AWS**: S3, SNS 서비스 연동
- **MongoDB**: 반정형 데이터 저장
- **Grafana**: 시각화 대시보드

## 아키텍처
```bash
[Client] <---> [Ingress Controller] <---> [Backend Service (Django)] 
                        ↓ 
            [Airflow Worker & Scheduler] 
                        ↓ 
            [AWS Services: S3, SNS] 
                        ↓ 
            [MongoDB / Grafana / Prometheus]
```

## 주요 구성 요소

- **Airflow**:
    - KubernetesExecutor를 사용해 동적으로 작업 컨테이너 생성 및 관리
    - 각 Airflow 구성 요소 (Scheduler, Worker, Webserver)는 Kubernetes Deployment로 배포

- **백엔드 서비스**:
    - Django 기반 API 서버를 Kubernetes Deployment로 배포
    - NGINX를 이용한 Ingress Controller를 통해 외부 트래픽을 라우팅

- **MQTT 브로커**:
    - Eclipse Mosquitto를 StatefulSet으로 배포하여 차량 데이터를 수집

- **모니터링**:
    - Prometheus로 클러스터 및 서비스 상태 모니터링
    - Grafana로 대시보드 시각화

## 설치 및 실행 방법

1. **Kubernetes 클러스터 설정**:
    - Kubernetes 클러스터를 준비하고, `kubectl`을 통해 클러스터에 접근 가능하도록 설정합니다.

2. **Docker 이미지 빌드**:
    - 각 서비스 (Airflow, Django, Mosquitto 등)에 대한 Docker 이미지를 빌드하고, Kubernetes에 배포합니다.

3. **AWS 설정**:
    - AWS IAM 역할을 설정하고, AWS 클라우드 서비스 (S3, RDS 등)와 연동할 수 있도록 설정합니다.

4. **Airflow DAG 설정**:
    - Airflow에 필요한 DAG을 설정하여 데이터 수집, 분석, 리포트 생성 등을 자동화합니다.

5. **시스템 실행**:
    - 시스템을 실행하여 차량 데이터 수집 및 분석 프로세스를 시작합니다.

## 학습 포인트

1. Kubernetes에서의 컨테이너 배포 및 관리
2. Airflow를 활용한 데이터 워크플로우 자동화
3. AWS 클라우드 서비스와 Kubernetes 연동
4. 실시간 데이터 수집 및 처리 (MQTT 사용)
5. 모니터링 및 시각화 (Prometheus, Grafana 사용)
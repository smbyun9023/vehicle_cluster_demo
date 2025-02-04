FROM apache/airflow:2.3.0

# pip 설치 명령을 airflow 사용자로 실행
USER airflow
RUN pip install pymongo boto3  # 필요한 추가 패키지 설치

EXPOSE 8080

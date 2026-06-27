FROM quay.io/centos/centos:stream9

WORKDIR /src

RUN dnf install -y python3 python3-pip gcc openssl-devel libffi-devel \
    && dnf clean all

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
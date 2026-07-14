# RCA-DNS_deployment

This repository contains the deployment scripts and configuration for deploying
an anycast service implementing the RCA-DNS architecture.

## Prerequisites For Google Cloud Run Deployment

To run the deployment and deletion scripts under `GoogleCloud/`, you need an
active Google Cloud CLI session and a project with required APIs enabled.

- [Installation documentation](https://docs.cloud.google.com/sdk/docs/install-sdk)

### Required Tools

- Google Cloud SDK (`gcloud`) installed and available in `PATH`.
- `bash` and `make` available on the local machine.

### Required Access

- Access to a Google Cloud project where resources can be created and deleted.
- IAM permissions for Cloud Run and Compute resources (load balancer, NEGs,
  backend services, URL maps, proxies, and forwarding rules).

### Initial Setup (Once Per Environment)

1. Authenticate in Google Cloud CLI:

```bash
gcloud auth login
```

2. Select the target project:

```bash
gcloud config set project <YOUR_PROJECT_ID>
```

3. Enable the APIs used by these scripts:

```bash
gcloud services enable run.googleapis.com compute.googleapis.com
```

4. Configure deployment variables in `GoogleCloud/.env`.

### Run Targets

From `GoogleCloud/` you can run:

```bash
make deploy-services
make delete-services
make deploy-infraestructure
make delete-infraestructure
```

### Experimental architecture with Google Cloud resources

```text
                Cloudflare DNS
                      │
              global.domain.com
                      │
          IP Anycast (Google Cloud)
                      │
             Forwarding Rule (80/443)
                      │
               Target HTTP(S) Proxy
                      │
                  URL Map
                      │
              Backend Service
                      │
     ┌────────────────┼────────────────┐
     │                │                │
NEG Madrid      NEG Tokyo       NEG Iowa
     │                │                │
Cloud Run       Cloud Run       Cloud Run
     │                │                │
Container       Container       Container
```

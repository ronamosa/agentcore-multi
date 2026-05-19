.PHONY: install dev dev-backend dev-frontend mock real infra-deploy infra-destroy setup-memory clean

# ---- Install ----

install:
	cd backend && pip install -r requirements.txt
	cd frontend && npm install
	cd infra && npm install

# ---- Local development ----

dev: dev-backend dev-frontend

dev-backend:
	cd backend && MOCK_MODE=true uvicorn server:app --reload --port 8000

dev-frontend:
	cd frontend && npm run dev

# ---- Run modes ----

mock:
	cd backend && MOCK_MODE=true uvicorn server:app --reload --port 8000

real:
	@echo "Starting in REAL mode (Strands + MCP + Bedrock)..."
	@echo "Ensure AWS credentials are configured and AGENTCORE_MEMORY_ID is set."
	cd backend && MOCK_MODE=false uvicorn server:app --reload --port 8000

# ---- AgentCore Memory setup ----

setup-memory:
	python scripts/setup-agentcore-memory.py --region $${AWS_REGION:-us-east-1}

# ---- CDK infrastructure ----

infra-deploy:
	cd infra && npm run deploy

infra-destroy:
	cd infra && npm run destroy

# ---- Cleanup ----

clean:
	rm -rf infra/dist infra/node_modules frontend/node_modules frontend/dist

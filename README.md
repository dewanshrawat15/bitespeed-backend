# Backend Bitespeed
This repository is an implementation for the Bitespeed Backend Task: Identity Reconciliation Task. [Notion Link](https://bitespeed.notion.site/Bitespeed-Backend-Task-Identity-Reconciliation-53392ab01fe149fab989422300423199)

## Steps to run
- Clone the repository
- Run `docker build -t webapp .`
- Run `docker run -d -p 8000:8000 webapp`
- Send a POST request with the payload
	- `email?: string`
	- `phoneNumber?: string`

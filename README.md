# Trello Workspace Exporter

![Python](https://img.shields.io/badge/python-3.6%2B-blue)

A Python script that exports all boards, members, roles, and activity data from a Trello workspace to a CSV file using the Trello API.

## Features

- Export all boards from a Trello workspace
- List all members with their roles for each board
- Include last activity date for each board
- Generate direct board links
- Lightweight and easy to use

## Prerequisites

- Python 3.6+
- Trello API key and token
- `requests` library

## Getting Started

### 1. Obtain Trello API Credentials

1. Visit https://trello.com/app-key
2. Copy your API key
3. Generate a token (you'll need to authorize it)

### 2. Installation

```bash
git clone https://github.com/yourusername/trello-workspace-exporter.git
cd trello-workspace-exporter
pip install requests

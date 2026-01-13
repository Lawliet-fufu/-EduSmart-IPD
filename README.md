# EduSmart Platform

<div align="center">

[![Vue](https://img.shields.io/badge/Vue-3.3.4-42b883?logo=vue.js)](https://vuejs.org/)
[![Vite](https://img.shields.io/badge/Vite-4.4.9-646cff?logo=vite)](https://vitejs.dev/)
[![Flask](https://img.shields.io/badge/Flask-latest-000000?logo=flask)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A modern teaching management system with a complete role-based permission system and elegant UI design.

</div>

---

## Overview

EduSmart is a modern educational management platform built with **Vue 3** and **Flask**. It features a comprehensive role-based access control system (RBAC) and a refined user interface.

### Key Features

- **Modern UI Design**: Deep green theme with gentle gradient backgrounds.
- **Role-Based System**: Distinct permissions for Students, Teachers, and Administrators.
- **AI Teaching Assistant**: File analysis, mind mapping, and courseware assistance.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Pure JavaScript**: Maintainable codebase without TypeScript dependencies.

---

## Features

### Core Modules

| Module | Description | Status |
|--------|-------------|--------|
| **Authentication** | Three-role login system (Admin/Teacher/Student) | Completed |
| **Dashboard** | Statistics cards, student performance, latest notices | Completed |
| **Assignments** | Create, track, and filter assignments | Completed |
| **Notices** | Priority-based announcements with timeline view | Completed |
| **Class Management** | Class statistics and student rosters | Teacher/Admin |
| **AI Assistant** | Smart dialogue, file analysis, mind mapping | Teacher/Admin |
| **Settings** | Personal configuration and security settings | Completed |

---

## Role System

### Roles & Permissions

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Administrator** | `admin` | `123456` | Full Access |
| **Teacher** | `teacher` | `123456` | 5 Core Features (incl. AI) |
| **Student** | `student` | `123456` | 3 Basic Features |

---

## Quick Start

### Prerequisites

- **Node.js** >= 16.0.0
- **Python** >= 3.8
- **npm** >= 8.0.0

### Local Development

#### 1. Clone the repository

**GitHub (International):**
```bash
git clone https://github.com/Lawliet-fufu/EduSmart-IPD.git
cd EduSmart-IPD
```

**Gitee (中国大陆):**
```bash
git clone https://gitee.com/zy-cdut/2025-l5-s6-group3.git
cd 2025-l5-s6-group3
```

#### 2. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

Access at: `http://localhost:5173`

#### 3. Start Backend (Optional)

```bash
cd backend

# Configure environment variables
cp .env.example .env
# Edit .env with your actual database credentials and API keys

pip install -r requirements.txt
python run.py
```

API Server: `http://localhost:5000`

---

## Project Structure

```
edu-smart-platform/
├── frontend/                   # Vue 3 Frontend
│   ├── src/
│   │   ├── views/             # Page Components
│   │   │   ├── LoginView.vue        # Login (Role Selection)
│   │   │   ├── HomeView.vue         # Dashboard
│   │   │   ├── AIAssistantView.vue  # AI Assistant
│   │   │   └── ...
│   │   ├── components/        # Reusable Components
│   │   ├── stores/            # Pinia State Management
│   │   └── style.css          # Global Styles & Variables
│   └── package.json
│
├── backend/                    # Flask Backend
│
└── README.md
```

---

## Tech Stack

### Frontend
- **Vue 3** (Composition API)
- **Vite** (Build Tool)
- **Pinia** (State Management)
- **Vue Router** (Routing)
- **Lucide Icons** (Iconography)

### Backend
- **Flask** (Web Framework)
- **SQLAlchemy** (ORM)
- **JWT** (Authentication)

---

## License

This project is licensed under the MIT License.

---

<div align="center">
Made by EduSmart Team
</div>

# Visitor Gate Pass Management System

## Project Overview

Industrial Visitor Management System with:

* Visitor Registration
* Department-based Approval Flow
* HOD Approval System
* QR Code Gate Passes
* Entry/Exit Tracking
* Employee Management
* Department Management
* Role-Based Access Control

Tech Stack:

* FastAPI
* Firebase Firestore
* JWT Authentication
* Pydantic
* QRCode Library

---

# Completed Modules

## Authentication

Status: ✅ Complete

Features:

* User Registration
* Login
* Password Hashing
* JWT Token Generation
* Role Based Access Control

Roles:

* Admin
* HOD
* Guard

---

## Visitor Application Module

Status: ✅ Complete

Features:

* Submit Visitor Request
* Store Visitor Information
* Department Selection
* Approval Workflow

Collections:

* visitor_applications

---

## Department Module

Status: ✅ Complete

Features:

* Create Department
* Get Department By ID
* Get All Departments

Collections:

* departments

---

## Employee Module

Status: ✅ Complete

Features:

* Create Employee
* Get Employee By ID
* Get All Employees

Collections:

* employees

---

## HOD Lookup

Status: ✅ Complete

Features:

* Find HOD by Department
* Automatic Approval Routing

Workflow:

Department
→ HOD Lookup
→ Employee Returned

---

## Approval Module

Status: ✅ Complete

Features:

* Approve Application
* Reject Application

---

## Gate Pass Module

Status: ✅ Complete

Features:

* Generate Gate Pass
* Generate QR Code
* Validate Gate Pass

Collections:

* gate_passes

---

## Access Logs

Status: ✅ Complete

Features:

* Record Entry
* Record Exit

Collections:

* access_logs

---

# Current Architecture

Visitor
↓
Select Department
↓
Find HOD
↓
Create Application
↓
HOD Approval
↓
Generate Gate Pass
↓
Generate QR
↓
Entry Log
↓
Exit Log

---

# Collections

## users

Fields:

* user_id
* employee_id
* email
* role
* hashed_password
* is_active

---

## employees

Fields:

* employee_id
* employee_name
* employee_email
* department_id
* role
* created_at

---

## departments

Fields:

* department_id
* department_name
* department_code
* hod_id

---

## visitor_applications

Fields:

* application_id
* visitor_name
* visitor_phone
* purpose
* host_id
* department_id
* status
* created_by
* created_at

---

## gate_passes

Fields:

* gatepass_id
* application_id
* visitor_name
* host_id
* qr_code_path
* status
* created_at

---

## access_logs

Fields:

* log_id
* gatepass_id
* action
* timestamp

---

# Current Blocker

User ↔ Employee Mapping

Current:

users.employee_id and employees.employee_id must be aligned.

Need:

JWT should include:

* user_id
* employee_id
* role

---

# Next Tasks

## Day 10

* [ ] Fix User ↔ Employee Mapping
* [ ] Add employee_id to JWT
* [ ] Complete HOD Pending Applications API
* [ ] Approval Authorization Check

## Day 11

* [ ] Guard Module
* [ ] QR Scan APIs
* [ ] Guard Authorization

## Future

* [ ] Audit Logs
* [ ] Jinja2 Frontend
* [ ] Intern Integration
* [ ] Docker
* [ ] Deployment
* [ ] Testing

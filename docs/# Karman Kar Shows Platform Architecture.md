# Karman Kar Shows Platform Architecture

Version: 0.10.0-beta

Last Updated: June 2026

---

# Purpose

The Karman Kar Shows Platform is a Flask-based event management platform designed to manage car shows, cruise-ins, fundraising events, and future event types from a single system.

The platform supports:

* Vehicle registration
* Day-of registration
* Placeholder vehicle inventory
* QR code voting
* Charity fundraising
* Sponsorship management
* Electronic waivers
* Judging classes
* Event administration
* Reporting and exports

Long-term ownership is expected to transition to Karman Technologies with Karman Kar Shows & Events serving as the first customer.

---

# Technology Stack

## Application

* Python
* Flask
* Jinja2 Templates

## Database

* SQLite

## Payments

* Stripe Checkout
* Stripe Connect

## Hosting

* Railway
* GitHub

## Front End

* HTML
* Tailwind CSS
* JavaScript

---

# High-Level Architecture

Public Users
↓
Registration / Voting / Sponsorship
↓
Flask Application
↓
SQLite Database
↓
Stripe Payment Processing
↓
Railway Hosting

Administrative Users
↓
Admin Dashboard
↓
Reporting / Registration Management
↓
Database

---

# Core Functional Areas

## 1. Show Management

Primary Entity:

shows

Stores:

* Event information
* Dates
* Location
* Charity information
* Registration settings
* Voting settings
* Sponsorship settings
* Stripe routing configuration

Examples:

* Full Show
* Cruise-In
* Pop-Up Event

---

## 2. Registration System

Primary Tables:

* people
* show_cars
* registration_intents

Responsibilities:

* Vehicle registration
* Owner information
* Registration payment tracking
* Vehicle numbering
* Session assignment
* Waiver tracking

Registration States:

* Pending
* Paid
* Paid Cash
* Manual Paid
* Comped
* Removed
* Cancelled

---

## 3. Placeholder System

Purpose:

Support day-of registration without requiring online registration.

Workflow:

Placeholder Card
↓
Assigned Car Number
↓
Day-Of Registration
↓
Owner Claims Card
↓
Registration Completed

Features:

* Create ranges
* Fill to max cars
* Print windshield cards
* Owner claim QR links

---

## 4. Registration Slot System

Primary Tables:

* show_registration_slots
* show_car_registration_slots

Purpose:

Support:

* Single day events
* Multi-day events
* Cruise-ins
* Tech sessions
* Driving tours

Modes:

* Single Selection
* Multiple Selection

Examples:

Saturday Show

Sunday Show

Friday Tech Session

Sunday Cruise

---

## 5. Judging Class System

Primary Table:

show_judging_classes

Purpose:

Vehicle classification.

Fields:

* Class Name
* Class Code
* Year Range
* Make Matching
* Model Matching
* Award Places

Examples:

British Pre-1980

Mustang 1965-1973

Modified Import

Truck

Motorcycle

Workflow:

Vehicle
↓
Class Assignment
↓
Judging
↓
Awards

---

## 6. Voting System

Purpose:

Fundraising and vehicle voting.

Workflow:

Vehicle QR Code
↓
Vote Purchase
↓
Stripe Payment
↓
Vote Recording
↓
Leaderboard

Supported Modes:

Fundraiser Unlimited
* Registered participants only
* Staff-issued judges only
* Participants and judges
* Voting disabled

---

## 7. Sponsorship System

Purpose:

Manage event sponsorships.

Capabilities:

* Online sponsor registration
* Payment processing
* Sponsor tracking
* Sponsor display

Typical Levels:

* Title
* Gold
* Silver
* Community

---

## 8. Waiver System

Purpose:

Liability management.

Features:

* Electronic waivers
* Printed waivers
* Waiver versions
* Waiver templates
* Signature capture

Storage:

instance/waivers

---

## 9. Windshield Card System

Purpose:

Vehicle identification.

Generated Information:

* Car Number
* Vehicle Information
* QR Code
* Owner Claim Link

Printing Modes:

* Front Only
* Duplex

Utility:

utils/print_cards.py

---

# Administrative System

## Command Center

Primary administrative dashboard.

Functions:

* Show Management
* Car Search
* Placeholder Management
* Reporting
* Waivers
* Sponsorships

---

## Car Search

Purpose:

Administrative registration management.

Search By:

* Name
* Phone
* Email
* Vehicle
* Car Number

Functions:

* Registration lookup
* Registration editing
* Check-in review

---

## Registration Editor

Purpose:

Modify registrations after creation.

Capabilities:

* Owner updates
* Vehicle updates
* Registration status updates
* Slot updates
* Judging class updates

---

# Payment Architecture

## Current Design

Voting Revenue
→ Charity Stripe Account

Registration Revenue
→ Karman Account

Sponsorship Revenue
→ Karman Account

Donations
→ Charity Account

Configurable Per Show

---

# Security Model

Current Roles:

Admin

Future Roles:

Super Admin

Organizer

Registration Staff

Judge

Volunteer

---

# Database Overview

Major Tables

shows

people

show_cars

registration_intents

votes

vote_intents

attendees

sponsors

waiver_templates

show_registration_slots

show_car_registration_slots

show_judging_classes

field_metrics

---

# Deployment Architecture

Developer Workstation
↓
Git Commit
↓
GitHub
↓
Railway Deployment
↓
Production Site

Domain:

[www.karmankarshowsandevents.com](http://www.karmankarshowsandevents.com)

---

# Documentation Requirements

Every Release Must Update:

CHANGELOG.md

RELEASE_HISTORY.md

ARCHITECTURE.md

PROJECT_WORKFLOW.md

If architecture changes, ARCHITECTURE.md must be updated before deployment is considered complete.

---

# Future Architecture

## Phase 1

Current KKSE Platform

## Phase 2

Multi-Show Platform

## Phase 3

Organizer Accounts

## Phase 4

SaaS Licensing

## Phase 5

Karman Technologies Ownership

## Phase 6

Additional Event Types

* Golf Tournaments
* Festivals
* Fundraisers
* Vendor Events
* Community Events

---

# Vision Statement

Build a scalable event management platform capable of supporting vehicle events, charity fundraisers, and future event verticals while providing registration, sponsorship, voting, waiver management, reporting, and fundraising tools through a unified SaaS platform operated by Karman Technologies.

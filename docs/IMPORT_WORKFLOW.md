# Import Workflow

Version: 0.9.2-beta v3
Date: 2026-06-09

## Purpose

The import center supports shows where judging classes, accepted car registrations, or paper-vote files were captured outside the platform.

## Location

Admin → Shows → Manage Show → Import

## Import Types

### Import Judging Classes

Preferred CSV headers:

```csv
class_code,class_name,description,year_min,year_max,make_contains,model_contains,keyword_contains,award_places,sort_order,is_active
```

Common aliases are accepted:

- code
- class
- class name
- judging class
- min year
- max year
- make
- model
- keyword
- awards
- places
- active

Existing classes are matched by class_code first, then class_name.

### Import Accepted Car Registrations

Preferred CSV headers:

```csv
car_number,owner_name,phone,email,year,make,model,class_code,class_name,payment_status,waiver_received,custom_1,custom_2
```

Common aliases are accepted:

- name
- full name
- owner
- mobile
- cell
- email address
- vehicle year
- vehicle make
- vehicle model
- car #
- entry number
- class
- division
- judging class

## Missing Class Rule

If an accepted-registration import contains class_code, class_name, class, division, or judging_class and that class does not exist for the show, the platform creates the class automatically and assigns the imported car to it.

This prevents imported registration files from leaving cars unclassified when the outside registration source already included the class.

## Custom Fields

The importer allows extra custom columns such as custom_1 and custom_2. They are ignored in 0.9.2-beta v3, but are allowed so outside spreadsheets do not need to be manually stripped down before import.

## Safety Rules

- Existing registered car numbers are skipped rather than overwritten.
- Placeholder car numbers can be claimed by imported registrations.
- Blank car numbers use the next placeholder or next available number.
- Imports are accepted registrations and do not trigger online checkout.


## 0.9.2-beta v4 — Downloadable Import Templates

The show import page now provides three downloadable CSV templates:

1. Judging Classes CSV
2. Accepted Registrations CSV
3. Combined Show Import CSV

### Judging Classes Template

Preferred columns:

```csv
class_code,class_name,description,sort_order,award_places,is_active
```

### Accepted Registrations Template

Preferred columns:

```csv
car_number,owner_name,owner_email,owner_phone,year,make,model,class_code,class_name,registration_status,custom_1,custom_2
```

### Combined Import Template

Preferred columns:

```csv
record_type,car_number,owner_name,owner_email,owner_phone,year,make,model,class_code,class_name,description,sort_order,award_places,is_active,registration_status,custom_1,custom_2
```

Use `record_type=class` for judging class rows and `record_type=registration` for accepted registration rows.

### Rule

Registrations that reference a missing class should create that class for the show when `class_code` or `class_name` is provided.

# Front-End Architecture & Template Guide

## Template Hierarchy

```
base.html (Base Layout)
├── Dashboard
│   └── dashboard.html
├── Projects
│   ├── projects.html (List)
│   ├── project_new.html (Create)
│   ├── project_edit.html (Edit)
│   └── project_detail.html (Details)
├── Samples
│   ├── samples.html (List)
│   ├── sample_new.html (Create)
│   ├── sample_edit.html (Edit)
│   └── sample_detail.html (Details)
├── Users (Admin only)
│   ├── users.html (List)
│   ├── user_new.html (Create)
│   └── user_edit.html (Edit)
├── Reports
│   └── audit_logs.html
└── Error Pages
    ├── 404.html
    └── 500.html
```

## Template Files Reference

### 1. `base.html` - Main Layout Template
**Purpose**: Base template that all other templates extend
**Key Features**:
- Navigation bar with Bootstrap 5
- Flash message display
- Footer section
- External CSS/JS imports

**CDN Resources**:
```html
- Bootstrap 5.3.0 CSS
- Bootstrap 5.3.0 JS Bundle
- Bootstrap Icons 1.10.0
- Custom style.css
```

**Structure**:
```
┌─────────────────────────────┐
│       Navigation Bar        │
├─────────────────────────────┤
│    Flash Messages (if any)  │
├─────────────────────────────┤
│                             │
│     Page Content            │
│    (block content)          │
│                             │
├─────────────────────────────┤
│         Footer              │
└─────────────────────────────┘
```

### 2. `login.html` - Authentication
**Purpose**: Standalone login page
**Features**:
- Gradient background
- Centered login form
- Username & password fields
- Demo credentials helper text
- Error message display

**Fields**:
- Username (text input, required)
- Password (password input, required)
- CSRF token (hidden)

### 3. `dashboard.html` - Home/Overview
**Purpose**: Main dashboard showing key metrics
**Components**:
- Welcome message with user role
- 4 Statistics cards:
  - Total Projects (blue)
  - Total Samples (teal)
  - Total Tests (green)
  - Pending Tests (yellow)
- Recent Samples table
- Tests Pending Approval section (if applicable)
- Quick Links section

**Data Required**:
```python
total_projects: int
total_samples: int
total_tests: int
pending_tests: int
recent_samples: list[Sample]
pending_approval: list[Test] (optional)
user: User object
```

### 4. `projects.html` - Projects List
**Purpose**: Display all projects with management options
**Features**:
- Projects data table
- Project Code, Name, Client, Status columns
- Action buttons (View, Edit, Delete)
- New Project button
- Empty state message

**Data Required**:
```python
projects: list[Project]
```

**Columns**:
- Project Code
- Project Name
- Client
- Status (badge)
- Created Date
- Actions

### 5. `project_new.html` - Create Project Form
**Purpose**: Form to create a new project
**Fields**:
- Project Code (text, required, max 20)
- Project Name (text, required)
- Client Name (text, optional)
- Description (textarea, optional)

**Validation**:
- Project Code & Name are required
- Project Code must be unique

### 6. `project_edit.html` - Edit Project Form
**Purpose**: Form to update project details
**Fields**:
- Project Code (text, required)
- Project Name (text, required)
- Client Name (text, optional)
- Description (textarea, optional)
- Status (select: Active, Completed, On Hold)
- Created Date (read-only)

### 7. `project_detail.html` - Project Overview
**Purpose**: Detailed view of a project with samples
**Sections**:
- Project Header with Edit button
- Project Information card:
  - Code, Status, Client, Created Date, Description
- Statistics cards:
  - Total Samples
  - Total Tests
- Samples table

**Data Required**:
```python
project: Project object
samples: list[Sample]
```

### 8. `samples.html` - Samples List
**Purpose**: Display all samples with filtering
**Features**:
- Search bar (Sample ID)
- Filter dropdown (Project, Type)
- Samples data table
- Action buttons (View, Edit, Delete)
- Empty state message

**Filter Options**:
- Sample Type: Concrete, Soil, Aggregate, All

**Data Required**:
```python
samples: list[Sample]
search: str
project_filter: str
type_filter: str
```

### 9. `sample_new.html` - Register Sample Form
**Purpose**: Form to register a new sample
**Fields**:
- Sample ID (text, required)
- Sample Type (select, required):
  - Concrete
  - Soil
  - Aggregate
- Project (select, optional):
  - Shows all active projects
  - Shows project code + name
- Project Name (text, optional):
  - Alternative to dropdown
  - For projects not in list
- Client Name (text, optional)
- Date Collected (date picker, optional)

**Data Required**:
```python
projects: list[Project]
```

### 10. `sample_detail.html` - Sample Overview
**Purpose**: Detailed view of a sample and its tests
**Sections**:
- Sample Header with action buttons
- Sample Information card
- Tests listing table
- Test management (add, edit, delete)

### 11. `sample_edit.html` - Edit Sample Form
**Purpose**: Update sample details
**Fields**:
- Sample ID (text, optional)
- Type (select)
- Project (select)
- Client Name (text)
- Date Collected (date picker)

### 12. `users.html` - User Management (Admin Only)
**Purpose**: List all users with management options
**Features**:
- Users data table
- Username, Role columns
- Edit button
- New User button
- Empty state message

**Data Required**:
```python
users: list[User]
```

### 13. `user_new.html` - Create User Form
**Purpose**: Form to create new user
**Fields**:
- Username (text, required, unique)
- Password (password, required)
- Confirm Password (password, required)
- Role (select: Admin, Lab Technician, Engineer)

### 14. `user_edit.html` - Edit User Form
**Purpose**: Update user details and role
**Fields**:
- Username (text, read-only)
- Role (select: Admin, Lab Technician, Engineer)
- Password (optional, for password reset)

### 15. `audit_logs.html` - Audit Trail (Admin Only)
**Purpose**: Display system audit logs
**Columns**:
- Timestamp
- User
- Action
- Entity Type
- Entity ID
- Details

### 16. `404.html` - Not Found Error
**Purpose**: Display 404 error page
**Features**:
- Friendly error message
- Link back to home/projects

### 17. `500.html` - Server Error
**Purpose**: Display 500 error page
**Features**:
- Error message
- Contact support message

## CSS Classes & Styles

### Card Component
```html
<div class="card">
  <div class="card-header">Title</div>
  <div class="card-body">Content</div>
</div>
```

### Table Component
```html
<table class="table table-hover table-striped">
  <thead>...</thead>
  <tbody>...</tbody>
</table>
```

### Buttons
```html
<!-- Primary Action -->
<button class="btn btn-primary">Primary</button>

<!-- Secondary Action -->
<button class="btn btn-secondary">Secondary</button>

<!-- Danger Action -->
<button class="btn btn-danger">Delete</button>

<!-- Outline Buttons -->
<button class="btn btn-outline-primary">Outline</button>

<!-- Small Buttons -->
<button class="btn btn-sm btn-outline-primary">Small</button>
```

### Status Badges
```html
<!-- Pending -->
<span class="status-pending">Pending</span>

<!-- Approved/Completed/Active -->
<span class="status-approved">Approved</span>

<!-- Rejected -->
<span class="status-rejected">Rejected</span>

<!-- In Progress -->
<span class="status-in-progress">In Progress</span>
```

### Alert Messages
```html
<!-- Success -->
<div class="alert alert-success">Success message</div>

<!-- Danger/Error -->
<div class="alert alert-danger">Error message</div>

<!-- Warning -->
<div class="alert alert-warning">Warning message</div>

<!-- Info -->
<div class="alert alert-info">Info message</div>
```

## Bootstrap Classes Used

### Grid System
- `.container-fluid` - Full-width container
- `.row` - Row container
- `.col`, `.col-md-6`, `.col-lg-8` - Column sizes

### Utilities
- `.mb-3`, `.mt-4` - Margin utilities
- `.p-4` - Padding utilities
- `.text-center`, `.text-muted` - Text utilities
- `.d-flex`, `.gap-2` - Flexbox utilities
- `.me-2`, `.ms-auto` - Margin left/right
- `.align-items-center` - Vertical alignment

### Components
- `.navbar`, `.navbar-expand-lg` - Navigation
- `.card` - Card component
- `.table`, `.table-hover` - Table component
- `.badge`, `.badge bg-primary` - Badge component
- `.alert` - Alert component
- `.form-control`, `.form-select` - Form elements
- `.btn`, `.btn-primary` - Button component
- `.dropdown` - Dropdown menu

## Responsive Breakpoints

Bootstrap 5 uses these breakpoints:
- `xs` (default): < 576px
- `sm`: ≥ 576px
- `md`: ≥ 768px
- `lg`: ≥ 992px
- `xl`: ≥ 1200px
- `xxl`: ≥ 1400px

## Icon Reference

Using Bootstrap Icons 1.10.0 via CDN

Common icons used:
- `bi-flask` - LIMS logo
- `bi-speedometer2` - Dashboard
- `bi-folder` - Projects
- `bi-vial` - Samples
- `bi-people` - Users
- `bi-gear` - Settings/Admin
- `bi-plus-circle` - Add/Create
- `bi-pencil` - Edit
- `bi-trash` - Delete
- `bi-eye` - View
- `bi-download` - Export
- `bi-info-circle` - Information
- `bi-exclamation-circle` - Warning

## Form Validation

Bootstrap's form validation is supported:
- Required fields marked with `*`
- HTML5 `required` attribute
- Helpful hints and labels
- Error messages via flash system

## Accessibility Features

- Semantic HTML5 elements
- ARIA labels for icons
- Keyboard navigation support
- Color contrast compliance
- Form labels associated with inputs
- Empty state messages

## Performance Considerations

- Bootstrap loaded from CDN (cached)
- Minimal custom CSS
- Responsive images
- Optimized table layouts
- Lazy loading where appropriate

---
**Last Updated**: December 2025

# Front-End Quick Reference Card

## Template Structure

```html
<!-- All pages extend base.html -->
{% extends 'base.html' %}
{% block content %}
  <!-- Page-specific content here -->
{% endblock %}
```

## Common Components

### Container
```html
<div class='container-fluid'>
  <div class='row'>
    <div class='col-lg-8 mx-auto'>
      <!-- Content -->
    </div>
  </div>
</div>
```

### Card
```html
<div class='card'>
  <div class='card-header'>
    <h5><i class='bi bi-icon-name'></i> Title</h5>
  </div>
  <div class='card-body'>
    <!-- Content -->
  </div>
</div>
```

### Table
```html
<div class='table-responsive'>
  <table class='table table-hover'>
    <thead>
      <tr>
        <th>Header 1</th>
        <th>Header 2</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Data 1</td>
        <td>Data 2</td>
      </tr>
    </tbody>
  </table>
</div>
```

### Form
```html
<div class='mb-3'>
  <label for='fieldId' class='form-label'>
    <i class='bi bi-icon'></i> Label
  </label>
  <input type='text' class='form-control' id='fieldId' name='fieldName'>
  <small class='text-muted'>Helper text</small>
</div>
```

### Button Group
```html
<div class='d-flex gap-2'>
  <button class='btn btn-primary'>Primary</button>
  <button class='btn btn-secondary'>Secondary</button>
</div>
```

### Alert
```html
<div class='alert alert-success'>
  <i class='bi bi-check-circle'></i> Success message
</div>
```

### Status Badge
```html
<span class='status-pending'>Pending</span>
<span class='status-approved'>Approved</span>
<span class='status-rejected'>Rejected</span>
<span class='status-active'>Active</span>
<span class='status-in-progress'>In Progress</span>
```

### Empty State
```html
<div class='alert alert-info'>
  <i class='bi bi-info-circle'></i> No items yet.
  <a href='/path' class='alert-link'>Create one</a>
</div>
```

## Bootstrap Classes Cheat Sheet

### Spacing
```
m-3   = margin: 1rem          p-3   = padding: 1rem
mb-3  = margin-bottom: 1rem   pb-3  = padding-bottom: 1rem
mt-4  = margin-top: 1.5rem    pt-4  = padding-top: 1.5rem
mx-auto = margin horizontal center
```

### Text
```
text-center     = text-align: center
text-muted      = color: #6c757d
text-primary    = color: #667eea
text-decoration-none = remove underline
```

### Display
```
d-flex          = display: flex
gap-2           = gap: 0.5rem
align-items-center = vertical align
justify-content-between = space between
flex-grow-1     = flex: 1
w-100           = width: 100%
```

### Grid
```
row             = flex row container
col-12          = full width
col-md-6        = 50% on medium+
col-lg-8        = 66% on large+
mx-auto         = center column
```

### Colors
```
bg-primary      = blue background
bg-success      = green background
bg-danger       = red background
bg-warning      = yellow background
bg-info         = teal background
text-white      = white text
```

### Sizing
```
btn-sm          = small button
btn-lg          = large button
form-control    = input styling
table-hover     = row hover effect
```

## Common Patterns

### Page Header with Action Button
```html
<div class='row mb-4 align-items-center'>
  <div class='col'>
    <h1><i class='bi bi-icon'></i> Page Title</h1>
  </div>
  <div class='col-auto'>
    <a href='/path' class='btn btn-primary'>
      <i class='bi bi-plus-circle'></i> Action
    </a>
  </div>
</div>
```

### Centered Form Card
```html
<div class='container-fluid'>
  <div class='row'>
    <div class='col-lg-8 mx-auto'>
      <div class='card'>
        <div class='card-header'>
          <h5><i class='bi bi-icon'></i> Form Title</h5>
        </div>
        <div class='card-body'>
          <form method='post'>
            <!-- Form fields -->
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
```

### Two-Column Layout
```html
<div class='row'>
  <div class='col-lg-8'>
    <!-- Main content -->
  </div>
  <div class='col-lg-4'>
    <!-- Sidebar -->
  </div>
</div>
```

### Statistics Cards Row
```html
<div class='row mb-4'>
  <div class='col-md-6 col-lg-3 mb-3'>
    <div class='card text-white bg-primary'>
      <div class='card-body'>
        <h6 class='card-title'>Title</h6>
        <h2>99</h2>
      </div>
    </div>
  </div>
  <!-- Repeat for other cards -->
</div>
```

### Table with Actions
```html
<table class='table table-hover'>
  <thead>
    <tr>
      <th>Name</th>
      <th style='width: 200px;'>Actions</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Item</td>
      <td>
        <a href='/view' class='btn btn-sm btn-outline-primary'>View</a>
        <a href='/edit' class='btn btn-sm btn-outline-warning'>Edit</a>
        <button class='btn btn-sm btn-outline-danger'>Delete</button>
      </td>
    </tr>
  </tbody>
</table>
```

## Icon Reference (Common)

```
bi-flask                = Laboratory/LIMS
bi-speedometer2         = Dashboard
bi-folder               = Projects/Folders
bi-vial                 = Samples
bi-people               = Users
bi-gear                 = Settings
bi-plus-circle          = Add/Create
bi-pencil               = Edit
bi-trash                = Delete
bi-eye                  = View
bi-download             = Download/Export
bi-info-circle          = Information
bi-exclamation-circle   = Warning
bi-check-circle         = Success
bi-clock                = Time/Pending
bi-clipboard-check      = Tests/Completed
bi-arrow-left           = Back
bi-box-arrow-right      = Logout
bi-person-circle        = User Profile
bi-funnel               = Filter
bi-search               = Search
bi-calendar             = Date
bi-barcode              = ID/Code
bi-tag                  = Tag/Type
bi-person-badge         = Person/Client
bi-file-text            = Document
bi-flag                 = Status
```

## Colors Quick Reference

```
Primary Blue:    class='bg-primary'  or  #667eea
Secondary Purple: (used in gradients)
Success Green:   class='bg-success'  or  #28a745
Danger Red:      class='bg-danger'   or  #dc3545
Warning Yellow:  class='bg-warning'  or  #ffc107
Info Teal:       class='bg-info'     or  #17a2b8
Light:           class='bg-light'    or  #f8f9fa
Dark:            class='bg-dark'     or  #212529
```

## Form Validation Pattern

```html
<form method='post' novalidate>
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
  
  <div class='mb-3'>
    <label for='fieldId' class='form-label'>
      Field <span class='text-danger'>*</span>
    </label>
    <input type='text' class='form-control' id='fieldId' name='fieldName' required>
    <small class='text-muted'>Helper text</small>
  </div>
  
  <div class='d-flex gap-2'>
    <button type='submit' class='btn btn-primary'>Submit</button>
    <a href='/back' class='btn btn-secondary'>Cancel</a>
  </div>
</form>
```

## Common Issues & Solutions

### CDN Not Loading
```html
<!-- Check CDN links in base.html are accessible -->
<!-- Fallback: Include local Bootstrap files -->
```

### Icons Not Showing
```html
<!-- Ensure Bootstrap Icons CDN is loaded -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css">
```

### Form Not Styling
```html
<!-- Add form-control class to inputs -->
<input class='form-control'>
<!-- Add form-select class to selects -->
<select class='form-select'></select>
```

### Table Not Responsive
```html
<!-- Wrap table in responsive div -->
<div class='table-responsive'>
  <table class='table'></table>
</div>
```

### Text Wrapping Issues
```html
<!-- Use word-break utilities -->
<td class='text-break'>Long text here</td>
```

## Responsive Breakpoints

```
xs (default)  : < 576px    - Mobile phones
sm            : ≥ 576px    - Landscape phones
md            : ≥ 768px    - Tablets
lg            : ≥ 992px    - Desktops
xl            : ≥ 1200px   - Large desktops
xxl           : ≥ 1400px   - Extra large monitors
```

## CSS Custom Properties (Variables)

```css
:root {
  --primary-color: #667eea;
  --secondary-color: #764ba2;
  --success-color: #28a745;
  --danger-color: #dc3545;
  --warning-color: #ffc107;
  --info-color: #17a2b8;
}

/* Usage in CSS */
color: var(--primary-color);
```

## Tips & Best Practices

1. **Always use responsive classes**
   ```html
   <!-- Good -->
   <div class='col-12 col-md-6'>
   
   <!-- Bad -->
   <div style='width: 50%'>
   ```

2. **Use icon library consistently**
   ```html
   <!-- Good -->
   <i class='bi bi-plus-circle'></i>
   
   <!-- Bad -->
   <span>+</span>
   ```

3. **Include helper text for forms**
   ```html
   <input class='form-control'>
   <small class='text-muted'>Helper text</small>
   ```

4. **Use status badges for indicators**
   ```html
   <!-- Good -->
   <span class='status-pending'>Pending</span>
   
   <!-- Bad -->
   <span>Pending</span>
   ```

5. **Always include accessibility features**
   ```html
   <!-- Good -->
   <label for='id'>Label</label>
   <input id='id'>
   
   <!-- Bad -->
   <input placeholder='Label'>
   ```

6. **Use proper heading hierarchy**
   ```html
   <h1>Page Title</h1>
   <h2>Section</h2>
   <h3>Subsection</h3>
   ```

---
**Quick Reference Version**: 1.0
**Bootstrap Version**: 5.3.0
**Last Updated**: December 2025

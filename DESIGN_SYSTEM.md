# Front-End Design System & Style Guide

## Color Palette

### Primary Colors
```
Primary Blue:      #667eea  (RGB: 102, 126, 234)
Secondary Purple:  #764ba2  (RGB: 118, 75, 162)
```
Used for: Primary actions, headers, main branding

### Status Colors
```
Success/Approved:  #28a745  (RGB: 40, 167, 69)
Danger/Rejected:   #dc3545  (RGB: 220, 53, 69)
Warning/Pending:   #ffc107  (RGB: 255, 193, 7)
Info/Active:       #17a2b8  (RGB: 23, 162, 184)
```

### Neutral Colors
```
Light:             #f8f9fa
Gray 100:          #f0f0f0
Gray 200:          #e8e8e8
Gray 500:          #999999
Dark:              #333333
Black:             #000000
White:             #ffffff
```

## Typography

### Font Family
```
Primary: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif
Fallback: Arial, sans-serif
```

### Font Sizes
```
h1: 2.5rem (40px)
h2: 2rem (32px)
h3: 1.75rem (28px)
h4: 1.5rem (24px)
h5: 1.25rem (20px)
h6: 1rem (16px)
body: 1rem (16px)
small: 0.875rem (14px)
```

### Font Weights
```
Regular: 400
Semibold: 600
Bold: 700
```

## Spacing System

All spacing follows a base unit of 4px or Bootstrap's spacing scale:

```
xs: 4px
sm: 8px
md: 12px (0.75rem)
lg: 16px (1rem)
xl: 20px (1.25rem)
2xl: 24px (1.5rem)
3xl: 32px (2rem)
```

Bootstrap class examples:
- `.mb-3` = margin-bottom: 1rem
- `.p-4` = padding: 1.5rem
- `.gap-2` = gap: 0.5rem

## Component Styles

### Navigation Bar
```
Background: #212529 (dark)
Height: 56px
Padding: 0.5rem 0
Text Color: white
Logo: 24px font with icon
Sticky: position-sticky, top: 0
Box Shadow: default
```

### Cards
```
Background: white
Border: none
Border Radius: 8px
Box Shadow: 0 2px 8px rgba(0,0,0,0.1)
Transition: transform 200ms, box-shadow 200ms
Hover: translateY(-2px), shadow deeper
```

### Tables
```
Background: white
Row Height: 48px
Header Background: gradient (primary to secondary)
Header Text: white
Border: 1px solid #e0e0e0
Hover Row: #f5f5f5
Striped: alternate #f9f9f9
```

### Buttons

#### Primary Button
```
Background: linear-gradient(135deg, #667eea, #764ba2)
Color: white
Border: none
Border Radius: 5px
Padding: 10px 16px
Font Weight: 600
Transition: 300ms
Hover: gradient reversed, shadow deeper, translateY(-2px)
```

#### Secondary Button
```
Background: #6c757d (gray)
Color: white
Border: none
Hover: #5a6268 (darker gray)
```

#### Outline Button
```
Background: transparent
Border: 1px solid color
Color: color
Hover: filled with background
```

#### Small Button
```
Padding: 0.4rem 0.8rem
Font Size: 0.85rem
```

### Forms

#### Form Controls
```
Border: 1px solid #ddd
Border Radius: 5px
Padding: 0.6rem 0.8rem
Background: white
Transition: border-color 300ms, box-shadow 300ms

Focus:
  Border Color: #667eea
  Box Shadow: 0 0 0 0.2rem rgba(102, 126, 234, 0.25)
```

#### Form Labels
```
Font Weight: 600
Color: #333
Margin Bottom: 0.5rem
Font Size: 0.95rem
```

#### Required Field Indicator
```
Content: "*"
Color: #dc3545
Margin Left: 0.25rem
```

### Badges

#### Default Badge
```
Padding: 4px 10px
Border Radius: 20px (pill shape)
Font Size: 0.85rem
Font Weight: 600
```

### Status Indicators

#### Pending
```
Background: #fff3cd
Color: #856404
```

#### Approved/Active/Completed
```
Background: #d4edda
Color: #155724
```

#### Rejected/Inactive
```
Background: #f8d7da
Color: #721c24
```

#### In Progress
```
Background: #d1ecf1
Color: #0c5460
```

### Alerts

#### Success Alert
```
Background: #d4edda
Border: 1px solid #c3e6cb
Color: #155724
```

#### Danger Alert
```
Background: #f8d7da
Border: 1px solid #f5c6cb
Color: #721c24
```

#### Warning Alert
```
Background: #fff3cd
Border: 1px solid #ffeeba
Color: #856404
```

#### Info Alert
```
Background: #d1ecf1
Border: 1px solid #bee5eb
Color: #0c5460
```

## Elevation (Shadow Depth)

```
Level 1: 0 2px 8px rgba(0, 0, 0, 0.1)
Level 2: 0 4px 16px rgba(0, 0, 0, 0.15)
Level 3: 0 6px 24px rgba(0, 0, 0, 0.2)
```

## Border Radius

```
Small: 4px (minor elements)
Medium: 5px (buttons, inputs)
Large: 8px (cards, panels)
XL: 10px (login container)
Full: 50% (circular badges)
```

## Transitions & Animations

### Standard Transition
```
Duration: 200ms - 300ms
Easing: ease-in-out
Properties: background, color, border-color, box-shadow, transform
```

### Button Hover
```
Duration: 300ms
Effects: 
  - Translate Y: -2px
  - Box Shadow: deeper
  - Background: gradient reversed
```

### Card Hover
```
Duration: 200ms
Effects:
  - Translate Y: -2px
  - Box Shadow: deeper
```

## Responsive Design

### Mobile First Approach
Design for mobile first, then enhance for larger screens.

### Breakpoint Strategy
```
Mobile (xs): Full width, stacked layout
Tablet (md): 2-column layout, side-by-side forms
Desktop (lg): 3-4 column layout, enhanced spacing
Large Desktop (xl+): Extended layout with margins
```

### Common Patterns
```
<!-- Stack on mobile, 2 cols on desktop -->
<div class="row">
  <div class="col-12 col-md-6">...</div>
  <div class="col-12 col-md-6">...</div>
</div>

<!-- Centered content with max width -->
<div class="container-lg">...</div>

<!-- Responsive tables -->
<div class="table-responsive">
  <table>...</table>
</div>
```

## Accessibility Guidelines

### Color Contrast
- Text on background: minimum 4.5:1 ratio
- Large text (18pt+): minimum 3:1 ratio

### Focus States
```
Outline: 2px solid #667eea
Outline Offset: 2px
```

### Icons
- Always include `aria-label` or descriptive text
- Use semantic HTML for buttons/links
- Ensure hover states are visible

### Form Accessibility
- All `<input>` elements have associated `<label>`
- Use `for` attribute matching `id`
- Required fields marked visually and in HTML
- Error messages linked to form fields

## Icon Guidelines

### Icon Sizing
```
Navigation/Header: 24px
Buttons: 16px
Labels/Forms: 18px
Standalone: 48px
```

### Icon Usage
- Use Bootstrap Icons consistently
- Include aria-label for icon-only buttons
- Pair icons with text when possible
- Maintain icon color consistency

## Login Page Design

### Layout
```
┌────────────────────────┐
│   Gradient Background  │
│                        │
│  ┌──────────────────┐  │
│  │  Icon (48px)     │  │
│  │  Title           │  │
│  │  Subtitle        │  │
│  │                  │  │
│  │  Login Form      │  │
│  │                  │  │
│  │  [Login Button]  │  │
│  │  Demo Hint       │  │
│  └──────────────────┘  │
│                        │
└────────────────────────┘
```

### Gradient
```
Direction: 135deg
From: #667eea
To: #764ba2
Creates diagonal gradient effect
```

### Card Container
```
Background: white
Max Width: 400px
Width: 100%
Padding: 40px
Border Radius: 10px
Box Shadow: 0 10px 40px rgba(0,0,0,0.2)
```

## Dashboard Statistics Cards

### Card Heights
```
Minimum height: 120px
Padding: 1.5rem
```

### Statistics Layout
```
Left side: Text content
Right side: Icon (48px, semi-transparent)
Bottom: Optional mini chart or trend indicator
```

### Color Coding
```
Projects: Primary Blue
Samples: Info Teal
Tests: Success Green
Pending: Warning Yellow
```

## Table Design

### Header Row
```
Background: gradient (primary to secondary)
Color: white
Font Weight: 600
Padding: 12px
Height: 50px
```

### Data Rows
```
Height: 48px
Padding: 12px
Border Bottom: 1px solid #e0e0e0
Hover: background #f5f5f5 with smooth transition
```

### Action Column
```
Width: 150-200px
Button Group: flex with gap-2
Button Size: btn-sm
```

## Form Design

### Field Layout
```
Label (above field)
Input/Select/Textarea
Helper text (optional)
Error message (if validation fails)
Spacing: 0.5rem between label and input
```

### Multi-Column Forms
```
Desktop (lg+): 2 columns
Tablet (md): Single column
Mobile: Single column (stacked)
```

### Button Layout
```
Primary action: Primary button (btn-primary)
Secondary action: Secondary button (btn-secondary)
Spacing: gap-2 (0.5rem)
Alignment: flex-start or center
```

## Loading & Error States

### Loading Indicator
```
Spinner: Bootstrap spinner (if needed)
Text: "Loading..."
Overlay: semi-transparent if blocking
```

### Error State
```
Border Color: #dc3545 (danger red)
Text Color: #721c24 (dark red)
Background: #f8d7da (light red)
Icon: bi-exclamation-circle
```

### Empty State
```
Icon: Large (48px)
Message: Friendly, action-oriented
Action: Link or button to create item
Padding: 2rem vertical
Text Color: #666 (muted)
```

## Print Styles

```
Background: white (no gradients)
Colors: CMYK-safe
Avoid: Box shadows, gradients
Font size: 12pt minimum
Page breaks: Logical breaks in tables
```

## Dark Mode (Future Enhancement)

```
Background: #1e1e1e
Text: #e0e0e0
Card: #2d2d2d
Accent: #667eea (unchanged)
```

---
**Last Updated**: December 2025
**Version**: 1.0
**Bootstrap Version**: 5.3.0
**Icons**: Bootstrap Icons 1.10.0

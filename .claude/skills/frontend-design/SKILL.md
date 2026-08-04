---
name: frontend-design
description: Use when building or restyling any user-facing UI - components, pages, landing pages, dashboards - or when an existing interface feels generic. Covers typography, color systems, motion, micro-interactions, and spacing, and lists the AI-slop patterns to avoid.
---

# Frontend Design Skill

## Purpose
This skill helps Claude create distinctive, memorable frontends that avoid generic AI-generated design patterns. It emphasizes typography, color cohesion, motion, and intentional interactions that elevate user experience.

## Principles

### 1. Distinctive Typography
- Use Google Fonts strategically for personality (serif + sans-serif combinations)
- Implement proper typographic hierarchy with `clamp()` for responsive scaling
- Employ letter-spacing and font-weight strategically for emphasis
- Examples: Playfair Display for headlines, custom sans-serif for body
- Avoid: Default system fonts, inconsistent font sizes, poor line-height

### 2. Cohesive Color Systems
- Define CSS variables for semantic color naming (primary, accent, background, text)
- Use gradients sparingly but effectively for visual interest
- Maintain contrast ratios (WCAG AA minimum 4.5:1 for text)
- Create a 5-8 color palette with defined relationships
- Use opacity and alpha channels for depth (rgba)
- Avoid: Random hex colors, unnamed colors scattered across CSS

### 3. Orchestrated Motion & Animation
- Apply staggered animations (offset delays) to sequenced elements
- Use easing functions like `cubic-bezier(0.34, 1.56, 0.64, 1)` for personality
- Animate transforms (scale, rotate, translateY) not properties that trigger layout
- Provide visual feedback on interactive elements (hover, focus)
- Use `backdrop-filter: blur()` for glassmorphism effects
- Avoid: Motion that doesn't serve purpose, jarring animations, excessive transitions

### 4. High-Impact Micro-Interactions
- Hover states that provide feedback (scale, color shift, border change)
- Animated underlines on navigation links
- Icon animations on hover (rotate, scale)
- Smooth transitions on state changes
- Loading states and visual confirmations
- Avoid: Static, unresponsive interfaces

### 5. Layout & Spacing
- Use CSS custom properties for consistent spacing (--spacing-xs through --spacing-2xl)
- Implement max-width containers for readability
- Use CSS Grid and Flexbox with proper gap management
- Responsive design with mobile-first approach
- Whitespace as a design element
- Avoid: Fixed pixels, inconsistent spacing, layouts that don't adapt

### 6. Anti-Patterns to Avoid (AI Slop)
- Flat, colorless purple/blue gradients without intention
- System font (Inter) with no personality
- Pure white backgrounds with gray text
- Generic emoji icons
- No visual hierarchy or emphasis
- Static content with zero interactivity
- Generic marketing copy ("Streamline Your Workflow")

## Implementation Checklist

- [ ] Define CSS variables for colors, spacing, typography
- [ ] Implement 2+ custom Google Fonts with clear hierarchy
- [ ] Create gradient effects that serve purpose
- [ ] Add entrance animations with staggered delays
- [ ] Include hover/focus states on interactive elements
- [ ] Use backdrop-filter or creative backgrounds
- [ ] Implement semantic color naming
- [ ] Ensure mobile responsiveness with @media queries
- [ ] Test contrast ratios with accessibility tools
- [ ] Avoid naming elements generically ("container", "wrapper")

## Example Patterns

### CSS Variables Pattern
```css
:root {
    --color-primary: #2563eb;
    --color-accent: #f97316;
    --color-text: #0f172a;
    --spacing-md: 1.5rem;
}
```

### Staggered Animation Pattern
```css
.element {
    animation: fadeInUp 0.8s ease-out 0.2s both;
}
.element:nth-child(2) {
    animation-delay: 0.3s;
}
```

### Hover Interaction Pattern
```css
.button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
}
```

### Typography Scale Pattern
```css
h1 {
    font-size: clamp(2rem, 6vw, 4rem);
    line-height: 1.2;
    letter-spacing: -0.02em;
}
```

## When to Apply

- Building new UI components or pages
- Redesigning existing interfaces that feel generic
- Creating marketing landing pages
- Elevating visual hierarchy in dashboards
- Adding polish and personality to applications

## Success Metrics

- Does the design feel intentional, not AI-generated?
- Does typography provide clear hierarchy?
- Are colors used systematically (via variables)?
- Do animations enhance, not distract?
- Is the interface responsive and accessible?
- Does motion serve a functional purpose?

## References

- https://fonts.google.com/
- https://cssgradient.io/
- https://easings.net/
- https://web.dev/responsive-web-design-basics/



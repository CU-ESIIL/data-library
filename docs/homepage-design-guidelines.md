# Homepage Design Guidelines

## Overview
The ESIIL Data Library homepage should evolve from a static sidebar list into an interactive library. The interface must make it easy to discover datasets, understand their provenance, and browse collections by tags.

## Goals
- **Search-first navigation** so users can quickly find datasets by name, tag, or description.
- **Visible provenance** including citation, license, and source information for each dataset.
- **Static tag system** that organizes datasets by consistent categories.
- **Engaging visuals** such as hover image buttons to improve discoverability.

## Layout
1. **Header**: search bar spanning the top of the page.
2. **Tag filter panel**: list of static tags on the left or top; clicking filters the dataset grid.
3. **Dataset grid**: responsive cards showing dataset image, title, short description, and key tags.
4. **Provenance drawer**: expandable area within each card that reveals citation, source URL, and license.

## Tag System
- Maintain a centrally defined list of tags (e.g., `climate`, `remote-sensing`, `hazards`, `education`).
- Tag definitions live in a static JSON or YAML file and are referenced in dataset metadata.
- Datasets may have multiple tags but each tag must come from the approved list to keep navigation consistent.
- The tag filter panel displays tags alphabetically with counts.

## Search
- The search bar queries dataset titles, descriptions, and tags.
- Use a client-side search library such as [lunr.js](https://lunrjs.com/) or [Fuse.js](https://fusejs.io/).
- Search results update the dataset grid in place without a full page reload.
- Highlight matching terms within dataset cards for clarity.

## Dataset Cards
- Cards show an image (thumbnail or animated GIF), title, brief description, and tag chips.
- Include a "View Details" hover button over the image that links to the dataset page.
- On hover, fade in a colored overlay with the button; keep images accessible with `alt` text.
- Provenance information appears in a collapsible section within the card to avoid clutter.

## Hover Image Buttons
- Use CSS transitions for smooth hover effects (opacity, scale, or slide).
- Ensure hover actions are keyboard accessible by using `<button>` elements styled as overlays.
- Recommended image size: 300 × 200 px thumbnails stored under `docs/assets/datasets/`.
- Provide text labels that appear with the button for accessibility and improved engagement.

## Accessibility and Responsiveness
- Follow WCAG AA contrast ratios for text and overlays.
- Ensure all interactions (search, tag filtering, hover buttons) are keyboard operable.
- Layout should be responsive: the dataset grid stacks to a single column on small screens.
- Test on modern browsers and assistive technologies.

## Implementation Notes
- Export dataset metadata with tags and provenance to a static JSON file at build time.
- Use JavaScript to load the JSON, render cards, and handle filtering/search.
- Keep dependencies light to preserve static hosting compatibility.
- Integrate with MkDocs by including custom scripts and styles in `mkdocs.yml`.

## Next Steps
1. Create the tag list and dataset metadata schema.
2. Prototype the dataset card grid with hover image buttons.
3. Implement search and tag filtering with a lightweight JS library.
4. Collect feedback and iterate on layout and accessibility.


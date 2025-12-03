# HBnB React Frontend

A React-based frontend for the HBnB (Airbnb clone) application.

## Project Structure

```
hbnb-react/
├── public/
│   └── index.html          # HTML template
├── src/
│   ├── components/         # Reusable components
│   │   ├── Header.js       # Navigation header
│   │   ├── Footer.js       # Page footer
│   │   ├── PlaceCard.js    # Place card for listings
│   │   ├── ReviewCard.js   # Review card display
│   │   ├── ReviewForm.js   # Review submission form
│   │   ├── PriceFilter.js  # Price filter dropdown
│   │   └── Loading.js      # Loading spinner
│   ├── pages/              # Page components
│   │   ├── HomePage.js     # Home page with places list
│   │   ├── PlaceDetailsPage.js  # Place details with reviews
│   │   ├── AddReviewPage.js     # Standalone review page
│   │   └── LoginPage.js    # Login page
│   ├── services/           # API services
│   │   └── api.js          # API calls and cookie management
│   ├── context/            # React contexts
│   │   └── AuthContext.js  # Authentication state management
│   ├── App.js              # Main app with routing
│   ├── index.js            # Entry point
│   └── styles.css          # All CSS styles
├── package.json            # Dependencies and scripts
└── README.md               # This file
```

## Features

- **Home Page**: Browse all available places with price filtering
- **Place Details**: View detailed information about a place and its reviews
- **Add Review**: Submit reviews (requires authentication)
- **Login**: User authentication with JWT tokens
- **Responsive Design**: Works on desktop and mobile devices

## Getting Started

### Prerequisites

- Node.js (v14 or higher)
- npm or yarn
- Backend API running at `http://127.0.0.1:5000`

### Installation

1. Navigate to the project directory:
   ```bash
   cd hbnb-react
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm start
   ```

4. Open [http://localhost:3000](http://localhost:3000) in your browser.

### Building for Production

```bash
npm run build
```

This creates an optimized build in the `build/` folder.

## API Configuration

The API base URL is configured in `src/services/api.js`:

```javascript
const API_BASE_URL = 'http://127.0.0.1:5000/api/v1';
```

Update this URL if your backend is hosted elsewhere.

## React Concepts Used

### Components
- **Functional Components**: All components are functional
- **Props**: Data passed from parent to child components
- **Children**: Nested components

### Hooks
- **useState**: Managing component state
- **useEffect**: Side effects (API calls, etc.)
- **useContext**: Accessing authentication state
- **useParams**: Getting URL parameters
- **useNavigate**: Programmatic navigation
- **useMemo**: Memoizing filtered places
- **useCallback**: Memoizing callback functions

### Context API
- **AuthContext**: Global authentication state management

### React Router
- **Routes & Route**: Defining application routes
- **Link**: Navigation links
- **useParams**: URL parameters
- **useNavigate**: Programmatic navigation

## Comparison with Vanilla JavaScript

| Feature | Vanilla JS | React |
|---------|-----------|-------|
| DOM Updates | Manual `innerHTML`, `createElement` | Automatic via state changes |
| State Management | Global variables | `useState`, Context API |
| Routing | Manual URL parsing | React Router |
| Components | HTML templates | JSX components |
| Event Handling | `addEventListener` | Props like `onClick` |
| Data Fetching | In any function | In `useEffect` hook |

## Key Differences from Flask Templates

1. **Single Page Application (SPA)**: React loads once and updates dynamically
2. **Client-Side Routing**: Routes handled in browser, not server
3. **Component-Based**: UI split into reusable components
4. **State-Driven**: UI updates automatically when state changes
5. **JSX**: HTML-like syntax in JavaScript files

## Styling

All styles are in `src/styles.css` using CSS variables for consistency:

```css
:root {
    --primary-color: #FF5A5F;
    --accent-color: #FC642D;
    --text-dark: #484848;
    /* ... */
}
```

## Authentication Flow

1. User enters credentials on login page
2. API validates and returns JWT token
3. Token stored in cookie (7 days expiration)
4. AuthContext tracks authentication state
5. Protected pages check `isAuthenticated`
6. Token included in API requests via Authorization header

## License

© 2024 HBnB Evolution. All rights reserved.

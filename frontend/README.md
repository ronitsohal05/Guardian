# Guardian Frontend

Two-portal React application built with TypeScript and Tailwind CSS:

## Portals

### Store Portal
- Store registration and login
- Photo upload interface
- Pipeline integration
- Upload history tracking

### User Portal
- User account creation and login
- Preference management (tag selection)
- Notification settings

## Tech Stack

- **Frontend Framework**: React 18 with TypeScript
- **Styling**: Tailwind CSS
- **Build Tool**: Vite
- **Routing**: React Router v6
- **HTTP Client**: Axios

## Setup

1. Install dependencies:
```bash
npm install
```

2. Start development server:
```bash
npm run dev
```

The app runs on `http://localhost:3000` and proxies API calls to `http://localhost:5001`

3. Build for production:
```bash
npm run build
```

## Project Structure

```
src/
├── components/        # Reusable UI components
├── pages/            # Page components
│   ├── store/        # Store portal pages
│   └── user/         # User portal pages
├── services/         # API services
│   ├── apiClient.ts  # Axios instance with auth
│   ├── storeService.ts
│   └── userService.ts
├── types/            # TypeScript types
├── App.tsx           # Main app with routing
└── main.tsx          # Entry point
```

## Features

### Store Portal
- Register store account with details
- Upload photos to trigger CV pipeline
- View detection history with identified items
- Real-time processing feedback

### User Portal
- Create personal account
- Browse and select item tags of interest
- Save preference updates
- Receive notifications for matching items

## API Integration

The app expects the following endpoints:
- `POST /api/store/register` - Store registration
- `POST /api/store/login` - Store login
- `POST /api/store/upload` - Image upload
- `GET /api/store/history` - Upload history
- `POST /api/user/register` - User registration
- `POST /api/user/login` - User login
- `GET /api/tags` - Available tags
- `POST /api/user/preferences` - Update preferences
- `GET /api/user/preferences` - Get preferences

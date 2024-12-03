# Gaming Chat App

The **Gaming Chat App** is a real-time chat application designed for gamers, built with **Next.js**. It enables users to send and receive messages in a gaming environment with built-in censorship functionality using a backend API. The project is structured into two main directories: `jigsaw-ui` for the user interface and `jigsaw-src` for other project resources.
Live demo: https://mswecqzn69mxfhz8gbehhwrtonzx0to3.vercel.app/

## Features

- **Real-Time Messaging**: Communicate with other players instantly.
- **Message Censorship**: Automatically filters inappropriate or toxic messages using a backend API.
- **Simulated User Interaction**: Dynamically generated messages simulate activity in the chat.
- **Responsive Design**: Optimized for both desktop and mobile use.
- **Smooth Scrolling**: Keeps the focus on the most recent messages.

## Technologies Used

- **Framework**: Next.js
- **UI Components**: Custom React components located in the `jigsaw-ui` directory.
- **Backend API**: AWS Lambda-based censorship API.
- **Hosting**: Vercel for deployment.

---

## Getting Started

### Prerequisites

Ensure you have the following installed:

- **Node.js** (v16 or higher)
- **npm** or **yarn**
- Access to the censorship API endpoint.

---

### Project Structure

root/ 
├── jigsaw-ui/ # Contains the Next.js application 
│ ├── components/ # Reusable UI components like Button, Input, ScrollArea 
│ ├── pages/ # Application pages (Next.js routing) 
│ ├── hooks/ # Custom React hooks 
│ ├── utils/ # Utility functions  
│ └── index.tsx # React DOM rendering 
├── jigsaw-src/ # Additional project resources


---

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/gaming-chat-app.git
   cd gaming-chat-app
   cd jigsaw-ui

2. Install dependencies:
```bash
   npm install
   or
   yarn install
```
3. Create a .env.local file in the jigsaw-ui directory and add the following:
```bash
   NEXT_PUBLIC_API_URL=https://<API_GATEWAY>.execute-api.us-east-1.amazonaws
```
4. Run the development server:
```bash
   npm run dev
   #or
   yarn dev
```
5. Open the app in your browser at http://localhost:3000.

## How It Works
User Interaction: Users type messages and submit them via a form.
Censorship Check: Messages are sent to the backend API, which returns whether the message should be censored.
Message Rendering: Messages are displayed in the chat area, with censored messages replaced by *** [censored] ***.
Simulated Activity: Auto-generated messages from simulated users keep the chat active.

## Customization
Update the API: Modify the censorship logic in the checkMessageCensorship function located in jigsaw-ui/pages/index.tsx.
Change UI Design: Update styles or components in the jigsaw-ui/components directory.

## Troubleshooting
CORS Issues: Verify that the backend API supports preflight OPTIONS requests and includes correct CORS headers.
API Endpoint: Ensure the NEXT_PUBLIC_API_URL in .env.local points to the correct API endpoint.
Logs and Debugging: Use browser DevTools to inspect API requests and responses.



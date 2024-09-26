# Credit Card Fraud Detection System

This project is a **Credit Card Fraud Detection System** built using **Next.js** for the frontend and **FastAPI** for the backend. The application leverages machine learning models to predict fraudulent transactions based on user input, such as card number and transaction amount. It provides a user-friendly interface for checking the validity of a card and the likelihood of fraud.

## Table of Contents

- [Credit Card Fraud Detection System](#credit-card-fraud-detection-system)
  - [Table of Contents](#table-of-contents)
  - [Getting Started](#getting-started)
  - [Project Structure](#project-structure)
  - [Dependencies](#dependencies)

## Getting Started

To get started with this project, follow the steps below:

1. **Clone the repository:**

   ```bash
   git clone <https://github.com/imadselka/creditcard-fraud-detection>
   cd frontend
   ```

2. **Install dependencies:**

   ```bash
   yarn install
   ```

3. **Run the development server:**

   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

4. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000) to see the application in action.

## Project Structure

The project follows a standard structure:

- `app/`: Contains the main application code.
- `components/`: Reusable React components.
- `server/`: Contains the FastAPI backend code for handling predictions.

## Dependencies

This project uses the following key dependencies:

- **Next.js**: A React framework for server-side rendering and static site generation.
- **FastAPI**: A modern web framework for building APIs with Python.
- **Axios**: A promise-based HTTP client for making requests.
- **Shadcn**: A set of accessible UI components that uses **Radix UI**.

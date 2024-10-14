import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '@telegram-apps/telegram-ui/dist/styles.css'; // Глобальные стили из библиотеки
import { AppRoot } from '@telegram-apps/telegram-ui';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <AppRoot>
    <App />
  </AppRoot>,
);
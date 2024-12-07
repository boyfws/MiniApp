import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import '@telegram-apps/telegram-ui/dist/styles.css'; // Глобальные стили из библиотеки
import { AppRoot } from '@telegram-apps/telegram-ui';
import { ContextProvider } from './state_management/context/Context';


document.documentElement.style.backgroundColor = 'var(--tgui--bg_color)';
document.body.style.backgroundColor = 'var(--tgui--bg_color)';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <ContextProvider>
        <AppRoot>
            <App />
        </AppRoot>
    </ContextProvider>,

);
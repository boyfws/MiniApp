import React from 'react';
import ReactDOM from 'react-dom/client';
import { ContextProvider } from './state_management/context/Context';
import AppWrapper from './AppWrapper'



document.documentElement.style.backgroundColor = 'var(--tgui--bg_color)';
document.body.style.backgroundColor = 'var(--tgui--bg_color)';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
    <ContextProvider>
        <AppWrapper />
    </ContextProvider>,

);
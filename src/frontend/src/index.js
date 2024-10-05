import React from 'react';
import ReactDOM from 'react-dom';
import './index.css'; // можно добавить свои стили
import App from './App'; // основной компонент приложения
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);

reportWebVitals();

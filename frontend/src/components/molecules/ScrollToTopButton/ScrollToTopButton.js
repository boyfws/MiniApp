// Css
import './ScrollToTopButton.css'

// Ext lib
import React, { useState, useEffect, useCallback } from 'react';

// Components
import ButtonForScrollToTop from '../../atoms/ButtonForScrollToTop/ButtonForScrollToTop';


const ScrollToTopButton = () => {
  const [isVisible, setIsVisible] = useState(false);

  const toggleVisibility = useCallback(() => {
    // Показываем кнопку, если прокрутка больше двух высот экрана, иначе скрываем её
    if (window.scrollY > window.innerHeight) {
      setIsVisible(true);
    } else {
      setIsVisible(false);
    } 
  }, []);

  useEffect(() => {
    // Добавляем обработчик события прокрутки
    window.addEventListener('scroll', toggleVisibility);
    // Удаляем обработчик при размонтировании
    return () => {
      window.removeEventListener('scroll', toggleVisibility);
    };
  }, [toggleVisibility]);

  const scrollToTop = () => {
    window.Telegram.WebApp.HapticFeedback.impactOccurred("medium")
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
  };

  return (
    <div className={isVisible ? 'scroll-to-top-visible' : 'scroll-to-top-hidden'}>
    <ButtonForScrollToTop
      onClick={scrollToTop}
    />
    </div>
  );
};

export default ScrollToTopButton;

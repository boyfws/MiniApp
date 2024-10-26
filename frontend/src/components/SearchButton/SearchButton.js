import React from 'react';
import { Button } from '@telegram-apps/telegram-ui';
import './SearchButton.css';

const Icon24SearchOutline = ({ ...restProps }) => (
    <svg width="24" height="24" fill="none" xmlns="http://www.w3.org/2000/svg" {...restProps}>
      <circle cx="11" cy="11" r="6" stroke="currentColor" strokeWidth="2" />
      <line x1="15.5" y1="15.5" x2="20" y2="20" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
    </svg>
  );
  


const SearchButton = ({ onSearchClick }) => {
    return (
        <Button 
            size="s" 
            mode="bezeled" 
            onClick={onSearchClick}
            className='search-button' >
            <Icon24SearchOutline  className='icon'/>
        </Button>
    );
}

export default SearchButton;